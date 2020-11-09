"""
Read eStat data by using api
Ref:
https://www.e-stat.go.jp/api/api-info/api-spec
https://www.e-stat.go.jp/api/api-info/e-stat-manual3-0


To-Do
  - somehow if parameter is not correctly specified, there would be no response until timeout
"""

import os

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from typing import Any, Dict, List, Optional, Sequence, Union

from ..config import options, setup_logger
from .util.validate import ParaError, QueryError, validate_list_para, validate_query

LOGGER = setup_logger(__name__)


class API:
    def __init__(self, key=None, lang=None):
        if key is None:
            KEY_ENV_NAME = options["estat.environment_variable"]
            if KEY_ENV_NAME in os.environ:
                key = os.environ[KEY_ENV_NAME]
            elif options["estat.api_key"] is not None:
                key = options["estat.api_key"]
            else:
                url = "https://www.e-stat.go.jp/api/"
                msg = f"BLS API key not detected. Please make one at {url}"
                msg += " and call `estat.options['estat.api_key']=key`"
                raise EnvironmentError(msg)
        if lang is None:
            lang = options["estat.data_lang"]

        self.key = key
        self.lang = lang

        self.api_ver = "3.0"
        self.api_type = "json"

        self.host = "http://api.e-stat.go.jp"
        self.params = {"appId": key}
        if lang == "E":
            self.params.update({"lang": lang})
        self._limit = 100_000

        self.sess = requests.Session()
        self.sess.mount(self.host, HTTPAdapter(max_retries=3))
        self.header = {'Access-Control-Allow-Origin': '*'}
        self.timeout = 60

    def build_url(self, mode):
        base_url = f"{self.host}/rest/{self.api_ver}/app/{self.api_type}/{mode}"
        return base_url

    def get_list(self, statsCode=None, searchWord=None,  **kwargs):
        """
        政府統計の総合窓口（e-Stat）で提供している統計表の情報を取得します。リクエストパラメータの指定により条件を絞った情報の取得も可能です。
        """
        url = self.build_url(mode="getStatsList")
        params = {'statsCode': statsCode, 'searchWord': searchWord}
        params.update(kwargs)
        params = validate_list_para(params)
        params = {**self.params, **params}

        res = self.sess.get(url, params=params, timeout=self.timeout)
        data = validate_query(res, root_meta='GET_STATS_LIST')
        return data

    def get_meta(self, ):
        """
        指定した統計表IDに対応するメタ情報（表章事項、分類事項、地域事項等）を取得します。
        """
        mode = "getMetaInfo"

    def get_data(self, statsDataId, **kwargs):
        """
        指定した統計表ID又はデータセットIDに対応する統計データ（数値データ）を取得します。
        """
        url = self.build_url(mode="getStatsData")
        params = {'statsDataId': statsDataId}
        params = {**self.params, **params}

        res = self.sess.get(url, params=params,)
        data = validate_query(res, root_meta='GET_STATS_DATA')
        return data


    def get_catalog(self,):
        """
        政府統計の総合窓口（e-Stat）で提供している統計表ファイルおよび統計データベースの情報を取得できます。統計表情報取得機能同様に、リクエストパラメータの指定により条件を絞った情報の取得も可能です。
        """
        mode = "getDataCatalog"
