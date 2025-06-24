from .nota import Nota
from .falta import Falta
from .avaliacao import Avaliacao

class Materia:
    def __init__(self, codigo, nome, horas):
        self._codigo = codigo
        self._horas = horas
        self._nome = nome
        self._registros = []  # Polimorfismo: lista de objetos RegistroAcademico (Nota, Falta, Avaliacao)

    def adicionar_registro(self, registro):
        self._registros.append(registro)

    def listar_registros(self):
        return [r.exibir_detalhes() for r in self._registros]

    def calcular_media(self):
        notas = [r.get_valor() for r in self._registros if isinstance(r, Nota)]
        if notas:
            return sum(notas) / len(notas)
        return 0

    def total_faltas(self):
        faltas = [r.get_quantidade() for r in self._registros if isinstance(r, Falta)]
        return sum(faltas)
