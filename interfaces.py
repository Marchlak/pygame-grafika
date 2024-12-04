from abc import ABC, abstractmethod

class IController(ABC):
    @abstractmethod
    def process_input(self):
        pass

    @abstractmethod
    def update_view(self):
        pass

class IView(ABC):
    @abstractmethod
    def draw(self):
        pass

class IModel(ABC):
    pass

