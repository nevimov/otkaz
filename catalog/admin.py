from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from sellers.models import Seller
from .models import Window


class WindowAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit 'place' choices to places owned by the window seller
        self.fields['place'].queryset = self.instance.seller.places.all()


class BaseWindowAdmin(admin.ModelAdmin):
    form = WindowAdminForm
    date_hierarchy = 'datetime_created'
    readonly_fields = [
        'datetime_created',
        'datetime_changed',
    ]
    fieldsets = [
        (None, {
            'fields': [
                'type',
                'width',
                'height',
                'color',
                'price',
                'place',
                'description',
            ],
        }),
    ]
    list_display = [
        'type',
        'width',
        'height',
        'color',
        'price',
        'datetime_created',
    ]
    list_filter = [
        'type',
        'color',
        'datetime_created',
    ]
    list_select_related = True

    def view_on_site(self, obj):
        protocol = settings.PROTOCOL
        domain = obj.place.city.site.domain
        return f'{protocol}://{domain}{obj.get_absolute_url()}'

    def save_model(self, request, obj, form, change):
        obj.seller = Seller.objects.get(user=request.user)
        super().save_model(request, obj, form, change)


@admin.register(Window)
class WindowAdmin(BaseWindowAdmin):

    list_display = BaseWindowAdmin.list_display + [
        'seller_company',
    ]

    list_filter = BaseWindowAdmin.list_filter + [
        'seller',
    ]

    readonly_fields = BaseWindowAdmin.readonly_fields + [
        'seller_link',
    ]

    fieldsets = BaseWindowAdmin.fieldsets + [
        ('Доп. информация', {
            'fields': [
                'datetime_created',
                'datetime_changed',
                'seller_link',
            ],
        }),
    ]

    def seller_company(self, model_instance):
        return model_instance.seller.public_name
    seller_company.admin_order_field = '-seller'
    seller_company.short_description = 'Компания'

    def seller_link(self, model_instance):
        seller = model_instance.seller
        return format_html(
            '<a href="{}">{}</a>',
            seller.main_admin_url,
            seller.user.username,
        )
    seller_link.short_description = 'Продавец'