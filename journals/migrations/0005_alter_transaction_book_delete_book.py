# Generated by Django 5.1.4 on 2025-01-02 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc_books', '0001_initial'),
        ('journals', '0004_alter_book_abbr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='acc_books.book'),
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
