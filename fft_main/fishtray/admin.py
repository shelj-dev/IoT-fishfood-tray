from django.contrib import admin
from fishtray.models import scheduler, LastFoodTime

admin.site.register(scheduler)
admin.site.register(LastFoodTime)

