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
    state = models.CharField(choices=STATE_CHOICES, max_length=14)
    customer = models.ForeignKey(AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, related_name='orders',
                                on_delete=models.CASCADE,
                                null=True, blank=True, default=None)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказов"


class OrderPositions(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='positions')
    good = models.ForeignKey(ProductItem, on_delete=models.CASCADE, related_name='positions')
    quantity = models.PositiveIntegerField()


