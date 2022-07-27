from django.contrib import admin
from management.models import Users


class UsersAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    list_display = ('email', 'mobile', 'phone' )

admin.site.register(Users, UsersAdmin)
# Register your models here.
