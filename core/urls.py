"""URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
  https://docs.djangoproject.com/en/3.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from sellers.admin import dummy_seller_admin_site
from .admin import main_admin_site
from .views import (
    MainPageView,
    AboutView,
    PiiAgreementView,
)

urlpatterns = [
    path('', MainPageView.as_view(), name="main"),
    path('catalog/', include('catalog.urls')),
    path('contacts/', include('contacts.urls')),
    path('about', AboutView.as_view(), name="about"),

    path('sellers/', include('sellers.urls')),
    path('seller-admin/', dummy_seller_admin_site.urls),
    path('accounts/', include('allauth.urls')), # Must be placed after 'sellers'

    path('pii-agreement', PiiAgreementView.as_view(), name="pii-agreement"),
    path('admin/', main_admin_site.urls),
]

if settings.DEBUG:
    # Serve user-uploaded media files from MEDIA_ROOT using the
    # django.views.static.serve() view.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Include django-debug-toolbar urls, if the DEBUG_TOOLBAR setting is truthy
    DEBUG_TOOLBAR = getattr(settings, 'DEBUG_TOOLBAR', False)
    if DEBUG_TOOLBAR:
        import debug_toolbar
        debug_toolbar_path = path('debug/', include(debug_toolbar.urls))
        urlpatterns.append(debug_toolbar_path)
