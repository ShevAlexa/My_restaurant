from django.core.management import BaseCommand
from django.db.models import Count
from my_restaurant.planes.models import Airplane


class Command(BaseCommand):
    def handle(self, *args, **options):
        plane = Airplane.objects.annotate(count_likes=Count("users_likes"))
        for p in plane:
            p.likes = p.count_like
        Airplane.objects.bulk_update(plane, ["likes"])
        print([(i.likes, i.count_likes) for i in plane])
