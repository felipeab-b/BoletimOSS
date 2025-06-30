from bottle import template, redirect
from .datarecord import DataRecord
import uuid


class Application():

    def __init__(self):
        self.pages = {
            'home' : self.home,
            'hub' : self.hub,
            'login' : self.login,
            'form_materia' : self.form_materia
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

    def autenticate_user(self,matricula):
        user = self.models.work_with_parameter(matricula)
        if user:
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = user
            return session_id, user
        return None, None
    
    def get_current_user(self, session_id):
        if session_id:
            return self.sessions.get(session_id)
        return None
    
    def form_materia(self, materia=None):
        return template('app/views/html/form_materia', materia=materia)