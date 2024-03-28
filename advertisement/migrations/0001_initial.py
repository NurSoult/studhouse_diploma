# Generated by Django 5.0.3 on 2024-03-28 22:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('location', models.CharField(max_length=255)),
                ('imagePaths', models.JSONField()),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('floor', models.IntegerField()),
                ('typeOfHouse', models.CharField(max_length=255)),
                ('numberOfRooms', models.IntegerField()),
                ('square', models.IntegerField()),
                ('isSold', models.BooleanField(default=False)),
                ('isArchived', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Advertisement',
                'verbose_name_plural': 'Advertisements',
                'db_table': 'advertisement',
                'ordering': ['-creationDate'],
            },
        ),
    ]
