"""
Core functions

To-Do:
  - over limit for get_data
"""

import sys
import pandas as pd

from .. import config
from .api import API
from .util.clean import clean_dict_cols


def get_list(statsCode=None, searchWord=None, outputRaw=False, key=None, lang=None, **kwargs):
    api = API(key=key, lang=lang)
    data = api.get_list(statsCode=statsCode, searchWord=searchWord, **kwargs)
    df = pd.DataFrame(data['DATALIST_INF']['TABLE_INF'])
    if outputRaw:
        return df
    cols_simple = ['@id', 'STAT_NAME', 'GOV_ORG',
                   'STATISTICS_NAME', 'TITLE',
                   'SURVEY_DATE', 'OPEN_DATE', 'OVERALL_TOTAL_NUMBER']
    df = df[cols_simple].pipe(clean_dict_cols, ['STAT_NAME', 'GOV_ORG', 'TITLE'])
    return df


def get_stat(key=None, lang=None,):
    api = API(key=key, lang=lang)
    data = api.get_list(statsNameList="Y")
    df = pd.DataFrame(data['DATALIST_INF']['LIST_INF'])
    df = df.pipe(clean_dict_cols, ['STAT_NAME', 'GOV_ORG'])
    return df


def get_data(statsDataId, return_note=True, key=None, lang=None,  **kwargs):
    api = API(key=key, lang=lang)
    data = api.get_data(statsDataId=statsDataId, **kwargs)
    df = pd.DataFrame(data['STATISTICAL_DATA']['DATA_INF']['VALUE'])

    res = data['STATISTICAL_DATA']['RESULT_INF']
    while 'NEXT_KEY' in res:
        _data = api.get_data(statsDataId=statsDataId, startPosition=res['NEXT_KEY'])
        _df = pd.DataFrame(_data['STATISTICAL_DATA']['DATA_INF']['VALUE'])
        df = pd.concat([df, _df], axis=0)

        sys.stdout.write(".")
        sys.stdout.flush()

        res = _data['STATISTICAL_DATA']['RESULT_INF']

    cats = data['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']
    for cat in cats:
        col_name = '@' + cat['@id']
        _cat_map = cat['CLASS']
        if isinstance(_cat_map, dict):
            _cat_map = [_cat_map]
        cat_map = {m['@code']: m['@name'] for m in _cat_map}
        df[cat['@name']] = df[col_name].map(cat_map)
        df.drop(col_name, axis=1, inplace=True)
    df['Value'] = df['$']
    df.drop('$', axis=1, inplace=True)
    if return_note:
        try:
            note = pd.DataFrame(data['STATISTICAL_DATA']['DATA_INF']['NOTE'])
            note = note.rename(columns={"$": "EXPLAIN"})
        except ValueError:
            note = data['STATISTICAL_DATA']['DATA_INF']['NOTE']
        return df, note
    else:
        return df
