from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase

from catalog.models import Window
from core.management.commands.prepdb import create_seller_group
from core.management.commands.filldevdb import (
    create_city,
    create_place,
    create_seller,
    create_window,
)
from sellers.models import Place


class CatalogModelTestCase(TestCase):

    def setUp(self):
        create_seller_group()

        # Create cities
        Site.objects.get(pk=1).delete()  # Remove the default 'example.com'
        self.moscow = create_city('Москва', '0.0.0.0', site_id=1)
        self.samara = create_city('Самара', '0.0.0.0:8001', site_id=2)
        self.sochi = create_city('Сочи', '0.0.0.0:8002', site_id=3)

        # Create sellers
        self.jeld = create_seller('JELD-WEN', places=[])
        self.alside = create_seller('Alside', places=[])
        self.pella = create_seller('Pella Corp', places=[])
        self.marvin = create_seller('Marvin Windows', places=[])
        self.finestra = create_seller('Finestra', places=[])
        self.mirokon = create_seller('Mir Okon', places=[])
        pt = Place.Types
        create_place(seller=self.jeld, type=pt.OFFICE, city=self.moscow)
        create_place(seller=self.jeld, type=pt.WAREHOUSE, city=self.moscow)
        create_place(seller=self.jeld, type=pt.WAREHOUSE, city=self.moscow)
        create_place(seller=self.alside, type=pt.OFFICE, city=self.moscow)
        create_place(seller=self.alside, type=pt.WAREHOUSE, city=self.moscow)
        create_place(seller=self.marvin, type=pt.WAREHOUSE, city=self.moscow)
        create_place(seller=self.finestra, type=pt.WAREHOUSE, city=self.samara)
        create_place(seller=self.mirokon, type=pt.WAREHOUSE, city=self.samara)
        create_place(seller=self.pella, type=pt.WAREHOUSE, city=self.sochi)


class WindowQuerySetTests(CatalogModelTestCase):
    """
    Test case for catalog.models.WindowQuerySet.
    """

    def test_in_city_without_arg(self):
        """If the `city` argument is not provided, the in_city() method
        should return windows associated with the user city only.
        """
        # Create 45 windows in Moscow
        for _ in range(20): create_window(seller=self.jeld)
        for _ in range(15): create_window(seller=self.alside)
        for _ in range(10): create_window(seller=self.marvin)
        # Create 25 windows in Samara
        for _ in range(15): create_window(seller=self.finestra)
        for _ in range(10): create_window(seller=self.mirokon)
        # Create 20 windows in Sochi
        for _ in range(20): create_window(seller=self.pella)

        with self.settings(SITE_ID=self.moscow.site.id):
            city_windows = Window.objects.in_city()
            self.assertEqual(city_windows.count(), 45)
            self.assertQuerysetEqual(
                city_windows,
                map(repr, Window.objects.filter(place__city=self.moscow)),
                ordered=False,
            )

        with self.settings(SITE_ID=self.samara.site.id):
            city_windows = Window.objects.in_city()
            self.assertEqual(city_windows.count(), 25)
            self.assertQuerysetEqual(
                city_windows,
                map(repr, Window.objects.filter(place__city=self.samara)),
                ordered=False,
            )

        with self.settings(SITE_ID=self.sochi.site.id):
            city_windows = Window.objects.in_city()
            self.assertEqual(city_windows.count(), 20)
            self.assertQuerysetEqual(
                city_windows,
                map(repr, Window.objects.filter(place__city=self.sochi)),
                ordered=False,
            )

    def test_in_city_with_arg(self):
        """If the `city` argument is provided, in_city() should return
        windows associated with the specified city, regardless of the
        current site.
        """
        # Create 20 windows in Moscow
        for _ in range(20): create_window(seller=self.jeld)
        # Create 10 windows in Sochi
        for _ in range(10): create_window(seller=self.pella)

        with self.settings(SITE_ID=self.moscow.site.id):
            city_windows = Window.objects.in_city(city=self.sochi)
            self.assertEqual(city_windows.count(), 10)
            self.assertQuerysetEqual(
                city_windows,
                map(repr, Window.objects.filter(place__city=self.sochi)),
                ordered=False,
            )


class WindowManagerTests(CatalogModelTestCase):
    """
    Test case for catalog.models.WindowManager.
    """

    def setUp(self):
        super().setUp()
        self.w1000_h600 = create_window(width=1000, height=600, seller=self.jeld)
        self.w1050_h400 = create_window(width=1050, height=400, seller=self.jeld)
        self.w900_h525  = create_window(width=900,  height=525, seller=self.jeld)
        self.w1100_h450 = create_window(width=1100, height=450, seller=self.finestra)
        self.w850_h500  = create_window(width=850,  height=500, seller=self.finestra)
        self.w900_h490  = create_window(width=900,  height=490, seller=self.jeld)
        self.w900_h700  = create_window(width=900,  height=700, seller=self.jeld)
        self.w1200_h700 = create_window(width=1200, height=700, seller=self.jeld)

    def test_calc_fit_width(self):
        """The calc_fit_width() method should return a named tuple 'Width'
        with the following attributes:
        * 'min' -- Min width of windows suitable for the given aperture width.
                   Suitable windows can be narrower than the aperture by 15 cm.
        * 'max' -- Max width of windows suitable for the given aperture width.
                   Suitable windows can be wider than the aperture by 5cm.
        * 'range' -- (min, max) tuple whose values described above.
        """
        fit_width = Window.objects.calc_fit_width(1000)
        self.assertEqual(fit_width.min, 850)
        self.assertEqual(fit_width.max, 1050)
        self.assertEqual(fit_width.range, (850, 1050))

    def test_calc_fit_height(self):
        """The calc_fit_height() method should return a named tuple 'Height'
        with the following attributes:
        * 'min' -- Min height of windows suitable for the given aperture height.
                   Suitable windows can be shorter than the aperture by 15 cm.
        * 'max' -- Max height of windows suitable for the given aperture height.
                   Suitable windows can be taller than the aperture by 5cm.
        * 'range' -- (min, max) tuple whose values described above.
        """
        height = Window.objects.calc_fit_height(1000)
        self.assertEqual(height.min, 850)
        self.assertEqual(height.max, 1050)
        self.assertEqual(height.range, (850, 1050))


    def test_sort_for_aperture(self):
        """sort_for_aperture() should sort windows according to the
        algorithm specified in the method docstring.
        """
        sorted_windows = Window.objects.sort_for_aperture(
            Window.objects.all(), aperture_width=1000, aperture_height=500,
            # Aperture area: 1 000 x 500 = 500 000
        )
        self.assertEqual(
            sorted_windows,
            [
                # (1) Fit windows whose height AND width are SMALLER than the
                # aperture, so they get the highest priority.
                self.w900_h490,  # Area diff: |59 000|
                self.w850_h500,  # Area diff: |75 000|

                # (2) Fit windows whose height and/or width is greater than the
                # corresponding aperture dimension.
                self.w900_h525,   # Area diff: |27 500|
                self.w1050_h400,  # Area diff: |80 000|

                # (3) "Unfit" windows
                self.w1100_h450,  # Area diff: |5 000|
                self.w1000_h600,  # Area diff: |-100 000|
                self.w900_h700,   # Area diff: |-130 000|
                self.w1200_h700,  # Area diff: |-340 000|
            ]
        )

    def test_get_min_width(self):
        """get_min_width() should return the narrowest window's width in the
        current city.
        """
        with self.settings(SITE_ID=self.moscow.site.id):
            self.assertEqual(Window.objects.get_min_width(), 900)

    def test_get_max_width(self):
        """get_max_width() should return the widest window's width in the
        current city.
        """
        with self.settings(SITE_ID=self.moscow.site.id):
            self.assertEqual(Window.objects.get_max_width(), 1200)

    def test_get_min_height(self):
        """get_min_height() should return the shortest window's height in the
        current city.
        """
        with self.settings(SITE_ID=self.moscow.site.id):
            self.assertEqual(Window.objects.get_min_height(), 400)

    def test_get_max_height(self):
        """get_max_height() should return the tallest window's height in the
        current city.
        """
        with self.settings(SITE_ID=self.moscow.site.id):
            self.assertEqual(Window.objects.get_max_height(), 700)