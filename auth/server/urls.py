from django.contrib import admin
from django.urls import path, include
from core.views import log_in, signup, user_logout, hello_world, verify_email, verify_otp
from django_email_verification import urls as mail_urls

urlpatterns = [
    path('', hello_world, name='hello'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', log_in, name='login'),
    path('logout/', user_logout, name='logout'),
    path('email/', include(mail_urls)),
    path('verify_otp/<int:authy_id>', verify_otp, name='verify_otp'),
]
