from .modelo_clases import Usuario, Lobby, Etiqueta, etiquetas_lobbies, usuarios_etiquetas, Miembro, sesion

def buscar_nombre_like(nombre):
    """
    Devuelve una lista de lobbies que coincidan aproximadamente con el nombre dado.
    :type nombre: String
    :rtype: List[Lobby]
    """
    return sesion.query(Lobby).filter(Lobby.nombre.like("%"+nombre+"%")).all()

def buscar_nombre_exacto(nombre):
    """
    Devuelve un lobby que coincida exactamente con el nombre dado.
    :type nombre: String
    :rtype: List[Lobby]
    """
    return sesion.query(Lobby).filter_by(nombre=nombre).one_or_none()

def buscar_descripcion(desc):
    """
    Devuelve una lista de lobbies que coincidan aproximadamente con la descripción dada.
    :type desc: String
    :rtype: List[Lobby]
    """
    return sesion.query(Lobby).filter(Lobby.descripcion.like("%"+desc+"%")).all()

def buscar_etiqueta(etiqueta):
    """
    Devuelve una lista de lobbies que coincidan aproximadamente con la etiqueta dada.
    :type etiqueta: String
    :rtype: List[Lobby]
    """
    return sesion.query(Lobby).join(etiquetas_lobbies).join(Etiqueta).filter(Etiqueta.descripcion.like("%"+etiqueta+"%")).all()

def cantidad_miembros(lobby):
    """
    Dado un Lobby devuelve la cantidad de miembros aceptados que tiene
    :type lobby: Lobby
    :rtype: Int
    """
    return sesion.query(Lobby).join(Miembro).filter(Lobby.id == lobby.id, Miembro.aceptado == True).count()

def get_owner(lobby):
    """
    dado un lobby te devuelve el usuario con el rol dueño
    :type lobby: Lobby
    :rtype: Usuario
    """
    owner = sesion.query(Usuario).join(Miembro).\
        filter(Miembro.id_lobby == lobby.id,\
             Miembro.rol == "Dueño").one()
    return owner

def alta(lobby):
    """
    Agrega los datos del lobby a la transacción y la confirma.
    :type lobby: Lobby
    :rtype: Lobby
    """
    try:
        sesion.add(lobby)
        sesion.commit()
    except:
        sesion.rollback()
    return lobby

def modificar(lobby):
    """
    modifica el lobby en la base de datos
    """
    regLobby = sesion.query(Lobby).get(lobby.id)
    regLobby.nombre = lobby.nombre
    regLobby.descripcion = lobby.descripcion
    regLobby.contacto = lobby.contacto
    regLobby.etiquetas = lobby.etiquetas
    sesion.commit
    return regLobby

def buscar_id(lobby_id):
    """
    Devuelve un lobby dado su id
    Si no lo encuentra tira error
    :type lobby_id: int
    :rtype: Lobby
    """
    return sesion.query(Lobby).filter(Lobby.id == lobby_id).one()

def solicitar_membresia(lobby, usuario):
    """
    Crea una relacion Miembro entre el usuario y el lobby
    con rol Miembro y aceptado false
    """
    membresia = Miembro(id_usuario=usuario.id, id_lobby=lobby.id, rol='Miembro', aceptado=False)
    try:
        sesion.add(membresia)
        sesion.commit()
    except:
        sesion.rollback()
    return membresia

def pertenece(id_lobby, id_usuario):
    return not sesion.query(Miembro).filter(Miembro.id_lobby == id_lobby, Miembro.id_usuario == id_usuario).first() is None

def aceptado(id_lobby, id_usuario):
    return sesion.query(Miembro).filter(Miembro.id_lobby == id_lobby, Miembro.id_usuario == id_usuario).first().aceptado
