from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView

from users.models import User
from users.serializers import UserSerializer



class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def send_token(self, request, user):
        current_site = get_current_site(request)
        print(request, user)
        # message = {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # }
        # mail_subject = 'Activate your blog account.'
        # email = EmailMessage(mail_subject, message, to=[user.email])
        # email.send()
        return JsonResponse({'message': 'message'})
