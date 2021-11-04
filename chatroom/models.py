from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.

# Create your models here.
class Room(models.Model):
  room_name = models.CharField(max_length=50)
  participants = models.CharField(max_length=1000, default="")
  host = models.CharField(max_length=50,default="")
  password = models.CharField(max_length=50, default="")
  def __str__(self):
    return self.room_name
  def add_user(self,user_name):
    self.participants+=(user_name+"|")
    self.save()
  def delete_user(self,user_name):
    self.participants=self.participants.replace(user_name+'|', '')
    self.save()
  def get_list_user_names(self):
    return self.participants.split("|")


# Create your models here.
class Message(models.Model):
  room_name = models.ForeignKey(Room, on_delete=models.CASCADE)
  message = models.CharField(max_length=100)
  sender = models.ForeignKey(User, on_delete=models.CASCADE)
  date_sent = models.DateTimeField(_('date sent'), default=timezone.now)

  def __str__(self):
    return self.message

