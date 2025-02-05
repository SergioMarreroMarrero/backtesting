import datetime

def ms_to_dt(ms: int)-> datetime.datetime:
    """
    Convertimos timestamp en milisegundos (milisegundos medidos desde 1 enero 1970) a formato datetime
    :param ms:
    :return:
    """
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.UTC)