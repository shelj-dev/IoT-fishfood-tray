from django.db import models

# Create your models here.
class scheduler (models.Model):
    
    rotaion_time=models.IntegerField()
    # on_time=models.TimeField(auto_now=False, auto_now_add=False)
    # off_time=models.TimeField(auto_now=False, auto_now_add=False)
    open_delay=models.IntegerField()
    servo_angle=models.IntegerField()
    status=models.BooleanField()
    