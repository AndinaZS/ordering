from django.db import models
from users.models import Company

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey('Category',
                                    related_name='products',
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL)
    parameters = models.ManyToManyField('Parameter', related_name='products', through='ParameterValue')
    companies = models.ManyToManyField(Company, related_name='products', through='ProductOnSale')

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Parameter(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ParameterValue(models.Model):
    parameter = models.ForeignKey(Parameter, related_name='values', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

class ProductOnSale(models.Model):
    product = models.ForeignKey(Product, related_name='goods', on_delete=models.CASCADE)
    shop = models.ForeignKey(Company, related_name='goods', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    instock = models.IntegerField()
    ext_id = models.IntegerField(null=True, blank=True)

