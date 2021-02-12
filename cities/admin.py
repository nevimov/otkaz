from django.contrib import admin
from django.utils.html import format_html

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    readonly_fields = ['city_link']

    def city_link(self, model_instance):
        city = model_instance
        return format_html('<a href="{0}">{0}</a>', city.site_url)
    city_link.short_description = 'Ссылка на сайт'