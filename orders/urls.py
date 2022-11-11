from django.contrib import admin
from django.urls import path

from orders.views import BasketView

urlpatterns = [
    path('basket/', BasketView.as_view()),
    # path('basket/<int:pk>/', UpdateOrderView.as_view())

]