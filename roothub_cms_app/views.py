from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from roothub_cms_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,logout
from django.contrib import messages


# Create your views here.

def showDemoPage(request):
    return render(request, "demo.html")

def showLoginPage(request):
    return render(request,"login.html")

def dologin (request):
    if request.method!="POST":
        return HttpResponse("error_404")
    else:
        user=EmailBackEnd.authenticate(request, username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            return HttpResponseRedirect("admin_home")
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")
        
def Get_User_Details(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+"usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")





