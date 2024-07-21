from django.core.management.base import BaseCommand
from posts.models import Post
from django.db.models import Count

class Command(BaseCommand):
    help = 'Remove duplicate post titles'

    def handle(self, *args, **kwargs):
        duplicates = Post.objects.values('title').annotate(title_count=Count('title')).filter(title_count__gt=1)
        for duplicate in duplicates:
            posts = Post.objects.filter(title=duplicate['title'])
            for post in posts[1:]:  # Keep the first occurrence, delete the rest
                post.delete()
