from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import User

# Register your models here.
# class UserAdmin(BaseUserAdmin):
#     list_display = ['email', 'first_name', 'last_name', 'is_active']
#     fieldsets = ()
# admin.site.register(User, UserAdmin)

class UserAdmin(BaseUserAdmin):
    # Fields to display in admin list page
    list_display = ("id", "email", "username", "is_staff", "is_active")

    # Fields which become clickable links
    list_display_links = ("email",)

    # Enable search
    search_fields = ("email", "username")

    # Add filters
    list_filter = ("is_staff", "is_active")

    # Make email required and unique in admin form
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    # For creating users in admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    ordering = ("email",)

admin.site.register(User, UserAdmin)
