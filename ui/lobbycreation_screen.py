from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from negocio import datos_lobby, datos_etiquetas
from negocio.modelo_clases import Lobby, Miembro, Etiqueta
from ui.screen_names import Screens
from ui.custom_widget import ConfirmPopup

class LobbyCreationScreen(Screen):

    def __init__(self, *args, **kwargs):
        Builder.load_file("ui/kv/lobbycreation.kv")
        super().__init__(*args, **kwargs)
        self.name = Screens.LobbyCreation.value
        self.lobby = None

    def on_btn_crear_lobby(self):
        input_nombre = self.ids.create_name_text.text.strip()
        if len(input_nombre) < 5:
            popup = ConfirmPopup(title='', message='Ingrese un nombre para el lobby de al menos 5 caracteres.')
            popup.open()
            return
        elif len(input_nombre) > 46:
            popup = ConfirmPopup(title='', message='El nombre del lobby no puede tener mas de 46 caracteres')
            popup.open()
            return

        app = App.get_running_app()

        if not self.lobby:
            if not datos_lobby.buscar_nombre_exacto(input_nombre) is None:
                popup = ConfirmPopup(title='', message='Lobby con este nombre ya existe. Pruebe otro.')
                popup.open()
                return

            self.lobby = Lobby(nombre=input_nombre, descripcion=self.ids.create_desc_text.text,
                contacto=self.ids.link_contacto.text, fecha_creacion=datetime.now())

            desc_etiquetas = self.ids.create_tag_text.text.replace(" ", "").split(sep=',')
            for desc_etiqueta in desc_etiquetas:
                etiqueta = datos_etiquetas.find_or_create(desc_etiqueta)
                self.lobby.etiquetas.append(etiqueta)
            
            miembro = Miembro(rol=Miembro.Rol.Dueño, aceptado=True, usuario=app.usuario_actual, lobby=self.lobby)
            datos_lobby.alta(self.lobby)
            popup = ConfirmPopup(title='Lobby', message='Lobby creado exitosamente.')
        else:
            self.lobby.nombre = self.ids.create_name_text.text
            self.lobby.descripcion = self.ids.create_desc_text.text
            self.lobby.contacto = self.ids.link_contacto.text
            
            self.lobby.etiquetas = []
            desc_etiquetas = self.ids.create_tag_text.text.replace(" ", "").split(sep=',')
            for desc_etiqueta in desc_etiquetas:
                etiqueta = datos_etiquetas.find_or_create(desc_etiqueta)
                self.lobby.etiquetas.append(etiqueta)
            
            datos_lobby.modificar(self.lobby)
            popup = ConfirmPopup(title='Lobby', message='Lobby modificado exitosamente.')
            
        app.go_screen(Screens.Main.value)
        popup.open()

    def on_pre_enter(self):
        print(self.lobby)
        if self.lobby:
            self.ids.create_name_text.text = self.lobby.nombre
            self.ids.create_desc_text.text = self.lobby.descripcion
            self.ids.link_contacto.text = self.lobby.contacto
            if self.lobby.etiquetas:
                self.ids.create_tag_text.text = ','.join(etiqueta.descripcion for etiqueta in self.lobby.etiquetas)
            self.ids.btn_crear.text = "Modificar"
            
    def on_pre_leave(self):
        self.ids.create_name_text.text = ''
        self.ids.create_desc_text.text = ''
        self.ids.link_contacto.text = ''
        self.ids.create_tag_text.text = ''
        self.ids.btn_crear.text =  "Crear"
        self.lobby = None
