from app.models.usuario import Usuario
from app.models.materia import Materia
from app.models.nota import Nota
from app.models.avaliacao import Avaliacao

# 1. Criar usuários
joao = Usuario("João", "20231234")
maria = Usuario("Maria", "20239876")

# 2. Criar matérias
poo_joao = Materia("CIC0201", "POO com Python", 60)
calculo_maria = Materia("MAT0101", "Cálculo 1", 80)

# 3. Adicionar faltas
poo_joao.atualizar_faltas(10)
calculo_maria.atualizar_faltas(25)

# 4. Adicionar notas
poo_joao.adicionar_nota(Nota("Prova 1", 7.0))
poo_joao.adicionar_nota(Nota("Prova 2", 8.5))

calculo_maria.adicionar_nota(Nota("Prova 1", 6.0))
calculo_maria.adicionar_nota(Nota("Prova 2", 6.5))

# 5. Adicionar avaliações
poo_joao.adicionar_avaliacao(Avaliacao("Excelente disciplina!"))
calculo_maria.adicionar_avaliacao(Avaliacao("Professor muito exigente."))

# 6. Associar as matérias aos usuários
joao.adicionar_materia(poo_joao)
maria.adicionar_materia(calculo_maria)

# 7. Exibir boletim de cada aluno
for usuario in [joao, maria]:
    print(f"\nAluno: {usuario.get_nome()} ({usuario.get_matricula()})")
    for materia in usuario.listar_materias():
        print(f"\nMatéria: {materia.get_codigo()} - {materia.get_nome()}")
        print(f"Horas: {materia.get_horas()}")
        print(f"Faltas: {materia.get_faltas()} / Limite: {materia.limite_faltas()}")
        print("Notas:")
        for nota in materia.listar_notas():
            print(" -", nota)
        print("Média final:", materia.calcular_media())
        print("Avaliações:")
        for av in materia.listar_avaliacoes():
            print(" -", av)
