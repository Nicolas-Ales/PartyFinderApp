from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.accordion import AccordionItem
from kivy.uix.screenmanager import Screen

from ui.custom_widget import ConfirmPopup
from ui.screen_names import Screens
from negocio.modelo_clases import Miembro, Lobby
from negocio import datos_miembro, datos_notificaciones


class MembersScreen(Screen):
    lobby = ObjectProperty()
    member_list_acc = ObjectProperty()

    def __init__(self, *args, **kwargs):
        Builder.load_file("ui/kv/members.kv")
        super().__init__(*args, **kwargs)
        self.name = Screens.Members.value

    def on_pre_enter(self):
        self.actualizar_lista()

    def actualizar_lista(self):
        self.member_list_acc.clear_widgets()
        for miembro in self.lobby.jugadores:
            member_detail = MemberDetail(self, miembro)
            self.member_list_acc.add_widget(member_detail)


class MemberDetail(AccordionItem):

    miembro = ObjectProperty()

    def __init__(self, parent_screen, miembro, **kwargs):
        super().__init__(**kwargs)
        self.parent_screen = parent_screen
        self.miembro = miembro
        App.get_running_app().bind(usuario_actual=self.autorizar_acciones)

    def autorizar_acciones(self, instance, value):
        if not value:
            return

        rol_actual = datos_miembro.buscar_id(value.id, self.miembro.id_lobby).rol

        if rol_actual == Miembro.Rol.Miembro:
            self.ids.accept_icon.disabled = True
            self.ids.delete_icon.disabled = True
            self.ids.ascend_icon.disabled = True
            self.ids.descend_icon.disabled = True
            return

        if rol_actual == Miembro.Rol.Admin and self.miembro.rol != Miembro.Rol.Miembro:
            self.ids.delete_icon.disabled = True
            self.ids.ascend_icon.disabled = True
            self.ids.descend_icon.disabled = True
            return

        if self.miembro.rol == Miembro.Rol.Dueño:
            self.ids.delete_icon.disabled = True
            self.ids.ascend_icon.disabled = True
            self.ids.descend_icon.disabled = True

    def on_miembro(self, instance, value):
        self.title = value.usuario.nombre
        self.ids.accept_icon.disabled = value.aceptado
        self.ids.delete_icon.disabled = False
        self.ids.ascend_icon.disabled = value.rol == Miembro.Rol.Dueño
        self.ids.descend_icon.disabled = value.rol == Miembro.Rol.Miembro
        self.autorizar_acciones(self, App.get_running_app().usuario_actual)

    def aceptar_miembro(self):
        datos_miembro.aceptar(self.miembro)
        mensaje = "¡Felicidades! Fuiste aceptado en {0}".format(self.miembro.lobby.nombre)
        datos_notificaciones.notif_aceptado(self.miembro.id_usuario, mensaje, datetime.now())
        self.popup("Usuario aceptado en el lobby")
        self.parent_screen.actualizar_lista()

    def borrar_miembro(self):
        # TODO: Borrar miembro y actualizar lista de miembros.
        # Para actualizar la lista se puede llamar al metodo self.parent_screen.actualizar_lista()
        pass

    def ascender_miembro(self):
        # TODO: Ascender rol del miembro y actualizar lista de miembros.
        # Si se asciende de admin a dueño, entonces el dueño se debe descender a admin.
        pass

    def descender_miembro(self):
        # TODO: Descender rol del miembro y actualizar lista de miembros.
        pass

    def popup(self, message):
        popup = ConfirmPopup(title='Usuario Aceptado', message=message)
        popup.open()
