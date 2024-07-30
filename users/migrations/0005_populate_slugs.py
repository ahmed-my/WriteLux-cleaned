from django.db import migrations
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    UserProfile = apps.get_model('users', 'UserProfile')
    for profile in UserProfile.objects.all():
        unique_slug = slugify(profile.user.username)  # Or another unique identifier
        profile.slug = unique_slug
        profile.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userprofile_bio_userprofile_profile_image'),
    ]

    operations = [
        migrations.RunPython(populate_slugs),
    ]
