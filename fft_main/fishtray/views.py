from django.shortcuts import render, get_object_or_404, redirect
from fishtray.forms import SchedulerForms
from fishtray.models import scheduler, LastFoodTime
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.utils import timezone
from datetime import timedelta



@require_GET
def manual_feed(request):
    sche = scheduler.objects.first()

    if sche:
        sche.status = True  
        sche.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def home(request):
    return render(request, "index.html")

def scheduler_update(request):
    data=get_object_or_404(scheduler, 1)
    
    if request.method == "POST":
        form = SchedulerForms(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect("read")
    else:
        form = SchedulerForms(instance=data)
        
    return render(request, "update.html", {"form":form})
            

from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def send_sensor_data(request):
    sche = scheduler.objects.first()

    if not sche or not sche.status:
        return JsonResponse({"status": False})

    last_food = LastFoodTime.objects.first()

    if not last_food:
        return JsonResponse({"status": False, "error": "No record"})

    now = timezone.localtime()

    # First time feeding
    if last_food.last_food is None:
        last_food.last_food = now
        last_food.save()

        return JsonResponse({
            "status": True,
            "open_delay": sche.open_delay,
            "servo_angle": sche.servo_angle
        })

    next_feed_time = last_food.last_food + timedelta(seconds=sche.rotaion_time)

    # ✅ Only trigger ONCE
    if now >= next_feed_time:
        last_food.last_food = now
        last_food.save()

        return JsonResponse({
            "status": True,
            "open_delay": sche.open_delay,
            "servo_angle": sche.servo_angle
        })

    # ❌ Otherwise don't trigger
    return JsonResponse({"status": False})