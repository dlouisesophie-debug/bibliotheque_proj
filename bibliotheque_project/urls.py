from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        'message': 'API Bibliothèque',
        'endpoints': {
            'api': '/api/',
            'admin': '/admin/',
        }
    })

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Inclut toutes les URLs de api/urls.py
]