from authemail.views import (SignupVerify,
                             Login, Logout,
                             PasswordReset,
                             PasswordResetVerify,
                             PasswordResetVerified)
from django.urls import path, include, re_path
from drf_spectacular.extensions import OpenApiAuthenticationExtension

from users.views import (RegisterApiView,
                         ContactViewSet,
                         CompanyViewSet,
                         UserDetailChangeAPIView)
from rest_framework import routers

contact = routers.SimpleRouter()
contact.register('contact', ContactViewSet, basename='contact')
company = routers.SimpleRouter()
company.register('company', CompanyViewSet)

urlpatterns = [
    path('signup/', RegisterApiView.as_view()),
    path('signup/verify/', SignupVerify.as_view()),
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('password/reset/', PasswordReset.as_view()),
    path('password/reset/verify/', PasswordResetVerify.as_view()),
    re_path('', include('social_django.urls', namespace='social')),
    path('users/me/', UserDetailChangeAPIView.as_view()),
    path('users/me/', include(contact.urls)),
    path('', include(company.urls)),

]

