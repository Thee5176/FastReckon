# Generated by Django 5.1.4 on 2025-01-25 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc_codes', '0002_account_code'),
        ('transactions', '0002_alter_entry_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='entries', to='acc_codes.account'),
        ),
    ]
