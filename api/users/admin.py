from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

class ProfileInline(admin.StackedInline):  # Use TabularInline for a compact view
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('phone', 'addressLine1', 'addressLine2', 'city', 'state', 'postalCode', 'country', 'bio', 'image')

# Extend UserAdmin to include Profile
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# Unregister default User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
