from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bugs_app.models import MyUser, Ticket

admin.site.register(MyUser, UserAdmin)
admin.site.register(Ticket)

UserAdmin.fieldsets += ('Custom fields set', {'fields' : ('display_name',)}),
