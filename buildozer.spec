[app]
title = Math Quiz Comores
package.name = quizapp_comores
package.domain = org.fazad
source.dir =.
source.include_exts = py,png,jpeg,kv,json,ogg
source.include_patterns = badges/*, musiques/*, icone_appli/*

version = 0.3.2
requirements = python3,kivy==2.3.0,kivymd==1.1.1,plyer,pillow

orientation = portrait
fullscreen = 0
android.arch = arm64-v8a
android.api = 33
android.minapi = 21
android.sdk_path =
android.ndk_path =
android.gradle_dependencies =

icon.filename = badges/logo.png

android.permissions = INTERNET,POST_NOTIFICATIONS,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.release_artifact = apk
android.filename = MathQuizComores.apk

# Laisse vide, on signe avec le yml
android.release_keystore =
android.release_keyalias =
android.release_keystore_password =
android.release_key_password =

android.p4a_branch = master
p4a.source_dir =
p4a.extra_args = --blacklist-regex=.*__pycache__.*

[buildozer]
log_level = 2
warn_on_root = 1
