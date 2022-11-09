from django.contrib import admin
from django.urls import path

from orders.views import CreateOrderView

urlpatterns = [
    path('', CreateOrderView.as_view())

]