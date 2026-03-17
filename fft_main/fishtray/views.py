from django.shortcuts import render, get_object_or_404, redirect
from fishtray.forms import SchedulerForms
from fishtray.models import scheduler, LastFoodTime
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.utils import timezone


def home(request):
    return render(request, "home.html")

def scheduler_update(request):
    data=get_object_or_404(scheduler, 1)
    
    if request.method == "POST":
        form = SchedulerForms(request.POST, instance=data)
        if form.is_vaild():
            form.save()
            return redirect("read")
    else:
        form = SchedulerForms(instance=data)
        
    return render(request, "update.html", {"form":form})
            

@require_GET
def send_sensor_data(request):
    sche = scheduler.objects.first()

    if sche.status:
        last_food = LastFoodTime.objects.first()
        if not last_food:
            return JsonResponse({"status": False, "error": "No last food record"})

        now = timezone.localtime()

        if last_food.last_food + sche.rotaion_time <= now:
            last_food.last_food = now
            last_food.save()

            return JsonResponse({
                "status": True,
                "open_delay": sche.open_delay,
                "servo_angle": sche.servo_angle
            })

    return JsonResponse({"status": False})