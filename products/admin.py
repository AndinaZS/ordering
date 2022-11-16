from django.contrib import admin

from products.models import *

admin.site.register(Product)

admin.site.register(Parameter)

admin.site.register(Category)

admin.site.register(ParameterValue)

admin.site.register(ProductItem)