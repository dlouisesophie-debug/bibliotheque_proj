from rest_framework import serializers
from .models import Auteur, Livre, Emprunt


# ─────────────── AUTEUR ───────────────
class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = '__all__'
        read_only_fields = ['id', 'date_creation']


# ─────────────── LIVRE ───────────────
class LivreSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.SerializerMethodField()

    class Meta:
        model = Livre
        fields = [
            'id',
            'titre',
            'isbn',
            'annee_publication',
            'categorie',
            'auteur',
            'auteur_nom',
            'disponible'
        ]
        read_only_fields = ['id']

    def get_auteur_nom(self, obj):
        return obj.auteur.nom if obj.auteur else None


# ─────────────── EMPRUNT ───────────────
from rest_framework import serializers
from .models import Emprunt

class EmpruntSerializer(serializers.ModelSerializer):
    livre_titre = serializers.ReadOnlyField(source='livre.titre')
    utilisateur_username = serializers.ReadOnlyField(source='utilisateur.username')

    class Meta:
        model = Emprunt
        fields = [
            'id',
            'utilisateur',
            'utilisateur_username',
            'livre',
            'livre_titre',
            'date_emprunt',
            'date_retour',
            'retourne'
        ]
        read_only_fields = ['date_emprunt']