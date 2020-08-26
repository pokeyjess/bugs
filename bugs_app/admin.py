from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bugs_app.models import MyUser

admin.site.register(MyUser, UserAdmin)

UserAdmin.fieldsets += ('Custom fields set', {'fields' : ('display_name',)}),
