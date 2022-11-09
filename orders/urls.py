from django.contrib import admin
from django.urls import path

from orders.views import CreateOrderView, UpdateOrderView

urlpatterns = [
    path('basket/', CreateOrderView.as_view()),
    path('basket/<int:pk>/', UpdateOrderView.as_view())

]