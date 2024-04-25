from django.db import models
from authenticate.models import User


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.author.login} - {self.rating}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
