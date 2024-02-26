from .main_screen import MainScreen
from .search_screen import SearchScreen
from .message_screen import MessageScreen
from .login_screen import LoginScreen
from .lobbycreation_screen import LobbyCreationScreen
from .profile_screen import ProfileScreen
from .members_screen import MembersScreen

# Pasos para crear una nueva pantalla:
# 1- Crear .py con la clase.
# 2- Crear .kv con el layout.
# 3- Registrarlo en el ui.__init__.py (este archivo).
# 4- Registrarlo en el método de carga de screenmanager.
