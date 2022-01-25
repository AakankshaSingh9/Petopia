from django.core import validators
from django import forms

class Registration(forms.Form):
    name = forms.CharField(error_messages={'required':'Enter Your Name'})
    email = forms.EmailField(error_messages={'required':'Enter Your Email'}, min_length=5, max_length=25)
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'required':'Enter Your Password'}, min_length=8, max_length=15)
