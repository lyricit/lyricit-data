FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install python3 -y && \
    apt-get install openjdk-8-jdk -y && \
    apt install python3-pip -y &&\
    pip3 install pandas &&\
    pip3 install pyspark &&\
    apt-get install wget -y && \
    wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz && \
    tar -xf spark-3.5.1-bin-hadoop3.tgz && \
    mv spark-3.5.1-bin-hadoop3 /opt/spark && \
    mkdir /opt/spark/logs && \
    rm *.tgz

COPY spark-env.sh /opt/spark/conf/spark-env.sh

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV SPARK_HOME /opt/spark
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3


WORKDIR /opt/spark/sbin
