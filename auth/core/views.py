from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from core.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from core.forms import SignupForm, OTPForm, LoginForm
from authy.api import AuthyApiClient
from django_email_verification import sendConfirm
from django_email_verification.models import User as Email_User
from django.http import HttpResponse
import requests
from django.contrib.auth.decorators import login_required


authy_api = AuthyApiClient('H7VjL9l9APs3A7LFZ0pf5jIBRD7dtVSG')

@login_required(login_url='login')
def hello_world(request):
    try:
        email_user= Email_User.objects.get(
            user = user
        )
    except:
        return render(request, 'index.html', {'user':request.user, 'verified':True})
    else:
        return render(request, 'index.html', {'user':request.user, 'verified':False})
    

def signup(request):
   if request.method == 'POST':
       form = SignupForm(request.POST)
       if form.is_valid():
            
            authy_user = authy_api.users.create(
                email=form.cleaned_data.get('email'),
                phone=form.cleaned_data.get('contact'),
                country_code=91
            )
            if authy_user.ok():
                print(authy_user.id)
                sms = authy_api.users.request_sms(authy_user.id, {'force': True})
                if sms.ok():
                    print('SMS request successful')

                    user= User.objects.create(
                        username=form.cleaned_data.get('username'),
                        name = form.cleaned_data.get('name'),
                        email=form.cleaned_data.get('email'),
                        contact = form.cleaned_data.get('contact'),
                        password = form.cleaned_data.get('password1'),
                        authy_id=authy_user.id
                    )
                    try:
                        sendConfirm(user)
                    except:
                        return HttpResponse('You may have entered a wrong email address. Please check it again!')

                    return redirect('verify_otp', authy_user.id)
                    #
                    # else:
                    #     login(request, user)
                    #     return render(request, 'index.html', {'user': user})
                else:
                    return HttpResponse('You may have entered a wrong contact number. Please check it!')
            else:
                print(authy_user.errors())
                return render(request, '500.html')
            
   else:
       form = SignupForm()
   return render(request,'signup.html',{'form':form})

def verify_otp(request, authy_id):
    if request.method == 'POST':
       form = OTPForm(request.POST)
       if form.is_valid():
            print(form.cleaned_data.get('otp'))
            # print(f"https://api.authy.com/protected/json/verify/{form.cleaned_data.get('otp')}/{authy_id}")
            verification = authy_api.tokens.verify(authy_id, token=str(form.cleaned_data.get('otp')))
            # print(req.json())
            # print(verification)
            if(verification.ok() and verification['success']):
                status = authy_api.users.status(authy_id)
                if status.ok():
                    try:
                        user = User.objects.get(authy_id=authy_id)
                    except:
                        return HttpResponse("User Not Registered")
                    else:
                        user.phone_verified=True
                        user.save()
                        try:
                            email_user= Email_User.objects.get(
                                user = user
                            )
                        except:
                            login(request, user)
                            return redirect('hello')
                        else:
                            login(request, user)
                            return render(request, 'verify_email.html')
                        
                else:
                    return HttpResponse("User Not Registered")
                # return render(request, 'index.html', )
            else:
                return HttpResponse("Wrong OTP")
    else:
        form = OTPForm()
        return render(request, 'verify_otp.html',  {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                print(form.cleaned_data.get('contact'))
                user = User.objects.get(
                    contact= form.cleaned_data.get('contact')
                )
            except:
                return HttpResponse("Enter Registered Contact Number!")
            else:
                sms = authy_api.users.request_sms(
                    user.authy_id
                )
                print(sms)
                if sms.ok():
                    return redirect('verify_otp', user.authy_id)
                else:
                    return render(request, "500.html")
    else:
        form = LoginForm()
        return render(request,'login.html',{'form':form})
       

    #    print(user)
    #    if user is not None:
    #        login(request,user)
    #        return redirect('hello')
    #    else:
    #        messages.error(request,'Invalid Credentials')
    #        return redirect('login')
    


def user_logout(request):
    logout(request)
    return redirect('login')

def verify_email(request, success):
    return render('confirm_template.html', {"success":success})