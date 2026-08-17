[app]

title = MonQuizKivy
package.name = monquizkivy
package.domain = org.fazad
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3==3.10.13
android.requirements = sdl2,kivy
android.api = 33
android.minapi = 21
android.arch = arm64-v8a
android.sdk_path = $HOME/.buildozer/android/platform/android-sdk
android.ndk_path = $HOME/.buildozer/android/platform/android-ndk-r25b
android.allow_backup = False
android.permissions = INTERNET
android.logcat_filters = *:S python:D
p4a.branch = master
p4a.source_dir =
orientation = portrait
fullscreen = 0
osx.kivy_statusbar_color = 000
ios.kivy_statusbar_color = 000000
ios.ios_deployment_target = 12.0
ios.codesign.debug =
ios.codesign.release =

[buildozer]

log_level = 2
warn_on_root = 1
