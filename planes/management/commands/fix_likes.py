from django.core.management import BaseCommand
from django.db.models import Count, Prefetch

from my_restaurant.planes.models import Comment, Dish


class Command(BaseCommand):
    def handle(self, *args, **options):
        comment = Comment.objects.annotate(count_like=Count("users_likes"))
        comments = Prefetch("comments")
        dishes = Dish.objects.prefetch_related(comments)
        for comment in dishes.comments:
            for c in comment:
                c.likes = c.count_like
                c.save()
        print([(i.likes, i.count_likes) for i in comment])
