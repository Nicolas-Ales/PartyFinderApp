import enum

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, DateTime, Enum, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
CONNECTION_STRING = 'sqlite:///base_datos.db'


def crear_conexion():
    """ Establece conexión con la base de datos. """
    return create_engine(CONNECTION_STRING)


def inicializar_bd():
    """ Carga la base de datos con todas las tablas. """
    Base.metadata.create_all(crear_conexion())


_Session = sessionmaker(bind=crear_conexion())
sesion = _Session()

etiquetas_lobbies = Table('etiqueta_lobby', Base.metadata,
                          Column('id_etiqueta', Integer, ForeignKey('etiquetas.id')),
                          Column('id_lobby', Integer, ForeignKey('lobbies.id')))

usuarios_etiquetas = Table('usuario_etiqueta', Base.metadata,
                           Column('id_usuario', Integer, ForeignKey('usuarios.id')),
                           Column('id_etiquetas', Integer, ForeignKey('etiquetas.id')))


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    nombre = Column(String, unique=True, nullable=False)
    pwd_hash = Column(String, nullable=False)
    mail = Column(String, unique=True, nullable=False)
    fecha_nacimiento = Column(Date)
    honor = Column(Integer)
    lobbies = relationship('Miembro', back_populates='usuario')
    favoritos = relationship('Etiqueta', secondary=usuarios_etiquetas)
    notificaciones = relationship('NotificacionUsuario')


class Lobby(Base):
    __tablename__ = 'lobbies'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_creacion = Column(DateTime, nullable=False)
    contacto = Column(String)
    jugadores = relationship('Miembro', back_populates='lobby')
    etiquetas = relationship('Etiqueta', secondary=etiquetas_lobbies, back_populates='lobbies')
    notificaciones = relationship('NotificacionLobby')


class Miembro(Base):
    class Rol(enum.Enum):
        Dueño = 'Dueño'
        Admin = 'Administrador'
        Miembro = 'Miembro'

    __tablename__ = 'miembros'

    id_usuario = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    id_lobby = Column(Integer, ForeignKey('lobbies.id'), primary_key=True)
    rol = Column(Enum(Rol))
    aceptado = Column(Boolean, nullable=False)
    usuario = relationship('Usuario', back_populates='lobbies')
    lobby = relationship('Lobby', back_populates='jugadores')


class Etiqueta(Base):
    __tablename__ = 'etiquetas'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    descripcion = Column(String, nullable=False)
    lobbies = relationship('Lobby', secondary=etiquetas_lobbies, back_populates='etiquetas')


class NotificacionLobby(Base):
    """
    notificaciones de que solicitudes de ingreso al lobby, para dueños y admin
    notificaciones grupales para todos los moembros (implementable a futuro)
    """

    __tablename__ = 'notificaciones_lobby'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    id_lobby = Column(Integer, ForeignKey('lobbies.id'))
    descripcion = Column(String)
    fecha_creacion = Column(DateTime, nullable=False)


class NotificacionUsuario(Base):
    """
    notificaciones de que fuiste aceptado en un lobby
    """

    __tablename__ = 'notificaciones_usuario'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    descripcion = Column(String)
    fecha_creacion = Column(DateTime, nullable=False)
