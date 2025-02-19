from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Order
from customer.models import Customer
from book.models import Book
from cart.models import Cart

@csrf_exempt
@login_required  # ✅ Ensure only logged-in users can place orders
def place_order(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Vui lòng đăng nhập để thanh toán'}, status=401)

    customer = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])

            if not items:
                return JsonResponse({'message': 'Không có sản phẩm trong giỏ hàng'}, status=400)

            total_price = 0
            order_instances = []

            for item in items:
                book_id = item.get('book_id')

                # ✅ Ensure book_id is valid
                if not book_id or not book_id.isdigit():
                    return JsonResponse({'message': f'ID sản phẩm không hợp lệ: {book_id}'}, status=400)

                try:
                    book = Book.objects.get(id=int(book_id))  # ✅ Convert to int
                except Book.DoesNotExist:
                    return JsonResponse({'message': f'Sách có ID {book_id} không tồn tại'}, status=404)

                quantity = int(item.get('quantity', 1))
                order_price = book.price * quantity
                total_price += order_price

                existing_order = Order.objects.filter(customer=customer, book=book, status=False).first()
                if existing_order:
                    existing_order.quantity += quantity
                    existing_order.price += order_price
                    existing_order.save()
                else:
                    new_order = Order(
                        book=book,
                        customer=customer,
                        quantity=quantity,
                        price=order_price,
                        status=False
                    )
                    order_instances.append(new_order)

            Order.objects.bulk_create(order_instances)

            # ✅ Clear cart after placing order
            request.session['cart'] = {}
            request.session['cart_items_count'] = 0
            Cart.objects.filter(customer=customer).delete()

            return JsonResponse({
                'message': 'Đặt hàng thành công!',
                'total_price': total_price,
                'success': True
            })

        except Exception as e:
            return JsonResponse({'message': 'Lỗi xử lý đơn hàng', 'error': str(e)}, status=500)

    return JsonResponse({'message': 'Phương thức không hợp lệ'}, status=400)


@login_required
def view_orders(request):
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer).order_by('-date')

    return render(request, 'orders.html', {'orders': orders})


@login_required
def customer_dashboard(request):
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer).order_by('-date')

    return render(request, 'customer/customer_main.html', {
        'customer_name': customer.user.username,
        'orders': orders
    })
