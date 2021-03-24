from django.contrib import admin

# Register your models here.
#superuser credentials: bentolima-bentolima100@gmail.com-123shop456
from .models import Category,Product
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields={'slug':('name',)}
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','slug','price','stock','available','created','updated']
    list_filter=['available','created','updated']
    list_editable=['price','stock','available']
    prepopulated_fields={'slug':('name',)}
