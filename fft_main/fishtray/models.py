from django.db import models


class scheduler (models.Model):
    rotaion_time = models.IntegerField()
    open_delay = models.IntegerField()
    servo_angle = models.IntegerField()
    status = models.BooleanField()
    
    
class LastFoodTime(models.Model):
    last_food = models.IntegerField()
    