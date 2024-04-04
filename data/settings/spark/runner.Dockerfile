FROM spark-container

COPY ../../. /opt/spark/app

COPY ./run-both.sh /opt/spark/sbin

RUN pip install -r /opt/spark/app/requirements.txt
RUN chmod +x /opt/spark/sbin/run-both.sh
WORKDIR /opt/spark/sbin


ENTRYPOINT ["./run-both.sh"]