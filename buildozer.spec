[app]

title = Math Quiz Comores

package.name = mathquizcomores

package.domain = org.mathquiz

source.dir = .

source.include_exts = py,png,jpg,kv,atlas,json

source.exclude_exts = spec

source.exclude_dirs = tests, bin

source.include_patterns = assets/*,images/*.png

version = 0.1

requirements = python3,kivy

orientation = portrait

android.archs = arm64-v8a

android.permissions = INTERNET

[buildozer]

log_level = 2

warn_root = 1

android.accept_sdk_license = True

android.api = 30

android.minapi = 21

android.sdk_build_tools_version = 30.0.3

android.ndk = 23b
