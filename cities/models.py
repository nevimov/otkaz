from django.db import models
from django.contrib.sites.models import Site

from django.conf import settings

__all__ = ['City']


class City(models.Model):
    name = models.CharField('Название', max_length=30, unique=True)
    site = models.OneToOneField(
        Site,
        on_delete=models.PROTECT,
        verbose_name='Сайт',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name

    @property
    def site_url(self):
        return f'{settings.PROTOCOL}://{self.site.domain}'