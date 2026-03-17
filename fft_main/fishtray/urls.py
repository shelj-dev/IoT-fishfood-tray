from django.urls import path
from fishtray import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('update/', views.scheduler_update, name="update"),
    path('send-relay/', views.send_sensor_data, name="send_relay"),
]
