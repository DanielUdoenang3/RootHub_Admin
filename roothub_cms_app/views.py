from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from roothub_cms_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,logout
from django.contrib import messages

from roothub_cms_app.models import Admin


# Create your views here.

def showDemoPage(request):
    return render(request, "demo.html")


def showLoginPage(request):
    return render(request,"login.html")

def dologin (request):
    if request.method!="POST":
        return HttpResponse("""<h2>Method not allowed</h2>
                            <p>Try reloading the page</p>
                            <br>Why you are seeing this is because your submision is not POST</br> """)
    else:
        user=EmailBackEnd.authenticate(request, username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type == "1":
                return HttpResponseRedirect("admin_home")
            elif user.user_type == "2":
                return HttpResponse("Welcome Boss")
            elif user.user_type == "3":
                return HttpResponse("Student")
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")
        
def Get_User_Details(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" "+  "Usertype : "+request.user.user_type)
    if request.user==None:
        return HttpResponse("Please Login First")
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")





