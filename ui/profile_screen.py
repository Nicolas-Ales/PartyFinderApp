from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from ui.screen_names import Screens
from ui.custom_widget import ConfirmPopup
from negocio.autentificacion import generar_hash,verificar_usuario
from negocio import datos_usuario

class ProfileScreen(Screen):
    
    def __init__(self, *args, **kwargs):
        Builder.load_file("ui/kv/profile.kv")
        super().__init__(*args, **kwargs)
        self.name = Screens.Profile.value
        App.get_running_app().bind(usuario_actual=self.actualizar_labels)
    
    def actualizar_labels(self, *args, **kwargs):
        usuario_actual = App.get_running_app().usuario_actual
        if usuario_actual:
            self.ids.email_label.text = usuario_actual.mail
            self.ids.nombre_label.text = usuario_actual.nombre
            self.ids.new_email_textinput.text = usuario_actual.mail
            self.ids.new_name_textinput.text = usuario_actual.nombre
    
    def update_pass(self):
        usuario = App.get_running_app().usuario_actual
        if self.ids.new_password_textinput.text != '':
            if self.ids.new_password_textinput.text == self.ids.password_repeat_textinput.text:
                if verificar_usuario(usuario.mail, self.ids.old_password_textinput.text):
                    usuario.pwd_hash = generar_hash(usuario.mail, self.ids.old_password_textinput.text)
                    usuario = datos_usuario.modificar(usuario)
                    self.popup('Contraseña modificada')
                    self.volver()
                else: self.popup('Contraseña incorrecta.')
            else: self.popup('Contraseñas no coinciden.')
        else: self.popup('Contraseñas no coinciden.')
    
    def update_name(self):
        usuario = App.get_running_app().usuario_actual
        
        if not verificar_usuario(usuario.mail, self.ids.password_textinput.text):
            self.popup('Contraseña Incorrecta')
            return

        if self.ids.new_email_textinput.text == '' or self.ids.new_name_textinput.text == '':
            self.popup('Falta ingresar el nombre o el mail')
            return

        if self.ids.new_name_textinput.text != usuario.nombre:
            if datos_usuario.buscar_nombre(self.ids.new_name_textinput.text):
                self.popup('Nombre de Usuario Ocupado')
                return
            
        if self.ids.new_email_textinput.text != usuario.mail:
            if datos_usuario.buscar_mail(self.ids.new_email_textinput.text):
                self.popup('Este Mail esta siendo utilizado por otro usuario')
                return
        
        usuario.nombre = self.ids.new_name_textinput.text
        usuario.mail = self.ids.new_email_textinput.text
        usuario.pwd_hash = generar_hash(self.ids.new_email_textinput.text, self.ids.password_textinput.text)
        datos_usuario.alta(usuario)
        self.actualizar_labels()
        self.popup('Datos modificados')
        self.volver()
        self.ids.password_textinput.text = ''

    def volver(self):
        self.ids.new_password_textinput.text = ''
        self.ids.password_repeat_textinput.text = ''
        self.ids.old_password_textinput.text = ''
        self.ids.password_textinput.text = ''
        self.ids.sm.current = 'standar'

    def cerrar_sesion(self):
        app = App.get_running_app()
        app.usuario_actual = None
        app.go_screen(Screens.Login.value)

    def popup(self, message):
        popup = ConfirmPopup(title='Error', message=message)
        popup.open()
