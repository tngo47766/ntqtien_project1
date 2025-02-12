
from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'book', 'quantity', 'price', 'status', 'date')  # Hiển thị cột trong admin
    list_filter = ('status', 'date')  # Bộ lọc bên phải admin
    search_fields = ('customer__name', 'book__name', 'phone')  # Tìm kiếm theo tên khách hàng, sách, số điện thoại
    list_editable = ('status',)  # Cho phép chỉnh sửa trạng thái trực tiếp trên danh sách
    ordering = ('-date',)  # Sắp xếp theo ngày mới nhất

admin.site.register(Order, OrderAdmin)
