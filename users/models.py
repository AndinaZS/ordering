from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models

USER_TYPE_CHOICES = (
    ('provider', 'Поставщик'),
    ('customer', 'Заказчик'),)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            email=email, username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email, username, password, **extra_fields
        )

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(
            email, username, password, **extra_fields
        )


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=30,
                                unique=True,
                                db_index=True,
                                validators=[username_validator, ])
    email = models.EmailField(unique=True,
                              max_length=255,
                              db_index=True)
    company = models.ForeignKey('Company', related_name='user', default=None, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(choices=USER_TYPE_CHOICES, default='customer', max_length=9)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Список пользователей"
        ordering = ('username',)


class Company(models.Model):
    title = models.CharField(max_length=255)
    ITN = models.PositiveIntegerField(unique=True, db_index=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    ready_to_order = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Список компаний"
        ordering = ('title',)


class Contacts(models.Model):
    user = models.ForeignKey(User, related_name='contacts', blank=True,on_delete=models.CASCADE)
    postcode = models.IntegerField()
    region = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=15,)
    apartment = models.CharField(max_length=15, blank=True)
    additional_info = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = "Список контактов пользователя"

    def __str__(self):
        return f'{self.city} {self.street} {self.building}'