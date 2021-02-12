import collections

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Min, Max
from django.urls import reverse
from django.utils.functional import cached_property

from ckeditor.fields import RichTextField

from cities.models import City

__all__ = ['Window']


class WindowQuerySet(models.QuerySet):

    def in_city(self, city=None):
        """
        Get windows associated with a given city.
        """
        if not city:
            city = Site.objects.get_current().city
        return self.filter(place__city=city)

    def order_by_newness(self):
        return self.order_by('-datetime_created')


class WindowManager(models.Manager):

    def get_queryset(self):
        return WindowQuerySet(self.model, using=self._db)

    def calc_fit_width(self, aperture_width):
        """
        Calculate minimal and maximal width of windows fit for the given
        aperture width.
        """
        aperture_width = int(aperture_width)
        window_min_width = aperture_width - 150
        window_max_width = aperture_width + 50
        Width = collections.namedtuple('FitWidth', ['min', 'max', 'range'])
        return Width(
            min=window_min_width,
            max=window_max_width,
            range=(window_min_width,  window_max_width),
        )

    def calc_fit_height(self, aperture_height):
        """
        Calculate minimal and maximal height of windows fit for the given
        aperture height.
        """
        aperture_height = int(aperture_height)
        window_min_height = aperture_height - 150
        window_max_height = aperture_height + 50
        Height = collections.namedtuple('FitHeight', ['min', 'max', 'range'])
        return Height(
            min=window_min_height,
            max=window_max_height,
            range=(window_min_height,  window_max_height),
        )

    def sort_for_aperture(self, windows, aperture_width, aperture_height,
                          reverse=False):
        """
        Sort windows by suitablity for the given aperture.

        The sorting is performed according to the following rules:
        * Firstly, all windows are divided into three groups:

          (1) FIT windows whose height and width are smaller than the aperture
              (the difference for both dimensions is <= |-150|mm).

          (2) FIT windows with at least one dimension greater than the
              corresponding aperture dimension (the difference for the
              greater dimension(s) is <= |+50|mm).

          (3) Windows considered UNFIT for installation into the given
              aperture (height and/or width difference is out of the
              allowed (-150mm, +50mm) range).

          The first group always has the highest priority and the second
          group is, obviously, more important than the last one.

        * The order inside each group is determined by the absolute
          difference between the aperture area and window area -- the
          smaller the difference, the higher the window priority is.

        By default, the sort order is descending, i.e. the best matches go
        first.
        """
        aperture_width = int(aperture_width)
        aperture_height = int(aperture_height)
        aperture_area = aperture_width * aperture_height
        fit_width = self.calc_fit_width(aperture_width)
        fit_height = self.calc_fit_height(aperture_height)

        def priority(window):
            window_area = window.width * window.height
            abs_area_diff = abs(aperture_area - window_area)

            # If the window is unfit for the aperture, put it in the third
            # group with the least priority.
            if any((window.width < fit_width.min,
                    window.width > fit_width.max,
                    window.height < fit_height.min,
                    window.height > fit_height.max)):
                return (3, abs_area_diff)

            if (window.width <= aperture_width and
                window.height <= aperture_height):
                return (1, abs_area_diff)
            return (2, abs_area_diff)

        return sorted(windows, key=priority, reverse=reverse)

    @cached_property
    def _dimension_extremes(self):
        return self.get_queryset().in_city().aggregate(
            Min('width'), Max('width'), Min('height'), Max('height')
        )

    def get_min_width(self):
        """
        Get width of the narrowest window in the current city.
        """
        return self._dimension_extremes['width__min']

    def get_max_width(self):
        """
        Get width of the widest window in the current city.
        """
        return self._dimension_extremes['width__max']

    def get_min_height(self):
        """
        Get height of the shortest window in the current city.
        """
        return self._dimension_extremes['height__min']

    def get_max_height(self):
        """
        Get height of the tallest window in the current city.
        """
        return self._dimension_extremes['height__max']


class Window(models.Model):

    class Colors(models.TextChoices):
        WHITE = 'white', 'Белый'
        WOOD_DARK  = 'wood_dark', 'Темное дерево '
        WOOD_LIGHT = 'wood_light','Светлое дерево'
        OTHER = 'other', 'Другой'

    class Types(models.TextChoices):
        SINGLE = 'single', 'Одностворчатое окно'
        DOUBLE = 'double', 'Двухстворчатое окно'
        TRIPLE = 'triple', 'Трехстворчатое окно'
        SINGLE_TRANSOM = 'single_transom', 'Одностворчатое окно с фрамугой'
        DOUBLE_TRANSOM = 'double_transom', 'Двухстворчатое окно с фрамугой'
        TRIPLE_TRANSOM = 'triple_transom', 'Трехстворчатое окно с фрамугой'

    type = models.CharField(
        "Тип конструкции",
        max_length=20,
        choices=Types.choices,
    )
    width = models.PositiveSmallIntegerField(
        "Ширина, мм",
        validators=[MinValueValidator(200), MaxValueValidator(5000)],
    )
    height = models.PositiveSmallIntegerField(
        "Высота, мм",
        validators=[MinValueValidator(200), MaxValueValidator(5000)],
    )
    color = models.CharField(
        "Цвет",
        max_length=20,
        choices=Colors.choices,
        default=Colors.WHITE,
    )
    price = models.PositiveIntegerField("Цена")
    description = RichTextField("Описание", blank=True)
    place = models.ForeignKey(
        'sellers.Place',
        on_delete=models.PROTECT,
        related_name='windows',
        related_query_name='window',
        verbose_name="Место покупки",
        help_text=(
            'Адрес, по которому можно самостоятельно забрать окно, после '
            'покупки.'
        ),
    )
    seller = models.ForeignKey(
        'sellers.Seller',
        editable=False,
        on_delete=models.CASCADE,
        related_name='windows',
        related_query_name='window',
        verbose_name='Продавец',
    )
    datetime_created = models.DateTimeField(
        'Время добавления',
        auto_now_add=True,
    )
    datetime_changed = models.DateTimeField(
        'Время последнего редактирования',
        auto_now=True,
    )

    objects = WindowManager.from_queryset(WindowQuerySet)()

    class Meta:
        verbose_name = "Окно"
        verbose_name_plural = "Окна"
        indexes = [
            models.Index(fields=['width']),
            models.Index(fields=['height']),
            models.Index(fields=['type']),
            # The vast majority of windows are white (low cardinality), which
            # means there's little sense in creating an index for the 'color'
            # field, even though it's used for filtering.
        ]

    def __str__(self):
        return f'{self.pk} ({self.width}x{self.height})'

    def get_absolute_url(self):
        return reverse('catalog:window-detail', kwargs={'pk': self.pk})