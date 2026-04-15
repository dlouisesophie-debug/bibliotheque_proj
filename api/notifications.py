cat > api/notifications.py << 'EOF'
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def envoyer_notification_emprunt(emprunt):
    """Envoyer un email lors d'un emprunt"""
    sujet = f"Confirmation d'emprunt - {emprunt.livre.titre}"
    message_html = render_to_string('emails/emprunt_confirmation.html', {
        'utilisateur': emprunt.utilisateur,
        'livre': emprunt.livre,
        'date_emprunt': emprunt.date_emprunt,
    })
    
    send_mail(
        sujet,
        '',  # Version texte vide car on utilise HTML
        settings.DEFAULT_FROM_EMAIL,
        [emprunt.utilisateur.email],
        fail_silently=False,
        html_message=message_html,
    )

def envoyer_notification_retard(emprunt):
    """Envoyer un email pour les retards"""
    sujet = f"Rappel : Retour de livre en retard - {emprunt.livre.titre}"
    message_html = render_to_string('emails/retard_notification.html', {
        'utilisateur': emprunt.utilisateur,
        'livre': emprunt.livre,
        'date_retour_prevue': emprunt.date_retour,
    })
    
    send_mail(
        sujet,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [emprunt.utilisateur.email],
        fail_silently=False,
        html_message=message_html,
    )
EOF