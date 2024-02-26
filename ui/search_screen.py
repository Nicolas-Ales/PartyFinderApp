from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.accordion import AccordionItem
from kivy.uix.screenmanager import Screen

from ui.screen_names import Screens
from ui.custom_widget import ConfirmPopup, ImageButton

from negocio import datos_lobby, datos_notificaciones, datos_miembro
from negocio.modelo_clases import Lobby, Miembro, Etiqueta

class SearchScreen(Screen):
    lobby_list_acc = ObjectProperty()

    def __init__(self, *args, **kwargs):
        Builder.load_file("ui/kv/search.kv")
        super().__init__(*args, **kwargs)
        self.name = Screens.Search.value

    def buscar(self):
        self.lobby_list_acc.clear_widgets()
        if self.ids.spinner.text == 'Etiqueta':
            lobbys = datos_lobby.buscar_etiqueta(self.ids.busqueda.text)
        if self.ids.spinner.text == 'Nombre':
            lobbys = datos_lobby.buscar_nombre_like(self.ids.busqueda.text)
        if self.ids.spinner.text == 'Descripcion':
            lobbys = datos_lobby.buscar_descripcion(self.ids.busqueda.text)

        for lobby in lobbys:
            miembros = datos_lobby.cantidad_miembros(lobby)
            owner = datos_lobby.get_owner(lobby)
            lobby_detail = LobbyDetailS()
            lobby_detail.cargar_datos(lobby, miembros, owner)
            self.lobby_list_acc.add_widget(lobby_detail)

class LobbyDetailS(AccordionItem):

    description_label = ObjectProperty()
    request_icon = ObjectProperty()
    creador_label = ObjectProperty()

    def __init__(self, **kwargs):
        super(LobbyDetailS, self).__init__(**kwargs)
        self.request_popup = ConfirmPopup(title='Solicitud de Membresia')

    def cargar_datos(self, lobby, miembros, owner):
        self.lobby = lobby
        self.title = lobby.nombre
        self.description_label.text = lobby.descripcion
        self.ids.cant_miembros.text = "Cantidad de miembros: " + str(miembros)
        self.creador_label.text = "Dueño: " + owner.nombre
        if datos_lobby.pertenece(self.lobby.id, App.get_running_app().usuario_actual.id):
            self.ids.request_icon.disabled = True
            if datos_miembro.fue_aceptado(self.lobby.id, App.get_running_app().usuario_actual.id):
                self.ids.request_icon.source = 'res/account-check.png'
            else:
                self.ids.request_icon.source = 'res/account-pending.png'

    def request(self):
        usuario_actual = App.get_running_app().usuario_actual
        datos_lobby.solicitar_membresia(self.lobby, usuario_actual)
        mensaje = 'El usuario {0} a solicitado unirse a {1}.'.format(usuario_actual.nombre, self.lobby.nombre)
        fecha = datetime.now()
        datos_notificaciones.notif_solicitud(self.lobby.id, mensaje, fecha)
        self.request_popup = ConfirmPopup(message='Solicitaste Unirte a {0}'.format(self.lobby.nombre))
        self.request_popup.open()
