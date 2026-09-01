[app]
title = Math Quiz Comores
package.name = quizapp_comores
package.domain = org.fazad
source.dir =.
source.include_exts = py,png,jpeg,kv,json,ogg
source.include_patterns = badges/*, musiques/*, icone_appli/*

version = 0.4.4
requirements = python3,kivy,pillow

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

# ON FORCE GRADLE 7.4.2 qui marche sur Github
android.gradle_version = 7.4.2
android.gradle_plugin_version = 7.4.2

android.p4a_branch = master

[buildozer]
log_level = 2
warn_on_root = 1
