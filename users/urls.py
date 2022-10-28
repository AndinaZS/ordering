from django.urls import path, include

from users.views import RegisterApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view())
]