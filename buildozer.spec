[app]
title = Math Quiz Comores
package.name = quizapp_comores
package.domain = org.fazad
source.dir =.
source.include_exts = py,png,jpeg,kv,json,ogg
source.include_patterns = badges/*, musiques/*, icone_appli/*

version = 0.4.10
requirements = python3,kivy,plyer@https://github.com/kivy/plyer/archive/master.zip,pillow

orientation = portrait
fullscreen = 0
android.arch = armeabi-v7a
android.api = 34
android.minapi = 21
android.ndk = 25b

icon.filename = badges/logo.png

android.permissions = INTERNET,POST_NOTIFICATIONS,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.release_artifact = apk
android.sign = True
android.debug = False
android.filename = MathQuizComores-v7a.apk

android.use_androidx = True
android.enable_androidx = True
android.gradle_dependencies = androidx.core:core:1.12.0

# CORRIGÉ: accolade fermée
android.add_gradle_configuration = configurations.all { resolutionStrategy { force 'androidx.core:core:1.12.0' } }

android.p4a_branch = master

[buildozer]
log_level = 2
warn_on_root = 1
