from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_client', 'mobile', 'country','gender','about','img_link'
        )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_client', 'mobile', 'country', 'gender','about','img_link')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_client', 'mobile', 'country', 'gender','about','img_link')
        })
    )

admin.site.register(User, CustomUserAdmin),



@admin.register(Job)
class CustomJob(admin.ModelAdmin):
    list_display =('id','title','price','posted_date')

admin.site.register(Skill)

admin.site.register(Proposal)
admin.site.register(Message)