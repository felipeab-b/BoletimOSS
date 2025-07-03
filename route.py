from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response, post
from app.models.materia import Materia
from app.models.nota import Nota
from app.models.avaliacao import Avaliacao


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/home', methods=['GET'])
def home():
    return ctl.render('home')

@app.route('/hub', method='GET')
def hub():
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    
    if user:
        return ctl.render('hub', usuario=user)
    else:
        redirect('/login')

@app.route('/login', method='GET')
def login_form():
    return ctl.render('login')

@app.route('/login', method='POST')
def login_action():
    matricula = request.forms.get('matricula')
    session_id, user = ctl.autenticate_user(matricula)
    
    if session_id:
        response.set_cookie('session_id', session_id)
        redirect('/hub')
    else:
        return "Matrícula inválida"

@app.route('/logout', method='POST')
def logout():
    session_id = request.get_cookie('session_id')
    if session_id and session_id in ctl.sessions:
        del ctl.sessions[session_id]
    response.delete_cookie('session_id')
    redirect('/home')

#----------------------------------------------------

@app.route('/materia/adicionar', method='GET')
def form_adicionar_materia():
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if user:
        return ctl.render('form_materia')
    else:
        redirect('/login')

@app.route('/materia/adicionar', method='POST')
def adicionar_materia():
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if not user:
        redirect('/login')
    
    codigo = request.forms.get('codigo')
    nome = request.forms.get('nome')
    horas = int(request.forms.get('horas'))
    
    nova_materia = Materia(codigo, nome, horas)
    user.adicionar_materia(nova_materia)
    ctl.models.salvar()
    
    redirect('/hub')

@app.route('/materia/<codigo>/editar', method='GET')
def form_editar_materia(codigo):
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if not user:
        redirect('/login')
    
    materia = user.encontrar_materia(codigo)
    if materia:
        return ctl.render('form_materia', materia=materia)
    else:
        redirect('/hub')

@app.route('/materia/<codigo>/editar', method='POST')
def editar_materia(codigo):
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if not user:
        redirect('/login')
    
    materia = user.encontrar_materia(codigo)
    if materia:
        nome = request.forms.get('nome')
        horas = int(request.forms.get('horas'))
        faltas = int(request.forms.get('faltas'))
        
        materia.atualizar_informacoes(nome=nome, horas=horas, faltas=faltas)
        ctl.models.salvar()
    
    redirect('/hub')

@app.route('/materia/<codigo>/excluir', method='POST')
def excluir_materia(codigo):
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if not user:
        redirect('/login')
    
    if user.remover_materia(codigo):
        ctl.models.salvar()
    
    redirect('/hub')

@app.route('/materia/<codigo>/nota/adicionar', method='POST')
def adicionar_nota(codigo):
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if not user:
        redirect('/login')
    
    materia = user.encontrar_materia(codigo)
    if materia:
        descricao = request.forms.get('descricao')
        valor = float(request.forms.get('valor'))
        
        materia.adicionar_nota(Nota(descricao, valor))
        ctl.models.salvar()
    
    redirect('/hub')

@app.route('/materia/<codigo>/avaliacao/adicionar', method='POST')
def adicionar_avaliacao(codigo):
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if not user:
        redirect('/login')
    
    materia = user.encontrar_materia(codigo)
    if materia:
        comentario = request.forms.get('comentario')
        
        materia.adicionar_avaliacao(Avaliacao(comentario))
        ctl.models.salvar()
    
    redirect('/hub')

@app.route('/materia/<codigo>/nota/<descricao>/excluir', method='POST')
def excluir_nota(codigo, descricao):
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if not user:
        redirect('/login')
    
    materia = user.encontrar_materia(codigo)
    if materia and materia.remover_nota(descricao):
        ctl.models.salvar()
    
    redirect('/hub')

@app.route('/materia/<codigo>/avaliacao/<comentario>/excluir', method='POST')
def excluir_avaliacao(codigo, comentario):
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if not user:
        redirect('/login')
    
    materia = user.encontrar_materia(codigo)
    if materia and materia.remover_avaliacao(comentario):
        ctl.models.salvar()
    
    redirect('/hub')

@app.post('/materia/<codigo>/faltas/adicionar')
def adicionar_falta(codigo):
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if not user:
        redirect('/login')
    
    materia = user.encontrar_materia(codigo)
    if materia:
        materia.atualizar_faltas(materia.get_faltas() + 1)
        ctl.models.salvar()
    
    redirect('/hub')

@app.post('/materia/<codigo>/faltas/remover')
def remover_falta(codigo):
    session_id = request.get_cookie('session_id')
    user = ctl.get_current_user(session_id)
    if not user:
        redirect('/login')
    
    materia = user.encontrar_materia(codigo)
    if materia and materia.get_faltas() > 0:
        materia.atualizar_faltas(materia.get_faltas() - 1)
        ctl.models.salvar()
    
    redirect('/hub')
#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
