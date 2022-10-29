from django.urls import path, include

from users.views import RegisterApiView, VerifiedApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('confirm_email/', VerifiedApiView.as_view())
]