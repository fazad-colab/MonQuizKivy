[app]
title = Math Quiz Comores
package.name = quizapp_comores
package.domain = org.fazad
source.dir =.
source.include_exts = py,png,jpeg,kv,json,ogg
source.include_patterns = badges/*, musiques/*, icone_appli/*

version = 0.3.2
requirements = python3,kivy==2.3.0,kivymd@https://github.com/kivymd/KivyMD/archive/master.zip,plyer,pillow

orientation = portrait
fullscreen = 0
android.arch = armeabi-v7a
android.api = 34
android.minapi = 21
android.ndk = 23c

icon.filename = badges/logo.png

android.permissions = INTERNET,POST_NOTIFICATIONS,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.release_artifact = apk
android.filename = MathQuizComores.apk

android.use_androidx = True
android.enable_androidx = True
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1,androidx.core:core:1.12.0
android.manifest.intent_filters =
android.manifest.launch_mode = singleTask

android.p4a_branch = master
p4a.source_dir =
p4a.extra_args = --android-api=34 --android-minapi=21 --bootstrap=sdl2 --use-setuptools --exclude-support-lib

[buildozer]
log_level = 2
warn_on_root = 1
