from django.db import models
from django.forms import Textarea

__all__ = ['change_textarea_widgets']


def del_url(urlpatterns, *names):
    """
    Delete given named URL patterns from `urlpatterns`.
    """
    for i, pattern in enumerate(urlpatterns):
        if pattern.name in names:
            del urlpatterns[i]
            break


def change_textarea_widgets(**textarea_attrs):

    def wrapper(cls):
        overrides = cls.formfield_overrides
        overrides.setdefault(models.TextField, {'widget': {}})
        overrides[models.TextField]['widget'] = Textarea(attrs=textarea_attrs)
        return cls

    return wrapper