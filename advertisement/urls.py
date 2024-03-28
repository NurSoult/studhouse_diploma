from rest_framework.routers import DefaultRouter
from .views import AdvertisementView

router = DefaultRouter()

router.register("", AdvertisementView, basename="advertisement")

urlpatterns = router.urls
