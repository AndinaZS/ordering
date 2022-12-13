from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

USER_TYPE_CHOICES = (
    ('seller', 'Продавец'),
    ('customer', 'Покупатель'),)


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=30,
                                unique=True,
                                db_index=True,
                                validators=[username_validator, ], verbose_name='Имя пользователя')
    email = models.EmailField(unique=True,
                              max_length=255,
                              db_index=True)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    password_confirmed = models.CharField(max_length=50,
                                          null=True, default=None,
                                          verbose_name='Подтверждение пароля')
    company = models.ForeignKey('Company', related_name='users',
                                default=None, null=True, on_delete=models.SET_NULL,
                                verbose_name='Компания')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(choices=USER_TYPE_CHOICES,
                            default='customer', max_length=9,
                            verbose_name='тип аккаунта')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def set_verified(self):
        self.is_verified = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Список пользователей"


class Company(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    ITN = models.PositiveIntegerField(unique=True, db_index=True, verbose_name='ИНН')
    website = models.URLField(max_length=255, null=True, blank=True, verbose_name='Сайт')
    ready_to_order = models.BooleanField(default=False, verbose_name='Принимает заказы')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Список компаний"


class Contact(models.Model):
    user = models.ForeignKey(User,
                             related_name='contacts',
                             blank=True, on_delete=models.CASCADE)
    postcode = models.PositiveIntegerField(verbose_name='Индекс')
    region = models.CharField(max_length=15, blank=True, verbose_name='Регион/область')
    city = models.CharField(max_length=50, verbose_name='Населенный пункт')
    street = models.CharField(max_length=100, verbose_name='Улица')
    building = models.CharField(max_length=5, verbose_name='Дом/здание')
    apartment = models.CharField(max_length=15, blank=True, verbose_name='Помещение')
    additional_info = models.CharField(max_length=255,
                                       blank=True, null=True,
                                       verbose_name='Дополнительная информация')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = "Список контактов пользователя"

    def __str__(self):
        return f'{self.city} {self.street} {self.building}'
