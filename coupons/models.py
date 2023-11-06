from django.db import models

# Create your models here.

from django.core.validators import MinValueValidator,MaxValueValidator

class MultiUseCoupon(models.Model):
    code=models.CharField(max_length=50,unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active=models.BooleanField(default=False)
    category = 'MultiUse'
    def __str__(self):
        return self.code
    

class SingleUseCoupon(models.Model):
    code=models.CharField(max_length=50,unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active=models.BooleanField(default=False)
    has_been_used = models.BooleanField(default=False)
    category = 'SingleUse'

    def deactivate_on_Use(self):
        self.has_been_used=True
        self.active=False
        self.save()

    def __str__(self) -> str:
        return self.code