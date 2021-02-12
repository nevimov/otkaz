from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from core import const
from core.utils import change_textarea_widgets
from catalog.admin import BaseWindowAdmin
from catalog.models import Window
from .models import Seller, Phone, Place


class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 1
    max_num = 4


@change_textarea_widgets(rows=3, cols=35)
class PlaceAdmin(admin.StackedInline):
    model = Place
    extra = 1
    max_num = 5


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime_created'
    inlines = [PhoneInline, PlaceAdmin]


class DummySellerAdminSite(AdminSite):
    """
    Temporary replacement for an actual admin interface that should be
    provided to sellers. It does not look pretty, but allows for basic
    features like profile editing and managing windows owned by the seller.
    """
    enable_nav_sidebar = False
    site_header = 'Личный кабинет'
    site_title = 'Личный кабинет'
    index_title = 'Главная страница'

    def each_context(self, request):
        context = super().each_context(request)

        # each_context() runs regardless of whether the user is logged-in or
        # not. Unauthorized users don't have any objects associated with them.
        # Thus, if the user is anonymous, then any queries using request.user,
        # will result in error.
        if request.user.is_authenticated:
            seller = Seller.objects.get(user=request.user)
            context['seller'] = seller
            context['nav_urls'] = {
                'seller': seller.dummy_seller_admin_url,
                'window_list': self.window_changelist_url,
            }

        return context

    def has_permission(self, request):
        user = request.user
        return user.is_active and user.is_seller

    @property
    def window_changelist_url(self):
        app_label, model_name = Window._meta.app_label, Window._meta.model_name
        return reverse_lazy(
            f'admin:{app_label}_{model_name}_changelist',
            current_app=const.SELLER_ADMIN_SITE,
        )

    def get_urls(self):
        urlpatterns = super().get_urls()

        # Redirect logged-in sellers to Window list admin instead of the
        # default index page.
        urlpatterns.insert(0, path(
            '',
            RedirectView.as_view(url=self.window_changelist_url),
            name='index',
        ))
        return urlpatterns

dummy_seller_admin_site = DummySellerAdminSite(const.SELLER_ADMIN_SITE)


@admin.register(Seller, site=dummy_seller_admin_site)
class DummyProfileAdmin(SellerAdmin):

    fieldsets = [
        (None, {
            'fields': ['public_name', 'email', 'website']
        }),
        ('Реквизиты компании', {
            'fields': ['legal_name', 'OGRN', 'INN']
        }),
    ]

    def get_queryset(self, request):
        """
        Restrict the queryset to a single Seller object associated with the
        logged-in user.
        """
        queryset = super().get_queryset(request).filter(user=request.user)
        assert len(queryset) == 1
        return queryset


@admin.register(Window, site=dummy_seller_admin_site)
class DummyWindowAdmin(BaseWindowAdmin):
    actions = None
    change_form_template = 'admin/sellers/window/change_form.html'
    change_list_template = 'admin/sellers/window/change_list.html'

    def get_queryset(self, request):
        """
        Restrict the queryset to a subset of windows owned by the seller.
        """
        queryset = super().get_queryset(request)
        return queryset.filter(seller__user=request.user)