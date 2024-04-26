from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from authenticate.models import User
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.author.login} - {self.rating}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Relocation(models.Model):
    payment_time = (
        ('daily', _('Daily')),
        ('monthly', _('Monthly')),
        ('yearly', _('Yearly')),
    )

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    paymentTime = models.CharField(max_length=255, choices=payment_time)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    floor = models.IntegerField()
    typeOfHouse = models.CharField(max_length=255)
    max_people_count = models.IntegerField()
    current_people_count = models.IntegerField()
    count_bedrooms = models.IntegerField()
    count_bathrooms = models.IntegerField()
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


class RelocationImage(models.Model):
    relocation = models.ForeignKey(Relocation, on_delete=models.CASCADE)
    image = models.FileField(
        upload_to='relocation/images/',
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
        verbose_name = _("Relocation image")
        verbose_name_plural = _("Relocation images")
        db_table = 'relocation_image'
