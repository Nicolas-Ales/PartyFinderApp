from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp

from negocio import datos_notificaciones

from ui.screen_names import Screens

class MainScreen(Screen):

    notif_scroll_list = ObjectProperty()

    def __init__(self, *args, **kwargs):
        Builder.load_file("ui/kv/main.kv")
        super().__init__(*args, **kwargs)
        self.name = Screens.Main.value

    def on_pre_enter(self):
        self.actualizar()

    def actualizar(self):
        self.notif_scroll_list.clear_widgets()
        usuario = App.get_running_app().usuario_actual
        notif_list = datos_notificaciones.notif_usuario(usuario)
        for notif in notif_list:
            notif_item = NotificationItem(notificacion=notif)
            self.notif_scroll_list.add_widget(notif_item)

class NotificationItem(Button):

    notificacion = ObjectProperty()

    def __init__(self, notificacion=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(72)
        self.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.notificacion = notificacion
    
    def on_notificacion(self, instance, value):
        fecha = value.fecha_creacion.strftime("%H:%M - %d/%m/%Y")
        self.text = '{0}\n{1}'.format(fecha, value.descripcion)
