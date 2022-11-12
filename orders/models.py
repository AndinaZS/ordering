from django.db import models
from ordering.settings import AUTH_USER_MODEL
from products.models import ProductOnSale
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


class OrderPositions(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='position')
    good = models.ForeignKey(ProductOnSale, on_delete=models.CASCADE, related_name='position')
    quantity = models.PositiveIntegerField()


