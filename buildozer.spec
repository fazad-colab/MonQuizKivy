[app]

# Nom affiché sous l'icone
title = Math Quiz Comores 

# Nom du package pour le Play Store
package.name = quizapp_comores

# Domaine inversé. Change "fazad" par ton nom
package.domain = org.fazad

# Version de l'app
version = 0.1.1

# Orientation portrait
orientation = portrait

# Plein écran
fullscreen = 0

# Dossier source
source.dir =.

# Fichiers à inclure dans l'APK. IMPORTANT pour musiques, images, json, logo
source.include_exts = py,png,jpeg,kv,json,ogg

# Dossiers à inclure EN PLUS
source.include_patterns = badges/*, musiques/*, icône_appli/*

# Icone de l'application. Mets ton logo.png dans le dossier racine
icon.filename = badges/logo.png

# Splash screen au démarrage. Optionnel
#presplash.filename = splash.png

# Nom des exigences python
requirements = kivy,pyjnius,plyer

# Permissions. Sur Android 13+ on a plus besoin du stockage
# INTERNET pour envoyer les avis
android.permissions = INTERNET,POST_NOTIFICATIONS

# API cible. 33 = Android 13
android.api = 33
android.minapi = 21
android.target_sdk_version = 33

# Architecture. arm64 pour téléphones récents
android.archs = armeabi-v7a

# Nom de l'APK de sortie
android.filename = MathQuizComores.apk

# Mode debug ou release
android.debug = True

# Utiliser p4a pour compiler
android.p4a_branch = develop

# Optimisations
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
