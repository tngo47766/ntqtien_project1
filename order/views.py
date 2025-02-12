from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from customer.models import Customer
from book.models import Book
import json

@csrf_exempt
def place_order(request):
    if 'customer_id' not in request.session:
        return JsonResponse({'message': 'Vui lòng đăng nhập để thanh toán'}, status=401)

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])

            if not items:
                return JsonResponse({'message': 'Không có sản phẩm trong giỏ hàng'}, status=400)

            total_price = 0  # ✅ Tính tổng tiền

            for item in items:
                book_id = item.get('book_id')
                quantity = int(item.get('quantity', 1))

                if not book_id:
                    return JsonResponse({'message': 'Sản phẩm không hợp lệ'}, status=400)

                try:
                    book = Book.objects.get(id=book_id)
                except Book.DoesNotExist:
                    return JsonResponse({'message': f'Sách có ID {book_id} không tồn tại'}, status=404)

                order_price = book.price * quantity
                total_price += order_price  # ✅ Cộng tổng tiền vào hóa đơn

                order = Order.objects.create(
                    book=book,
                    customer=customer,
                    quantity=quantity,
                    price=order_price,
                    status=False
                )

            return JsonResponse({
                'message': 'Đặt hàng thành công!',
                'total_price': total_price,  # ✅ Trả về tổng tiền
                'success': True
            })

        except Exception as e:
            return JsonResponse({'message': 'Lỗi xử lý đơn hàng', 'error': str(e)}, status=500)

    return JsonResponse({'message': 'Phương thức không hợp lệ'}, status=400)

def view_orders(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer_id = request.session['customer_id']
    orders = Order.get_orders_by_customer(customer_id)
    return render(request, 'orders.html', {'orders': orders})
from django.shortcuts import render, redirect
from .models import Order
from customer.models import Customer

def customer_dashboard(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)
    orders = Order.get_orders_by_customer(customer_id)

    return render(request, 'customer_main.html', {'customer_name': customer.name, 'orders': orders})
