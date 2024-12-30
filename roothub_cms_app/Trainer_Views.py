from django.shortcuts import get_object_or_404, render


def trainer_home(request):
    return render(request,"trainer_template/trainer_home_template.html")

def trainer_take_attendance(request):
    return render(request,"trainer_template/trainer_take_attendance.html")
