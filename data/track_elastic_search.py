"""
search data from elastic search
"""
import os
import json
import csv
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
import certifi
import pprint

class ElasticAPI:
    """
    Elastic search, insert API
    """
    load_dotenv()
    ES_HOST = os.environ.get("ELASTIC_HOST")
    ES_PORT = os.environ.get("ELASTIC_PORT")
    client = Elasticsearch(
        f"https://{ES_HOST}:{ES_PORT}",
        http_auth =('elastic','a109_lyricit'),
        verify_certs=False
    )
    index_name = "track"

    @classmethod
    def data_isin(cls, track_id_list: list) -> list:
        """
        check if index exists
        """
        print("data find!")
        print("track_id_list: ", track_id_list)
        print("=====================================")
        
        response = cls.client.search(
            index="tracks",
            body={
                "query": {
                    "terms": {
                        "code": track_id_list
                    }
                },
                "size": 100
            }
        )

        json_response = json.loads(json.dumps(response.body))
        with open("data/elastic_search.json", "w", encoding = "utf-8") as jsonfile : 
            jsonfile.write(json.dumps(json_response, indent = 4, ensure_ascii=False))

        data_in = [ code_resp.get("_source").get("code") for code_resp in json_response.get("hits").get("hits")]
        print("\n\n\n")
        print(data_in)
        return [ code_resp.get("_source").get("code") for code_resp in json_response.get("hits").get("hits")]


    @classmethod
    def insert_data(cls):
        """
        insert data to elastic search
        """
        print("insert data!")
        file_path = os.path.join("data", "spotify","melon_chart_new.csv")
        actions = []

        print("########################bulk data make start#########################")
        
        if os.path.isfile(file_path) :
            with open(file_path, 'r', encoding = "utf-8-sig") as csvfile :
                csvreader = csv.reader(csvfile)
                next(csvfile) # 첫번째 헤더 건너 뛰기
                actions = []
                for line in csvreader:

                    code,title,artist,lyrics,spotify_track_id,spotify_track_title,spotify_track_artist,spotify_album_image_url_300,spotify_album_image_url_64,is_playable,spotify_preview_play_url,spotify_popularity = line

                    action = {"index": {"_index": "tracks"}}
                    document = {
                        "code" : "m" + str(code),
                        "title" : title,
                        "artist" : artist,
                        "spotify_info" : {
                            "id" : spotify_track_id,
                            "title" : spotify_track_title,
                            "artist" : spotify_track_artist,
                            "preview_play_url" : spotify_preview_play_url,
                            "album_url" : {
                                "image_size_300" : spotify_album_image_url_300,
                                "image_size_64" : spotify_album_image_url_64
                            },
                            "popularity" : spotify_popularity
                        },
                        "lyrics" : lyrics
                    }
                    actions.append(json.dumps(action, ensure_ascii=False))
                    actions.append(json.dumps(document, ensure_ascii=False))
                # elastic에 100개 단위로 넣기 
                print('\n'.join(actions) + '\n')
                cls.client.bulk(body='\n'.join(actions) + '\n')
                # elastic에 100개 단위로 넣기 
            print("########################bulk data make end #########################")
            print("\n\n")
            print("########################bulk data insert start!#########################")
            # helpers.bulk(cls.client, actions)
            print("########################bulk data insert end!#########################")
        with open("./data/elatic_kysing_bulk.jsonl", "w", encoding = "utf-8") as jsonfile : 
            for line in actions :
                jsonfile.write(str(line)+ "\n")

if __name__ == "__main__":
    print(ElasticAPI.data_isin(["k87335", "m30829858", "m5742256", "test"]))
    