from django.urls import path
from . import views

urlpatterns = [
    path('vehicle_positions/', views.get_vehicle_positions),
    path('get_weather/', views.get_weather),
    path('get-cal-fire/', views.get_geojson_data, name='get-cal-fire'),
]
