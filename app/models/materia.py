
from app.models.nota import Nota
from app.models.avaliacao import Avaliacao

class Materia:
    def __init__(self, codigo, nome, horas):
        self._codigo = codigo
        self._horas = horas
        self._nome = nome
        self._faltas = 0
        self._notas = []
        self._avaliacoes = []

    #NOTAS-------------
    def adicionar_nota(self, nota):
        self._notas.append(nota)

    def calcular_media(self):
        if not self._notas:
            return 0
        return sum(n.get_valor() for n in self._notas) / len(self._notas)

    def listar_notas(self):
        return [n.render() for n in self._notas]
    
    #FALTAS------------
    def atualizar_faltas(self, faltas):
        self._faltas = faltas

    def limite_faltas(self):
        return int((self._horas * 0.25)/2)
    
    def get_faltas(self):
        return self._faltas
    
    #AVALIACOES---------
    def adicionar_avaliacao(self, avaliacao):
        self._avaliacoes.append(avaliacao)

    def listar_avaliacoes(self):
        return [a.render() for a in self._avaliacoes]
    
    #GETTERS-------
    def get_horas(self):
        return self._horas
    
    def get_nome(self):
        return self._nome
    
    def get_codigo(self):
        return self._codigo
