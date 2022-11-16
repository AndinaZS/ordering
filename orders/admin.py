from django.contrib import admin

from orders.models import Order, OrderPositions

admin.site.register(Order)

admin.site.register(OrderPositions)