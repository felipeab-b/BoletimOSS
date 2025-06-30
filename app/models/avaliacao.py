class Avaliacao():
    def __init__(self, comentario):
        self._comentario = comentario

    def get_comentario(self):
        return self._comentario

    def render(self):
        return f"Avaliação: \"{self._comentario}\""

    def __str__(self):
        return f"\"{self._comentario}\""