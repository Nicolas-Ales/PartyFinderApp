from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from negocio.modelo_clases import Usuario
from negocio.autentificacion import generar_hash, verificar_usuario
import negocio.datos_usuario as datos_usuario

from ui.custom_widget import ConfirmPopup
from ui.screen_names import Screens


class LoginScreen(Screen):

    def __init__(self, *args, **kwargs):
        Builder.load_file("ui/kv/login.kv")
        super().__init__(*args, **kwargs)
        self.name = Screens.Login.value

    def on_pre_enter(self):
        self.ids.login_email_text.text = ''
        self.ids.login_password_text.text = ''

    def on_btn_login_release(self):
        usuario = verificar_usuario(self.ids.login_email_text.text, self.ids.login_password_text.text)
        if not usuario is None:
            app = App.get_running_app()
            app.usuario_actual = usuario
            app.go_screen(Screens.Main.value)
        else:
            self.popup('Email y contraseña no son válidos.')

    def on_btn_register_release(self):
        if self.ids.register_password_text.text != self.ids.register_password_repeat_text.text:
            self.popup('Contraseñas no coinciden.')
            return

        usuario = Usuario()
        usuario.nombre = self.ids.register_name_text.text
        usuario.mail = self.ids.register_email_text.text
        usuario.pwd_hash = generar_hash(usuario.mail, self.ids.register_password_text.text)
        datos_usuario.alta(usuario)  # TODO: Verificar unicidad del email y nombre.
        self.ids.sm.current = 'login'

    def popup(self, message):
        popup = ConfirmPopup(title='Error', message=message)
        popup.open()

    def on_pre_leave_register(self):
        self.ids.register_email_text.text = ''
        self.ids.register_name_text.text = ''
        self.ids.register_password_text.text = ''
        self.ids.register_password_repeat_text.text = ''
