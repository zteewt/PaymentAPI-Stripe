from django.contrib import admin
from .models import Item, Order, OrderItem, Discount, Tax


class ItemsAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_price_in_dollars']
    list_display_links = ('name', )
    search_fields = ('name', )

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'item', 'quantity', 'total_price']
    list_display_links = ('order', )
    search_fields = ('item', )

class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    list_display_links = ('id', )
    search_fields = ('id', )


class DiscountsAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage', 'stripe_coupon_id']
    list_display_links = ('name', )
    search_fields = ('name', 'stripe_coupon_id')

class TaxesAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage', 'stripe_tax_rate_id']
    list_display_links = ('name', )
    search_fields = ('name', 'stripe_tax_rate_id')

admin.site.register(Item, ItemsAdmin)
admin.site.register(OrderItem, OrderItemsAdmin)
admin.site.register(Order, OrdersAdmin)
admin.site.register(Discount, DiscountsAdmin)
admin.site.register(Tax, TaxesAdmin)