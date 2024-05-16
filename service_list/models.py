from django.db import models
from django.conf import settings

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    overview = models.TextField(verbose_name='Описание')
    picture = models.ImageField(upload_to='service_list/', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    overview = models.TextField(verbose_name='Короткое описание')
    overview_big = models.TextField(verbose_name='Полное описание', **NULLABLE)
    picture = models.ImageField(upload_to='service_list/', **NULLABLE)
    category = models.ForeignKey('Category', verbose_name='Категория',
                                 on_delete=models.SET_DEFAULT, default='000')
    price = models.IntegerField(verbose_name='Цена')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                verbose_name='Создатель')
    time_to_session = models.PositiveSmallIntegerField(default=15, verbose_name='время на сеанс')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'обследование'
        verbose_name_plural = 'обследование'
