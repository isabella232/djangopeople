from django.contrib.auth.models import User
from django.test import TestCase

from ..views import _make_hash


class TestUtils(TestCase):
    def test_make_hash(self):
        self.assertEqual(_make_hash('add', User(id=432), 'xxx'), 'd1d20d6ade210ab64237397adb2a4a14')
