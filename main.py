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
