cat > api/management/commands/check_retards.py << 'EOF'
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Emprunt
from api.notifications import envoyer_notification_retard

class Command(BaseCommand):
    help = 'Vérifie les emprunts en retard et envoie des notifications'

    def handle(self, *args, **kwargs):
        aujourd_hui = timezone.now().date()
        
        # Trouver les emprunts en retard (date_retour dépassée et non retournés)
        emprunts_retard = Emprunt.objects.filter(
            retourne=False,
            date_retour__lt=aujourd_hui
        )
        
        count = 0
        for emprunt in emprunts_retard:
            # Mettre à jour le statut
            emprunt.statut = 'en_retard'
            emprunt.save()
            
            # Envoyer la notification
            try:
                envoyer_notification_retard(emprunt)
                count += 1
                self.stdout.write(f"✓ Notification envoyée pour: {emprunt.livre.titre}")
            except Exception as e:
                self.stdout.write(f"✗ Erreur pour {emprunt.livre.titre}: {e}")
        
        self.stdout.write(
            self.style.SUCCESS(f"\n✅ {count} notification(s) de retard envoyée(s)")
        )
EOF