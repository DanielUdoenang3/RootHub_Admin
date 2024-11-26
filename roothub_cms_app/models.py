import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
# class MagicLinkToken(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='magic_tokens')
#     token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_used = models.BooleanField(default=False)

#     def is_valid(self):
#         # Token is valid for 15 minutes
#         return not self.is_used and (timezone.now() - self.created_at).seconds < 900

class CustomUser(AbstractUser):
  user_type_data=((1,"Admin"),(2,"Trainer"),(3,"Trainee"))
  user_type= models.CharField(default=1,choices=user_type_data,max_length=10)

  middle_name = models.CharField(max_length=255, blank=True, null=True)
  gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
  address = models.TextField(blank=True, null=True)
  religion = models.CharField(max_length=255, blank=True, null=True)
  state = models.CharField(max_length=255, blank=True, null=True)
  country = models.CharField(max_length=255, blank=True, null=True)

class Admin(models.Model):
  id = models.AutoField(primary_key=True)
  admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  objects = models.Manager()

class Trainers(models.Model):
  id = models.AutoField(primary_key=True)
  admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  objects = models.Manager()

class Courses(models.Model):
  id = models.AutoField(primary_key=True)
  course_name = models.CharField(max_length=255)
  price_name = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()



class Trainee(models.Model):
  id = models.AutoField(primary_key=True)
  admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
  gender = models.CharField(max_length=255)
  profile_pic = models.FileField()
  address = models.TextField()
  course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  objects = models.Manager()

class Attendance(models.Model):
  id = models.AutoField(primary_key=True)
  course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
  attendance_date = models.DateTimeField(auto_now_add=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  objects = models.Manager()

class Presentation(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=255)
  course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="presentations")
  trainer = models.ForeignKey(Trainers, on_delete=models.CASCADE, related_name="presentations")
  date = models.DateField(default=timezone.now)
  score_appearance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
  score_content = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()

class AttendanceReport(models.Model):
  id = models.AutoField(primary_key=True)
  student_id = models.ForeignKey(Trainee, on_delete=models.DO_NOTHING)
  attendance_id = models.ForeignKey(Attendance, on_delete=models.DO_NOTHING)
  status = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  objects = models.Manager()

class FeedBackStudent(models.Model):
  id = models.AutoField(primary_key=True)
  student_id = models.ForeignKey(Trainee, on_delete=models.CASCADE)
  feedback = models.TextField()
  feedback_reply = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  objects = models.Manager()

class FeedBackTrainer(models.Model):
  id = models.AutoField(primary_key=True)
  trainer_id = models.ForeignKey(Trainers, on_delete=models.CASCADE)
  feedback = models.TextField()
  feedback_reply = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  objects = models.Manager()

class NotificationStudent(models.Model):
  id = models.AutoField(primary_key=True)
  student_id = models.ForeignKey(Trainers, on_delete=models.CASCADE)
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  objects = models.Manager()

class NotificationTrainer(models.Model):
  id = models.AutoField(primary_key=True)
  trainer_id = models.ForeignKey(Trainers, on_delete=models.CASCADE)
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  objects = models.Manager()

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
      if instance.user_type==1:
        Admin.objects.create(admin=instance)
      if instance.user_type==2:
        Trainers.objects.create(admin=instance)
      if instance.user_type==3:
        Trainee.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
  if instance.user_type==1:
    instance.admin.save()
  if instance.user_type==2:
    instance.trainers.save()
  if instance.user_type==3:
    instance.trainee.save()
