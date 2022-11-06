from django.urls import path

from products.views import ProductCreateAPIView

urlpatterns = [
    path('', ProductCreateAPIView.as_view()),

]