from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# it is used to customize the display and behavior of the Django admin interface for a custom user mode
class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)