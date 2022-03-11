from datetime import datetime, timedelta
import datetime as dt_time


def monta_nomenclatura_rem():
    # 0002-20200105083325.REM
    dt_nomenclatura = data_hoje_aaaammddhhmmss('')
    return '0002-{0}.REM'.format(dt_nomenclatura)

# retorna data hoje AAAA[separador]MM[separador]DD


def data_hoje_aaaammdd(separador=''):
    '''retorna string data'''
    now = datetime.now()
    dateFormatted = '{0}{3}{1}{3}{2}'.format(str(now.year).zfill(
        4), str(now.month).zfill(2), str(now.day).zfill(2), separador)
    return dateFormatted

# retorna data hoje AAAA[separador]MM[separador]DD HHMMSS


def data_hoje_aaaammddhhmmss(separador=''):
    '''retorna string data'''
    now = datetime.now()
    dateFormatted = '{0}{6}{1}{6}{2}{3}{4}{5}'.format(str(now.year).zfill(4), str(now.month).zfill(2), str(
        now.day).zfill(2), str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2), separador)
    return dateFormatted

# retorna data de ontem AAAAMMDD


def data_ontem_aaaammdd(separador=''):
    '''retorna string data'''
    now = datetime.now() - dt_time.timedelta(days=1)
    dateFormatted = '{0}{1}{2}'.format(str(now.year).zfill(
        4), str(now.month).zfill(2), str(now.day).zfill(2))
    return dateFormatted

# retorna data de ontem AAAAMMDD HH:MM:SS


def dt_ctrl():
    now = datetime.now()
    dateFormatted = '{0}{1}{2} {3}:{4}:{5}'.format(str(now.year).zfill(4), str(now.month).zfill(2), str(
        now.day).zfill(2), str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2))
    return dateFormatted
