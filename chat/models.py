from django.db import models
from django.utils.translation import gettext_lazy as _

from authenticate.models import User


class Chat(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    interlocutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interlocutor')
    creationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.creationDate}'

    class Meta:
        ordering = ['-creationDate']
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")
        db_table = 'chat'


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.creationDate}'

    class Meta:
        ordering = ['-creationDate']
        verbose_name = _("Chat Message")
        verbose_name_plural = _("Chat Messages")
        db_table = 'chat_message'
