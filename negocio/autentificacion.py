from passlib.hash import pbkdf2_sha256
import negocio.datos_usuario as datos_usuario
from negocio.modelo_clases import Usuario

def generar_hash(email, contraseña):
    return pbkdf2_sha256.hash(email+contraseña)

def verificar_usuario(email, contraseña):
    usuario = datos_usuario.buscar_mail(email) 
    if (not usuario is None) and pbkdf2_sha256.verify(email+contraseña, usuario.pwd_hash):
        return usuario
    else: 
        return None