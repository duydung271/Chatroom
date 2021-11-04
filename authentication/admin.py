from django.contrib import admin

from authentication.models import Profile, Status
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class StatusInline(admin.StackedInline):
    model = Status
    can_delete = False
    verbose_name_plural = 'status'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,StatusInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(User, UserAdmin)