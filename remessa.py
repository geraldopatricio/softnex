import os
import csv
from db import getWebDatabase, getStageDatabase
from utils import data_hoje_aaaammddhhmmss, data_hoje_aaaammdd, monta_nomenclatura_rem
from settings import get_config_env


def monta_header_rem():
    dt_geracao = data_hoje_aaaammdd('-')
    # H;SOFTNEX CREDENCIAMENTO V1.0;2020-02-20;REMESSA;0002
    header = ['H', 'SOFTNEX CREDENCIAMENTO V1.0',
              dt_geracao, 'REMESSA', '0002', 'FORTBRASIL']
    return header


def monta_trailler_rem(qtd_d1):
    # T1214
    trailler = ['T', qtd_d1, ((qtd_d1*2) + 2)]
    return trailler


def gera_arquivo_remessa(nome_arquivo):
    header = monta_header_rem()
    config_env = get_config_env()
    local = config_env["path_remessa"]
    print(local)
    # conect db Stage
    try:
        print('Conectando no banco Stage...')
        #conn = getStageDatabase()
        conn = getWebDatabase()
        with conn.cursor() as cursor:
            # query = '''SELECT NU_CNPJ, NU_ESTABELECIMENTO ,NU_DIGITO_ESTABELECIMENTO,
            #     DS_RAZAO_SOCIAL, DS_NOMEFANTASIA, CONTATO, FONE, EMAIL, CD_TIPO_EQUIPAMENTO
            #     FROM VI_ESTABELECIMENTOS_CREDENCIADOS
            #     WHERE nu_cnpj in ('24883843000141', '29730696000193') and DT_CADASTRAMENTO IS NOT NULL
            #     order by DT_CADASTRAMENTO desc  '''
            query = '''
                SELECT NU_CNPJ, NU_ESTABELECIMENTO ,NU_DIGITO_ESTABELECIMENTO,
                       DS_RAZAO_SOCIAL, DS_NOMEFANTASIA, CONTATO, FONE, EMAIL, MEIO_CAPTURA
                    FROM T_CONTROLE_CREDENCIAMENTO_SOFTNEX
                    WHERE NM_ARQUIVO = '{0}' ORDER BY MEIO_CAPTURA'''.format(nome_arquivo)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                print(rows)
                print('Gerando arquivo SOFTNEX {}...'.format(nome_arquivo))
                with open('{0}/{1}'.format(local, nome_arquivo), 'w', encoding='ISO-8859-1') as arquivo:
                    qtd_d1 = 0
                    escrever = csv.writer(arquivo, delimiter=';')
                    escrever.writerow(header)
                    for row in rows:
                        meio = 'GLOBALPAYMENTS' if row[8] == 'GPAY' else 'FIRSTDATA'
                        linha_d1 = 'D1', row[0], '{0}{1}'.format(row[1], row[2]), row[3][:150], \
                            row[4][:100], row[5], row[6][:20], row[7][:50], 'I'
                        linha_d2 = 'D2', row[0], '{0}{1}'.format(
                            row[1], row[2]), meio, 'H'
                        escrever.writerow(linha_d1)
                        escrever.writerow(linha_d2)
                        qtd_d1 += 1
                    trailler = monta_trailler_rem(qtd_d1)
                    escrever.writerow(trailler)
                return True
            else:
                print(' Não existe arquivo ')
                return False
    except Exception as e:
        print(str(e))
