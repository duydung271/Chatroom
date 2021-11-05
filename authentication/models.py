from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import default
GENDER_CHOICES = ((0,"Gender"),(1,"Female"),(2,"Male"))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(default='2000-01-01')
    phone = models.CharField(max_length=10)
    gender = models.IntegerField(default=0,choices=GENDER_CHOICES)
    avatar = models.ImageField(default='Unknown.jpg')
    cover = models.ImageField(default='background.jpg')
    friends = models.CharField(max_length=1000, default='')

    def add_friend(self,user_name):
        self.friends+=(user_name+"|")
        self.save()
    def unfriend(self,user_name):
        if user_name=='' or user_name==None:
            return "Fail"
        self.friends=self.friends.replace(user_name+'|', '')
        self.save()
    def get_friend_list(self):
        return self.friends.split("|")
    def is_friend(self, username):
        tmp = username+"|"
        if tmp in self.friends:
            return True
        return False

    def __str__(self):
        return self.user.username


class Status(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(default="offline", max_length=50)
    def __str__(self):
        return self.user.username




