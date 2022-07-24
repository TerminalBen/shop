# Register your models here.
from dataclasses import field
from datetime import datetime
from django.contrib import admin
from .models import Order,OrderItem
import csv
from django.http import HttpResponse
from django.shortcuts import render
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def export_to_csv(modeladmin,request,queryset):
    opts = modeladmin.model._meta
    date_time = datetime.now().strftime("%d/%m/%Y_%Hh_%Mm_%Ss")	
    content_diposition = 'attachment; filename=orders'+date_time+'.csv'
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

a = ['celery.accumulate',
     'celery.backend_cleanup',
     'celery.chain',
     'celery.chord',
     'celery.chord_unlock',
     'celery.chunks',
     'celery.group',
     'celery.map',
     'celery.starmap',
     'orders.tasks.order_created_user']    


def export_to_pdf(modeladmin,request,queryset):
    opts = modeladmin.model._meta
    fields1 = [field.verbose_name for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    fields2 = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    data_row = []
    for obj in queryset:
        for field in fields2:
            value = getattr(obj,field.name)
            if (isinstance(value,datetime)):
                value = value.strftime('%d/%m/%y')
            data_row.append(str(value))
    buffer = io.BytesIO()
    p=canvas.Canvas(buffer)
    p.drawString(10,20,' '.join(fields1))
    p.drawString(100,100,' '.join(data_row))
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
export_to_csv.short_description = 'Export to CSV'


@admin.register(Order)
class OrderAdmin (admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name','email','phone', 'address','postal_code','city','paid', 'created', 'updated']
    list_filter = ['paid','phone','first_name', 'created', 'updated']
    #list_editable = ['price', 'stock', 'available']
    inlines = [OrderItemInLine]
    actions = [export_to_csv,export_to_pdf]
    