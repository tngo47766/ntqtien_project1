from django.urls import path
from .views import (
    customer_list, signup, customer_login, customer_logout, 
    customer_main, all_books, add_to_cart, buy_now
)

urlpatterns = [
    path('list/', customer_list, name='customer_list'),
    path('signup/', signup, name='signup'),
    path('login/', customer_login, name='customer_login'),
    path('logout/', customer_logout, name='customer_logout'),
    path('main/', customer_main, name='customer_main'),
    path('books/', all_books, name='all_books'),
    path('add_to_cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('buy_now/<int:book_id>/', buy_now, name='buy_now'),
]
