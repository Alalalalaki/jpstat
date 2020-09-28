"""
Read eStat data by using api
Ref:
https://www.e-stat.go.jp/api/api-info/api-spec
https://www.e-stat.go.jp/api/api-info/e-stat-manual3-0
"""

import os

import pandas as pd

import requests

from typing import Any, Dict, List, Optional, Sequence, Union

# from .config import key

BASE_URL = "http://api.e-stat.go.jp/rest/3.0/app/"
BASE_URL_JSON = BASE_URL + "json/"





