from django.contrib import admin
from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = [
        'product',
        'quantity',
        'price',
        'total_price'
    ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'subtotal',
        'tax_amount',
        'grand_total',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)
    inlines = [OrderItemInline]

# Optional (not needed if inline is used)
# admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)
