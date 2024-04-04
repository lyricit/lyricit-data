#  SPARK 포팅 매뉴얼

## 개발환경

- Ubuntu: 22.04
- Spark: 3.5.1

#### 모든 매뉴얼은 settings/spark에서 진행합니다.

### How to Install

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