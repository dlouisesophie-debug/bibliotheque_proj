from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Ajoute cette vue pour la racine
def home(request):
    return JsonResponse({
        'message': 'API Bibliothèque',
        'endpoints': {
            'auteurs': '/api/auteurs/',
            'livres': '/api/livres/',
            'emprunts': '/api/emprunts/',
            'admin': '/admin/',
        }
    })

urlpatterns = [
    path('', home),  # 👈 Ajoute cette ligne
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]