from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Request, Vendor

# Customize the User admin to display the custom fields
class UserAdmin(BaseUserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')

    # Add custom fields for adding or editing a user in admin
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register the models
admin.site.register(User, UserAdmin)
admin.site.register(Request)
admin.site.register(Vendor)
