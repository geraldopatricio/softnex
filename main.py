import sys
from remessa import gera_arquivo_remessa
from db import consulta_novos_credenciados, insere_novos_credenciados
from utils import data_ontem_aaaammdd, monta_nomenclatura_rem
from ftp import send_rem_ftp, return_ret_ftp
from dotenv import load_dotenv

load_dotenv()

"""     Função principal da aplicação.   """


def run():
    # print('======== Rotina arquivo Remessa SOFTNEX  ========')
    nome_arquivo = monta_nomenclatura_rem()
    # verifica se tem novos credenciados para cadastro na Softnex (data de ontem)
    novos_credenciados = consulta_novos_credenciados(
        data_ontem_aaaammdd(), nome_arquivo)

    if novos_credenciados:
        print('Existem novos credenciados na Stage')
        # insere novos na tabela de controle T_CONTROLE_CREDENCIAMENTO_SOFTNEX
        retorno = insere_novos_credenciados(
            data_ontem_aaaammdd(), novos_credenciados)
        # se inserido gera arquivo remessa
        gera = gera_arquivo_remessa(nome_arquivo) if retorno else print(
            'Erro ao inserir novos credenciados!')
        # se gerado envia arquivo via FTP
        enviou = send_rem_ftp(nome_arquivo) if gera else print(
            'Arquivo REM nao foi gerado com sucesso.')
        print('Arquivo remessa enviado com sucesso!') if enviou else print(
            'Arquivo REM não enviado')
    else:
        print('Sem novos credenciados para a data de ontem!')

    print('======== Rotina arquivo Retorno SOFTNEX  ========')
    retorno = return_ret_ftp()


run()
