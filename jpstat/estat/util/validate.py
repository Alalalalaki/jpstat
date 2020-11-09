import string
import warnings
from ...config import _get_option


class ParaError(Exception):
    def __init__(self, msg, para):
        super(ParaError, self).__init__(msg)
        self.para = para


class QueryError(Exception):
    def __init__(self, msg, response):
        super(QueryError, self).__init__(msg)
        self.response = response


def validate_api_key(key):
    API_KEY_LENGTH = 40
    if len(key) > API_KEY_LENGTH:
        key = key[:API_KEY_LENGTH]
        msg = "API key too long. Should be {API_KEY_LENGTH} characters"
        warnings.warn(msg)
    elif len(key) < API_KEY_LENGTH:
        msg = "API key too short. Should be {API_KEY_LENGTH} characters"
        raise ValueError(msg)

    if not all(i in string.hexdigits for i in key):
        msg = "API key {} contains invalid characters".format(key)
        raise ValueError(msg)


_get_option("estat", "api_key").validator = validate_api_key


def validate_list_para(params):
    _param_keys = ['statsCode', 'searchWord',
                   'surveyYears', 'openYears', 'statsField', 'searchKind',
                   'statsNameList', 'startPosition', 'limit']
    for k in params:
        if k not in _param_keys:
            msg = f"Invalid parameter: {k}"
            raise ParaError(msg, params)

    params = {k: v.encode() for k, v in params.items() if v}

    if len(params) == 0:
        msg = "No valid parameters."
        raise ParaError(msg, params)

    return params


def validate_query(res, root_meta):
    if res.status_code == 200:
        data = res.json()[root_meta]
    else:
        msg = f"Request failed unexpectedly with code {res.status_code}"
        raise QueryError(msg, res)
    status = data['RESULT']['STATUS']
    if status not in [0, 1]:
        error_msg = data['RESULT']['ERROR_MSG']
        msg = f"Request failed unexpectedly with code {status}: {error_msg}"
        raise QueryError(msg, res)
    return data

