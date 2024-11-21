from django.shortcuts import render


def error_500(request):
    return render(request,"500_error.html")

def error_404(request):
    return render(request, "404_error.html")