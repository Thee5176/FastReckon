# Generated by Django 5.1.4 on 2025-01-01 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='record_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
