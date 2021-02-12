from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
     path(
          '',
          views.WindowList.as_view(),
          name='window-list'
     ),
     path(
         '<int:pk>',
         views.WindowDetail.as_view(),
         name='window-detail'
     ),
]