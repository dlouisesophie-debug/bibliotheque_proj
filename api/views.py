from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from .models import Auteur, Livre, Emprunt
from .serializers import AuteurSerializer, LivreSerializer, EmpruntSerializer


# =========================
# AUTEUR - APIView (CRUD manuel)
# =========================

class AuteurListAPIView(APIView):

    def get(self, request):
        auteurs = Auteur.objects.all()
        serializer = AuteurSerializer(auteurs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuteurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuteurDetailAPIView(APIView):

    def get_object(self, pk):
        return Auteur.objects.get(pk=pk)

    def get(self, request, pk):
        auteur = self.get_object(pk)
        serializer = AuteurSerializer(auteur)
        return Response(serializer.data)

    def put(self, request, pk):
        auteur = self.get_object(pk)
        serializer = AuteurSerializer(auteur, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        auteur = self.get_object(pk)
        auteur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =========================
# LIVRE - VIEWSET (automatique)
# =========================

class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer


# =========================
# AUTEUR - VIEWSET (optionnel)
# =========================

class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer


# =========================
# EMPRUNT - VIEWSET
# =========================

class EmpruntViewSet(viewsets.ModelViewSet):
    queryset = Emprunt.objects.all()
    serializer_class = EmpruntSerializer

    def perform_create(self, serializer):
        livre = serializer.validated_data['livre']

        # empêcher double emprunt
        if not livre.disponible:
            raise ValueError("Ce livre est déjà emprunté")

        livre.disponible = False
        livre.save()

        serializer.save()