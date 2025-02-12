from django.urls import path
from .views import signup, login, customer_main, logout
from django.urls import path
from .views import customer_list
from .views import all_books
urlpatterns = [
    path('customers/', customer_list, name='customer_list'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('main/', customer_main, name='customer_main'),
    path('logout/', logout, name='logout'),
    path('books/', all_books, name='all_books'),
    # path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    # path('buy/<int:book_id>/', buy_now, name='buy_now'),   
]
