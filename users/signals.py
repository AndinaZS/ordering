from authemail.models import SignupCode
from django.conf import settings
from random import randint
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_verified_email(sender, instance, created, **kwargs):
    if created:
        must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)

        if must_validate_email:
            ipaddr = f'{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}'
            signup_code = SignupCode.objects.create_signup_code(instance, ipaddr)
            signup_code.send_signup_email()