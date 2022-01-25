from django.db import models
import datetime

# Create your models here.
class UserRegister(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=15)
    # profile_pic = models.ImageField(upload_to = "profiles/%Y/%m/%d", null=True)
    def __str__(self):
        return self.name

# class EditDetails(models.Model):
#     user = models.OneToOneField
    
class Userfeedback(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=25)
    phno = models.IntegerField()
    subject = models.CharField(max_length=25)
    msg = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class Userdonation(models.Model):
    name = models.CharField(max_length=30)
    paymode = models.CharField(max_length=25)
    amount = models.IntegerField()
    trn_date = datetime.datetime.now()
    def __str__(self):
        return self.name