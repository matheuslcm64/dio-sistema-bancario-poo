import os
import time
import math
import itertools


def trunc(num,decimals):
    truncated_num = math.floor(num * 10**decimals) / 10**decimals 
    return truncated_num

def count_value_size(value):
    if isinstance(value,(int, float)): 
        size = len(f'{value:.2f}')
    else:
        size = len(value)
    return size

def max_column_size(column_names, values, prefix_size, default=20):
    sizes = []
    
    for i in column_names:
        sizes.append(len(i))
    
    value_size = count_value_size(values[0][0])
    if (sizes[0] < value_size+prefix_size):
        sizes[0] = value_size+prefix_size
    
    for value in values:
        for i in range(1,len(value)):
            value_size = count_value_size(value[i])
            if(sizes[i] < value_size+prefix_size):
                sizes[i] = value_size+prefix_size
    
    for i in range(len(sizes)):
        if(sizes[i]<default):
            sizes[i] = default
    return sizes

def exibir_extrato_linha(value, prefix, size, decimals):
    
    if isinstance(value,(int, float)): 
        text = f'{prefix}{value:.{decimals}f}'
        print(f'{text.center(size)}', end=f'')
    else:  
        space = ' '
        print(f'{space*size}',end=f'')

def show_column_names(column_names, sizes):
    exibir_extrato_formatado = f'''{column_names[0].center(sizes[0])}{column_names[1].center(sizes[1])}{column_names[2].center(sizes[2])}'''
    print(exibir_extrato_formatado)

def exibir_extrato(saldo, /, *, extrato):
    column_names = ['Saldo Atual'] + list(extrato.keys())
    values = list(itertools.zip_longest([saldo],extrato['Depositos'],extrato['Saques'],fillvalue=''))
    
    prefix = 'R$ '
    decimals = 2
    sizes = max_column_size(column_names,values,len(prefix))

    show_column_names(column_names, sizes)
    
    for value in values:
        for i in range(len(value)):
            exibir_extrato_linha(value[i], prefix, sizes[i], decimals)
        print()

def depositar(saldo, extrato,/):
    deposito = input('Digite o valor que deseja depositar: ')
    try: 
        deposito = float(deposito)
    except ValueError:
        print('Insira um valor numérico')
        time.sleep(2)
        return

    if(deposito<=0):
        print('Valor de depósito inválido')
        time.sleep(2)
        return
    else:
        deposito = trunc(deposito,2)
        saldo+=deposito
        extrato['Depositos'].append(deposito)
        print(f'Deposito de R$ {deposito:.2f} efetuado!')
        input('Pressione enter para prosseguir')    
    return saldo


def sacar(*, saldo, extrato, limite, numero_saques):
    if(numero_saques<=0):
        print('Limite de saque diário atingido.')
        time.sleep(2)
        return

    valor = input('Digite o valor que deseja sacar: ')
    try: 
        valor = float(valor)
    except ValueError:
        print('Insira um valor numérico')
        time.sleep(2)
        return
    if(valor<=0 or valor>limite):
        print('Valor de saque inválido. Máximo R$ 500.00.')
        time.sleep(2)
    elif(valor>saldo):
        print('Operação inválida: O valor de saque excede o saldo atual!')
        time.sleep(2)
    else:
        saldo = trunc(saldo,2)
        saldo-=valor
        numero_saques-=1
        extrato['Saques'].append(valor)
        print(f'Saque de {valor:.2f} realizado com sucesso!')
        input('Pressione enter para continuar')    

    return saldo, numero_saques

def verificar_usuario(usuarios, cpf):
    return cpf in usuarios

def criar_usuario(usuarios):
    cpf = input('Digite o seu cpf: ')
    if(verificar_usuario(usuarios, cpf)):
        print('CPF já cadastrado')
        time.sleep(2)
        return
    nome = input('Digite o seu nome: ')
    data_nascimento = input('Digite a sua data de nascimento [DD/MM/AAAA]: ')
    endereco = input('Digite seu endereço Logradouro, N° - Bairro - Cidade/UF: ')
    usuario = {cpf: {'nome': nome, 'cpf': cpf, 'data_nascimento': data_nascimento, 'endereco': endereco}}
    usuarios.update(usuario)
    print('Usuário criado com sucesso!')
    input('Pressione enter para prosseguir')

def criar_conta(usuarios, contas, agencia, numero_conta):
    cpf = input('Digite o seu cpf: ')
    if(not verificar_usuario(usuarios, cpf)):
        print('CPF não existe. Por favor cadastre-se.')
        time.sleep(2)
        return
    conta = {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuarios[cpf]}
    contas.append(conta)
    numero_conta+=1
    print('Conta criada com sucesso!')
    input('Pressione enter para prosseguir') 

    return numero_conta

def listar_contas(contas):
    if not contas:
        print('Nenhuma conta cadastrada')
        time.sleep(2)
        return
    for conta in contas:
        txt = f'''------------------------------
            Agencia: {conta['agencia']}
            N° Conta: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        '''
        print(txt)
    input('Pressione enter para prosseguir') 

    

def listar_contas_usuario(usuarios, contas):
    cpf = input('Digite o seu cpf: ')
    if(not verificar_usuario(usuarios, cpf)):
        print('CPF não existe. Por favor cadastre-se.')
        time.sleep(2)
        return
    for conta in contas:
        if(cpf == conta['usuario']['cpf']):
            txt = f'''------------------------------
                Agencia: {conta['agencia']}
                N° Conta: {conta['numero_conta']}
                Titular: {conta['usuario']['nome']}
            '''
            print(txt)
    input('Pressione enter para prosseguir') 

def main():
        
    title = ' Sistema Bancário DIO '
    title = title.center(len(title)+6,'$')
    menu = f'''{title}
        Escolha uma operação:
            1 - Criar Usuário
            2 - Criar Conta
            3 - Depósito
            4 - Saque
            5 - Extrato
            6 - Listar todas as contas
            7 - Listar contas de um usuário
            8 - Sair
    '''
    sair = False
    saldo = 0
    extrato = {'Depositos':[],'Saques':[]}
    LIM_SAQUE_DIARIO = 3
    numero_saques = LIM_SAQUE_DIARIO
    LIM_MAX_SAQUE = 500

    usuarios = dict()
    contas = []
    numero_conta = 1
    agencia = '0001'

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
        if(op==1):
            criar_usuario(usuarios)
        elif(op==2):
            resp = criar_conta(usuarios, contas, agencia, numero_conta)
            numero_conta = resp if resp else numero_conta

        elif(op==3):
            resp = depositar(saldo,extrato)
            saldo = resp if resp else saldo

        elif(op==4):
            resp = sacar(saldo=saldo, extrato=extrato, limite=LIM_MAX_SAQUE, numero_saques=numero_saques)
            if(resp):
                saldo, numero_saques = resp

        elif(op==5):
            exibir_extrato(saldo, extrato=extrato) if extrato['Depositos'] or extrato['Saques'] else print(f'Sem movimentações!\nSaldo: R$ {saldo:.2f}')
            input('Pressione enter para prosseguir')
        elif(op==6):
            listar_contas(contas)
        elif(op==7):
            listar_contas_usuario(usuarios, contas)
        elif(op==8):
            sair = True
        else:
            print('Opção inválida')
            time.sleep(2)
        
    else:
        os.system('cls')
        print('Sessão encerrada!')

main()