[app]

# (str) Titre de votre application
title = Math Quiz Comores

# (str) Nom du paquet (doit être unique, sans espaces ni caractères spéciaux)
package.name = mathquizcomores

# (str) Domaine du paquet
package.domain = org.mathquiz

# (str) Fichiers source à inclure (séparés par des virgules)
source.include_exts = py,png,jpg,kv,atlas,ogg

# (str) Répertoire source de l'application
source.dir = .

# (list) Application par défaut (point d'entrée)
source.main.ext = py

# (str) Version de l'application
version = 1.0

# (list) Application requirements
requirements = python3,kivy

# (str) Version de l'API Android cible (version stable recommandée)
android.api = 33

# (str) Version minimale de l'API Android
android.minapi = 21

# (str) Version du NDK Android (fixée pour correspondre au téléchargement stable)
android.ndk = 25b

# (list) Permissions nécessaires
android.permissions = INTERNET

# (str) Orientation de l'écran
orientation = portrait

# (bool) Plein écran
fullscreen = 1

[buildozer]

# (int) Niveau de log (2 = debug pour voir les détails si besoin)
log_level = 2

# (int) Afficher les avertissements
warn_on_root = 1
