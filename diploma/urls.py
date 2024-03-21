from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from authenticate.views import CustomTokenObtainPairView

api_version = 'api/v1/'


urlpatterns = [
    path(f'{api_version}swagger/', SpectacularAPIView.as_view(), name='schema'),

    # SWAGGER UI:
    path(f'{api_version}swagger/ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(f'{api_version}schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls),

    path(f'{api_version}api-auth/', include('rest_framework.urls')),
    path(f'{api_version}', include([re_path(r"^jwt/create/?", CustomTokenObtainPairView.as_view(), name="jwt-create")])),

    path(f'{api_version}auth/', include('authenticate.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
