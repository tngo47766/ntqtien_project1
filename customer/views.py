from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Customer
from book.models import Book
from order.models import Order

# 📌 View: List all customers
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})


# 📌 View: User Registration
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        contact = request.POST['contact']

        # 🔥 Create User & Customer Profile
        user = User.objects.create_user(username=username, email=email, password=password)
        Customer.objects.create(user=user, address=address, contact=contact)
        
        login(request, user)  # Auto login after signup
        return redirect('customer_main')

    return render(request, 'customer/signup.html')


# 📌 View: User Login
@csrf_exempt
def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('customer_main')
        else:
            return render(request, 'customer/login.html', {'error': 'Invalid username or password'})

    return render(request, 'customer/login.html')


# 📌 View: Customer Dashboard
@login_required
def customer_main(request):
    customer = get_object_or_404(Customer, user=request.user)
    
    # Fetch orders for the logged-in customer
    orders = Order.objects.filter(customer=customer).order_by('-date')

    return render(request, 'customer/customer_main.html', {
        'customer_name': customer.user.username,
        'orders': orders
    })


# 📌 View: Logout User
def customer_logout(request):
    logout(request)
    messages.success(request, "Đăng xuất thành công!")
    return redirect('landing_page')  # Redirect to home page


# 📌 View: Show All Books with Filters
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

    return render(request, 'customer/all_books.html', {'books': books})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

from cart.models import Cart
from book.models import Book
from customer.models import Customer


@csrf_exempt
@login_required  # ✅ Ensure only logged-in users can add items to cart
def add_to_cart(request, book_id):
    if request.method != "POST":
        return JsonResponse({'message': 'Phương thức không hợp lệ'}, status=405)

    try:
        customer = get_object_or_404(Customer, user=request.user)
        book = get_object_or_404(Book, id=book_id)

        # ✅ Parse JSON request body
        data = json.loads(request.body)
        quantity = data.get("quantity", 1)

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



# 📌 View: Buy Now (Redirect to Checkout)
@login_required
def buy_now(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'checkout.html', {'book': book})
