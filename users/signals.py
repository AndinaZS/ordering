from authemail.models import SignupCode, send_multi_format_email
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_verified_email(sender, instance, created,  **kwargs):
    if created:
        must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)

        if must_validate_email:
            ipaddr = '127.0.0.1:8000/api/v1/'
            signup_code = SignupCode.objects.create_signup_code(instance, ipaddr)
            signup_code.send_signup_email()
