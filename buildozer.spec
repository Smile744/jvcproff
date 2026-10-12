[app]

title = JVC-PRO-GAME
package.name = jvcprogame
package.domain = org.jvcsmile

source.dir = .
source.include_extn = py,png,jpg,jpeg,txt,json,atlas,csv
version = 1.0

# REQUERIMIENTOS CORRECTOS (Añadido android y shizuku)
requirements = python3,kivy,android,shizuku

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a
android.api = 33
android.minapi = 21

# UNICA LINEA DE PERMISOS VALIDA (Sin duplicados)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,moe.shizuku.manager.permission.API_V23

android.accept_sdk_license = True
p4a.branch = master

icon.filename = %(source.dir)s/joker.png
