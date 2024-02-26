from .modelo_clases import NotificacionLobby, NotificacionUsuario, Usuario, Lobby, Miembro, sesion

def notif_usuario(usuario):
    """ 
    Obtiene todas las notificaciones del usuario y notificaciones de los lobbies suscriptos, ordenados
    """
    notif_usuario = sesion.query(NotificacionUsuario).filter(NotificacionUsuario.id_usuario == usuario.id).all()
    id_lobbies = [miembro.lobby.id for miembro in usuario.lobbies if miembro.rol in (Miembro.Rol.Admin, Miembro.Rol.Dueño)]
    notif_lobbies = sesion.query(NotificacionLobby).filter(NotificacionLobby.id_lobby.in_(id_lobbies)).all()
    notif = notif_usuario + notif_lobbies
    notif.sort(key=lambda x: x.fecha_creacion)
    return notif if notif else []

def notif_solicitud(lobby_id, mensaje,fecha):
    """
    crea la notificacion dando el id del lobby y el mensaje
    :type: lobby_id: int , mensaje: String
    """
    notification = NotificacionLobby(id_lobby=lobby_id, descripcion=mensaje,fecha_creacion=fecha)
    try:
        sesion.add(notification)
        sesion.commit()
    except:
        sesion.rollback()
    return notification

def notif_aceptado(usuario_id, mensaje,fecha):
    """
    crea una notificacion dado el id del usuario que
    la recibira y el mensaje
    :type: usuario_id: int , mensaje: String
    """
    notication = NotificacionUsuario(id_usuario=usuario_id, descripcion=mensaje,fecha_creacion=fecha)
    try:
        sesion.add(notication)
        sesion.commit()
    except:
        sesion.rollback()
    return notication