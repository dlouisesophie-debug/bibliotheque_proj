from rest_framework.routers import DefaultRouter
from .views import LivreViewSet, AuteurViewSet, EmpruntViewSet
from django.urls import path, include
from django.http import JsonResponse

router = DefaultRouter()
router.register(r'livres', LivreViewSet, basename='livres')
router.register(r'auteurs', AuteurViewSet, basename='auteurs')
router.register(r'emprunts', EmpruntViewSet, basename='emprunts')

def home(request):
    return JsonResponse({
        "message": "API Bibliothèque OK 🚀",
        "routes": [
            "/livres/",
            "/auteurs/",
            "/emprunts/"
        ]
    })

urlpatterns = [
    path('', home),          # 👈 IMPORTANT
    path('', include(router.urls)),
]