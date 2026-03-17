from django import forms
from fishtray.models import scheduler

class SchedulerForms(forms.ModelForm):
    class Meta:
        model=scheduler
        fields=['rotaion_time', 'open_delay', 'servo_angle', 'status']