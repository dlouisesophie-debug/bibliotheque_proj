from rest_framework.routers import DefaultRouter
from .views import LivreViewSet, AuteurViewSet, EmpruntViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'livres', LivreViewSet, basename='livres')
router.register(r'auteurs', AuteurViewSet, basename='auteurs')
router.register(r'emprunts', EmpruntViewSet, basename='emprunts')

urlpatterns = [
    path('', include(router.urls)),
]