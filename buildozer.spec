[app]

title = JVC-PRO-GAME
package.name = jvcprogame
package.domain = org.jvcsmile

source.dir = .
source.include_extn = py,png,jpg,jpeg,txt,json,atlas,csv
version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.permissions = INTERNET
android.accept_sdk_license = True
p4a.branch = master

icon.filename = %(source.dir)s/joker.png
