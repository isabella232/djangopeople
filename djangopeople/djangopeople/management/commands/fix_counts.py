from django.core.management.base import BaseCommand

from ...models import Country, Region


class Command(BaseCommand):
    """
    Countries and regions keep a denormalized count of people that gets out of
    sync during migrate.  This updates it.
    """
    def handle(self, **options):
        for qs in (Country.objects.all(), Region.objects.all()):
            for geo in qs:
                qs.model.objects.filter(pk=geo.pk).update(
                    num_people=geo.djangoperson_set.count(),
                )
