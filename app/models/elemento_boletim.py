from abc import ABC, abstractmethod

class ElementoBoletim(ABC):
    @abstractmethod
    def render(self):
        pass
