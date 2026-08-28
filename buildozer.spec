[app]
title = Math Quiz Comores
package.name = quizapp_comores
package.domain = org.fazad
version = 0.3.2
orientation = portrait
fullscreen = 0
source.dir =.

source.include_exts = py,png,jpeg,kv,json,ogg,ttf
source.include_patterns = badges/*, musiques/*, icone_appli/*

icon.filename = badges/logo.png

requirements = python3,kivy==2.3.0,kivymd==1.1.1,plyer,pillow,pyjnius

android.api = 33
android.minapi = 21
android.target_sdk_version = 33
android.arch = arm64-v8a
android.permissions = INTERNET,POST_NOTIFICATIONS
android.release_artifact = apk
android.filename = MathQuizComores.apk

android.release_keystore =
android.release_keyalias =
android.release_keystore_password =
android.release_key_password =

android.p4a_branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
