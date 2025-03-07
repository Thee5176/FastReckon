# Generated by Django 5.1.4 on 2025-01-28 13:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc_books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='abbr',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterUniqueTogether(
            name='book',
            unique_together={('abbr', 'created_by')},
        ),
    ]
