import os
import sys
import shutil
import time
from os.path import isfile, join
from ftplib import FTP
from settings import get_config_env
from retorno import ler_arquivo_retorno

config_env = get_config_env()

"""     Função de Conexão FTP   """


def conect_ftp(host, port, user, passwd, path_remote):
    print('host:', host, port)
    print('user:', user)
    try:
        ftp = FTP()
        print('Conectando...')
        ftp.connect(host=host, port=21)
        ftp.login(user=user, passwd=passwd)
        ftp.cwd(path_remote)
        print('Conectado')
        return ftp
    except Exception as ex:
        print('Erro de conexao FTP!')
        print(ex)
        return False


"""     Função REM via FTP   """


def send_rem_ftp(nome_arquivo):
    # conecta ao FTP SOFTNEX
    print("Conectando FTP SOFTNEX Remessa")
    ftp = conect_ftp(config_env['host_ftp_softnex'], config_env['port_ftp_softnex'],
                     config_env['username_ftp_softnex'], config_env['passwd_ftp_softnex'], config_env['path_remote_rem'])
    #local_file = open('{0}/{1}'.format(config_env["path_remessa"], nome_arquivo), 'rb')
    with open('{0}/{1}'.format(config_env["path_remessa"], nome_arquivo), 'rb') as local_file:
        ftp.storlines('STOR {0}'.format(nome_arquivo), local_file)
        # local_file.close()
        tamanho = ftp.size('{0}'.format(nome_arquivo))
        tamanho_local = os.path.getsize(
            '{0}/{1}'.format(config_env["path_remessa"], nome_arquivo))
    # verifica se transferiu todo o arquivo
    if tamanho == tamanho_local:
        print("Arquivo transferido confere com o arquivo original. Move para /remessa/enviados")
        # move dos /remessa local para /remessa/enviados
        shutil.move('{0}/{1}'.format(config_env["path_remessa"], nome_arquivo),
                    '{0}/{1}'.format(config_env["path_remessa_enviados"], nome_arquivo))
        return True
    else:
        print("Arquivo transferido não confere com o arquivo original.")
        return False


"""     Função recepciona RET via FTP.   """


def return_ret_ftp():
    try:
        print("Conectando FTP SOFTNEX Retorno")
        with conect_ftp(config_env['host_ftp_softnex'], config_env['port_ftp_softnex'], config_env['username_ftp_softnex'], config_env['passwd_ftp_softnex'], config_env['path_remote_ret']) as ftp:
            filenames = ftp.nlst()
            print(filenames)
            if filenames:
                for filename in filenames:
                    extensao = filename[-4:]
                    print(filename)
                    print(extensao)
                    if extensao.upper() == '.RET':
                        print(filename)
                        with open('{0}/{1}'.format(config_env["path_retorno"], filename), 'wb') as file:
                            tamanho = ftp.size('{0}'.format(filename))
                            ftp.retrbinary('RETR {0}'.format(
                                filename), file.write, 2000)
                        tamanho_local = os.path.getsize(
                            '{0}/{1}'.format(config_env["path_retorno"], filename))
                        print(tamanho, tamanho_local)
                        if tamanho == tamanho_local:
                            print('Ler arquivo retorno')
                            print(
                                '{0}/{1}'.format(config_env["path_retorno"], filename))
                            rows = ler_arquivo_retorno(
                                '{0}/{1}'.format(config_env["path_retorno"], filename))
                            print('Move RET para pasta recepcionados')
                            shutil.move('{0}/{1}'.format(config_env["path_retorno"], filename), '{0}/{1}'.format(
                                config_env["path_retorno_recepcionados"], filename))

                        else:
                            shutil.move('{0}/{1}'.format(config_env["path_retorno"], filename), '{0}/{1}'.format(
                                config_env["path_retorno_nao_recepcionados"], filename))
                            print('Não baixou completo')
            else:
                print('Sem arquivos retornos para a data de hoje!')
                return False
        return True
    except Exception as ex:
        print('Erro na função return_ret_ftp')
        print(ex)
        return False
