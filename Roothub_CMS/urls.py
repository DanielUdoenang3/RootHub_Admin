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

from roothub_cms_app import Error, Trainer_Views, views,HodViews
# from roothub_cms_app import settings

urlpatterns = [
    path("demo",views.showDemoPage),
    path("admin/", admin.site.urls),

    # Log in and Out
    path("", views.showLoginPage, name="login_page"),
    path("get_user_details", views.Get_User_Details),
    path("logout_user", views.logout_user, name="logout_user"),
    path("dologin", views.dologin, name="login"),


# Admin
    path("admin_home", HodViews.admin_home, name="admin_home"),

    # Add Trainer
    path("add_trainer", HodViews.add_trainer, name="add_trainer"),
    path("add_trainer_save", HodViews.add_trainer_save, name="add_trainer_save"),
    path("view_trainer", HodViews.view_trainer, name="view_trainer"),

    # Edit Trainer
    path("edit_trainer/<int:trainer_id>", HodViews.edit_trainer, name="edit_trainer"),
    path("edit_trainer_save/<int:trainer_id>", HodViews.edit_trainer_save, name="edit_trainer_save"),

    # Delete Trainer
    path("delete_trainer/<int:trainer_id>", HodViews.delete_trainer, name="delete_trainer"),

    # Add Trainee
    path("add_trainee", HodViews.add_trainee, name="add_trainee"),
    path("add_trainee_save", HodViews.add_trainee_save, name="add_trainee_save"),
    path("view_trainee", HodViews.view_trainee, name="view_trainee"),

    # Edit Trainee
    path("edit_trainee/<int:trainee_id>", HodViews.edit_trainee, name="edit_trainee"),
    path("edit_trainee_save/<int:trainee_id>", HodViews.edit_trainee_save, name="edit_trainee_save"),

    # Delete Trainee
    path("delete_trainee/<int:trainer_id>", HodViews.delete_trainee, name="delete_trainee"),

    #  Assign Trainer
    path('assign_trainer', HodViews.assign_trainer, name='assign_trainer'),
    path('get_current_trainer/<int:course_id>', HodViews.get_current_trainer, name='get_current_trainer'),

    # Mark Trainee either Present or Absent
    path('mark_attendance', HodViews.mark_attendance, name='mark_attendance'),
    path('get-trainees/', HodViews.get_trainees, name='get_trainees'),
    path('get-attendance-data/<int:trainee_id>/', HodViews.get_attendance_data, name='get_attendance_data'),
    path('get-students/', HodViews.get_students, name='get_students'),

    path("mark_presentation", HodViews.mark_presentation, name="mark_presentation"),

    #  View Attendance Report
    path('view_attendance', HodViews.view_attendance, name='view_attendance'),

    # Courses and Price
    path("add_course", HodViews.add_course, name="add_course"),
    path("add_course_save", HodViews.add_courses_save, name="add_course_save"),
    path("view_course", HodViews.view_course, name="view_course"),
    # Edit course and price
    path("edit_course/<int:course_id>", HodViews.edit_course, name="edit_course"),
    path("edit_course_save/<int:course_id>", HodViews.edit_course_save, name="edit_course_save"),

# Trainer
    path("trainer_home", Trainer_Views.trainer_home, name="trainer_home"),
    path("trainer_take_attendance", Trainer_Views.trainer_take_attendance, name="trainer_take_attendance"),

    



    # Error Pages
    path("error_500", Error.error_500),
    path("error_404", Error.error_404),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)