from django.urls import path

from products.views import ProductListAPIView, ProductCreateAPIView

urlpatterns = [
    path('', ProductListAPIView.as_view()),
    path('loadprice/', ProductCreateAPIView.as_view()),

]