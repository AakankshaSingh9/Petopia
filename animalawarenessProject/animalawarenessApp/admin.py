from django.contrib import admin
from .models import UserRegister, Userfeedback, Userdonation

# Register your models here.
@admin.register(UserRegister)
class UserRegisterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'password')

@admin.register(Userfeedback)
class UserfeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phno', 'subject', 'msg')

@admin.register(Userdonation)
class UserdonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'paymode', 'amount', 'trn_date')
