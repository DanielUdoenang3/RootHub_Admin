"""
URL configuration for Roothub_CMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from roothub_cms_app import Error, views,HodViews
# from roothub_cms_app import settings

urlpatterns = [
    path("demo",views.showDemoPage),
    path("admin/", admin.site.urls),

    # Log in and Out
    path("", views.showLoginPage),
    path("get_user_details", views.Get_User_Details),
    path("logout_user", views.logout_user),
    path("dologin", views.dologin),


    # Hod
    path("admin_home", HodViews.admin_home),
    path("add_staff", HodViews.add_staff),
    path("add_staff_save", HodViews.add_staff_save),
    path("add_trainee", HodViews.add_student),
    path("view_trainee", HodViews.view_trainee),
    path("add_trainee_save", HodViews.add_student_save),
    path("view_trainer", HodViews.view_trainer),


    # Courses and Price
    path("add_course", HodViews.add_course),
    path("add_course_save", HodViews.add_courses_save),
    path("view_course", HodViews.view_course),
    # path("add_price_save", HodViews.add_price_save),
    # path("add_price", HodViews.add_price),


    # Error Pages
    path("error_500", Error.error_500),
    path("error_404", Error.error_404),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)