from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
