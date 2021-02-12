from django.contrib.auth import models as auth_models

from core import const

__all__ = ['User', 'Group']


class User(auth_models.AbstractUser):

    def is_member(self, group_name):
        if self.groups.filter(name=group_name).exists():
            return True
        return False

    @property
    def is_seller(self):
        return self.is_member(const.SELLERS_GROUPNAME)


# When a custom User model is used, the admin index page shows the 'users'
# and the 'groups' links under two different apps. This seems redundant and
# confusing. We can fix the problem by unregistering the Group model from
# django.contrib.auth.models and registering a proxy for it in the same app as
# the custom user model.
class Group(auth_models.Group):

    class Meta:
        proxy = True
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'