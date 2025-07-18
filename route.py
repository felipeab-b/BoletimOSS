# route.py

from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file, HTTPResponse
from bottle import redirect, template, response
from bottle.ext.websocket import GeventWebSocketServer, websocket

import json

from app.models.materia import Materia
from app.models.nota import Nota
from app.models.avaliacao import Avaliacao
from app.models.usuario import Usuario

# ——————————————————————————————————————————————————————————————
# Globals para WebSocket
WS_CONNECTIONS = {}    # { session_id: [ws1, ws2, …] }
PENDING_EVENTS = {}    # { session_id: [json_msg1, json_msg2, …] }

def broadcast_event(session_id, event_name, payload):
    """
    Envia um JSON {"event":..., "data":...} a todos os WebSockets
    daquela sessão. Se não houver conexão ativa, bufferiza.
    """
    msg = json.dumps({"event": event_name, "data": payload})
    conns = WS_CONNECTIONS.get(session_id, [])
    if conns:
        for ws in conns:
            try:
                ws.send(msg)
            except:
                pass
    else:
        PENDING_EVENTS.setdefault(session_id, []).append(msg)

# ——————————————————————————————————————————————————————————————
app = Bottle()
ctl = Application()

# Static files
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper():
    return ctl.render('helper')

# ——————————————————————————————————————————————————————————————
# Rotas principais

@app.route('/home', method='GET')
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
    return ctl.render('login', mostrar_alerta=False)

@app.route('/login', method='POST')
def login_action():
    matricula = request.forms.get('matricula')
    senha      = request.forms.get('password')
    session_id, user = ctl.autenticate_user(matricula, senha)

    if session_id:
        response.set_cookie('session_id', session_id)
        redirect('/hub')
    else:
        return template(
            'app/views/html/login',
            mostrar_alerta=True,
            mensagem="Matrícula ou senha inválida"
        )

@app.route('/logout', method='POST')
def logout():
    session_id = request.get_cookie('session_id')
    if session_id in ctl.sessions:
        del ctl.sessions[session_id]
    response.delete_cookie('session_id')
    redirect('/home')

# Registro de usuário
@app.route('/form_registro.html', method='GET')
def form_registro_page():
    return ctl.render('form_registro', mostrar_alerta=False)

@app.route('/registro', method='POST')
def registro_action():
    matricula = request.forms.get('matricula')
    nome      = request.forms.get('nome')
    curso     = request.forms.get('curso')
    password  = request.forms.get('password')

    if ctl.models.work_with_parameter(matricula):
        return ctl.render(
            'form_registro',
            mostrar_alerta=True,
            mensagem="Matrícula já registrada."
        )

    novo_usuario = Usuario(nome, matricula, curso, password)
    ctl.models.adicionar_usuario(novo_usuario)
    redirect('/login')

# ——————————————————————————————————————————————————————————————
# CRUD de matérias, notas, avaliações e faltas

@app.route('/materia/adicionar', method='GET')
def form_adicionar_materia():
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if user:
        return ctl.render('form_materia')
    else:
        redirect('/login')

@app.route('/materia/adicionar', method='POST')
def adicionar_materia():
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if not user:
        redirect('/login')

    codigo = request.forms.get('codigo')
    nome   = request.forms.get('nome')
    horas  = int(request.forms.get('horas'))

    nova_materia = Materia(codigo, nome, horas)
    user.adicionar_materia(nova_materia)
    ctl.models.salvar()
    broadcast_event(sid, 'nova_materia', {
        'codigo': nova_materia.get_codigo(),
        'nome':   nova_materia.get_nome(),
        'horas':  nova_materia.get_horas()
    })
    redirect('/hub')

@app.route('/materia/<codigo>/editar', method='GET')
def form_editar_materia(codigo):
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if not user:
        redirect('/login')

    materia = user.encontrar_materia(codigo)
    if materia:
        return ctl.render('form_materia', materia=materia)
    else:
        redirect('/hub')

@app.route('/materia/<codigo>/editar', method='POST')
def editar_materia(codigo):
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if not user:
        redirect('/login')

    materia = user.encontrar_materia(codigo)
    if materia:
        nome   = request.forms.get('nome')
        horas  = int(request.forms.get('horas'))
        faltas = int(request.forms.get('faltas'))

        materia.atualizar_informacoes(nome=nome, horas=horas, faltas=faltas)
        ctl.models.salvar()
        broadcast_event(sid, 'materia_editada', {
            'codigo': codigo,
            'nome':   nome,
            'horas':  horas,
            'faltas': faltas
        })
    redirect('/hub')

@app.route('/materia/<codigo>/excluir', method='POST')
def excluir_materia(codigo):
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if not user:
        redirect('/login')

    if user.remover_materia(codigo):
        ctl.models.salvar()
        broadcast_event(sid, 'materia_excluida', {
            'codigo': codigo
        })
    redirect('/hub')

@app.route('/materia/<codigo>/nota/adicionar', method='POST')
def adicionar_nota(codigo):
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if not user:
        redirect('/login')

    materia = user.encontrar_materia(codigo)
    if materia:
        descricao = request.forms.get('descricao')
        valor     = float(request.forms.get('valor'))

        materia.adicionar_nota(Nota(descricao, valor))
        ctl.models.salvar()
        broadcast_event(sid, 'nota_adicionada', {
            'codigo':    codigo,
            'descricao': descricao,
            'valor':      valor
        })
    redirect('/hub')

@app.route('/materia/<codigo>/nota/<descricao>/excluir', method='POST')
def excluir_nota(codigo, descricao):
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if not user:
        redirect('/login')

    materia = user.encontrar_materia(codigo)
    if materia and materia.remover_nota(descricao):
        ctl.models.salvar()
        broadcast_event(sid, 'nota_excluida', {
            'codigo':    codigo,
            'descricao': descricao
        })
    redirect('/hub')

@app.route('/materia/<codigo>/avaliacao/adicionar', method='POST')
def adicionar_avaliacao(codigo):
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if not user:
        redirect('/login')

    materia = user.encontrar_materia(codigo)
    if materia:
        comentario = request.forms.get('comentario')

        materia.adicionar_avaliacao(Avaliacao(comentario))
        ctl.models.salvar()
        broadcast_event(sid, 'avaliacao_adicionada', {
            'codigo':     codigo,
            'comentario': comentario
        })
    redirect('/hub')

@app.route('/materia/<codigo>/avaliacao/<comentario>/excluir', method='POST')
def excluir_avaliacao(codigo, comentario):
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if not user:
        redirect('/login')

    materia = user.encontrar_materia(codigo)
    if materia and materia.remover_avaliacao(comentario):
        ctl.models.salvar()
        broadcast_event(sid, 'avaliacao_excluida', {
            'codigo':     codigo,
            'comentario': comentario
        })
    redirect('/hub')

@app.post('/materia/<codigo>/faltas/adicionar')
def adicionar_falta(codigo):
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if not user:
        redirect('/login')

    materia = user.encontrar_materia(codigo)
    if materia:
        materia.atualizar_faltas(materia.get_faltas() + 1)
        ctl.models.salvar()
        broadcast_event(sid, 'falta_incrementada', {
            'codigo': codigo,
            'faltas': materia.get_faltas()
        })
    redirect('/hub')

@app.post('/materia/<codigo>/faltas/remover')
def remover_falta(codigo):
    sid  = request.get_cookie('session_id')
    user = ctl.get_current_user(sid)
    if not user:
        redirect('/login')

    materia = user.encontrar_materia(codigo)
    if materia and materia.get_faltas() > 0:
        materia.atualizar_faltas(materia.get_faltas() - 1)
        ctl.models.salvar()
        broadcast_event(sid, 'falta_decrementada', {
            'codigo': codigo,
            'faltas': materia.get_faltas()
        })
    redirect('/hub')

# ——————————————————————————————————————————————————————————————
# Rota para entregar eventos que chegaram antes do WS abrir
@app.route('/pending_events', method='GET')
def pending_events():
    sid = request.get_cookie('session_id')
    evs = PENDING_EVENTS.get(sid, [])
    PENDING_EVENTS[sid] = []
    return HTTPResponse(
        status=200,
        body=json.dumps({ "events": evs }),
        content_type="application/json"
    )

# ——————————————————————————————————————————————————————————————
# WebSocket handshake e loop
@app.route('/ws', apply=[websocket])
def ws_handler(ws):
    # 1) Recebe {"session_id":"..."}
    init = ws.receive()
    data = json.loads(init or "{}")
    sid  = data.get("session_id")
    if not sid:
        ws.close()
        return

    # 2) Registra conexão
    WS_CONNECTIONS.setdefault(sid, []).append(ws)

    # 3) Envia buffer de pendentes
    for raw in PENDING_EVENTS.get(sid, []):
        try: ws.send(raw)
        except: pass
    PENDING_EVENTS[sid] = []

    # 4) Loop até desconectar
    try:
        while True:
            msg = ws.receive()
            if msg is None:
                break
    finally:
        # 5) Cleanup
        conns = WS_CONNECTIONS.get(sid, [])
        if ws in conns:
            conns.remove(ws)

# ——————————————————————————————————————————————————————————————
if __name__ == '__main__':
    run(
        app,
        server=GeventWebSocketServer,
        host='0.0.0.0',
        port=8080,
        debug=True,
        reloader=True
    )
