import os
import pandas as pd

from ..config import options
from .scrape import scrape_stat, scrape_list
from ..util import io
from ..util.download import download_file

def get_stat(update=False):
    file_format = options["options.file_format"]
    path = os.path.join(options["estat.data_dir"], f"file_stat.{file_format}")
    if os.path.exists(path) & (update == False):
        data = io.read(path)
    else:
        data = scrape_stat()
        io.save(data, path)
    return data


def get_list(statsCode, year=None, save=False):
    file_format = options["options.file_format"]
    path = os.path.join(options["estat.data_dir"], f"{statsCode}.{file_format}")
    if os.path.exists(path):
        data = io.read(path)
    else:
        data = scrape_list(statsCode=statsCode, year=year)
        if save:
            io.save(data, path)
    return data


def get_file(statsDataId, file_type, save_path=None, file_name=None):
    kind_map = {"EXCEL": "0", "CSV": "1", "PDF": "2"}
    type_map = {"EXCEL": "xls", "CSV": "csv", "PDF": "pdf"}
    assert file_type in type_map.keys(), f"file_type must be one in {type_map.keys()}"

    url = f'https://www.e-stat.go.jp/stat-search/file-download?statInfId={statsDataId}&fileKind={kind_map[file_type]}'

    if save_path is None:
        save_path = os.path.abspath(os.curdir)
    if file_name is None:
        file_name = f"{statsDataId}.{type_map[file_type]}"

    download_file(url, save_path, file_name=file_name)

