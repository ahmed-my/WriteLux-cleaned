# Generated by Django 5.0.7 on 2024-08-05 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_conversation_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_chat',
            field=models.BooleanField(default=False),
        ),
    ]
