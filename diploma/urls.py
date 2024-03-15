from django.contrib import admin
from django.urls import path, include
from authenticate.views import CustomTokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('authenticate.urls')),

    path('auth/login', CustomTokenObtainPairView.as_view(), name='login'),
]
