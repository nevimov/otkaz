from django.urls import path

from . import views

app_name = "contacts"

urlpatterns = [
    path(
        'request-callback/',
        views.RequestCallback.as_view(),
        name='request-callback',
    ),
    path(
        'request-feedback/',
        views.RequestFeedback.as_view(),
        name='request-feedback',
    )
]