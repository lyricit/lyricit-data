#  Data 포팅 메뉴얼

## 개발환경

- Elasticsearch : 8.12.2
- kibana : 8.12.2
- Ubuntu: 22.04
- Spark: 3.5.1
- Reverse Proxy Nginx (Nginx Proxy Manager) : 2.11.1
- Portainer : 2.19

#### Docker Compose

- Nginx Proxy Manger
- ElasticSearch

#### Dockerfile

- Spark

#### 모든 매뉴얼은 settings에서 진행합니다.


---

### How to Install Elasticsearch Container

1. `.env` 파일에 환경변수를 설정해줍니다.

2. `docker-compose` 파일을 이용해서 elasitc cluster 컨테이너를 만들어 줍니다.
    - 해당 프로젝트는 Nginx Proxy Manger 와 docker-network로 통신하므로 docker-compose 파일 내 network 탭을 삭제합니다.

```bash
docker compose up -d
```


#### Environment Variables

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





### How to Install Spark Container

1. Dockerfile을 활용해 베이스가 될 spark-container 이미지를 만들어줍니다.

```bash
docker build --tag spark-container .
```

2. standalone으로 spark master 하나와 spark worker 3개를 생성할 env파일을 포함한 spark runner image를 빌드합니다.

```bash
docker build -f runner.Dockfile --tag sparkrunner .
```

3. sparkrunnerimage를 기반으로 컨테이너를 생성합니다.

```bash
// /frontend
docker run -itd -p 8080:8080 -p 4040:4040 -h sparkrunner -v data:/opt/spark/app --name sparkrunner sparkrunner /bin/bash
```


4. 분산 처리 코드는 다음 명령어로 실행합니다.
```bash
./spark-submit --master sparkr://spark-runner:7077 {실행 파일}
```

### Python

#### .env 파일

```toml

# Elasticsearch 접근 host 예시: https://127.0.0.1:9200
ELASTIC_HOST=
# Elasticsearch ssh 접근 API KEY :
ELASTIC_API_KEY=

# Elasticsearch 사용 Index 버전 정보
ELASTIC_TRACKS_VERSION=

# 저장 파일
LOG_DIR = "/data/log"
DATA_PATH = "/data/source"
```

- elasticsearch 접근을 위한 API Key 발급
    - [Create API key API | Elasticsearch Guide [8.12] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html)

```toml
curl -X POST "localhost:9200/_security/api_key?pretty" -H 'Content-Type: application/json' -d'
{
  "name": "my-api-key",
  "expiration": "1d",   
  "role_descriptors": { 
    "role-a": {
      "cluster": ["all"],
      "indices": [
        {
          "names": ["index-a*"],
          "privileges": ["read"]
        }
      ]
    },
    "role-b": {
      "cluster": ["all"],
      "indices": [
        {
          "names": ["index-b*"],
          "privileges": ["all"]
        }
      ]
    }
  },
  "metadata": {
    "application": "my-application",
    "environment": {
       "level": 1,
       "trusted": true,
       "tags": ["dev", "staging"]
    }
  }
}
```