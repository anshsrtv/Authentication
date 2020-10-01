from django import forms
from core.models import User
from django.contrib.auth.forms import UserCreationForm



class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields['password2'] 

    class Meta:
        model = User
        fields = ('name','username','contact','email')

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=7)

class LoginForm(forms.Form):
    contact = forms.CharField(max_length=10)
