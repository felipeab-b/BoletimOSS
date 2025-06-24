from abc import ABC, abstractmethod

class RegistroAcademico(ABC):
    @abstractmethod
    def exibir_detalhes(self):
        pass
