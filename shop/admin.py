from unicodedata import category
from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import Product
from datetime import datetime
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

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

def export_to_pdf(modeladmin,request,queryset):
    opts = modeladmin.model._meta
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    prod_id,cat,slug,price,stock,available,updated = fields[0],fields[1],fields[4],fields[6],fields[7],fields[8],fields[10]
    data = [prod_id,cat,slug,price,stock,available,updated]

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

    textobj.textLine('--------------------Product List-------------------')
    textobj.textLine('=====================================================')


    for chunk in data_row[::-1]:
        textobj.textLine(str(chunk))

    p.drawText(textobj)
    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='Products.pdf')
export_to_pdf.short_description = 'Export to PDF'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [export_to_csv,export_to_pdf]
    list_display=['name','slug','price','category','stock','available','created','updated']
    list_filter=['available','created','updated','category']
    list_editable=['price','stock','available']
    prepopulated_fields={'slug':('name',)}
