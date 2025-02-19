from django.db import models
from customer.models import Customer
from book.models import Book
import datetime

class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=255, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.get_customer_username()} - {self.book.name}"

    def get_customer_username(self):
        """ ✅ Get the username from related User model """
        return self.customer.user.username if self.customer.user else "Unknown Customer"
