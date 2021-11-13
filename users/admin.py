from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
@admin.register(models.User)
class UserAdmin(UserAdmin):
    """ Custom User Admin """
    
    custom_fieldsets = (
        ('Custom', {
            "fields": (
                'avatar', 
                'bio', 
                'birthdate', 
                'currency', 
                'gender', 
                'language', 
                'superhost',
            ),
        }),
    )
    fieldsets = UserAdmin.fieldsets + custom_fieldsets
    