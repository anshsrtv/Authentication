from django import forms
from core.models import User
from django.contrib.auth.forms import UserCreationForm



class SignupForm(UserCreationForm):
  class Meta:
       model = User
       fields = ('name','username','contact','email')

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=7)

class LoginForm(forms.Form):
    contact = forms.CharField(max_length=10)
