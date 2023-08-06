"""
Simple ES singleton
"""
from typing import Dict

from elasticsearch import Elasticsearch
# noinspection PyProtectedMember
from elasticsearch.client import IndicesClient, _normalize_hosts
from singleton_decorator import singleton


@singleton
class ElasticSearchManager:
    """
    Simple getter for es
    """

    def __init__(self, url: str = 'localhost',
                 verify_certs=False) -> None:
        super().__init__()
        self._es = Elasticsearch([url], verify_certs=verify_certs)
        self._es_info = _normalize_hosts(url)
        self._ic = IndicesClient(self._es)

    def es(self) -> Elasticsearch:
        """
        Returns configured es instance
        :return: es instance
        """
        return self._es

    def ic(self) -> IndicesClient:
        """
        Returns configured ic instance
        :return: ic instance
        """
        return self._ic

    def info(self) -> Dict:
        """
        Returns es info
        :return: dict with info
        """
        return self._es_info
