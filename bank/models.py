from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    addres = models.TextField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    acn = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
class history(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     acn = models.PositiveIntegerField()
     crid = models.PositiveIntegerField(default=0)
     dev = models.PositiveIntegerField(default=0)
     action = models.CharField(max_length=10)
     date_time = models.DateTimeField(auto_now_add=True)

class vrf(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    vf = models.BooleanField(default=False)
class email_token(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    forget_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

