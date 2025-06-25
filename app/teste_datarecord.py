from app.controllers.datarecord import DataRecord
from app.models.usuario import Usuario
from app.models.materia import Materia
from app.models.nota import Nota
from app.models.avaliacao import Avaliacao

# Criar um usuário novo
usuario = Usuario("João da Silva", "20240001")

# Criar uma matéria
materia = Materia("HIS101", "História do Brasil", 60)
materia.atualizar_faltas(3)
materia.adicionar_nota(Nota("Prova 1", 6.0))
materia.adicionar_nota(Nota("Prova 2", 8.0))
materia.adicionar_avaliacao(Avaliacao("Bom professor, conteúdo claro."))

# Adicionar matéria ao usuário
usuario.adicionar_materia(materia)

# Inicializar o banco de dados
db = DataRecord()

# Adicionar usuário ao banco
db.adicionar_usuario(usuario)

# Carregar os dados de volta e mostrar
print("Usuários no sistema:")
for i, u in enumerate(db.listar_usuarios()):
    print(f"[{i}] Nome: {u.get_nome()} | Matrícula: {u.get_matricula()}")
    for m in u.listar_materias():
        print(f"  Matéria: {m.get_nome()} - Código: {m.get_codigo()}")
        print(f"    Faltas: {m.get_faltas()}/{m.limite_faltas()}")
        print(f"    Média: {m.calcular_media():.2f}")
        print(f"    Avaliações: {m.listar_avaliacoes()}")
