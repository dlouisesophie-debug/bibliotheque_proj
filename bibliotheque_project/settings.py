# =========================
# ALLOWED HOSTS - PythonAnywhere
# =========================
ALLOWED_HOSTS = [
    '.pythonanywhere.com',           # Pour PythonAnywhere
    'votre_nom_utilisateur.pythonanywhere.com',  # Remplacez par votre username
    'localhost',
    '127.0.0.1',
]

# =========================
# DATABASE - PythonAnywhere utilise MySQL par défaut
# =========================
# PythonAnywhere offre MySQL (gratuit) et PostgreSQL (payant)

# Option 1: MySQL (recommandé pour gratuit)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'votre_username$bibliotheque',  # ⚠️ Important: $ pour séparer
        'USER': 'votre_username',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'votre_username.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}

# Option 2: SQLite (simple mais limité)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# =========================
# STATIC FILES - PythonAnywhere
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = '/home/votre_username/bibliotheque_proj/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/votre_username/bibliotheque_proj/media'

# =========================
# DEBUG - Toujours False en production
# =========================
DEBUG = False