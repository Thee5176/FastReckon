# Generated by Django 5.1.4 on 2025-01-02 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('abbr', models.CharField(max_length=2, unique=True)),
                ('record_count', models.IntegerField(blank=True, null=True)),
                ('guideline', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
                'ordering': ['abbr'],
            },
        ),
    ]
