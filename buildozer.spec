[app]
title = Math Quiz Comores
package.name = mathquizcomores
package.domain = org.mathquiz
source.include_exts = py,png,jpg,kv,atlas,ogg
source.dir = .
source.main.ext = py
version = 1.0
requirements = python3,kivy

# Laisse Buildozer gérer les versions recommandées pour éviter l'erreur de sdkmanager
android.api = 34
android.minapi = 21
android.ndk = 25b

android.permissions = INTERNET
orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1
