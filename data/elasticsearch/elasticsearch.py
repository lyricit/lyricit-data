"""
Elastic api
"""
import os
import json
import csv
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
import certifi

class ElasticSearchAPI :
    """
    Elastic search insert API
    """
    load_dotenv()
    ELASTIC_HOST = os.environ.get("ELASTIC_HOST")
    ELASTIC_API_KEY = os.environ.get("ELASTIC_API_KEY")
    ELASTIC_INDEX_NAME = "tracks_" + os.environ.get("ELASTIC_TRACKS_VERSION")

    def __init__(self) : 
        """
        elastic search Client 와 연결한다.
        """
        self.es = Elasticsearch(
            hosts = self.ELASTIC_HOST,
            api_key = self.ELASTIC_API_KEY
        )
    
    @classmethod
    def search_track(self) :
        response = self.es.search(
            index = self.ELASTIC_INDEX_NAME,
            body = {
                "query" : {
                    "match" : {
                        "lyrics" : "사랑"
                    }
                }
            }
        )
        
        print(response)
        print("test")


    # @classmethod
    # def bulk_data(self, data : list) : 

    #     # 먼저 



if __name__ == "__main__" :
    es_client = ElasticSearchAPI()
    es_client.search_track()