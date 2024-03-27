"""
search data from elastic search
"""
import os
import json
import csv
from dotenv import load_dotenv
from elasticsearch import Elasticsearch



class ElasticAPI:
    """
    Elastic search, insert API
    """
    load_dotenv()
    ES_HOST = os.environ.get("ELASTIC_HOST")
    ES_PORT = os.environ.get("ELASTIC_PORT")
    client = Elasticsearch(
        f"http://{ES_HOST}:{ES_PORT}"
    )
    index_name = "tracks"
    @classmethod
    def data_isin(cls, track_id_list: list) -> list:
        """
        check if index exists
        """
        response = cls.client.search(
            index="tracks",
            body={
                "query": {
                    "terms": {
                        "code": track_id_list
                    }
                }
            }
        )
        json_response = json.loads(json.dumps(response.body))
        
        return [ code_resp.get("_source").get("code") for code_resp in json_response.get("hits").get("hits")]


    @classmethod
    def insert_data(cls, data: dict):
        """
        insert data to elastic search
        """
        
if __name__ == "__main__":
    print(ElasticAPI.data_isin(["k87335", "m30829858", "m5742256", "test"]))
    