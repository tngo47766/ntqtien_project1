from django.db import models
from customer.models import Customer
from book.models import Book
import datetime

class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Change Products to Book
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=255, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def place_order(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

    def __str__(self):
        return f"Order {self.id} - {self.customer.name} - {self.book.name}"
