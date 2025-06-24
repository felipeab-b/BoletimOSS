from .registro_academico import RegistroAcademico

class Avaliacao(RegistroAcademico):
    def __init__(self, comentario):
        self._comentario = comentario

    def exibir_detalhes(self):
        return f"Avaliação: {self._comentario}"
