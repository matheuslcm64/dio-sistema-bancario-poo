from abc import ABC, abstractmethod
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta) -> None:
        pass

class Deposito(Transacao):
    def __init__(self, valor:float) -> None:
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta) -> None:
        if (conta.depositar(self._valor)):
            conta._historico.adicionar_transacao(self, conta)
        

class Saque(Transacao):
    def __init__(self, valor:float) -> None:
        self._valor = valor   

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta) -> None:
        if (conta.sacar(self._valor)):
            conta._historico.adicionar_transacao(self, conta)