from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User, Authy_User
from django_email_verification.models import User as email_user

admin.site.register(User, UserAdmin)
admin.site.register(email_user)
admin.site.register(Authy_User)