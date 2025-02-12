from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart
from book.models import Book
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_to_cart(request, book_id):
    if 'customer_id' not in request.session:
        return JsonResponse({'message': 'Vui lòng đăng nhập để thêm vào giỏ hàng'}, status=401)

    customer_id = request.session['customer_id']
    book = Book.objects.get(id=book_id)

    data = json.loads(request.body)
    quantity = data.get('quantity', 1)

    cart_item, created = Cart.objects.get_or_create(customer_id=customer_id, book=book)
    if not created:
        cart_item.quantity += quantity
    cart_item.save()

    # 🔥 Update cart count in session
    request.session['cart_items_count'] = Cart.objects.filter(customer_id=customer_id).count()

    return JsonResponse({'message': 'Sách đã được thêm vào giỏ hàng!', 'cart_count': request.session['cart_items_count']})

def view_cart(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer_id = request.session['customer_id']
    cart_items = Cart.get_cart_items_by_customer(customer_id)
    
    # 🔥 Ensure session count is accurate
    request.session['cart_items_count'] = cart_items.count()

    total_price = sum(item.quantity * item.book.price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, cart_id):
    if 'customer_id' not in request.session:
        return redirect('login')

    cart_item = Cart.objects.get(id=cart_id)
    customer_id = cart_item.customer.id
    cart_item.delete()

    # 🔥 Update cart count in session
    request.session['cart_items_count'] = Cart.objects.filter(customer_id=customer_id).count()

    return redirect('view_cart')
