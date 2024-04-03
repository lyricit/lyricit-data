"""
Elastic api
"""
import os, sys
import json
import csv
import errno
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from util.tools.logger import Logger

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
        self.logger = Logger().get_logger()
        self.es = Elasticsearch(
            hosts = self.ELASTIC_HOST,
            api_key = self.ELASTIC_API_KEY
        )
        self.logger.info("Elasticsearch client has been initialized.")
        self.check_exist_index() # index 없으면 업데이트

    def load_index_settings(self) -> json:
        """
        index update version과 일치한지 검증한다.
        """
        with open("./settings/" + self.ELASTIC_INDEX_NAME + ".json", 'r') as file :
            settings = json.loads(file)
        return settings

    def check_exist_index(self) -> None:
        """
        index가 ElasticSearch에 존재하는 지 확인한다.
        만약 없다면, 혹은 버전이 업데이트 된다면, index를 새로 생성한다.
        """ 
        index_name = self.ELASTIC_INDEX_NAME
        if not self.es.indices.exists(index=index_name) : 
            settings = self.load_index_settings()
            response = self.es.indices.create(index = index_name, body = settings)
            self.logger.info(f"Created index {index_name} with settings file.")
        else : 
            self.logger.info(f"Index {index_name} already exists.")

    def search_by_query(self, query : dict) -> None:
        """
        search 
        """
        response = self.es.search(
            index = self.ELASTIC_INDEX_NAME,
            body = query
        )
        self.logger.info(f"Search completed with query : {response}")

    def search_by_code(self, list: list) -> list :
        """
        search로 code를 조회합니다.
        """
        response = self.es.search(
            index = self.ELASTIC_INDEX_NAME,
            body = {"query" : {"terms" : "code" : list}, "size" : 100}
        )
        self.logger.info(f"Search completed with list : {list}")

    def mapping_data(self, data:list) -> dict:
        """
        data를 documets로 매핑합니다.
        """
        title,artist, code, spotify_track_id,spotify_track_title,spotify_track_artist, lyrics ,spotify_is_playable,spotify_preview_play_url,spotify_album_image_url_64,spotify_album_image_url_300,spotify_popularity = data

        # 실제 문서 데이터
        document = {
            "code": code,
            "title": title,
            "artist": artist,
            "spotify_info": {
                "id": spotify_track_id,
                "title": spotify_track_title,
                "artist": spotify_track_artist,
                "preview_play_url": spotify_preview_play_url,
                "album_url": {
                    "image_size_300": spotify_album_image_url_300,
                    "image_size_64": spotify_album_image_url_64
                },
                "popularity": spotify_popularity
            },
            "lyrics": lyrics.replace("-", ""),
        }

        return document


    def bulk_data(self, chapter ,total_data : list) -> None: 
        """
        한꺼번에 insert 할 데이터를 만들고, ElasticSearch에 bulk 합니다.
        """

        self.logger.info(f"Total Data Count : {len(data)}")

        # index action meta data
        action = {"index": {"_index": index_name}}
        
        # change to mapping bulk type
        bulk_total_data = []
        for idx, data in enumerate(total_data) :
            document = mapping_data(data)
            bulk_total_data.append(json.dumps(action, ensure_ascii=False))  # 액션 메타데이터
            bulk_total_data.append(json.dumps(document, ensure_ascii=False))  # 실제 문서 데이터
        self.logger.info(f"Changed data to mapping format {len(bulk_total_data) / 2} ")

        # data insert 
        try : 
            # BULK 
            response = self.es.bulk(body='\n'.join(bulk_total_data) + '\n')
            if response["errors"] is False :
                self.logger.info(f"Success data bulk Chapter '{chapter}' Section")
            else :
                self.logger.error(f"ERROR || Fail data bulk Chapter '{chapter}' Section - check the data format")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            err_lineno = exc_tb.tb_lineno
            self.logger.error(f"ERROR || {err_lineno}")

        self.logger.info(f"Done bulk data.")

