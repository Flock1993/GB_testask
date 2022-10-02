from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path("write_values",
         views.WriteSensorValuesView.as_view(),
         name='write_values'),
]
