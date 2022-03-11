from cofre import Cofre

# home producao
# path_home = "/home/geraldo/Documentos/FORTBRASIL/Desenvolvimento/Softnex/arquivos"

# home desenvolvimento


def get_config_env():
    cofre = Cofre()

# alterar o caminho no servidor que será salvo o projeto
    path_home = "/arquivos"
    config_env = {
        # FTP Softnex
        'host_ftp_softnex': cofre.get_secret_azure('FTP-SOFTNEX-HOST'),
        'port_ftp_softnex': cofre.get_secret_azure('FTP-SOFTNEX-PORT'),
        'username_ftp_softnex': cofre.get_secret_azure('FTP-SOFTNEX-USERNAME'),
        'passwd_ftp_softnex': cofre.get_secret_azure('FTP-SOFTNEX-PASSWORD'),
        'path_remote_rem': 'Softnex/Remessa',
        'path_remote_ret': 'Softnex/Retorno',

        # diretorios
        'path_remessa': '{0}/remessa'.format(path_home),  # remessa gerado
        'path_remessa_enviados': '{0}/remessa/enviados'.format(path_home),
        'path_retorno': '{0}/retorno'.format(path_home),
        'path_retorno_recepcionados': '{0}/retorno/recepcionados'.format(path_home),
        'path_retorno_nao_recepcionados': '{0}/retorno/nao_recepcionados'.format(path_home)
    }
    # config_env = {
    #     # FTP Softnex
    #     'host_ftp_softnex': 'ftp.fortbrasil.com.br',
    #     'port_ftp_softnex': '21',
    #     'username_ftp_softnex': 'ticonc',
    #     'passwd_ftp_softnex': 'acesso@123',
    #     'path_remote_rem': 'Softnex/Remessa',
    #     'path_remote_ret': 'Softnex/Retorno',

    #     # diretorios
    #     'path_remessa': '{0}/remessa'.format(path_home), #remessa gerado
    #     'path_remessa_enviados': '{0}/remessa/enviados'.format(path_home),
    #     'path_retorno': '{0}/retorno'.format(path_home),
    #     'path_retorno_recepcionados': '{0}/retorno/recepcionados'.format(path_home),
    #     'path_retorno_nao_recepcionados': '{0}/retorno/nao_recepcionados'.format(path_home)
    # }

    return config_env
