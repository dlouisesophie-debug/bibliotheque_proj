from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Auteur, Livre, Emprunt


class AuteurSerializer(serializers.ModelSerializer):
    nombre_livres = serializers.SerializerMethodField()

    class Meta:
        model = Auteur
        fields = ['id', 'nom', 'biographie', 'nationalite', 
                  'date_creation', 'nombre_livres']  # Enlevé 'prenom' et 'date_naissance'

    def get_nombre_livres(self, obj):
        return obj.livres.count()


class LivreListSerializer(serializers.ModelSerializer):
    """Serializer léger pour la liste"""
    auteur_nom = serializers.CharField(source='auteur.nom', read_only=True)

    class Meta:
        model = Livre
        fields = ['id', 'titre', 'auteur_nom', 'categorie', 'disponible', 'isbn', 'annee_publication']


class LivreDetailSerializer(serializers.ModelSerializer):
    """Serializer complet pour le détail"""
    auteur = AuteurSerializer(read_only=True)
    auteur_id = serializers.PrimaryKeyRelatedField(
        queryset=Auteur.objects.all(), source='auteur', write_only=True
    )
    nombre_emprunts = serializers.SerializerMethodField()

    class Meta:
        model = Livre
        fields = ['id', 'titre', 'auteur', 'auteur_id', 'categorie',
                  'disponible', 'isbn', 'annee_publication', 'date_creation', 
                  'nombre_emprunts']

    def get_nombre_emprunts(self, obj):
        return obj.emprunts.count()

    def validate_isbn(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("L'ISBN ne doit contenir que des chiffres.")
        return value


class EmpruntSerializer(serializers.ModelSerializer):
    utilisateur_nom = serializers.CharField(source='utilisateur.username', read_only=True)
    livre_titre = serializers.CharField(source='livre.titre', read_only=True)
    jours_restants = serializers.SerializerMethodField()

    class Meta:
        model = Emprunt
        fields = ['id', 'livre', 'livre_titre', 'utilisateur', 'utilisateur_nom',
                  'date_emprunt', 'date_retour', 'retourne', 'jours_restants']
        read_only_fields = ['utilisateur', 'date_emprunt', 'jours_restants']

    def get_jours_restants(self, obj):
        if obj.retourne or not obj.date_retour:
            return None
        from datetime import date
        if obj.date_retour:
            return (obj.date_retour - date.today()).days
        return None

    def validate(self, data):
        livre = data.get('livre')
        if livre and not livre.disponible:
            raise serializers.ValidationError("Ce livre n'est pas disponible.")
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)