from historico import Historico
from math import trunc

class Conta:
    AGENCIA = ['0001']
    def __init__(self, saldo:float, numero:int, agencia:str, cliente) -> None:
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia if agencia in self.AGENCIA else self.AGENCIA[0]
        self._cliente = cliente
        self._historico = Historico()
    
    @staticmethod
    def decimal_cases(num,decimals):
        num_with_decimals = trunc(num * 10**decimals) / 10**decimals 
        return num_with_decimals
    
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero:int):
        historico = Historico()
        return cls(saldo=0.0, numero=numero, agencia=cls.AGENCIA[0], cliente=cliente)
    
    def sacar(self, valor:float) -> bool:
        if(valor<=0):
            print('Operação inválida: Valor de saque inválido.')
            return False
        
        if(valor > self._saldo):
            print('Operação inválida: O valor de saque excede o saldo atual!')
            return False

        valor = self.decimal_cases(valor,2)
        self._saldo = self.decimal_cases(self._saldo,2)
        self._saldo -= valor
        print(f'Saque de R$ {valor:.2f} efetuado!')
        return True
    
    def depositar(self, valor:float) -> bool:
        if(valor <= 0):
            print('Operação inválida: Valor de depósito inválido.')
            return False
        
        valor = self.decimal_cases(valor,2)
        self._saldo = self.decimal_cases(self._saldo,2)
        self._saldo += valor
        print(f'Deposito de R$ {valor:.2f} efetuado!')
        return True
    
class ContaCorrente(Conta):
    LIMITE = 500.0
    LIMITE_SAQUES = 3
    saques_diarios = 0
    def sacar(self, valor: float) -> bool:
        if(self.saques_diarios >= self.LIMITE_SAQUES):
            print('Limite de saque diário atingido.')
            return False
        if(valor > self.LIMITE):
            print('Valor de saque inválido. Máximo R$ 500.00.')
            return False
        resp = super().sacar(valor)
        if(resp):
            self.saques_diarios += 1
        return resp
        

        


