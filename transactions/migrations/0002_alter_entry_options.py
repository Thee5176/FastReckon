# Generated by Django 5.1.4 on 2025-01-10 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['entry_type', 'code', 'amount'], 'verbose_name': 'Entry', 'verbose_name_plural': 'Entries'},
        ),
    ]
