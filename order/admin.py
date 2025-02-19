from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_customer_username', 'get_customer_email', 'book', 'quantity', 'price', 'status', 'date')
    list_filter = ('status', 'date')  # ✅ Add filtering by status & date
    search_fields = ('customer__user__username', 'customer__user__email', 'book__name')  # ✅ Search by user fields
    list_editable = ('status',)  # ✅ Editable status
    ordering = ('-date',)  # ✅ Sort by newest orders first

    def get_customer_username(self, obj):
        return obj.customer.user.username if obj.customer and obj.customer.user else "Unknown"
    get_customer_username.short_description = "Khách Hàng"  # ✅ Rename column header

    def get_customer_email(self, obj):
        return obj.customer.user.email if obj.customer and obj.customer.user else "No Email"
    get_customer_email.short_description = "Email"

admin.site.register(Order, OrderAdmin)
