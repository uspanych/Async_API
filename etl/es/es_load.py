import logging

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from config.settings import (
    ES_HOST,
    ES_PORT,
    ES_INDEX
)
from services.backoff import backoff
from .scheme import MOVIES_SCHEMA, GENRES_SCHEMA, PERSONS_SCHEMA

logger = logging.getLogger(__name__)


class ElasticService:
    """Класс загружает пачку данных в Elasticsearch."""

    def __init__(
            self,
    ):
        self.host = ES_HOST
        self.port = int(ES_PORT)
        self.index = ES_INDEX
        self.client = Elasticsearch(
            [
                {
                    'host': self.host, 'port': self.port,
                }
            ]
        )
        self.schema = {
            'movies': MOVIES_SCHEMA,
            'genres': GENRES_SCHEMA,
            'persons': PERSONS_SCHEMA,
        }

    @backoff()
    def check_schema(self):
        if not self.client.ping():
            raise ConnectionError('No connection to Elasticsearch')
        indexes = list(self.client.indices.get_alias().keys())
        for index in self.index.split(', '):
            if index not in indexes:
                logger.info('Index not found ElasticService')

                self.create_index(index)

    def create_index(
            self,
            index: str
    ):
        logger.info('Create Index ElasticService')
        self.client.indices.create(index=index, body=self.schema.get(index))

    @backoff()
    def load_data_to_es(
            self,
            data: list,
    ):
        self.check_schema()

        """
        document = [
            {
                "_index": item.index,
                "_id": item.id,
                "_source": item.dict()
            }
            for item in data
        ]
        """
        document = []

        for item in data:
            item = item.dict()
            id = item.get('id')
            index = item.pop('index')
            document.append(
                {
                    "_index": index,
                    "_id": id,
                    "_source": item,
                }
            )

        logger.info('Load data to Elasticsearch')

        bulk(self.client, document)
