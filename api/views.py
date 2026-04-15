from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from datetime import date

from .models import Auteur, Livre, Emprunt
from .serializers import (
    AuteurSerializer, 
    LivreListSerializer, 
    LivreDetailSerializer,
    EmpruntSerializer, 
    RegisterSerializer,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin


class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nom', 'nationalite']
    ordering_fields = ['nom']


class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.select_related('auteur').all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['categorie', 'disponible', 'auteur']
    search_fields = ['titre', 'isbn']
    ordering_fields = ['annee_publication', 'titre']

    def get_serializer_class(self):
        if self.action == 'list':
            return LivreListSerializer
        return LivreDetailSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def emprunter(self, request, pk=None):
        livre = self.get_object()
        
        if not livre.disponible:
            return Response(
                {'erreur': 'Ce livre n\'est pas disponible.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier si l'utilisateur n'a pas déjà 3 emprunts en cours
        emprunts_actifs = Emprunt.objects.filter(
            utilisateur=request.user, 
            retourne=False
        ).count()
        
        if emprunts_actifs >= 3:
            return Response(
                {'erreur': 'Vous avez déjà 3 emprunts en cours.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        emprunt = Emprunt.objects.create(
            livre=livre,
            utilisateur=request.user
        )
        
        livre.disponible = False
        livre.save()
        
        return Response(
            EmpruntSerializer(emprunt).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        livres = Livre.objects.filter(disponible=True)
        return Response(LivreListSerializer(livres, many=True).data)


class EmpruntViewSet(viewsets.ModelViewSet):
    serializer_class = EmpruntSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Emprunt.objects.select_related('livre', 'utilisateur').all()
        return Emprunt.objects.filter(utilisateur=user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

    @action(detail=True, methods=['post'])
    def retourner(self, request, pk=None):
        emprunt = self.get_object()
        
        if emprunt.retourne:
            return Response(
                {'erreur': 'Ce livre a déjà été retourné.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        emprunt.retourne = True
        emprunt.date_retour = date.today()
        emprunt.save()
        
        emprunt.livre.disponible = True
        emprunt.livre.save()
        
        return Response({'message': 'Livre retourné avec succès !'})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta

@api_view(["GET"])
def stats_emprunts_par_mois(request):
    aujourd_hui = datetime.now().date()
    six_mois_avant = aujourd_hui - timedelta(days=180)
    
    emprunts_par_mois = (
        Emprunt.objects.filter(date_emprunt__date__gte=six_mois_avant)
        .annotate(mois=TruncMonth("date_emprunt"))
        .values("mois")
        .annotate(total=Count("id"))
        .order_by("mois")
    )
    
    mois_labels = [e["mois"].strftime("%B %Y") for e in emprunts_par_mois]
    mois_data = [e["total"] for e in emprunts_par_mois]
    
    return Response({"mois": mois_labels, "emprunts": mois_data})

