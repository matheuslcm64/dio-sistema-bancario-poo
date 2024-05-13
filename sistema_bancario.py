import os
import time
import math
import itertools
 

title = ' Sistema Bancário DIO '
title = title.center(len(title)+6,'$')
menu = f'''{title}
    Escolha uma operação:
        1 - Depósito
        2 - Saque
        3 - Extrato
        4 - Sair
'''
sair = False
saldo = 0
extrato = {'Depositos':[],'Saques':[]}
LIM_SAQUE_DIARIO = 3
lim_atual = LIM_SAQUE_DIARIO
lim_max_saque = 500


def trunc(num,decimals):
    truncated_num = math.floor(num * 10**decimals) / 10**decimals 
    return truncated_num


def exibir_extrato_linha(value, prefix, size, value_size, decimals, space1, space2=''):
    if isinstance(value,(int, float)): 
        print(f'{prefix}{value:{value_size}.{decimals}f}{space1}'.center(size),end=f'')
    else:
        print(f'{space2}{value}{space1}'.center(size),end=f'')

def column_sizes(items, total_size, prefix):
    sizes = []

    for i in range(len(items)):
        length = len(items[i])
        if(length<total_size):
            sizes.append(total_size)
        elif(length==total_size):
            space = ' '*2
            prefix[i] = space + prefix[i] 
            sizes.append(total_size+2)
        else:
            space_size = length-total_size+2
            space = ' '*space_size
            prefix[i] = space + prefix[i] 
            sizes.append(length+2)

    return sizes,prefix


def exibir_extrato(extrato):
    items = ['Saldo Atual'] + list(extrato.keys())
    values = itertools.zip_longest([saldo],extrato['Depositos'],extrato['Saques'],fillvalue='')
    
    prefix = ['R$']*len(items)
    digits = 6
    decimals = 2
    value_size = digits+decimals+1
    value_prefix_size = value_size+len(prefix)
    space1 = ' '*9
    total_column_size = len(space1)+value_prefix_size
    sizes,prefix = column_sizes(items, total_column_size, prefix)
    space2 = []
    for i in prefix:
        space2.append(' '*(value_size+len(i)))

    exibir_extrato_formatado = f'''{items[0].center(sizes[0])}{items[1].center(sizes[1])}{items[2].center(sizes[2])}'''
    print(exibir_extrato_formatado)
    for value in values:
        for i in range(len(value)):
            if(i<len(value)-1):
                exibir_extrato_linha(value[i], prefix[i], sizes[i], value_size, decimals, space1=space1, space2=space2[i])
            else:
                exibir_extrato_linha(value[i], prefix[i], sizes[i], value_size, decimals, space1='', space2=space2[i])
        print()


    

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
        deposito = input('Digite o valor que deseja depositar: ')
        try: 
            deposito = float(deposito)
        except ValueError:
            print('Insira um valor numérico')
            time.sleep(2)
            continue
        if(deposito>0):
            deposito = trunc(deposito,2)
            saldo+=deposito
            extrato['Depositos'].append(deposito)
            print(f'Deposito de R$ {deposito:.2f} efetuado!')
            input('Pressione enter para prosseguir')
        else:
            print('Valor de depósito inválido')
            time.sleep(2)


    elif(op==2):
        if(lim_atual>0 and lim_atual<=LIM_SAQUE_DIARIO):
            saque = input('Digite o valor que deseja sacar: ')
            try: 
                saque = float(saque)
            except ValueError:
                print('Insira um valor numérico')
                time.sleep(2)
                continue
            if (saque>0 and saque<=lim_max_saque):
                if(saque<=saldo):
                    saldo-=saque
                    lim_atual-=1
                    extrato['Saques'].append(saque)
                    print(f'Saque de {saque:.2f} realizado com sucesso!')
                    input('Pressione enter para continuar')

                else:
                    print('Operação inválida: O valor de saque excede o saldo atual!')
                    time.sleep(2)
            else:
                print('Valor de saque inválido. Máximo R$ 500.00.')
                time.sleep(2)
        else:
            print('Limite de saque diário atingido.')
            time.sleep(2)
    elif(op==3):
        exibir_extrato(extrato) if extrato['Depositos'] or extrato['Saques'] else print(f'Sem movimentações!\nSaldo: R$ {saldo:.2f}')
        input('Pressione enter para prosseguir')
    elif(op==4):
        sair = True
    else:
        print('Opção inválida')
        time.sleep(2)
    
else:
    os.system('cls')
    print('Sessão encerrada!')
      
