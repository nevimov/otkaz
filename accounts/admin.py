from django.contrib import admin
from django.contrib.auth import admin as auth_admin, models as auth_models

from .models import User, Group

# Group 'users' and 'groups' under the same app
admin.site.unregister(auth_models.Group)
admin.site.register(Group, auth_admin.GroupAdmin)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    pass
