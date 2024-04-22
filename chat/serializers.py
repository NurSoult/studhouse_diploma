from rest_framework import serializers
from .models import Chat, ChatMessage
from authenticate.models import User


class ChatSerializer(serializers.ModelSerializer):
    creationDate = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Chat
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ChatMessageSerializer(serializers.ModelSerializer):
    author_detail = serializers.SerializerMethodField()
    creationDate = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat', 'author', 'text', 'creationDate', 'author_detail']
        extra_kwargs = {
            'chat': {'read_only': True},
            'author': {'read_only': True}
        }

    def get_author_detail(self, obj):
        request = self.context.get('request')
        if obj.author == request.user:
            return {'author_type': 'me', 'author': UserSerializer(obj.author).data}
        else:
            return {'author_type': 'interlocutor', 'author': UserSerializer(obj.author).data}
