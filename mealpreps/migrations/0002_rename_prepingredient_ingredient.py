# Generated by Django 5.1.4 on 2025-01-06 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mealpreps', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PrepIngredient',
            new_name='Ingredient',
        ),
    ]
