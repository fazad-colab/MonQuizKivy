[app]
title = Math Quiz Comores
package.name = quizapp_comores
package.domain = org.fazad
source.dir =.
source.include_exts = py,png,jpeg,kv,json,ogg
source.include_patterns = badges/*, musiques/*, icone_appli/*

version = 0.4.1
requirements = python3,kivy==2.3.0,kivymd@https://github.com/kivymd/KivyMD/archive/master.zip,plyer@https://github.com/kivy/plyer/archive/master.zip,pillow

orientation = portrait
fullscreen = 0
android.arch = armeabi-v7a
android.api = 34
android.minapi = 21
android.ndk = 25b

icon.filename = badges/logo.png

android.permissions = INTERNET,POST_NOTIFICATIONS,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.release_artifact = apk
android.filename = MathQuizComores-v7a.apk

android.use_androidx = True
android.enable_androidx = True
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1,androidx.core:core:1.12.0

# Ça c'est la clé pour ndk25 + v7a
android.add_gradle_repositories = mavenCentral()
android.add_aar_dependencies = 
android.add_jars = 
android.blacklist = android.support.*,androidx.legacy.*

android.p4a_branch = master

[buildozer]
log_level = 2
warn_on_root = 1
