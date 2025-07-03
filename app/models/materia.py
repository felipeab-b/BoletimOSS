class Materia:
    def __init__(self, codigo, nome, horas):
        self._codigo = codigo
        self._horas = horas
        self._nome = nome
        self._faltas = 0
        self._notas = []
        self._avaliacoes = []

    def atualizar_informacoes(self, nome=None, horas=None, faltas=None):
        if nome:
            self._nome = nome
        if horas is not None:
            self._horas = horas
        if faltas is not None:
            self._faltas = faltas

    def remover_nota(self, descricao):
        for i, nota in enumerate(self._notas):
            if nota.get_descricao() == descricao:
                del self._notas[i]
                return True
        return False
    
    def remover_avaliacao(self, comentario):
        for i, avaliacao in enumerate(self._avaliacoes):
            if avaliacao.get_comentario() == comentario:
                del self._avaliacoes[i]
                return True
        return False

    #NOTAS-------------
    def adicionar_nota(self, nota):
        self._notas.append(nota)

    def calcular_media(self):
        if not self._notas:
            return 0
        return sum(n.get_valor() for n in self._notas) / len(self._notas)

    def listar_notas(self):
        return self._notas
    
    #FALTAS------------
    def atualizar_faltas(self, faltas):
        self._faltas = max(0, faltas)
        return self._faltas

    def limite_faltas(self):
        return int((self._horas * 0.25)/2)
    
    def get_faltas(self):
        return self._faltas
    
    #AVALIACOES---------
    def adicionar_avaliacao(self, avaliacao):
        self._avaliacoes.append(avaliacao)

    def listar_avaliacoes(self):
        return self._avaliacoes
    
    #GETTERS-------
    def get_horas(self):
        return self._horas
    
    def get_nome(self):
        return self._nome
    
    def get_codigo(self):
        return self._codigo
