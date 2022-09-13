from abc import ABC, abstractmethod


class Order(ABC):
    @abstractmethod
    def Execute(self):
        pass
