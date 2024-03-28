from rest_framework.routers import DefaultRouter
from .views import StudentView, LandlordView


router = DefaultRouter()

router.register("student", StudentView, basename="student")
router.register("landlord", LandlordView, basename="landlord")

urlpatterns = router.urls
