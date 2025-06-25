from app.models.elemento_boletim import ElementoBoletim

class Nota(ElementoBoletim):
    def __init__(self, descricao, valor):
        self._descricao = descricao
        self._valor = valor

    def get_descricao(self):
        return self._descricao

    def get_valor(self):
        return self._valor

    def render(self):
        return f"Nota {self._descricao} = {self._valor}"
