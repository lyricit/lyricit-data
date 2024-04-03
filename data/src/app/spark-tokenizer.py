"""
tokenizing and count for elastic dictionary and game words

"""
import re

import nltk
import pandas as pd
from konlpy.tag import Okt
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf

nltk.download("punkt")



class Tokenizer:
    """
    Tokenizer class
    
    """
    @classmethod
    def english_dictionary(cls, my_str :str) -> str:
        """
        english tokenizer and make string set
        """
        sets = set(
            [i.lower() for i in nltk.word_tokenize(re.sub(r"[^a-zA-Z\s]", "", my_str))]
        )
        return " ".join(sets)

    @classmethod    
    def korean_dictionary(cls, my_str:str) -> str:
        """
        korean tokenizer and make string set
        """
        kor_str = re.sub(r"[^ㄱ-ㅣ가-힣\s]", "", my_str)
        okt = Okt()  # 함수 내부에서 Okt 인스턴스 생성
        sets = set(okt.nouns(kor_str))
        return " ".join(sets)


def make_dictionary(lang : str) -> str:
    """
    make dictionary
    """
    tokenizer = Tokenizer()
    spark = SparkSession.builder.getOrCreate()
    df_test = pd.read_csv("/opt/spark/app/data/data/melon_chart.csv")
    df_spark = spark.createDataFrame(df_test)

    udf_myfunc = None

    if lang == "eng":
        udf_myfunc = udf(tokenizer.english_dictionary)
    if lang == "kor":
        udf_myfunc = udf(tokenizer.korean_dictionary)

    # make tokenizer string 
    df_spark = df_spark.select(
    udf_myfunc(col("lyric")).alias(f"{lang}_lyrics"),  # 3
    col("lyric"),
    col("title"),
    )

    # word count by map reduce
    rdd = df_spark.select(f"{lang}_lyrics").rdd.flatMap(lambda x: x)
    rdd_stop = rdd.flatMap(lambda x: x.split())
    rdd_stop_cnt = (
        rdd_stop.map(lambda x: (x, 1))
        .groupByKey()
        .mapValues(sum)
        .sortBy(lambda x: x[1], ascending=False)
    )
    collected_data = rdd_stop_cnt.collect()
    #save to txt file
    with open(f"{lang}_output.txt", "w", encoding="utf-8") as file:
        for item in collected_data:
            print(item)
            file.write(item[0] + " " + str(item[1]) + "\n")


    spark.stop()


if __name__ == "__main__":
    print("=== Start Eng Dictionary===")
    make_dictionary("eng")
    # make_dictionary("kor")