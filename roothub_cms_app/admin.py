from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from roothub_cms_app.models import *

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)

admin.site.register(Courses)

admin.site.register(Trainee)

admin.site.register(Trainers)