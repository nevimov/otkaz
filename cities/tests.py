from django.test import TestCase
from django.urls import reverse

from core.management.commands.filldevdb import create_city
from .context_processors import cities

class CtxProcessorsTests(TestCase):
    """
    Test case for cities.context_processors module.
    """

    def test_cities(self):
        """Test the 'city' context processor.

        The processor should return a dictionary of 3 keys:
          - 'all' (all cities in alphabetical order)
          - 'current' (current city)
          - 'others' (all cities except the current one, in alphabetical order)

        """
        moscow = create_city('Москва', site_domain='otkaz.net')
        ekat = create_city('Екатеринбург', site_domain='ekat.otkaz.net')
        novokuz = create_city('Новокузнецк', site_domain='nk.otkaz.net')
        novosib = create_city('Новосибирск', site_domain='nsk.otkaz.net')
        samara = create_city('Самара', site_domain='samara.otkaz.net')
        piter = create_city('Санкт-Петербург', site_domain='spb.otkaz.net')
        sochi = create_city('Сочи', site_domain='sochi.otkaz.net')

        with self.settings(SITE_ID=moscow.site.id):
            response = self.client.get(reverse('main'))

        cities_ctx = cities(response.wsgi_request)['cities']
        all_cities = cities_ctx['all']
        current_city = cities_ctx['current']
        other_cities = cities_ctx['others']

        self.assertEqual(current_city, moscow)
        self.assertEqual(
            other_cities,
            [ekat, novokuz, novosib, samara, piter, sochi]
        )
        self.assertEqual(
            list(all_cities),
            [ekat, moscow, novokuz, novosib, samara, piter, sochi]
        )