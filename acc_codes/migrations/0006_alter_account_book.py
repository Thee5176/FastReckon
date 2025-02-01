# Generated by Django 5.1.4 on 2025-01-29 04:24

import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('acc_books', '0002_alter_book_abbr_alter_book_unique_together'),
        ('acc_codes', '0005_account_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='acc_books.book'),
        ),
    ]
