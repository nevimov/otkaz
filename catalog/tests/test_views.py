from django.urls import reverse

from .test_models import CatalogModelTestCase
from catalog.models import Window
from core.management.commands.filldevdb import create_window


class CatalogViewTestCase(CatalogModelTestCase):

    def setUp(self):
        super().setUp()

        # Create 10 windows in cities other than Moscow
        for _ in range(5): create_window(seller=self.finestra)
        for _ in range(5): create_window(seller=self.pella)

        jeld, col, wt = self.jeld, Window.Colors, Window.Types
        self.w1000_h600 = create_window(width=1000, height=600, seller=jeld, type=wt.DOUBLE, color=col.WHITE)
        self.w1050_h400 = create_window(width=1050, height=400, seller=jeld, type=wt.DOUBLE_TRANSOM, color=col.WHITE)
        self.w900_h525  = create_window(width=900,  height=525, seller=jeld, type=wt.DOUBLE, color=col.WHITE)
        self.w1100_h450 = create_window(width=1100, height=450, seller=jeld, type=wt.DOUBLE, color=col.WHITE)
        self.w850_h500  = create_window(width=850,  height=500, seller=jeld, type=wt.DOUBLE, color=col.WHITE)
        self.w900_h490  = create_window(width=900,  height=490, seller=jeld, type=wt.DOUBLE, color=col.WOOD_DARK)
        self.w900_h700  = create_window(width=900,  height=700, seller=jeld, type=wt.DOUBLE, color=col.WHITE)
        self.w1200_h700 = create_window(width=1200, height=700, seller=jeld, type=wt.DOUBLE, color=col.WHITE)


class WindowListTests(CatalogViewTestCase):
    """
    Test case for catalog.views.WindowList.
    """
    URL = reverse('catalog:window-list')

    def test_with_empty_querystring(self):
        """
        If no GET parameters are passed to the view, it displays a list of
        all windows available in the current city, ordered by newness.
        """
        with self.settings(SITE_ID=self.moscow.site.id):
            response = self.client.get(self.URL, data=None)

        self.assertEqual(response.status_code, 200)
        displayed_windows = response.context['window_list']
        self.assertEqual(len(displayed_windows), 8)
        self.assertQuerysetEqual(
            displayed_windows,
            map(repr,
                Window.objects.filter(
                    place__city=self.moscow
                ).order_by('-datetime_created')),
        )

    def test_with_aperture_dimensions_specified(self):
        """
        If GET parameters passed to the view contain aperture height and
        aperture width, then only the windows suitable for that aperture
        should be shown. The best matches should be listed first.
        """
        with self.settings(SITE_ID=self.moscow.site.id):
            response = self.client.get(
                self.URL,
                {'aperture_height': 500, 'aperture_width': 1000},
            )

        self.assertEqual(response.status_code, 200)
        displayed_windows = response.context['window_list']
        self.assertQuerysetEqual(
            displayed_windows,
            map(repr, [
                # (1) Both height and width of these windows are smaller than
                # the aperture, so they get the highest priority.
                self.w900_h490,  # Area diff: |59 000|
                self.w850_h500,  # Area diff: |75 000|

                # (2) Fit windows whose height and/or width is greater than the
                # corresponding aperture dimension.
                self.w900_h525,   # Area diff: |27 500|
                self.w1050_h400,  # Area diff: |80 000|

                # The rest of the windows are "unfit" for the specified
                # aperture.
            ])
        )

    def test_with_aperture_dimensions_and_color_specified(self):
        """
        If GET parameters passed to the view contain both aperture
        dimensions and filter parameters, then only the windows satisfying
        all the requirements should be shown.
        """
        # Create 10 windows in cities other than Moscow
        for _ in range(5): create_window(seller=self.finestra)
        for _ in range(5): create_window(seller=self.pella)

        with self.settings(SITE_ID=self.moscow.site.id):
            response = self.client.get(
                self.URL,
                {'aperture_height': 500, 'aperture_width': 1000,
                 'color': Window.Colors.WHITE},
            )

        self.assertEqual(response.status_code, 200)
        displayed_windows = response.context['window_list']
        self.assertQuerysetEqual(
            displayed_windows,
            map(repr, [
                # (1) Both height and width of these windows are smaller than
                # the aperture, so they get the highest priority.
                # w900_h490 (Area diff: |59 000|) is excluded because of the
                # different color.
                self.w850_h500,  # Area diff: |75 000|

                # (2) Fit windows whose height and/or width is greater than the
                # corresponding aperture dimension.
                self.w900_h525,
                self.w1050_h400,  # Area diff: |80 000|

                # The rest of the windows are "unfit" for the specified
                # aperture.
            ])
        )

    def test_with_aperture_dimensions_type_and_color_specified(self):
        """
        If GET parameters passed to the view contain both aperture
        dimensions and filter parameters, then only the windows satisfying
        all the requirements should be shown.
        """
        with self.settings(SITE_ID=self.moscow.site.id):
            response = self.client.get(
                self.URL,
                {'aperture_height': 500, 'aperture_width': 1000,
                 'color': Window.Colors.WHITE, 'type': Window.Types.DOUBLE},
            )

        self.assertEqual(response.status_code, 200)
        displayed_windows = response.context['window_list']
        self.assertQuerysetEqual(
            displayed_windows,
            map(repr, [
                # (1) Both height and width of these windows are smaller than
                # the aperture, so they get the highest priority.
                # w900_h490 (Area diff: |59 000|) is excluded because of the
                # different color.
                self.w850_h500,  # Area diff: |75 000|

                # (2) Fit windows whose height and/or width is greater than the
                # corresponding aperture dimension.
                self.w900_h525,  # Area diff: |27 500|)
                # w1050_h400 (Area diff: |80 000|) is excluded because of the
                # non-matching type.

                # The rest of the windows are "unfit" for the specified
                # aperture.
            ])
        )

    def test_with_filter_parameters_only(self):
        """
        If GET parameters passed to the view do NOT contain aperture
        dimensions, but contain filter parameters, then windows satisfying
        the requirements should be shown in the order of newness.
        """
        with self.settings(SITE_ID=self.moscow.site.id):
            response = self.client.get(
                self.URL,
                {'width_max': 1150, 'color': Window.Colors.WHITE,
                 'type': Window.Types.DOUBLE},
            )

        self.assertEqual(response.status_code, 200)
        displayed_windows = response.context['window_list']
        self.assertQuerysetEqual(
            displayed_windows,
            map(repr, [
                self.w900_h700,
                self.w850_h500,
                self.w1100_h450,
                self.w900_h525,
                self.w1000_h600,
                # w1050_h400 -- excluded because of 'type'
                # w1200_h700 -- excluded because of 'width-max'
                # w900_h490  -- excluded because of 'color'
            ])
        )


class WindowDetailTests(CatalogViewTestCase):
    """
    Test case for catalog.views.WindowDetail.
    """

    def test_correct_window_is_displayed(self):
        """
        When the view receives the 'pk' of a valid window, it should display
        the page for this window.
        """
        some_window = self.w900_h490
        url = reverse('catalog:window-detail', args=[some_window.pk])
        with self.settings(SITE_ID=self.moscow.site.id):
            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        displayed_window = response.context['window']
        self.assertEqual(displayed_window, some_window)
