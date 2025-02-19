from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'get_name', 'address', 'contact')  # ✅ Use user-related fields correctly

    def get_name(self, obj):
        return obj.user.username  # ✅ Get name from Django User model
    get_name.short_description = "Tên Khách Hàng"

    def get_email(self, obj):
        return obj.user.email  # ✅ Get email from Django User model
    get_email.short_description = "Email"

admin.site.register(Customer, CustomerAdmin)
