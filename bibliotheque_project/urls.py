from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .admin import admin_site  # ← AJOUT : Import de votre admin personnalisé

# Vue pour la racine
def home_view(request):
    return JsonResponse({
        "message": "API Bibliothèque est opérationnelle",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "auth": {
                "token": "/api/auth/token/",
                "refresh": "/api/auth/token/refresh/",
                "verify": "/api/auth/token/verify/"
            },
            "docs": {
                "swagger": "/api/swagger/",
                "redoc": "/api/redoc/",
                "schema": "/api/schema/"
            }
        }
    })

urlpatterns = [
    # Racine
    path('', home_view, name='home'),
    
    # Admin - MODIFICATION ICI (admin_site.urls au lieu de admin.site.urls)
    path('admin/', admin_site.urls),
    
    # Documentation API (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Authentification JWT
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Vos endpoints API (si vous avez une app 'api')
    path('api/', include('api.urls')),
]