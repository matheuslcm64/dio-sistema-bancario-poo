import os
import time
from conta import *
from cliente import *
from transacao import *

def exibir_entrada_historico(historico:dict):
    print(' / '.join([f'{k}: {v}' for k,v in historico.items() if v]))

def exibir_historico(usuarios, cpf):
    for i in range(len(usuarios[cpf].contas)):
        if (len(usuarios[cpf].contas[i].historico.lista_de_transacoes) > 0):
            print(f'Conta {usuarios[cpf].contas[i].numero} transações:')
            for transacao in usuarios[cpf].contas[i].historico.lista_de_transacoes:
                exibir_entrada_historico(transacao)
            print('')
        else:
            print(f'Conta {usuarios[cpf].contas[i].numero} Sem movimentações')
            print('')


def verificar_usuario(usuarios, cpf):
    return cpf in usuarios

def verificar_usuario_conta(usuarios, cpf):
    if(not verificar_usuario(usuarios, cpf)):
        print('CPF não existe. Por favor cadastre-se.')
        time.sleep(2)   
        return False
    if(len(usuarios[cpf].contas) == 0):
        print('Não possui conta. Por favor abra uma conta.')
        time.sleep(2)   
        return False
    return True


def criar_usuario(usuarios):
    cpf = input('Digite o seu cpf: ')
    if(verificar_usuario(usuarios, cpf)):
        print('CPF já cadastrado')
        time.sleep(2)
        return
    nome = input('Digite o seu nome: ')
    data_nasc = input('Digite a sua data de nascimento [DD/MM/AAAA]: ')
    endereco = input('Digite seu endereço Logradouro, N° - Bairro - Cidade/UF: ')
    pessoaFisica = PessoaFisica(endereco, cpf, nome, data_nasc)
    usuario = {cpf: pessoaFisica}
    usuarios.update(usuario)
    print('Usuário criado com sucesso!')
    input('Pressione enter para prosseguir')

def entrar_usuario(usuarios):
    cpf = input('Digite o seu cpf: ')
    if(not verificar_usuario(usuarios, cpf)):
        print('CPF não existe. Por favor cadastre-se.')
        return
    print(f'Entrou no usuario {usuarios[cpf].nome}')
    return cpf

def criar_conta(usuarios, cpf, numero_conta, agencia):
    
    print('1-Criar conta corrente')
    print('2-Criar conta normal')
    print('3-Sair')
    op = input('Digite um dos digitos: ')
    try:
        op = int(op)
    except ValueError:
        print('Opção inválida')
        time.sleep(2)
        return numero_conta
    
    match op:
        case 1:
            conta = ContaCorrente.nova_conta(usuarios[cpf],numero_conta)
            usuarios[cpf].adicionar_conta(conta)
            numero_conta+=1
        case 2:
            conta = Conta(0.0, numero_conta, agencia, usuarios[cpf])
            usuarios[cpf].adicionar_conta(conta)
            numero_conta+=1
        case 3:
            print('Cancelando operação!')
        case _:
            print('Opção inválida')
       
    input('Pressione enter para prosseguir') 
    return numero_conta

def depositar(usuarios, cpf, valor):
    deposito = Deposito(valor)
    usuarios[cpf].exibir_contas()
    try:
        i = int(input('Escolha uma conta (primeiro digito): '))
        if(i<=0):
            print('Escolha inválida.')
            return
        usuarios[cpf].realizar_transacao(usuarios[cpf].contas[i-1], deposito)
    except ValueError:
        print('Escolha inválida.')
    except IndexError:
        print('Escolha inválida.')
    input('Pressione enter para prosseguir') 

def sacar(usuarios, cpf, valor):
    saque = Saque(valor)
    usuarios[cpf].exibir_contas()
    try:
        i = int(input('Escolha uma conta (primeiro digito): '))
        if(i<=0):
            print('Escolha inválida.')
            return
        usuarios[cpf].realizar_transacao(usuarios[cpf].contas[i-1], saque)
    except ValueError:
        print('Escolha inválida.')
    except IndexError:
        print('Escolha inválida.')
    input('Pressione enter para prosseguir') 
 

def listar_contas_usuario(usuarios, cpf):

    for conta in usuarios[cpf].contas:
            txt = f'''------------------------------
                Agencia: {conta.agencia}
                N° Conta: {conta.numero}
                Titular: {conta.cliente.nome}
                Saldo: R$ {conta.saldo:.2f}
            '''
            print(txt)
    input('Pressione enter para prosseguir') 


def main():
        
    title = ' Sistema Bancário DIO '
    title = title.center(len(title)+6,'$')
    menu = f'''{title}
        Escolha uma operação:
            1 - Criar Usuário
            2 - Entrar
            3 - Criar Conta
            4 - Depósito
            5 - Saque
            6 - Extrato 
            7 - Listar contas de um usuário
            8 - Sair
    '''
    sair = False

    usuarios = dict()
    numero_conta = 1
    agencia = '0001'
    cpf = ''

    while(not sair):
        os.system('cls')
        print(menu)
        op = input('Digite um dos digitos: ')
        try:
            op = int(op)
        except ValueError:
            print('Opção inválida')
            time.sleep(2)
            continue
        
        match op:
            case 1:
                criar_usuario(usuarios)
            
            case 2:
                resp = entrar_usuario(usuarios)
                cpf = resp if resp else cpf
                time.sleep(2)

            case 3:
                if(verificar_usuario(usuarios, cpf)):
                    numero_conta = criar_conta(usuarios, cpf, numero_conta, agencia)
                else:
                    print('CPF não existe. Por favor cadastre-se.')
                    time.sleep(2)

            case 4:
                if(verificar_usuario_conta(usuarios, cpf)):
                    try:
                        valor = float(input('Digite o valor de depósito: '))
                        depositar(usuarios,cpf,valor)
                    except ValueError:
                        print('Valor inválido')        

            case 5:
                if(verificar_usuario_conta(usuarios, cpf)):
                    try:
                        valor = float(input('Digite o valor de saque: '))
                        sacar(usuarios,cpf,valor)
                    except ValueError:
                        print('Valor inválido') 

            case 6:
                if(verificar_usuario_conta(usuarios, cpf)):
                    exibir_historico(usuarios, cpf)                
                    input('Pressione enter para prosseguir')

            case 7:
                if(verificar_usuario_conta(usuarios, cpf)):
                    listar_contas_usuario(usuarios, cpf)

            case 8:
                sair = True
            case _:
                print('Opção inválida')
                time.sleep(2)

        
    else:
        os.system('cls')
        print('Sessão encerrada!')

main()