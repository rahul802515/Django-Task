from django.contrib import admin

# Register your models here.

from .models import User, Books
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.unregister(Group)

admin.site.register(Books)
admin.site.register(User)