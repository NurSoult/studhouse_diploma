from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from authenticate.models import User


class Advertisement(models.Model):
    payment_time = (
        ('daily', _('Daily')),
        ('monthly', _('Monthly')),
        ('yearly', _('Yearly')),
    )

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    paymentTime = models.CharField(max_length=255, choices=payment_time)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    floor = models.IntegerField()
    typeOfHouse = models.CharField(max_length=255)
    numberOfRooms = models.IntegerField()
    square = models.IntegerField()
    isSold = models.BooleanField(default=False)
    isArchived = models.BooleanField(default=False)
    haveWifi = models.BooleanField(default=False)
    haveTV = models.BooleanField(default=False)
    haveWashingMachine = models.BooleanField(default=False)
    haveParking = models.BooleanField(default=False)
    haveConditioner = models.BooleanField(default=False)
    nearbyTradeCenter = models.BooleanField(default=False)
    nearbyHospital = models.BooleanField(default=False)
    nearbySchool = models.BooleanField(default=False)
    nearbyGym = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} - {self.price}'

    class Meta:
        ordering = ['-creationDate']
        verbose_name = _("Advertisement")
        verbose_name_plural = _("Advertisements")
        db_table = 'advertisement'


class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    image = models.FileField(
        upload_to='advertisement/images/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    def clean(self):
        super().clean()
        if self.image:
            extension = self.image.name.split('.')[-1]
            if extension.lower() not in ['jpg', 'jpeg', 'png']:
                raise ValidationError(
                    'Invalid file extension. Allowed extensions are: jpg, jpeg, png.'
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("AdvertisementImage")
        verbose_name_plural = _("AdvertisementImages")
        db_table = 'advertisement_image'


class AdvertisementFavorite(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.advertisement.title} - {self.user.login}'

    class Meta:
        verbose_name = _("Advertisement Favorite")
        verbose_name_plural = _("Advertisement Favorites")
        db_table = 'advertisement_favorite'
