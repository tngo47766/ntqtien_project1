from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'contact', 'address')
    search_fields = ('name', 'email', 'contact')

