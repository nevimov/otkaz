from django.urls import path

from .views import SellerProfileView, SellerWindowList

app_name = "sellers"

urlpatterns = [
    path('profile', SellerProfileView.as_view(), name="profile"),
    path('window-list', SellerWindowList.as_view(), name="window-list"),
]