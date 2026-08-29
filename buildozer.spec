[app]
title = Math Quiz Comores
package.name = quiz_app_comores
package.domain = org.fazad
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,ogg,ttf
source.include_patterns = badges/*, musiques/*, icone_appli/*

version = 0.3.2
requirements = python3,kivy==2.3.0,kivymd==1.1.1,plyer,pillow
orientation = portrait
fullscreen = 0

android.arch = arm64-v8a
android.api = 33
android.minapi = 21

icon.filename = badges/logo.png

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.release_artifact = apk
android.filename = MathQuizComores.apk

# Laisser vide pour signer avec GitHub
android.release_keystore =
android.release_keyalias =
android.release_keystore_password =
android.release_key_password =

p4a.branch = master
p4a.extra_args = --blacklist-regex=.*__pycache__.*

[buildozer]
log_level = 2
warn_on_root = 1
