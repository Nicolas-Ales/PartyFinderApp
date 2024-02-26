from .modelo_clases import Usuario, Lobby, Etiqueta, sesion

def find_or_create(descripcion):
        """
        Busca una etiqueta por la descripcion. En caso de no encontrarla crea una con esa descripción.
        :type descripcion: String
        :rtype: Etiqueta
        """
        etiqueta = sesion.query(Etiqueta).filter_by(descripcion=descripcion).one_or_none()
        if etiqueta is None:
            etiqueta = Etiqueta(descripcion=descripcion)
            try:
                sesion.add(etiqueta)
                sesion.commit()
            except:
                sesion.rollback()
        return etiqueta
