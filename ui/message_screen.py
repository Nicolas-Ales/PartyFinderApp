from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.accordion import AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp

from ui.screen_names import Screens
from ui.custom_widget import ConfirmPopup, YesNoPopup, ImageButton


from negocio.modelo_clases import Lobby, Usuario, Miembro
import negocio.datos_lobby as datos_lobby
import negocio.datos_miembro as datos_miembro

class MessageScreen(Screen):

    lobby_list_acc = ObjectProperty()

    def __init__(self, *args, **kwargs):
        Builder.load_file("ui/kv/message.kv")
        super().__init__(*args, **kwargs)
        self.name = Screens.Message.value
    
    def on_pre_enter(self):
        self.update_content()

    def update_content(self):
        self.lobby_list_acc.clear_widgets()
        membrecia_lobbies = App.get_running_app().usuario_actual.lobbies
        if membrecia_lobbies:
            for miembro in membrecia_lobbies:
                lobby_detail = LobbyDetail(self, miembro)
                self.lobby_list_acc.add_widget(lobby_detail)

    def on_btn_create_lobby_release(self):
        App.get_running_app().go_screen(Screens.LobbyCreation.value)
    
    def abandonar_lobby(self, miembro):
        print('Borrar miembro {0}'.format(miembro))

    def borrar_lobby(self, lobby):
        print('Borrar lobby {0}.'.format(lobby.nombre))

class LobbyDetail(AccordionItem):

    miembro = ObjectProperty()

    description_label = ObjectProperty()
    accepted_icon = ObjectProperty()
    members_icon = ObjectProperty()
    leave_icon = ObjectProperty()
    delete_icon = ObjectProperty()
    edit_icon = ObjectProperty()

    def __init__(self, parent_screen, miembro, **kwargs):
        super(LobbyDetail, self).__init__(**kwargs)
        self.parent_screen = parent_screen

        self.accepted_popup = ConfirmPopup(title='Estado de Membresia')
        self.accepted_icon.bind(on_press=self.accepted_popup.open)

        self.members_icon.bind(on_press=lambda _: App.get_running_app().go_screen(Screens.Members.value, lobby=self.miembro.lobby))

        self.leave_popup = YesNoPopup(title='Abandonar Lobby', message='¿Esta seguro que desea abandonar el lobby?')
        self.leave_popup.yes_callback = lambda: parent_screen.abandonar_lobby(self.miembro.lobby)
        self.leave_icon.bind(on_press=self.leave_popup.open)

        self.delete_popup = YesNoPopup(title='Borrar Lobby', message='¿Esta seguro que desea borrar el lobby? Esta acción no se puede deshacer.')
        self.delete_popup.yes_callback = lambda: parent_screen.borrar_lobby(self.miembro.lobby)
        self.delete_icon.bind(on_press=self.delete_popup.open)

        self.edit_icon.bind(on_press=lambda _: App.get_running_app().go_screen(Screens.LobbyCreation.value, lobby=self.miembro.lobby))

        self.miembro = miembro
    
    def autorizar_acciones(self):
        usuario_actual = App.get_running_app().usuario_actual
        rol_actual = datos_miembro.buscar_id(usuario_actual.id, self.miembro.id_lobby).rol
        
        if rol_actual == Miembro.Rol.Miembro:
            self.leave_icon.disabled = False
            self.delete_icon.disabled = True
            self.edit_icon.disabled = True
        
        if rol_actual == Miembro.Rol.Admin:
            self.leave_icon.disabled = False
            self.delete_icon.disabled = True
            self.edit_icon.disabled = False
        
        if rol_actual == Miembro.Rol.Dueño:
            self.leave_icon.disabled = True
            self.delete_icon.disabled = False
            self.edit_icon.disabled = False

    def on_miembro(self, instance, value):
        self.title = value.lobby.nombre
        self.description_label.text = value.lobby.descripcion
        if value.aceptado:
            self.ids.contacto_label.text = value.lobby.contacto
            self.ids.contacto_label.opacity = 1
            self.accepted_icon.source = 'res/account-check.png'
            self.accepted_popup.message = 'Has sido aceptado en el lobby!'
        else:
            self.ids.contacto_label.opacity = 0
            self.accepted_icon.source = 'res/account-pending.png'
            self.accepted_popup.message = 'Tu solicitud para entrar aún no ha sido aceptada.'
        self.autorizar_acciones()
