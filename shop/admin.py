from unicodedata import category
from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import Product
from datetime import datetime

# Register your models here.
#superuser credentials: bentolima-bentolima100@gmail.com-123shop456
from .models import Category,Product
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields={'slug':('name',)}

def export_to_csv(modeladmin,request,queryset):
    opts = modeladmin.model._meta
    date_time = datetime.now().strftime("%d/%m/%Y_%Hh_%Mm_%Ss")	
    content_diposition = 'attachment; filename=products'+date_time+'.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_diposition
    writer =csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    #write the coolumns name row
    writer.writerow([field.verbose_name for field in fields])

    #write data row

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj,field.name)
            if (isinstance(value,datetime)):
                value = value.strftime('%d/%m/%y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [export_to_csv]
    list_display=['name','slug','price','category','stock','available','created','updated']
    list_filter=['available','created','updated','category']
    list_editable=['price','stock','available']
    prepopulated_fields={'slug':('name',)}
