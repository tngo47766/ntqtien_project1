from django.db import models
from customer.models import Customer
from book.models import Book

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @staticmethod
    def get_cart_items_by_customer(customer_id):
        return Cart.objects.filter(customer=customer_id)

    def __str__(self):
        return f"Cart - {self.customer.name} - {self.book.name} ({self.quantity})"
