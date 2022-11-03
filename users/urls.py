from django.urls import path, include

from users.views import RegisterApiView, ContactListCreateApiView, ContactDetailUpdateDelApiView

urlpatterns = [
    path('signup/', RegisterApiView.as_view()),
    path('', include('authemail.urls')),
    path('users/me/contacts/', ContactListCreateApiView.as_view()),
    path('users/me/contacts/<int:pk>/', ContactDetailUpdateDelApiView.as_view())

]