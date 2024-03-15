from rest_framework.routers import DefaultRouter
from .views import UserRoleView, UserView, UserInfoView


router = DefaultRouter()

router.register("role", UserRoleView, basename="role")
router.register("user", UserView, basename="user")
router.register("user_info", UserInfoView, basename="user_info")

urlpatterns = router.urls
