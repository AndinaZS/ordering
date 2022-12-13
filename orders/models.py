from django.db import models
from ordering.settings import AUTH_USER_MODEL
from products.models import ProductItem
from users.models import Contact


STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
    )

class Order(models.Model):

    state = models.CharField(choices=STATE_CHOICES, max_length=14, verbose_name='Статус заказа')
    customer = models.ForeignKey(AUTH_USER_MODEL,
                                 related_name='orders',
                                 on_delete=models.CASCADE,
                                 verbose_name='Покупатель')
    contact = models.ForeignKey(Contact, related_name='orders',
                                on_delete=models.CASCADE,
                                null=True, blank=True, default=None,
                                verbose_name='Адрес доставки')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказов"


class OrderPositions(models.Model):
    # for m2m relation between Order and Product
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='positions',
                              verbose_name='Заказ')
    good = models.ForeignKey(ProductItem, on_delete=models.CASCADE,
                             related_name='positions',
                             verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')


