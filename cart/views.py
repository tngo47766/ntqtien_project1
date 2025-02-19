from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import Cart
from book.models import Book
from customer.models import Customer

@csrf_exempt
@login_required
def add_to_cart(request, book_id):
    if request.method != "POST":
        return JsonResponse({'message': 'Phương thức không hợp lệ'}, status=405)

    try:
        book = get_object_or_404(Book, id=book_id)
        customer = get_object_or_404(Customer, user=request.user)

        # Parse JSON data from request
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)

        # ✅ Get or create cart item
        cart_item, created = Cart.objects.get_or_create(customer=customer, book=book)
        if not created:
            cart_item.quantity += quantity  # Update quantity if already in cart
        cart_item.save()

        # ✅ Update session cart count
        request.session['cart_items_count'] = Cart.objects.filter(customer=customer).count()

        return JsonResponse({
            'message': 'Sách đã được thêm vào giỏ hàng!',
            'cart_count': request.session['cart_items_count']
        })

    except Exception as e:
        return JsonResponse({'message': 'Lỗi khi thêm vào giỏ hàng', 'error': str(e)}, status=500)


@login_required
def view_cart(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart_items = Cart.get_cart_items_by_customer(customer.id)

    # ✅ Update session cart count
    request.session['cart_items_count'] = cart_items.count()

    total_price = sum(item.quantity * item.book.price for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cart

@csrf_exempt
def remove_from_cart(request, cart_id):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Bạn cần đăng nhập để xóa sản phẩm!', 'success': False}, status=401)

    try:
        cart_item = Cart.objects.get(id=cart_id, customer=request.user.customer)
        cart_item.delete()

        # ✅ Update cart count in session
        remaining_cart_items = Cart.objects.filter(customer=request.user.customer)
        request.session['cart_items_count'] = sum(item.quantity for item in remaining_cart_items)

        return JsonResponse({
            'message': '✅ Sản phẩm đã bị xóa!',
            'success': True,
            'cart_count': request.session['cart_items_count']  # ✅ Return updated cart count
        })
    except Cart.DoesNotExist:
        return JsonResponse({'message': '❌ Sản phẩm không tồn tại!', 'success': False}, status=404)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cart
import json

@csrf_exempt
def update_cart(request, cart_id):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Bạn cần đăng nhập để cập nhật giỏ hàng!', 'success': False}, status=401)

    try:
        data = json.loads(request.body)
        new_quantity = int(data.get('quantity', 1))

        cart_item = Cart.objects.get(id=cart_id, customer=request.user.customer)
        cart_item.quantity = new_quantity
        cart_item.save()

        # ✅ Update cart count in session
        remaining_cart_items = Cart.objects.filter(customer=request.user.customer)
        request.session['cart_items_count'] = sum(item.quantity for item in remaining_cart_items)

        return JsonResponse({
            'message': '✅ Số lượng đã cập nhật!',
            'success': True,
            'cart_count': request.session['cart_items_count']
        })
    except Cart.DoesNotExist:
        return JsonResponse({'message': '❌ Sản phẩm không tồn tại!', 'success': False}, status=404)

