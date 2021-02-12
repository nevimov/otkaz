import json

from django.db import models
from django.conf import settings
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
    URLValidator,
)
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from core import const

__all__ = ['Seller']


class Seller(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    public_name = models.CharField(
        'Название компании',
        max_length=60,
        help_text='Например: Мир Окон.',
        unique=True,
    )
    legal_name = models.CharField(
        'Наименование юрлица или ИП',
        max_length=60,
        blank=True,
        help_text='Например: ООО Победа, ЗАО Лотос, ИП Кузнецов Иван Андреевич.'
    )
    OGRN = models.CharField(
        'ОГРН',
        max_length=13,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{13}$', 'Неверный ОГРН')],
        help_text='Введите 13 цифр, без пробелов.'
    )
    INN = models.CharField(
        'ИНН',
        max_length=12,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^(\d{10}|\d{12})$', 'Неверный ИНН')],
        help_text='Введите 10 или 12 цифр, без пробелов.'
    )
    website = models.URLField(
        'Ссылка на ваш вебсайт',
        blank=True,
        validators=[URLValidator(schemes=['http', 'https'])],
    )
    email = models.EmailField(
        'Контактный E-mail',
        blank=True,
        max_length=100,
        help_text='Если вы оставите свой Email, мы сможем уведомить вас в '
                  'случае возникновения неполадок с вашей учетной записью.'
    )
    datetime_created = models.DateTimeField(
        'Время создания записи',
        auto_now_add=True,
    )
    datetime_changed = models.DateTimeField(
        'Время последнего изменения',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return f'{self.public_name}'

    def _get_absolute_url(self, site=None):
        return reverse(
            f'admin:{self._meta.app_label}_{self._meta.model_name}_change',
            args=[self.pk],
            current_app=site,
        )

    @property
    def main_admin_url(self):
        return self._get_absolute_url()

    @property
    def dummy_seller_admin_url(self):
        return self._get_absolute_url(site=const.SELLER_ADMIN_SITE)

    def list_phones(self):
        """
        Return a list of the sellers' contact phones in the E164 format.
        """
        return [
            {"e164": p.number.as_e164, "national": p.number.as_national}
            for p in self.phones.all()
        ]

    def list_places(self):
        """
        Return places owned by the seller as a list of named tuples of 2
        elements (label, address).
        """
        return [
            {"label": p.get_type_display(), "address": p.full_address}
            for p in self.places.all()
        ]

    @property
    def as_json(self):
        return json.dumps({
            "public_name": self.public_name,
            "legal_name": self.legal_name,
            "OGRN": self.OGRN,
            "INN": self.INN,
            "website": self.website,
            "phones": self.list_phones(),
            "places": self.list_places(),
        })


class Phone(models.Model):
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='phones',
        related_query_name='phone',
        verbose_name='Продавец',
    )
    number = PhoneNumberField(
        'Номер',
        help_text='Телефон, по которому покупатели смогут с вами связаться.'
    )

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

    def __str__(self):
        return f'{self.number.as_national}'


class Place(models.Model):

    class Types(models.TextChoices):
        OFFICE = 'O', 'Офис'
        WAREHOUSE = 'W', 'Склад'

    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='places',
        related_query_name='place',
    )
    type = models.CharField('Тип', max_length=1, choices=Types.choices)
    city = models.ForeignKey(
        'cities.city',
        on_delete=models.CASCADE,
        related_name='places',
        related_query_name='place',
        verbose_name='Город',
    )
    street_address = models.TextField(
        'Городской адрес',
        validators=[MinLengthValidator(3), MaxLengthValidator(70)],
    )

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.full_address

    @property
    def full_address(self):
        return f"{self.city}, {self.street_address}"