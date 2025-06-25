
from app.models.elemento_boletim import ElementoBoletim

class Avaliacao(ElementoBoletim):
    def __init__(self, comentario):
        self._comentario = comentario

    def get_comentario(self):
        return self._comentario

    def render(self):
        return f"Avaliação: \"{self._comentario}\""
