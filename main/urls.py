from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'review', views.ReviewViewSet, basename='review')

urlpatterns = router.urls
