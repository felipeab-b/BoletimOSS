from .registro_academico import RegistroAcademico

class Nota(RegistroAcademico):
    def __init__(self, descricao, valor):
        self._descricao = descricao
        self._valor = valor

    def get_valor(self):
        return self._valor

    def exibir_detalhes(self):
        return f"Nota: {self._descricao} - Valor: {self._valor}"

