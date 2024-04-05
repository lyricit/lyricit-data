import os, glob
import datetime

from dotenv import load_dotenv

from util.tools.module import read_csvfile, chunk_list
from util.tools.logger import Logger
from util.elastic.elastic_search import ElasticSearchAPI

ymd = datetime.datetime.now().strftime("%Y-%m-%d")

load_dotenv()
data_path = os.getenv('DATA_PATH')

if __name__ == "__main__" : 

    folder_path = os.path.join(data_path, "mart", ymd) # 폴더 경로
    total_file_list = glob.glob(folder_path + "/*")

    # 파일이 공용 경로에 업데이트 되어 있으면 파일 불러오기
    logger = Logger().get_logger()

    # 오늘 일자에 dir 가져오기
    if not os.path.exists(folder_path):
        logger.info("Can not find file from lyricit data directory ")

    for idx, file_path in enumerate(total_file_list) : 
        # 파일 한개씩 es로 bulk 한다.
        file_name = os.path.basename(file_path)
        logger.info(f"[{idx+1}/{len(total_file_list)}] :: Read csv file from {file_name}" )


        es_client = ElasticSearchAPI()                  # elastic client 연결
        es_client.check_exist_index()

        """
        Elastic Search에 Bulk 할 데이터를 분할 합니다.
        - 데이터 양이 많으면 es_connection이 종료되기 때문에 chunk 단위로 분할합니다
        """
        total_data_list = read_csvfile(file_path)         # csv파일을 list로 분리
        chunk_data_list = chunk_list(total_data_list, 500)

        for idx, data_list in enumerate(chunk_data_list) :
            es_client.bulk_data(idx + 1, data_list)

        logger.info(f"[{idx+1}/{len(total_file_list)}] :: Done insert Elastic Search {file_name}")