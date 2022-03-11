import pyodbc

from utils import dt_ctrl
from cofre import Cofre


def build_connection_string_web():
    cofre = Cofre()
   #  cx_string_web = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=Ametista\db01,1433;DSN=ametista;DATABASE=WEB;UID=web;PWD=w3b!ng'
    cx_string_web = "DRIVER={0};SERVER={1},1433;DATABASE={2};UID={3};PWD={4}".format(
        '{ODBC Driver 17 for SQL Server}', cofre.get_secret_azure(
            'DB-AMETISTA-HOST'), cofre.get_secret_azure('DB-AMETISTA-DATABASE'),
        cofre.get_secret_azure('DB-AMETISTA-RDKESTABELECIMENTOSCREDENCIADOS-USERNAME'), cofre.get_secret_azure('DB-AMETISTA-RDKESTABELECIMENTOSCREDENCIADOS-PASSWORD'))
    return cx_string_web


def build_connection_string_stage():
    cofre = Cofre()
    #  cx_string_stage = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=baseunica.database.windows.net,1433;DSN=Stage;DATABASE=Stage;UID=Operacao;PWD=0p3r@c03s'
    cx_string_stage = "DRIVER={0};SERVER={1},1433;DATABASE={2};UID={3};PWD={4}".format(
                      '{ODBC Driver 17 for SQL Server}', cofre.get_secret_azure(
                          'DB-STAGE-HOST'), cofre.get_secret_azure('DB-STAGE-DATABASE'),
        cofre.get_secret_azure('DB-STAGE-RDKESTABELECIMENTOSCREDENCIADOS-USERNAME'), cofre.get_secret_azure('DB-STAGE-RDKESTABELECIMENTOSCREDENCIADOS-PASSWORD'))
    return cx_string_stage


def getWebDatabase():
    conn = pyodbc.connect(build_connection_string_web())
    return conn


def getStageDatabase():
    conn = pyodbc.connect(build_connection_string_stage())
    return conn


def consulta_novos_credenciados(dt_ontem, nome_arquivo):
    print('Consulta novos credenciados na Stage...')
    conn = getStageDatabase()
    with conn.cursor() as cursor:
        # consulta credenciados na data de ontem
        data = '19000101'
        query = ''' SELECT NU_CNPJ, NU_ESTABELECIMENTO, NU_DIGITO_ESTABELECIMENTO, DS_RAZAO_SOCIAL, 
         DS_NOMEFANTASIA, CONTATO, FONE, EMAIL, DS_CLASSIFICACAO, '{0}', 'I', '{1}','{2}',
         CD_TIPO_EQUIPAMENTO,'{3}'
         FROM VI_ESTABELECIMENTOS_CREDENCIADOS WHERE DT_CANCELAMENTO IS NULL AND DT_CADASTRAMENTO = '{0}' 
         AND CD_TIPO_EQUIPAMENTO IN ('FTDATA', 'GPAY')'''.format(dt_ontem, nome_arquivo, dt_ctrl(), data)
        print(query)
        # month(DT_CADASTRAMENTO) = 3 AND
        # query = """select NU_CNPJ, NU_ESTABELECIMENTO, NU_DIGITO_ESTABELECIMENTO, DS_RAZAO_SOCIAL,
        #    DS_NOMEFANTASIA, CONTATO, FONE, EMAIL, DS_CLASSIFICACAO, '20200415', 'I', '{0}','{1}',
        #    CD_TIPO_EQUIPAMENTO, '{2}'
        #    FROM VI_ESTABELECIMENTOS_CREDENCIADOS where CD_TIPO_EQUIPAMENTO IN ('FTDATA', 'GPAY') AND
        #    NU_CNPJ IN ('28832218000121')""".format(nome_arquivo, dt_ctrl(),data)
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows


def check_duplicidade_controle_softnex(dt_ontem):
    conn = getWebDatabase()
    with conn.cursor() as cursor:
        query = '''
         SELECT * FROM T_CONTROLE_CREDENCIAMENTO_SOFTNEX 
         WHERE DT_CADASTRAMENTO = '{0}' '''.format(dt_ontem)
        cursor.execute(query)
        rows = cursor.fetchall()
        rows = ''
        return rows


def insere_novos_credenciados(dt_ontem, novos_credenciados):
    print('Verifica duplicidade na tabela de controle...')
    duplicidade = check_duplicidade_controle_softnex(dt_ontem)
    if duplicidade:
        print('Já existe CNPJs inclusos com a data {}'.format(dt_ontem))
        return False
    else:
        # prepara insert
        print('Insere novos credenciados na tabela de controle.')
        conn = getWebDatabase()
        with conn.cursor() as cursor:
            query = """ INSERT INTO T_CONTROLE_CREDENCIAMENTO_SOFTNEX (
         NU_CNPJ, NU_ESTABELECIMENTO, NU_DIGITO_ESTABELECIMENTO, DS_RAZAO_SOCIAL, DS_NOMEFANTASIA,
         CONTATO, FONE, EMAIL, DS_CLASSIFICACAO, DT_CADASTRAMENTO, SITUACAO_SOFTNEX, NM_ARQUIVO, 
         DT_CTRL, MEIO_CAPTURA, DT_CTRL_RET
         ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            cursor.executemany(query, novos_credenciados)
            conn.commit()
            return True


def atualiza_softnex(rowlist):
    print(rowlist)
    conn = getWebDatabase()
    with conn.cursor() as cursor:
        for row in rowlist:
            query = """ UPDATE T_CONTROLE_CREDENCIAMENTO_SOFTNEX
         SET SITUACAO_SOFTNEX = '{0}', DT_CTRL_RET = '{1}'
         WHERE NU_CNPJ = '{2}' AND MEIO_CAPTURA = '{3}'""".format(row[2], dt_ctrl(), row[0], row[1])
            print(query)
            cursor.execute(query)
    return True
