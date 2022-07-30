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
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.urls import reverse
from django.utils.safestring import mark_safe


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
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    order_id,firstname,lastname,email,phone,address,paid = fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[10]
    data = [order_id,firstname,lastname,email,phone,address,paid]

    data_row = []

    for obj in queryset:
        for field in data:
            value = getattr(obj,field.name)
            if (isinstance(value,datetime)):
                value = value.strftime('%d/%m/%y')
            data_row.append(str(value))
    
    data_row = [data_row[i:i + 7] for i in range(0, len(data_row), 7)]
   
    buffer = io.BytesIO()
    p=canvas.Canvas(buffer,pagesize=letter,bottomup=0)
    textobj = p.beginText()
    textobj.setTextOrigin(inch,inch)
    textobj.setFont("Helvetica",11)

    textobj.textLine('--------------------Order Invoices-------------------')
    textobj.textLine('=====================================================')


    for chunk in data_row[::-1]:
        textobj.textLine(str(chunk))

    p.drawText(textobj)
    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
export_to_pdf.short_description = 'Export to PDF'


@admin.register(Order)
class OrderAdmin (admin.ModelAdmin):
    def order_detail(obj):
        url = reverse('orders:admin_order_detail', args=[obj.id])
        return mark_safe(f'<a href="{url}">View</a>')
    order_detail.short_description = 'Details'

    def order_pdf(obj):
        url = reverse('orders:admin_order_pdf', args=[obj.id])
        return mark_safe(f'<a href="{url}">PDF</a>')
    order_pdf.short_description = 'Invoice'


    list_display = ['id', 'first_name', 'last_name','email','phone', 'address','postal_code','city','paid', 'created', 'updated',order_detail,order_pdf]
    list_filter = ['paid','phone','first_name', 'created', 'updated']
    #list_editable = ['price', 'stock', 'available']
    inlines = [OrderItemInLine]
    actions = [export_to_csv,export_to_pdf]
    
    