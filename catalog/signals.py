from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Window


@receiver(post_save, sender=Window, dispatch_uid='clear_window_dimension_xtr')
@receiver(post_delete, sender=Window, dispatch_uid='clear_window_dimension_xtr')
def clear_window_dimension_extremes(sender, **kwargs):
    """
    When a window is saved or deleted, clear cached minimal and maximal
    window dimensions for the current city.
    """
    # Because of the way the descriptor protocol works, using del (or delattr)
    # on a cached_property that hasn’t been accessed raises AttributeError.
    Window.objects._dimension_extremes  # Avoids AttributeError in tests
    del Window.objects._dimension_extremes