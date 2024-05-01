from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from authenticate.models import User
from .models import Chat, ChatMessage
from .serializers import ChatSerializer, ChatMessageSerializer
from django.db.models import Prefetch


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        interlocutor_id = request.data.get('interlocutor')
        chat = Chat.objects.create(author=request.user, interlocutor_id=interlocutor_id)
        return Response(self.get_serializer(chat).data)


class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        return ChatMessage.objects.filter(chat_id=chat_id).order_by('creationDate').prefetch_related(
            Prefetch('author', queryset=User.objects.only('id', 'login'))
        )

    def create(self, request, *args, **kwargs):
        chat_id = self.kwargs.get('chat_id')

        chat = Chat.objects.get(pk=chat_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chat=chat, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        grouped = {}
        today = timezone.localtime(timezone.now()).date()
        yesterday = today - timedelta(days=1)

        for message in queryset:
            message_date = timezone.localtime(message.creationDate).date()
            if message_date == today:
                day_key = 'Today'
            elif message_date == yesterday:
                day_key = 'Yesterday'
            else:
                day_key = timezone.localtime(message.creationDate).strftime('%Y-%m-%d')

            if day_key not in grouped:
                grouped[day_key] = []
            grouped[day_key].append(self.get_serializer(message, context={'request': request}).data)

        return Response(grouped)