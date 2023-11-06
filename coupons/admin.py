from django.contrib import admin
from .models import MultiUseCoupon,SingleUseCoupon
# Register your models here.

@admin.register(MultiUseCoupon)
class MultiUseCouponAdmin(admin.ModelAdmin):
    list_display=['code','valid_from','valid_to','discount','active']
    list_filter=['active','valid_from','active']
    search_fields=['code']

@admin.register(SingleUseCoupon)
class SingleUseCouponAdmin(admin.ModelAdmin):
    list_display=['code','valid_from','valid_to','discount','has_been_used','active']
    list_filter=['active','valid_from','active','has_been_used']
    search_fields=['code']