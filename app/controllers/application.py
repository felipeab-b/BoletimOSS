from bottle import template, redirect
from .datarecord import DataRecord
import uuid
from app.models.usuario import Usuario


class Application():

    def __init__(self):
        self.pages = {
            'home' : self.home,
            'hub' : self.hub,
            'login' : self.login,
            'form_materia' : self.form_materia,
            'form_registro' : self.form_registro
        }

        self.models = DataRecord()
        self.sessions = {}


    def render(self,page,parameter=None, **kwargs):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content(**kwargs)
        else:
            return content(parameter, **kwargs)

    def helper(self):
        return template('app/views/html/helper')

    def home(self):
        return template('app/views/html/home')

    def hub(self, usuario =None, **kwargs):
        return template('app/views/html/hub', usuario=usuario)
        
    def login(self):
        return template('app/views/html/login')

    def autenticate_user(self, matricula, password):
        # tenta autenticar via DataRecord
        session_id = self.models.check_user(matricula, password)
        if session_id:
            user = self.models.get_current_user(session_id)
            #também guarda em self.sessions
            self.sessions[session_id] = user
            return session_id, user
        return None, None
    
    def get_current_user(self, session_id):
        if session_id:
            return self.sessions.get(session_id)
        return None
    
    def form_materia(self, materia=None):
        return template('app/views/html/form_materia', materia=materia)
    
    def form_registro(self):
        return template('app/views/html/form_registro')

    def save_changes(self):
        self.models.salvar()