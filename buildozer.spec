[app]

# (str) Titre de votre application
title = Math Quiz Comores

# (str) Nom du paquet (doit être unique, sans espaces ni caractères spéciaux)
package.name = mathquizcomores

# (str) Domaine du paquet
package.domain = org.mathquiz

# (str) Fichiers source à inclure (séparés par des virgules)
source.include_exts = py,png,jpg,kv,atlas,ogg

# (list) Répertoire(s) source (relatif à .spec)
source.dir = .

# (list) Application par défaut (point d'entrée)
source.main.ext = py

# (str) Version de l'application
version = 1.0

# (list) Application requirements
# Spécifie les modules nécessaires (ex: kivy, python3, etc.)
requirements = python3,kivy

# (str) Version de l'API Android cible
android.api = 31

# (str) Version minimale de l'API Android
android.minapi = 21

android.ndk = 25b 

# (list) Permissions nécessaires (laisse vide si aucune, ou ajoute les permissions Android)
android.permissions = INTERNET

# (str) Orientation de l'écran (portrait, landscape ou all)
orientation = portrait

# (bool) Indique si l'application est un service en arrière-plan ou non
fullscreen = 1

[buildozer]

# (int) Niveau de log (0 = error, 1 = info, 2 = debug (avec traces de compilation))
log_level = 2

# (int) Afficher les avertissements (0 = désactivé, 1 = activé)
warn_on_root = 1
