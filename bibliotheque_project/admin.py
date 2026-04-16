from django.contrib.admin import AdminSite
from api.models import Auteur, Livre, Emprunt

class BibliothequeAdminSite(AdminSite):
    site_header = "Administration Bibliotheque"
    site_title = "Bibliotheque Admin"
    
    def index(self, request, extra_context=None):
        context = {
            'total_livres': Livre.objects.count(),
            'livres_disponibles': Livre.objects.filter(disponible=True).count(),
            'emprunts_cours': Emprunt.objects.filter(retourne=False).count(),
            'total_auteurs': Auteur.objects.count(),
        }
        return super().index(request, extra_context=context)

admin_site = BibliothequeAdminSite(name='myadmin')
