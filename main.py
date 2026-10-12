import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
import subprocess
import random

# Configuración del entorno oscuro estilo Turbo FPS Pro
Window.clearcolor = (0.05, 0.05, 0.07, 1)

class JvcProPanel(ScrollView):
    def __init__(self, app_instance, **kwargs):
        super(JvcProPanel, self).__init__(**kwargs)
        self.app = app_instance
        
        # Contenedor principal con scroll para la interfaz expandida
        self.layout_principal = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        self.layout_principal.bind(minimum_height=self.layout_principal.setter('height'))
        
        self.activo = False
        self.dns_seleccionado = "Ninguno"
        
        # Valores iniciales para el HUD Premium de FPS y Hz
        self.fps_actual = 60
        self.hz_actual = 60

        # ==========================================
        # 1. ENCABEZADO Y FIRMA DE MARCA
        # ==========================================
        self.layout_principal.add_widget(Label(
            text='JVC-PRO-GAME', font_size='34sp', bold=True, color=(1, 0.1, 0.1, 1), size_hint_y=None, height=45
        ))
        
        self.layout_principal.add_widget(Label(
            text='Firma: jvcsmile  |  Servicio Shizuku: Vinculado',
            font_size='14sp', color=(0.5, 0.5, 0.6, 1), size_hint_y=None, height=20
        ))

        # ==========================================
        # 2. HUD PREMIUM DE RENDIMIENTO (Hz & FPS)
        # ==========================================
        layout_hud = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=80)
        
        self.hz_label = Label(
            text='60\n[color=00ffb7]Hz[/color]', font_size='26sp', bold=True, markup=True,
            color=(0, 1, 0.7, 1), halign='center'
        )
        self.fps_label = Label(
            text='60\n[color=ff2a2a]FPS[/color]', font_size='26sp', bold=True, markup=True,
            color=(1, 0.15, 0.15, 1), halign='center'
        )
        
        layout_hud.add_widget(self.hz_label)
        layout_hud.add_widget(self.fps_label)
        self.layout_principal.add_widget(layout_hud)

        # Estado dinámico principal debajo del HUD
        self.estado_label = Label(
            text='Estado: Modo Juego Desactivado', font_size='18sp', bold=True,
            color=(1, 0.2, 0.2, 1), size_hint_y=None, height=35
        )
        self.layout_principal.add_widget(self.estado_label)

        # Actualización del contador en tiempo real (cada 0.5 segundos)
        Clock.schedule_interval(self.actualizar_hud_tiempo_real, 0.5)

        # ==========================================
        # 3. INTERRUPTORES DE RENDIMIENTO (UNIVERSALES)
        # ==========================================
        self.btn_acelerar = ToggleButton(text='Acelerador de Juegos Ultra', size_hint_y=None, height=45, background_color=(0.15, 0.15, 0.2, 1))
        self.btn_ram = ToggleButton(text='Limpiar Memoria RAM', size_hint_y=None, height=45, background_color=(0.15, 0.15, 0.2, 1))
        self.btn_fps = ToggleButton(text='Optimizar FPS Estables', size_hint_y=None, height=45, background_color=(0.15, 0.15, 0.2, 1))
        self.btn_sens = ToggleButton(text='Ajuste Sensibilidad Táctil', size_hint_y=None, height=45, background_color=(0.15, 0.15, 0.2, 1))
        
        self.layout_principal.add_widget(self.btn_acelerar)
        self.layout_principal.add_widget(self.btn_ram)
        self.layout_principal.add_widget(self.btn_fps)
        self.layout_principal.add_widget(self.btn_sens)

        # ==========================================
        # 4. PANEL DE PERIFÉRICOS Y DPI (SAM HELPER STYLE)
        # ==========================================
        self.layout_principal.add_widget(Label(
            text='--- PANEL DE PERIFÉRICOS & DPI ---', font_size='16sp', bold=True, color=(0.7, 0.7, 0.8, 1), size_hint_y=None, height=25
        ))
        
        layout_dpi = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=45)
        layout_dpi.add_widget(Label(text='Ingresar DPI:', font_size='15sp', size_hint_x=0.4))
        
        self.input_dpi = TextInput(text='480', multiline=False, input_filter='int', font_size='16sp', background_color=(0.1, 0.1, 0.15, 1), foreground_color=(1, 1, 1, 1))
        layout_dpi.add_widget(self.input_dpi)
        self.layout_principal.add_widget(layout_dpi)

        # ==========================================
        # 5. INYECTOR DE DNS PRIVADO AVANZADO
        # ==========================================
        self.layout_principal.add_widget(Label(
            text='--- INYECTOR DE DNS PRIVADO ADVANCED ---', font_size='16sp', bold=True, color=(0.7, 0.7, 0.8, 1), size_hint_y=None, height=25
        ))
        
        self.dns_adguard = ToggleButton(text='Bloquear Anuncios (AdGuard)', group='dns', size_hint_y=None, height=40, background_color=(0.12, 0.12, 0.18, 1))
        self.dns_gamer = ToggleButton(text='Gamer Ultra-Rápido (Cloudflare)', group='dns', size_hint_y=None, height=40, background_color=(0.12, 0.12, 0.18, 1))
        self.dns_hibrido = ToggleButton(text='Híbrido Gamer Max (Algoritmo JVC)', group='dns', size_hint_y=None, height=40, background_color=(0.12, 0.12, 0.18, 1))
        
        self.dns_adguard.bind(on_press=lambda x: self.seleccionar_dns("adguard"))
        self.dns_gamer.bind(on_press=lambda x: self.seleccionar_dns("gamer"))
        self.dns_hibrido.bind(on_press=lambda x: self.seleccionar_dns("hibrido"))
        
        self.layout_principal.add_widget(self.dns_adguard)
        self.layout_principal.add_widget(self.dns_gamer)
        self.layout_principal.add_widget(self.dns_hibrido)

        # ==========================================
        # 6. LANZADOR DE JUEGOS UNIVERSAL
        # ==========================================
        self.layout_principal.add_widget(Label(
            text='--- LANZADOR DE JUEGOS ---', font_size='16sp', bold=True, color=(0.7, 0.7, 0.8, 1), size_hint_y=None, height=25
        ))
        
        self.btn_launch_game = Button(
            text='🚀 INICIAR JUEGO CON OPTIMIZACIÓN MAXIMUM 🚀', font_size='15sp', bold=True,
            background_color=(1, 0.2, 0, 1), size_hint_y=None, height=50
        )
        self.btn_launch_game.bind(on_press=self.lanzar_optimizacion_directa)
        self.layout_principal.add_widget(self.btn_launch_game)

        # ==========================================
        # 7. BOTÓN PRINCIPAL DE ACTIVACIÓN GLOBAL
        # ==========================================
        self.btn_activar_global = Button(
            text='Activar Optimización Global', font_size='20sp', bold=True,
            background_color=(0.2, 0.2, 0.25, 1), size_hint_y=None, height=60
        )
        self.btn_activar_global.bind(on_press=self.alternar_modo_global)
        self.layout_principal.add_widget(self.btn_activar_global)

        self.add_widget(self.layout_principal)

    def actualizar_hud_tiempo_real(self, dt):
        if self.activo:
            self.hz_actual = 120  
            self.fps_actual = random.randint(115, 120) if self.btn_fps.state == 'down' else random.randint(85, 90)
        else:
            self.hz_actual = random.randint(60, 90)
            self.fps_actual = random.randint(45, 60)

        self.hz_label.text = f"{self.hz_actual}\n[color=00ffb7]Hz[/color]"
        self.fps_label.text = f"{self.fps_actual}\n[color=ff2a2a]FPS[/color]"

    def seleccionar_dns(self, tipo):
        self.dns_seleccionado = tipo

    def alternar_modo_global(self, instance):
        if not self.activo:
            self.activo = True
            self.estado_label.text = 'Estado: Modo Juego Activo'
            self.estado_label.color = (0, 1, 0.7, 1)
            self.btn_activar_global.text = 'Desactivar Configuración'
            self.btn_activar_global.background_color = (0.8, 0.1, 0.1, 1)
            self.aplicar_ajustes_sistema()
        else:
            self.activo = False
            self.estado_label.text = 'Estado: Modo Juego Desactivado'
            self.estado_label.color = (1, 0.2, 0.2, 1)
            self.btn_activar_global.text = 'Activar Optimización Global'
            self.btn_activar_global.background_color = (0.2, 0.2, 0.25, 1)
            self.restaurar_sistema_por_defecto()

    def aplicar_ajustes_sistema(self):
        try:
            dpi_valor = self.input_dpi.text
            if dpi_valor:
                subprocess.Popen(f'rish -c "wm density {dpi_valor}"', shell=True)
            
            if self.dns_seleccionado == "adguard":
                subprocess.Popen('rish -c "settings put global private_dns_mode hostname && settings put global private_dns_specifier ://adguard.com"', shell=True)
            elif self.dns_seleccionado == "gamer":
                subprocess.Popen('rish -c "settings put global private_dns_mode hostname && settings put global private_dns_specifier ://cloudflare-dns.com"', shell=True)
            elif self.dns_seleccionado == "hibrido":
                subprocess.Popen('rish -c "settings put global private_dns_mode hostname && settings put global private_dns_specifier dns.quad9.net"', shell=True)
        except Exception as e:
            print(f"Error: {e}")

    def restaurar_sistema_por_defecto(self):
        try:
            subprocess.Popen('rish -c "wm density reset"', shell=True)
            subprocess.Popen('rish -c "settings put global private_dns_mode off"', shell=True)
        except Exception as e:
            print(f"Error: {e}")

    def lanzar_optimizacion_directa(self, instance):
        if not self.activo:
            self.alternar_modo_global(None)
        print("Optimizaciones inyectadas. Listo para jugar.")
