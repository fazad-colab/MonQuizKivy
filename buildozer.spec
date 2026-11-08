[app]
title = Math Quiz Comores
package.name = quizapp_comores
package.domain = org.fazad
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,ogg,mp3,wav,json,html,js,css,woff,woff2,ttf
source.include_patterns = katex/*,katex/contrib/*,katex/fonts/*,sons/*,musiques/*,badges/*,icone_appli/*

version = 1.6.1
requirements = python3,kivy,plyer@https://github.com/kivy/plyer/archive/master.zip,pillow,android,pyjnius,requests,urllib3,certifi,idna,chardet


orientation = portrait
fullscreen = 0
android.arch = armeabi-v7a
android.api = 34
android.minapi = 21
android.ndk = 28c

icon.filename = badges/logo.png

android.permissions = INTERNET,ACCESS_NETWORK_STATE,POST_NOTIFICATIONS
android.release_artifact = apk
android.sign = True
android.debug = False
android.filename = MathQuizComores-armeabi-v7a.apk

android.use_androidx = True
android.enable_androidx = True
android.gradle_dependencies = androidx.core:core:1.12.0

# CORRIGÉ: accolade fermée
android.add_gradle_configuration = configurations.all { resolutionStrategy { force 'androidx.core:core:1.12.0' } }

android.p4a_branch = master

[buildozer]
log_level = 2
warn_on_root = 1
