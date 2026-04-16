from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def home(request):
    return JsonResponse({
        'message': 'API Bibliothèque en ligne !',
        'endpoints': {
            'auteurs': '/api/auteurs/',
            'livres': '/api/livres/',
            'emprunts': '/api/emprunts/',
            'token': '/api/token/',
            'admin': '/admin/',
        }
    })

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('api.urls')),
]