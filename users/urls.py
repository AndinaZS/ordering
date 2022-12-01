from authemail.views import (SignupVerify,
                             Login, Logout,
                             PasswordReset,
                             PasswordResetVerify,
                             PasswordResetVerified)
from django.urls import path, include

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
    path('', include('allauth.urls')),
    # path('password/reset/verified/', PasswordResetVerified.as_view()),
    path('users/me/', UserDetailChangeAPIView.as_view()),
    path('users/me/', include(contact.urls)),
    path('', include(company.urls)),

]
