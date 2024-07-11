from transacao import *
from datetime import datetime
class Historico:
    def __init__(self) -> None:
        self.lista_de_transacoes = []
    
    def adicionar_transacao(self, transacao:Transacao, conta) -> None:
        self.lista_de_transacoes.append(
            {
                'Operação': transacao.__class__.__name__,
                'Valor': f'{transacao.valor:.2f}',
                'Numero_Conta': conta.numero,
                'Agencia': conta.agencia,
                'Saldo': f'{conta.saldo:.2f}',
                'Data': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            }
        )
    