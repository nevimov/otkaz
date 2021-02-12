from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView

from sellers.admin import dummy_seller_admin_site
from .models import Seller


# XXX Temporary replacement for an actual view.
class SellerProfileView(LoginRequiredMixin, RedirectView):
    """
    Display the seller profile on a GET request, edit the profile on a POST
    request.
    """

    def get_redirect_url(self, *args, **kwargs):
        seller = Seller.objects.get(user=self.request.user)
        return seller.dummy_seller_admin_url



# XXX Temporary replacement for an actual view.
class SellerWindowList(LoginRequiredMixin, RedirectView):
    """
    Display a list of windows owned by the seller on a GET request, change
    the list on a POST request.
    """
    url = dummy_seller_admin_site.window_changelist_url