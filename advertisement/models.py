from django.db import models
from django.utils.translation import gettext_lazy as _

from authenticate.models import User


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    imagePaths = models.JSONField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    floor = models.IntegerField()
    typeOfHouse = models.CharField(max_length=255)
    numberOfRooms = models.IntegerField()
    square = models.IntegerField()
    isSold = models.BooleanField(default=False)
    isArchived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} - {self.price}'

    class Meta:
        ordering = ['-creationDate']
        verbose_name = _("Advertisement")
        verbose_name_plural = _("Advertisements")
        db_table = 'advertisement'
