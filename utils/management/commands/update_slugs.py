from django.core.management.base import BaseCommand
from posts.models import Post
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Update slugs to ensure uniqueness'

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()
        for post in posts:
            original_slug = slugify(post.title)
            slug = original_slug
            counter = 1
            queryset = Post.objects.filter(slug__iexact=slug).exclude(pk=post.pk)
            while queryset.exists():
                slug = f'{original_slug}-{counter}'
                counter += 1
                queryset = Post.objects.filter(slug__iexact=slug).exclude(pk=post.pk)
            post.slug = slug
            post.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated slugs'))
