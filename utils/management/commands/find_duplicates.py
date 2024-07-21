from django.core.management.base import BaseCommand
from posts.models import Post
from django.db.models import Count

class Command(BaseCommand):
    help = 'Find duplicate post titles'

    def handle(self, *args, **kwargs):
        duplicates = Post.objects.values('title').annotate(title_count=Count('title')).filter(title_count__gt=1)
        for duplicate in duplicates:
            print(f"Duplicate title: {duplicate['title']}, Count: {duplicate['title_count']}")
