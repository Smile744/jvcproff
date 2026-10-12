# -*- coding: utf-8 -*-
# =====================================================================
# JVC-PRO-FF · CELDA UNICA para Google Colab
# Pega TODO el contenido de este archivo en UNA sola celda de Colab
# y pulsa Ejecutar. Al terminar se descarga el APK automaticamente.
# Es re-ejecutable: si se corta, vuelve a ejecutar la misma celda y
# retoma donde iba (no repite lo ya instalado).
# =====================================================================

import os, re, glob, subprocess

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
os.environ["PIP_USER"] = "false"
VENV = "/content/venv_build"
os.environ["PATH"] = VENV + "/bin:" + os.environ["PATH"]


def run(cmd, marker=None):
    print("\n>>> " + cmd, flush=True)
    if subprocess.call(cmd, shell=True, executable="/bin/bash") != 0:
        raise SystemExit("FALLO: " + cmd)
    if marker:
        open(marker, "w").write("ok")


# ---------- 1) dependencias del sistema ----------
if not os.path.exists("/content/.ok_apt"):
    run("apt-get update -y")
    run("apt-get install -y openjdk-17-jdk git zip unzip autoconf libtool pkg-config "
        "zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev")
    run("update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java",
        marker="/content/.ok_apt")
else:
    print("dependencias del sistema: ya instaladas, omitidas")

# ---------- 2) main.py ----------
APP_CODE = """
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window

Window.clearcolor = (0.05, 0.05, 0.05, 1)


class JVCSmileRoot(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.add_widget(Label(text='[b]JVC-PRO-FF[/b]', font_size='28sp',
                              markup=True, color=(0.9, 0.1, 0.1, 1)))
        try:
            self.add_widget(Image(source='joker.png', size_hint=(1, 0.5)))
        except Exception:
            self.add_widget(Label(text='[ Icono ]', font_size='16sp'))

        self.add_widget(Label(text='Firma: jvcsmile', font_size='14sp',
                              color=(0.5, 0.5, 0.5, 1)))

        self.status_label = Label(text='Estado: Listo para optimizar',
                                  font_size='18sp', color=(0.1, 0.8, 0.1, 1))
        self.add_widget(self.status_label)

        self.btn = Button(text='Activar Optimizacion', size_hint=(1, 0.2),
                          background_color=(0.8, 0.1, 0.1, 1), font_size='18sp')
        self.btn.bind(on_press=self.toggle)
        self.add_widget(self.btn)

    def toggle(self, _):
        if 'Listo' in self.status_label.text:
            self.status_label.text = 'Estado: Modo Juego Activo'
            self.status_label.color = (0.1, 0.9, 0.9, 1)
            self.btn.text = 'Desactivar'
            self.btn.background_color = (0.3, 0.3, 0.3, 1)
        else:
            self.status_label.text = 'Estado: Listo para optimizar'
            self.status_label.color = (0.1, 0.8, 0.1, 1)
            self.btn.text = 'Activar Optimizacion'
            self.btn.background_color = (0.8, 0.1, 0.1, 1)


class JVCSmileApp(App):
    def build(self):
        self.title = 'JVC-PRO-FF'
        return JVCSmileRoot()


if __name__ == '__main__':
    JVCSmileApp().run()
"""
open("/content/main.py", "w").write(APP_CODE.strip() + "\n")
print("main.py creado")

# ---------- 3) icono ----------
if not os.path.exists("/content/joker.png"):
    from PIL import Image as PILImage, ImageDraw
    im = PILImage.new("RGB", (512, 512), (13, 13, 13))
    ImageDraw.Draw(im).ellipse([96, 96, 416, 416], fill=(200, 25, 25))
    im.save("/content/joker.png")
print("joker.png listo")

# ---------- 4) venv + buildozer ----------
if not os.path.exists(VENV + "/bin/buildozer"):
    run("rm -rf " + VENV)
    run("python3 -m venv " + VENV)
    run(VENV + "/bin/pip install -q --upgrade pip")
    run(VENV + '/bin/pip install -q "cython<3.0.0" "setuptools<66.0.0" '
        '"wheel~=0.40.0" buildozer appdirs sh jinja2')
else:
    print("buildozer: ya instalado, omitido")
run("buildozer --version")

# ---------- 5) buildozer.spec ----------
def set_key(content, key, value):
    pat = r'^[ \t]*#?[ \t]*' + re.escape(key) + r'[ \t]*=.*$'
    if re.search(pat, content, flags=re.M):
        return re.sub(pat, key + " = " + value, content, count=1, flags=re.M)
    return content.rstrip() + "\n" + key + " = " + value + "\n"


if not os.path.exists("/content/buildozer.spec"):
    run("buildozer init")

spec = open("/content/buildozer.spec").read()
for k, v in {
    "title": "JVC-PRO-FF",
    "package.name": "jvcsmile",
    "package.domain": "org.jvc",
    "requirements": "python3,kivy",
    "source.include_extn": "py,png,jpg,jpeg,txt,json,atlas,csv",
    "icon.filename": "%(source.dir)s/joker.png",
    "android.permissions": "INTERNET",
    "android.arch": "arm64-v8a",
    "android.api": "33",
    "android.minapi": "21",
}.items():
    spec = set_key(spec, k, v)
open("/content/buildozer.spec", "w").write(spec)

ok = True
for k in ("requirements", "icon.filename", "android.arch", "package.name"):
    for line in spec.splitlines():
        if re.match(r'\s*#?\s*' + re.escape(k) + r'\s*=', line):
            activo = not line.strip().startswith("#")
            ok = ok and activo
            print(("  OK   " if activo else "  MAL  ") + line.strip())
if not ok:
    raise SystemExit("El spec quedo comentado, no se puede compilar aun")

# ---------- 6) compilar ----------
run("yes | buildozer -v android debug")

# ---------- 7) descargar ----------
apks = sorted(glob.glob("/content/bin/*.apk"), key=os.path.getmtime)
print("\nAPK generados:", apks)
if apks:
    size_mb = os.path.getsize(apks[-1]) / 1048576.0
    print("=> %s  (%.1f MB)" % (apks[-1], size_mb))
    from google.colab import files
    files.download(apks[-1])
else:
    print("No aparecio APK: revisa el log de buildozer arriba")
