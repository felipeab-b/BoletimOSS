from .materia import Materia

class Usuario:
    def __init__(self, nome, usuario, senha):
        self._nome = nome
        self._usuario = usuario
        self._senha = senha
        self._materias = []

    def adicionar_materia(self, materia):
        self._materias.append(materia)

    def listar_materias(self):
        return self._materias
