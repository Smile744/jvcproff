[app]

title = JVC-PRO-FF
package.name = jvcsmile
package.domain = org.jvc

source.dir = .
source.include_extn = py,png,jpg,jpeg,txt,json,atlas,csv
version = 1.0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,moe.shizuku.manager.permission.API_V23

orientation = portrait
fullscreen = 0

android.arch = arm64-v8a
android.api = 33
android.minapi = 21
android.permissions = INTERNET
android.accept_sdk_license = True
p4a.branch = master

icon.filename = %(source.dir)s/joker.png
