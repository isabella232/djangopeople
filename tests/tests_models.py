from django.test import TestCase

from djangopeople.djangopeople.models import (Country, DjangoPerson, Region,
                                              CountrySite, PortfolioSite)


class DjangoPeopleUnitTest(TestCase):
    fixtures = ['test_data']

    def test_region(self):
        ak = Region.objects.get(pk=36)
        self.assertEqual(str(ak), 'Alaska')
        self.assertEqual(ak.get_absolute_url(), '/us/ak/')

    def test_country(self):
        us = Country.objects.get(pk=219)
        self.assertEqual(str(us), 'United States')
        hawaii = Region.objects.get(pk=32)
        self.assertTrue(hawaii in us.top_regions())
        self.assertTrue(us in Country.objects.top_countries())
        us.num_people = 100000
        us.save()
        self.assertEqual(us, Country.objects.top_countries()[0])

    def test_portfolio_site(self):
        p = PortfolioSite.objects.get(pk=1)
        self.assertEqual(str(p), 'cheese-shop <http://example.org/>')

    def test_country_site(self):
        cs = CountrySite.objects.get(pk=1)
        self.assertEqual(str(cs), 'django AT <http://example.org/>')

    def test_django_person(self):
        dave = DjangoPerson.objects.get(pk=1)
        louis = DjangoPerson.objects.get(pk=2)
        self.assertEqual(str(dave), 'Dave Brubeck')
        self.assertEqual(dave.irc_nick(), 'davieboy')
        self.assertEqual(louis.irc_nick(), '<none>')
        self.assertTrue(dave.irc_tracking_allowed())
        self.assertEqual(dave.get_nearest(), [louis])
        self.assertEqual(
            louis.location_description_html(),
            'Paris, France')
        self.assertEqual(louis.get_absolute_url(), '/satchmo/')
