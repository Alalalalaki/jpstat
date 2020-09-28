from estat.io.estat import eStatReader


def DataReader(dataid, data_source='estat', start=None, end=None, appid=None, **kwargs):
    if data_source == 'estat':
        return eStatReader(dataid=dataid, appid=appid, **kwargs)
