from django.db import models
from users.models import Company

class Product(models.Model):
    # модель товара
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey('Category',
                                    related_name='products',
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL, verbose_name='Категория')
    parameters = models.ManyToManyField('Parameter',
                                        related_name='products',
                                        through='ParameterValue',
                                        verbose_name='Параметры')
    companies = models.ManyToManyField(Company,
                                       related_name='products',
                                       through='ProductItem',
                                       verbose_name='Поставщики')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Список товаров"

class Category(models.Model):
    #модель категории товара
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"

class Parameter(models.Model):
    #модель свойств товара
    name = models.CharField(max_length=50, unique=True, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров"

class ParameterValue(models.Model):
    #модель для установки значения свойства конкретного товара
    parameter = models.ForeignKey(Parameter, related_name='values',
                                  on_delete=models.CASCADE, verbose_name='Параметр')
    product = models.ForeignKey(Product, related_name='values',
                                on_delete=models.CASCADE, verbose_name='Товар')
    value = models.CharField(max_length=50, verbose_name='Значение')

    class Meta:
        verbose_name = 'Значение параметра'
        verbose_name_plural = "Список значений параметров"

class ProductItem(models.Model):
    # модель связи товара с продавцом
    model = models.CharField(max_length=250, verbose_name='Модель')
    product = models.ForeignKey(Product, related_name='goods',
                                on_delete=models.CASCADE,
                                verbose_name='Наименование товара')
    shop = models.ForeignKey(Company, related_name='goods',
                             on_delete=models.CASCADE,
                             verbose_name='Продавец')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    price_rrc = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Рекомендованная розничная цена')
    instock = models.PositiveIntegerField(verbose_name='Количество')
    ext_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='Номер позиции прайса')

    class Meta:
        verbose_name = 'Товар поставщиков'
        verbose_name_plural = "Список товаров поставщиков"


