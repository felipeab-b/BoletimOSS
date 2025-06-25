from app.models.materia import Materia

class Usuario:
    def __init__(self, nome, matricula):
        self._nome = nome
        self._matricula = matricula
        self._materias = []

    def adicionar_materia(self, materia):
        self._materias.append(materia)

    def listar_materias(self):
        return self._materias

    def get_nome(self):
        return self._nome

    def get_matricula(self):
        return self._matricula
