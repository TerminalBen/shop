# Register your models here.
from django.contrib import admin
from .models import Order,OrderItem


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin (admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name','email','phone', 'address','postal_code','city','paid', 'created', 'updated']
    list_filter = ['paid','phone','first_name', 'created', 'updated']
    #list_editable = ['price', 'stock', 'available']
    inlines = [OrderItemInLine]
    