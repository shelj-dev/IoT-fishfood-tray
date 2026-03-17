from django.shortcuts import render, get_object_or_404, redirect
from fishtray.forms import SchedulerForms
from fishtray.models import scheduler


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
            
            
    
