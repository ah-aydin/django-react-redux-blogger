from django.contrib import admin
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'username')

    readonly_fields = ('email', 'username', 'date_joined', 'last_login', 'password', 'blog_count')
    fieldsets = (
        ('Personal Information', {
            'fields': ('email', 'username', 'password'),
        }),
        ('Account Information', {
            'fields': ('date_joined', 'last_login', 'blog_count'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_admin'),
        })
    )