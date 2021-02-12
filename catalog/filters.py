import django_filters as filters

from core.forms.widgets import (
    BootstrapMultipleCheckbox,
    BootstrapRange,
    BootstrapSelect,
)
from sellers.models import Seller
from .models import Window


def get_sellers(request=None):
    """
    Return sellers available in the user city.
    """
    city_windows = Window.objects.in_city()
    city_seller_pks = city_windows.values_list('seller').distinct()
    return Seller.objects.filter(pk__in=city_seller_pks).order_by('public_name')


class WindowFilter(filters.FilterSet):
    seller = filters.ModelChoiceFilter(
        queryset=get_sellers,
        widget=BootstrapSelect,
    )
    width = filters.RangeFilter(
        widget=BootstrapRange(
            attrs_0={"placeholder": Window.objects.get_min_width},
            attrs_1={"placeholder": Window.objects.get_max_width},
        ),
    )
    height = filters.RangeFilter(
        widget=BootstrapRange(
            attrs_0={"placeholder": Window.objects.get_min_height},
            attrs_1={"placeholder": Window.objects.get_max_height},
        ),
    )
    type = filters.ChoiceFilter(
        'type',
        choices=Window.Types.choices,
        widget=BootstrapSelect,
    )
    color = filters.MultipleChoiceFilter(
        'color',
        choices=Window.Colors.choices,
        widget=BootstrapMultipleCheckbox,
    )

    class Meta:
        model = Window
        fields = [
            'width',
            'height',
            'type',
            'color',
            'seller',
        ]