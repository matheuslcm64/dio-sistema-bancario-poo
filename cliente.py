from conta import Conta
from transacao import Transacao

class Cliente:
    
    def __init__(self, endereco:str) -> None:
        self._endereco = endereco
        self._contas = []
    
    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas
    
    def realizar_transacao(self, conta:Conta, transacao:Transacao):
        if not conta in self.contas:
            print('Operação inválida: Conta inválida')
            return
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta:Conta):
        self.contas.append(conta)
        print('Conta registrada com sucesso!')


class PessoaFisica(Cliente):

    def __init__(self, endereco:str, cpf:str, nome:str, data_nasc:str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nasc = data_nasc

    @property
    def cpf(self):
        return self._cpf  
    @property
    def nome(self):
        return self._nome  
    @property
    def data_nasc(self):
        return self._data_nasc  
    
    def exibir_contas(self):
        i = 1
        tipo_contas = {'ContaCorrente': 'Conta Corrente', 'Conta': 'Conta'}
        print(f'Contas de {self.nome}:')
        for conta in self.contas:
            print(f'{i} - Tipo: {tipo_contas[conta.__class__.__name__]} / Agencia: {conta.agencia} / Numero: {conta.numero} / Saldo: {conta.saldo:.2f}')
            i+=1



    