from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'minimum_width', '250')
Config.set('graphics', 'minimum_height', '250')
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.graphics import Rectangle
from kivy.animation import Animation
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

import ui.custom_widget
from ui import MainScreen, MessageScreen, SearchScreen, LoginScreen, LobbyCreationScreen, ProfileScreen, MembersScreen
from ui.custom_widget import ImageButton
from ui.screen_names import Screens

from negocio.modelo_clases import inicializar_bd

class RootLayout(BoxLayout):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.orientation = "vertical"

        # Action bar (top)
        self.actionbar = ActionBar()
        self.actionview = ActionView()
        self.actionview.action_previous = ActionPrevious(with_previous=False, app_icon="res/appicon.png")
        actionbtn = ActionButton(text="Perfil", icon="res/profile.png", on_release=lambda _: App.get_running_app().go_screen(Screens.Profile.value))
        self.actionview.add_widget(actionbtn)
        actionbtn = ActionButton(text="Ajustes", icon="res/settings.png")
        self.actionview.add_widget(actionbtn)
        self.actionbar.add_widget(self.actionview)

        # Navigation bar (bottom)
        self.navigationbar = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48), padding=dp(8))
        navbtn = ImageButton(source="res/search.png")
        navbtn.on_press = lambda: App.get_running_app().go_screen(Screens.Search.value)
        self.navigationbar.add_widget(navbtn)
        navbtn = ImageButton(source="res/home.png")
        navbtn.on_press = lambda: App.get_running_app().go_screen(Screens.Main.value)
        self.navigationbar.add_widget(navbtn)
        navbtn = ImageButton(source="res/message.png")
        navbtn.on_press = lambda: App.get_running_app().go_screen(Screens.Message.value)
        self.navigationbar.add_widget(navbtn)

        # Screen manager
        self.screenmanager = ScreenManager()
        self._load_screen_manager()
        self.add_widget(self.screenmanager)

    def show_bars(self, show):
        if show:
            self.add_widget(self.actionbar, 1)
            self.add_widget(self.navigationbar)
        else:
            self.remove_widget(self.actionbar)
            self.remove_widget(self.navigationbar)
    
    def is_bar_visible(self):
        return self.actionbar in self.children and self.navigationbar in self.children

    def _load_screen_manager(self):
        """ Carga las pantallas de la aplicación en el screenmanager. """
        # Las transiciones se realizan respetando el orden en el que fueron agregadas las pantallas
        self.screenmanager.add_widget(LoginScreen())
        self.screenmanager.add_widget(SearchScreen())
        self.screenmanager.add_widget(MainScreen())
        self.screenmanager.add_widget(MessageScreen())
        self.screenmanager.add_widget(LobbyCreationScreen())
        self.screenmanager.add_widget(ProfileScreen())
        self.screenmanager.add_widget(MembersScreen())
        self.screenmanager.current = Screens.Login.value
        self.actionview.action_previous.title = self.screenmanager.current_screen.title

class FinderApp(App):

    usuario_actual = ObjectProperty(None, allownone=True)

    def build(self):
        return RootLayout()

    def go_screen(self, screen, **kwargs):
        """ Abre una nueva ventana a través del screenmanager. """
        if self.root.screenmanager.current == screen:
            return

        if screen == Screens.Login.value and self.root.is_bar_visible():
            self.root.show_bars(False)
        elif screen != Screens.Login.value and not self.root.is_bar_visible():
            self.root.show_bars(True)

        if screen in (Screens.Search.value, Screens.Main.value, Screens.Message.value) and \
            self.root.screenmanager.current in (Screens.Search.value, Screens.Main.value, Screens.Message.value):
            old_pos = self.root.screenmanager.screen_names.index(self.root.screenmanager.current)
            new_pos = self.root.screenmanager.screen_names.index(screen)
            self.root.screenmanager.transition.direction = "left" if old_pos < new_pos else "right"
        else:
            self.root.screenmanager.transition.direction = "down"

        for kw, arg in kwargs.items():
            setattr(self.root.screenmanager.get_screen(screen), kw, arg)

        self.root.screenmanager.current = screen
        self.root.actionview.action_previous.title = self.root.screenmanager.current_screen.title

if __name__ == "__main__":
    inicializar_bd()
    FinderApp().run()
