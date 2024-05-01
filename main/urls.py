from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'review', views.ReviewViewSet, basename='review')
router.register(r'report', views.ReportView, basename='report')
router.register(r'relocation', views.RelocationViewSet, basename='relocation')

urlpatterns = router.urls
