import os
import errno

import logging
from dotenv import load_dotenv


class Logger :

    def __init__(self) :
        import datetime

        load_dotenv()

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H:%M:%S")
        ymd = now.strftime("%Y-%m-%d")


        # log formatter 생성
        self.logger = logging.getLogger(timestamp)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # stream handler 생성
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)

        # 로그 파일 경로 확인 및 설정 
        log_directory_path = os.getenv('LOG_DIR') + "/" + ymd 
        self.ensuer_log_directory_exists(log_directory_path)

        # 파일 핸들러 설정
        file_handler = logging.FileHandler(log_directory_path + f"/{timestamp}.log")
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def ensuer_log_directory_exists(self, log_directory_path : str) -> None:
        """
        log dir 이 존재하지 않으면, 생성
        """

        try :
            if not os.path.isdir(log_directory_path) :
                os.makedirs(log_directory_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory")
                raise

    def get_logger(self) :
        """
        logger instance 반환
        """
        return self.logger

if __name__ == "__main__" :
    """
    사용 예시
    """
    mylogger = Logger().get_logger()
    mylogger.info("This is an info message")    