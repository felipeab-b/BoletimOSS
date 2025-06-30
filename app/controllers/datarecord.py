import json
import os
from app.models.usuario import Usuario
from app.models.materia import Materia
from app.models.nota import Nota
from app.models.avaliacao import Avaliacao

class DataRecord:
    def __init__(self):
        self.usuarios = []
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db", "usuarios.json")

        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                for u in dados:
                    usuario = Usuario(u["nome"], u["matricula"], u.get("curso", "Não informado"))
                    for m in u.get("materias", []):
                        materia = Materia(m["codigo"], m["nome"], m["horas"])
                        materia.atualizar_faltas(m["faltas"])
                        for n in m.get("notas", []):
                            materia.adicionar_nota(Nota(n["descricao"], n["valor"]))
                        for a in m.get("avaliacoes", []):
                            materia.adicionar_avaliacao(Avaliacao(a["comentario"]))
                        usuario.adicionar_materia(materia)
                    self.usuarios.append(usuario)
        else:
            # Cria um usuário padrão se o JSON não existir
            self.usuarios.append(Usuario("Visitante", "000000"))
            self.salvar()

    def salvar(self):
        dados = []
        for u in self.usuarios:
            usuario_dict = {
                "nome": u.get_nome(),
                "matricula": u.get_matricula(),
                "curso": u.get_curso(),
                "materias": []
            }
            for m in u.listar_materias():
                materia_dict = {
                    "codigo": m.get_codigo(),
                    "nome": m.get_nome(),
                    "horas": m.get_horas(),
                    "faltas": m.get_faltas(),
                    "notas": [{"descricao": n.get_descricao(), "valor": n.get_valor()} for n in m._notas],
                    "avaliacoes": [{"comentario": a.get_comentario()} for a in m._avaliacoes]
                }
                usuario_dict["materias"].append(materia_dict)
            dados.append(usuario_dict)

        with open(self.db_path, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def work_with_parameter(self, parametro):
        clean_param = ''.join(filter(str.isdigit, str(parametro)))
        
        for user in self.usuarios:
            user_matricula = ''.join(filter(str.isdigit, user.get_matricula()))
            if user_matricula == clean_param:
                return user
        return None

    def listar_usuarios(self):
        return self.usuarios

    def adicionar_usuario(self, usuario):
        self.usuarios.append(usuario)
        self.salvar()
