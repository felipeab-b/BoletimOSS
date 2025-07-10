class Usuario:
    def __init__(self, nome, matricula,curso="Não Informado", password=None):
        self._nome = nome
        self._matricula = matricula
        self._curso = curso
        self._materias = []
        self._password = password  

    def get_nome(self):
        return self._nome

    def get_matricula(self):
        return self._matricula

    def get_curso(self):
        return self._curso

    def get_password(self):
        return self._password

    def adicionar_materia(self, materia):
        self._materias.append(materia)

    def remover_materia(self, codigo):
        for i, materia in enumerate(self._materias):
            if materia.get_codigo() == codigo:
                del self._materias[i]
                return True
        return False

    def encontrar_materia(self, codigo):
        for materia in self._materias:
            if materia.get_codigo() == codigo:
                return materia
        return None

    def listar_materias(self):
        return self._materias if self._materias else []

    def get_nome(self):
        return self._nome

    def get_matricula(self):
        return self._matricula
    
    def get_curso(self):
        return self._curso
