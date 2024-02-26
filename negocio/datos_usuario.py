from .modelo_clases import Usuario, Lobby, Etiqueta, sesion

def buscar_mail(mail):
    """
    Devuelve la instancia del usuario, dando su mail.
    :type mail: String
    :rtype: Usuario
    """
    return sesion.query(Usuario).filter_by(mail=mail).one_or_none()

def alta(usuario):
    """
    Agrega los datos del usuario a la transacción y la confirma.
    :type usuario: Usuario
    :rtype: Usuario
    """
    try:
        sesion.add(usuario)
        sesion.commit()
    except:
        sesion.rollback()
    return usuario

def modificar(usuario):
    """
    Modifica los datos del usuario
    id, nombre, mail y contraseña
    """
    regUsuario = sesion.query(Usuario).filter_by(id=usuario.id).one()
    regUsuario.id = usuario.id
    regUsuario.pwd_hash = usuario.pwd_hash
    regUsuario.mail = usuario.mail
    regUsuario.nombre = usuario.nombre
    sesion.commit()
    return regUsuario

def buscar_nombre(nombre):
    """
    Devuelve la instancia del usuario, dando su nombre.
    :type mail: String
    :rtype: Usuario
    """
    return sesion.query(Usuario).filter_by(nombre=nombre).one_or_none()
