from django.db import models
from users.models import Company

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(null=True, blank=True)
    cathegories = models.ManyToManyField('Cathegory', related_name='products')
    properties = models.ManyToManyField('Property', related_name='products', through='Value')
    companies = models.ManyToManyField(Company, related_name='products', through='Goods')

class Cathegory(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Property(models.Model):
    name = models.CharField(max_length=50, unique=True)

class PropertyValue(models.Model):
    property = models.ForeignKey(Property, related_name='values', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

class Goods(models.Model):
    product = models.ForeignKey(Product, related_name='goods', on_delete=models.CASCADE)
    shop = models.ForeignKey(Company, related_name='goods', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField()
    ext_id = models.IntegerField()

