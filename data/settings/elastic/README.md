# Elastic 포팅 메뉴얼

### 개발 환경

- Elasticsearch : 8.12.2
- kibana : 8.12.2

#### 모든 매뉴얼은 setts/elastic 에서 진행합니다.


### How to Install

### Environment Variables

- Elastic Username : elastic
- Kibana Username : elastic

| Key | Value Example | Description |
| --- | --- | --- |
| ELASTIC_CERTS_DIR | /usr/share/elasticsearch/data/certs | Elasticsearch 3개의 클러스터에 동일한 ca 인증서를 발급받기 위한 입니다. |
| ELASTIC_DATA_DIR | /usr/share/elasticsearch/data/ | EC2에 3개의 클러스터를 올리기 때문에 공유하는 폴더을 지정합니다. |
| ELASITC_CONFIG_DIR | /usr/share/elasticsearch/config | EC2  |
| ELASTIC_PASSWORD | elastic | Elasticsearch 패스워드 |
| KIBANA_PASSWORD | changeme | Kibana 패스워드 |
| STACK_VERSION | 8.12.2 | ELK 버전 정보 |
| CLUSTER_NAME | elastic-cluster | docker 클러스터 명 |
| LICENSE | basic | 라이센스 명 |
| ES_PORT | 9200 | ElasticSearch 포트 |
| KIBANA_PORT | 5601 | Kibana 포트 |
| MEM_LIMIT | 1073741824 | 메모리 제한 설정 |