# Create your models here.

# import braintree
from django.db import models
from shop.models import Product

class Order(models.Model):
    first_name= models.CharField(max_length=50,help_text='')
    last_name=models.CharField(max_length=50)
    email=models.EmailField(help_text='')
    phone=models.IntegerField(max_length=20,help_text='')  #change this charfield?
    address=models.CharField(max_length=200)
    postal_code= models.CharField(max_length=20)
    city=models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    paid=models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150,blank=True)
    #add a 'closed' field
    class Meta():
        ordering = ['-created',]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_items(self):
        return [item.get_order()for item in self.items.all()]


class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_product_id(self):
        return self.product.id
    
    def get_quantity(self):
        return self.quantity

    def get_order(self):
        return self