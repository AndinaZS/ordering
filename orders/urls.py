from django.contrib import admin
from django.urls import path

from orders.views import BasketView, OrderView

urlpatterns = [
    path('basket/', BasketView.as_view()),
    path('', OrderView.as_view())

]