import os
import json
import csv
from elasticsearch import Elasticsearch


class BaseElasticSearchClient:

    def __init__(self, index_name) :
        from dotenv import load_dotenv

        ES_HOST = os.environ.get("ELASTIC_HOST")
        ES_PORT = os.environ.get("ELASTIC_PORT")

        self.index_name = index_name
        self.client = Elasticsearch(f"http://{ES_HOST}:{ES_PORT}")
        