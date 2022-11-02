from django.urls import path, include

from users.views import RegisterApiView

urlpatterns = [
    path('signup/', RegisterApiView.as_view(), name='authemail-signup'),
    path('', include('authemail.urls')),
]