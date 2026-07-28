[app]

# (str) Title of your application
title = Math Quiz Comores

# (str) Package name
package.name = mathquizcomores

# (str) Package domain (needed for android packaging)
package.domain = org.mathquiz

# (list) Source files to include (let empty to include all files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Source files to exclude (let empty to exclude all files)
source.exclude_exts = spec

# (list) List of directory to exclude (from source.include_exts)
source.exclude_dirs = tests, bin

# (list) List of inclusions in your application
source.include_patterns = assets/*,images/*.png

# (str) Application versioning
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Custom source folders for requirements
#requirements.source.dir = ../../../kivy

# (list) Permissions
#android.permissions = INTERNET

# (str) Icon of your application
icon.filename = %(source.dir)s/logo.png

# (list) Supported orientations
orientation = portrait

# (list) The format used to package for android
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_root = 1
