from .modelo_clases import Miembro, sesion

def buscar_id(id_usuario, id_lobby):
    return sesion.query(Miembro).get((id_usuario, id_lobby))

def aceptar(miembro):
    """
    Cambia el booleano aceptado de esta fila a true
    """
    regMem = buscar_id(miembro.id_usuario, miembro.id_lobby)
    regMem.id_usuario = miembro.id_usuario
    regMem.id_lobby = miembro.id_lobby
    regMem.rol = miembro.rol
    regMem.aceptado = True
    sesion.commit()
    return regMem

def fue_aceptado(id_lobby, id_usuario):
    """
    Devuelve el valor aceptado de la fila miembro dados
    el id del usuario y el del lobby
    """
    member = sesion.query(Miembro).get((id_usuario, id_lobby))
    return member.aceptado
