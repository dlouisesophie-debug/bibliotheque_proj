from django.db import models
from django.contrib.auth.models import User


class Auteur(models.Model):
    nom = models.CharField(max_length=200)
    biographie = models.TextField(blank=True, null=True)
    nationalite = models.CharField(max_length=100, blank=True, default='')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Livre(models.Model):
    CATEGORIES = [
        ('roman', 'Roman'),
        ('essai', 'Essai'),
        ('poesie', 'Poésie'),
        ('science', 'Science'),
    ]

    titre = models.CharField(max_length=300)
    isbn = models.CharField(max_length=17, unique=True)
    annee_publication = models.IntegerField()
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='roman')
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE, related_name='livres')
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class Emprunt(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField(null=True, blank=True)
    retourne = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.utilisateur} - {self.livre}"