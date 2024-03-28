from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from authenticate.models import User


class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = PhoneNumberField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        db_table = 'student'


class Landlord(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = PhoneNumberField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Landlord')
        verbose_name_plural = _('Landlords')
        db_table = 'landlord'
