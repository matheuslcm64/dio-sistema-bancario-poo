from conta import *
from historico import *
from cliente import *
from transacao import *

cliente1 = Cliente('Rua 123') 

conta1 = ContaCorrente.nova_conta(cliente1, 1)

deposito = Deposito(1000)        
deposito.registrar(conta1)
print(conta1.saldo)

saque = Saque(300)
saque.registrar(conta1)
print(conta1.saldo)

saque = Saque(501)
saque.registrar(conta1)
print(conta1.saldo)

deposito = Deposito(-1)
deposito.registrar(conta1)
print(conta1.saldo)

print(conta1._historico.lista_de_transacoes)