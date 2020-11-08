import pandas as pd


def clean_dict_cols(df, cols, key='$'):
    df = df.copy()
    for c in cols:
        df[c] = df[c].apply(lambda x: x.get(key) if isinstance(x, dict) else x)
    return df
