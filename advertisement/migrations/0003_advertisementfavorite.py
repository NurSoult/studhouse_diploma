# Generated by Django 5.0.3 on 2024-03-29 08:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0002_remove_advertisement_imagepaths_advertisementimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertisementFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.advertisement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Advertisement Favorite',
                'verbose_name_plural': 'Advertisement Favorites',
                'db_table': 'advertisement_favorite',
            },
        ),
    ]
