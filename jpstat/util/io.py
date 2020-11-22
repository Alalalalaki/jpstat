import os
import pandas as pd

from ..config import options

def read(path):
    file_format = options["options.file_format"]
    if file_format == "pkl":
        df = pd.read_pickle(path)
    elif file_format == "csv":
        df = pd.read_csv(path, dtype=str)
    elif file_format == "feather":
        df = pd.read_feather(path)
    return df

def save(df, path):
    p_dir = os.path.dirname(path)
    if not os.path.isdir(p_dir):
        os.mkdir(p_dir)

    file_format = options["options.file_format"]
    if file_format == "pkl":
        df.to_pickle(path)
    elif file_format == "csv":
        df.to_csv(path, index=False)
    elif file_format == "feather":
        df.to_feather(path)

