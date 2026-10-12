# ============================================================
# JVC-PRO-FF  ·  Buildozer + Kivy en Google Colab
# Copia cada bloque (=== CELLA n ===) en una celda del notebook.
# Los bloques 1..4 son un script de Python; el 5 es shell.
# ============================================================

# ============ CELLA 1 · dependencias del sistema ============
!apt-get update -y
!apt-get install -y openjdk-17-jdk git zip unzip autoconf libtool pkg-config \
  zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
!update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java

import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
os.environ["PIP_USER"] = "false"


# ============ CELLA 2 · código de la app + icono ============
main_code = """\
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window

Window.clearcolor = (0.05, 0.05, 0.05, 1)


class JVCSmileRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.add_widget(Label(
            text="[b]JVC-PRO-FF[/b]",
            font_size='28sp', markup=True, color=(0.9, 0.1, 0.1, 1)))

        try:
            self.add_widget(Image(source='joker.png', size_hint=(1, 0.5)))
        except Exception:
            self.add_widget(Label(text="[ Icono del Joker ]", font_size='16sp'))

        self.add_widget(Label(text="Firma: jvcsmile", font_size='14sp',
                              color=(0.5, 0.5, 0.5, 1)))

        self.status_label = Label(text="Estado: Listo para optimizar",
                                  font_size='18sp', color=(0.1, 0.8, 0.1, 1))
        self.add_widget(self.status_label)

        self.btn_boost = Button(text="Activar Optimizacion", size_hint=(1, 0.2),
                                background_color=(0.8, 0.1, 0.1, 1), font_size='18sp')
        self.btn_boost.bind(on_press=self.toggle_optimization)
        self.add_widget(self.btn_boost)

    def toggle_optimization(self, instance):
        if "Listo" in self.status_label.text:
            self.status_label.text = "Estado: Modo Juego Activo"
            self.status_label.color = (0.1, 0.9, 0.9, 1)
            self.btn_boost.text = "Desactivar"
            self.btn_boost.background_color = (0.3, 0.3, 0.3, 1)
        else:
            self.status_label.text = "Estado: Listo para optimizar"
            self.status_label.color = (0.1, 0.8, 0.1, 1)
            self.btn_boost.text = "Activar Optimizacion"
            self.btn_boost.background_color = (0.8, 0.1, 0.1, 1)


class JVCSmileApp(App):
    def build(self):
        self.title = "JVC-PRO-FF"
        return JVCSmileRoot()


if __name__ == '__main__':
    JVCSmileApp().run()
"""
with open("main.py", "w") as f:
    f.write(main_code)

from PIL import Image, ImageDraw
img = Image.new("RGB", (512, 512), (13, 13, 13))
ImageDraw.Draw(img).ellipse([96, 96, 416, 416], fill=(200, 25, 25))
img.save("joker.png")

import os
print("archivos:", os.listdir("."))


# ============ CELLA 3 · venv + buildozer (ANTES del init) ============
!rm -rf venv_build .buildozer /root/.buildozer
!python3 -m venv venv_build
import os
os.environ["PATH"] = os.path.abspath("venv_build/bin") + ":" + os.environ["PATH"]
!pip install --upgrade pip
!pip install "cython<3.0.0" "setuptools<66.0.0" "wheel~=0.40.0" buildozer appdirs sh jinja2
!buildozer --version


# ============ CELLA 4 · generar y parchear buildozer.spec ============
!rm -f buildozer.spec
!buildozer init

import re

def set_key(content, key, value):
    pat = rf'^[ \t]*#?[ \t]*{re.escape(key)}[ \t]*=.*$'
    if re.search(pat, content, flags=re.M):
        return re.sub(pat, f'{key} = {value}', content, count=1, flags=re.M)
    return content.rstrip() + f'\n{key} = {value}\n'

c = open("buildozer.spec").read()
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
    c = set_key(c, k, v)
open("buildozer.spec", "w").write(c)

# verificacion: ninguna clave debe quedar comentada
for k in ("requirements", "icon.filename", "android.arch", "package.name"):
    line = [l for l in c.splitlines() if re.match(rf'\s*#?\s*{re.escape(k)}\s*=', l)]
    print(k, "->", line)


# ============ CELLA 5 · compilar (esto puede tardar 30-60 min) ============
# %%bash
# yes | buildozer -v android debug
# ls -lh bin/


# ============ CELLA 6 · descargar el APK ============
import glob
from google.colab import files
apks = glob.glob("bin/*.apk")
print("APK encontrados:", apks)
if apks:
    files.download(apks[0])
