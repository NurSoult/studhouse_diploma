from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'chats', views.ChatViewSet)
router.register(r'chats/(?P<chat_id>\d+)/messages', views.ChatMessageViewSet, basename='chat-message')

urlpatterns = router.urls
