from django.db import models
from datetime import datetime


class TimeStampedModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=datetime.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последняя дата обновления')

    class Meta:
        abstract = True


class InvoiceModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=datetime.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последняя дата обновления')

    class Meta:
        abstract = True
