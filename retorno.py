import os
import csv
from db import atualiza_softnex


def ler_arquivo_retorno(path_retorno):
    try:
        print('Lendo arquivo RET...')
        with open(path_retorno, 'rt', encoding='ISO-8859-1') as arquivo:
            rowlist = []
            linha = []
            linhas = arquivo.readlines()
            for l in linhas:
                linha = l.split(';')
                if linha[0] == '02':
                    cnpj = linha[1]
                    meio_captura = 'GPAY' if linha[4] == 'GLOBALPAYMENTS' else 'FTDATA'
                    status_habilitacao = linha[5]
                    status_processamento = linha[6]  # O-OK / E-Erro
                    if status_habilitacao == 'H':
                        status_habilitacao = 'HABILITADO'
                    elif status_habilitacao == 'D':
                        status_habilitacao = 'DESABILITADO'
                    else:
                        status_habilitacao = 'PENDENTE'
                    linha = (cnpj.strip(), meio_captura.strip(
                    ), status_habilitacao.strip(), status_processamento.strip())
                    meio_captura = ''
                    rowlist.append(linha)
            if rowlist:
                print('Atualiza tabela de controle...')
                atualiza = atualiza_softnex(rowlist)
                if atualiza:
                    print('Retorno atualizado com sucesso!')
                    return True
                else:
                    print('Retorno não atualizado!')
                    return False
    except Exception as ex:
        print('Erro na função ler_arquivo_retorno')
        print(ex)
        return False
