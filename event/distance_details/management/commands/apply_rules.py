from django.core.management.base import BaseCommand

from event.distance_details.models import DistanceEvent
from event.distance_details.tasks import apply_cost_change_rules


class Command(BaseCommand):
    help = 'Applies cost change rules to DistanceEvent instances with published events and existing cost change rules.'

    def handle(self, *args, **kwargs):
        distances = DistanceEvent.objects.filter(
            event__status='published',
            costChangeRules__isnull=False
        ).distinct()

        if not distances.exists():
            self.stdout.write('No distances found with cost change rules for published events.')
            return

        for distance in distances:
            new_cost = apply_cost_change_rules(distance)
            self.stdout.write(f"Updated cost for DistanceEvent '{distance.name}' to {new_cost}")
