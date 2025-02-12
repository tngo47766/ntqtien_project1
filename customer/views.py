from .models import Customer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import HttpResponse

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

# View đăng ký
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        address = request.POST['address']
        contact = request.POST['contact']

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email này đã được sử dụng!")
            return redirect('signup')

        customer = Customer(name=name, email=email, password=password, address=address, contact=contact)
        customer.save()
        messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
        return redirect('login')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Use .get() to avoid KeyError
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Vui lòng nhập email và mật khẩu!")
            return redirect('login')

        try:
            customer = Customer.objects.get(email=email)
            if check_password(password, customer.password):
                request.session['customer_id'] = customer.id
                request.session['customer_name'] = customer.name
                messages.success(request, "Đăng nhập thành công!")
                return redirect('customer_main')
            else:
                messages.error(request, "Mật khẩu không đúng!")
        except Customer.DoesNotExist:
            messages.error(request, "Email không tồn tại!")

    return render(request, 'login.html')


# View trang chính của khách hàng
from order.models import Order
def customer_main(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer_id = request.session['customer_id']

    # Get customer info (handle missing data safely)
    try:
        customer = Customer.objects.get(id=customer_id)
        customer_name = customer.name
    except Customer.DoesNotExist:
        return redirect('login')

    # Fetch orders for the logged-in customer
    orders = Order.objects.filter(customer=customer).order_by('-date')

    return render(request, 'customer_main.html', {
        'customer_name': customer_name,
        'orders': orders
    })


# View đăng xuất

def logout(request):
    request.session.flush()  # Xóa tất cả session
    messages.success(request, "Đăng xuất thành công!")
    return redirect('landing_page')  # Chuyển hướng về trang chủ

from book.models import Book

def all_books(request):
    search_query = request.GET.get('search', '')  # Get search query
    price_filter = request.GET.get('price', '')  # Get price filter
    sort_by = request.GET.get('sort', '')  # Get sorting order

    books = Book.objects.all()

    # 🔍 Apply Search Filter
    if search_query:
        books = books.filter(name__icontains=search_query)

    # 💰 Apply Price Filter
    if price_filter == 'low_to_high':
        books = books.order_by('price')
    elif price_filter == 'high_to_low':
        books = books.order_by('-price')

    # 🔡 Apply A-Z Sorting
    if sort_by == 'a_to_z':
        books = books.order_by('name')
    elif sort_by == 'z_to_a':
        books = books.order_by('-name')

    return render(request, 'all_books.html', {'books': books})
from django.http import JsonResponse

def add_to_cart(request, book_id):
    if 'customer_id' not in request.session:
        return JsonResponse({'message': 'Vui lòng đăng nhập để thêm vào giỏ hàng'}, status=401)

    cart = request.session.get('cart', [])
    cart.append(book_id)
    request.session['cart'] = cart
    return JsonResponse({'message': 'Sách đã được thêm vào giỏ hàng!'})

def buy_now(request, book_id):
    if 'customer_id' not in request.session:
        return redirect('login')

    book = Book.objects.get(id=book_id)
    return render(request, 'checkout.html', {'book': book})
