from django.urls import path
from fishtray import views

urlpatterns = [
    path('home/', views.home),
    path('update/', views.scheduler_update),
    path('send-relay/', views.send_sensor_data),
    path('manual-feed/', views.manual_feed),
]
