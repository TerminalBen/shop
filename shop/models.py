from django.db import models
from django.urls import reverse
# Create your models here.
#admin credentials
# #bentolima
#123shop456

class Category(models.Model):
    name= models.CharField(max_length=200,db_index=True)
    slug= models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering=['-name',]
        verbose_name='category'
        verbose_name_plural='categories'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug])


class Product(models.Model):
    category=models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    name=models.CharField(max_length=200,db_index=True)
    image=models.ImageField(upload_to='products/%Y/%M/%D',blank=True)
    slug=models.SlugField(max_length=200,db_index=True)
    description=models.TextField(max_length=500,blank=True)
    price= models.DecimalField(decimal_places=1,max_digits=10)
    stock=models.IntegerField(null=False,blank=False,db_index=True)
    available= models.BooleanField(default=True)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['name',]
        index_together=[['id','slug'],]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id,self.slug])

#Order and Customer model Next
#update: order as separated app 