"""
find not inserted data from es
"""
from track_elastic_search import ElasticAPI



if __name__ == "__main__":
    es = ElasticAPI()
    es.insert_data()
    
    