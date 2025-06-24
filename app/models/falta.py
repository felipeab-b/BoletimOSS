from .registro_academico import RegistroAcademico

class Falta(RegistroAcademico):
    def __init__(self, quantidade, limite):
        self._quantidade = quantidade
        self._limite = limite

    def get_quantidade(self):
        return self._quantidade

    def exibir_detalhes(self):
        if self._limite == self._quantidade:
            return f"Faltas: {self._quantidade} || ANTENÇÃO! VOCÊ ATINGIU SEU LIMITE DE FALTAS" 
        else:
            return f"Faltas: {self._quantidade}"
    
