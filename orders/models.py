from django.db import models
from ordering.settings import AUTH_USER_MODEL
from products.models import ProductOnSale


class State(models.Model):

    STATE_CHOICES = (
        ('basket', 'Статус корзины'),
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('assembled', 'Собран'),
        ('sent', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    )
    state = models.CharField(max_length=15, choices=STATE_CHOICES)


class Order(models.Model):
    state = models.ManyToManyField(State, related_name='order', through='OrderState')
    customer = models.ForeignKey(AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True, null=True)


class OrderState(models.Model):
    order = models.ForeignKey(Order, related_name='states', on_delete=models.CASCADE)
    state = models.ForeignKey(State, related_name='states', on_delete=models.CASCADE)
    state_beg = models.DateTimeField(auto_now_add=True)
    state_end = models.DateTimeField()

class OrderedProduct(models.Model):
    product = models.ForeignKey(ProductOnSale, on_delete=models.CASCADE)
    quantity = models.IntegerField()