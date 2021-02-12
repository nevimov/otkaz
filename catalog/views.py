from django.db.models import Prefetch
from django.views import generic
from django_filters.views import FilterView

from .filters import WindowFilter
from .models import Window
from sellers.models import Place, Seller

# Names of filter GET parameters
APERTURE_WIDTH    = 'aperture_width'
APERTURE_HEIGHT   = 'aperture_height'
WINDOW_HEIGHT_MAX = 'height_max'
WINDOW_HEIGHT_MIN = 'height_min'
WINDOW_WIDTH_MAX  = 'width_max'
WINDOW_WIDTH_MIN  = 'width_min'


class WindowList(FilterView):
    """
    Show a list of windows available in the current city.

    * If the query string specifies aperture height and aperture width, then
      only the windows suitable for that aperture will be shown. The best
      matches will be listed first.

    * If the query string contains any filter parameters, like color or window
      type (see catalog.filters.WindowFilter), the shown list will be filtered
      according to those parameters.

    * Otherwise, the list of all city windows, ordered by newness, is
      displayed.
    """
    http_method_names = ['get']
    context_object_name = 'window_list'
    template_name = 'catalog/window_list.html'
    paginate_by = 21
    paginate_orphans = 5
    filterset_class = WindowFilter

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        request = self.request
        self.aperture_width  = request.GET.get(APERTURE_WIDTH)
        self.aperture_height = request.GET.get(APERTURE_HEIGHT)

    def get_queryset(self):
        # Return all windows in the current city
        return Window.objects.in_city().select_related('seller')

    def paginate_queryset(self, queryset, page_size):
        # Once all filters are applied, sort the resulting queryset before
        # passing it further, to the paginator.
        sorted_windows = self.sort_windows(queryset)
        return super().paginate_queryset(sorted_windows, page_size)

    def sort_windows(self, windows):
        # If aperture dimensions are specified, sort windows by their
        # suitability for the aperture.
        if self.aperture_width and self.aperture_height:
            return Window.objects.sort_for_aperture(
                windows,
                aperture_width=self.aperture_width,
                aperture_height=self.aperture_height,
            )
        # Otherwise, just put the newest windows first
        return windows.order_by_newness()

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        filterset_data = kwargs['data'].copy() if kwargs['data'] else {}

        aperture_width = self.aperture_width
        if aperture_width:
            fit_width = Window.objects.calc_fit_width(aperture_width)
            filterset_data[WINDOW_WIDTH_MIN] = fit_width.min
            filterset_data[WINDOW_WIDTH_MAX] = fit_width.max

        aperture_height = self.aperture_height
        if aperture_height:
            fit_height = Window.objects.calc_fit_height(aperture_height)
            filterset_data[WINDOW_HEIGHT_MIN] = fit_height.min
            filterset_data[WINDOW_HEIGHT_MAX] = fit_height.max

        kwargs['data'] = filterset_data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a URL query string without the 'page' parameter.
        # Used to create pagination links.
        context['qs_without_page'] = self._clip_querystring('page')

        context['sellers'] = Seller.objects.prefetch_related(
            'phones',
            Prefetch('places', queryset=Place.objects.select_related('city')),
        )
        return context

    def _clip_querystring(self, *params, prefix='&'):
        """
        Return a query string without given parameters.

        The string will be prefixed with `prefix`.
        """
        copy = self.request.GET.copy()

        for param in params:
            if param in copy:
                del copy[param]

        querystring = copy.urlencode()
        if querystring:
            return prefix + querystring
        return ''


class WindowDetail(generic.DetailView):
    """
    Show a page containing detailed info about a given window.
    """
    http_method_names = ['get']
    context_object_name = 'window'
    template_name = 'catalog/window_detail.html'

    def get_queryset(self):
        return Window.objects.in_city().select_related('seller')