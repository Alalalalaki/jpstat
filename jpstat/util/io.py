import pandas as pd

from ..config import options

def read(path):
    file_format = options["options.file_format"]
    if file_format == "pkl":
        df = pd.read_pickle(path)
    elif file_format == "csv":
        df = pd.read_csv(path)
    elif file_format == "feather":
        df = pd.read_feather(path)
    return df

def save(df, path):
    file_format = options["options.file_format"]
    if file_format == "pkl":
        df.save_pickle(path)
    elif file_format == "csv":
        df.save_csv(path)
    elif file_format == "feather":
        df.save_feather(path)

