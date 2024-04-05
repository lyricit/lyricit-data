import os, sys
import re
import time

import threading
import base64
import json,csv
import queue
import spotify
import requests

from util.tools.logger import Logger



def get_spotify_access_token(client_id: str, client_secret: str) -> dict:
    """
    - Spotify API를 사용할 때, 필요한 Token 인증 방식
    - 1시간동안 유효한 토큰 발급
    """
    auth_header = base64.b64encode(
        "{}:{}".format(client_id, client_secret).encode("utf-8")
    ).decode(
        "ascii"
    )  # Base64로 인코딩된 인증 헤더 생성
    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {auth_header}"}
    payload = {"grant_type": "client_credentials"}
    response = requests.post(token_url, data=payload, headers=headers)
    access_token = json.loads(response.text)["access_token"]

    return {"Authorization": f"Bearer {access_token}"}

def parse_string_title(text: str) -> str:
    text = re.split(r"\(|-", text, 1)[0]  # ()와 - 전까지 사용
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    return text

def parse_string_artist(text: str) -> str:
    text = text.split(",", 1)[0]
    text = text.lower()
    return text

def change_json_to_list(title: str, data: json) -> list:
    """
    데이터가 다른 데이터가 나올까봐 track명과 title이 일치할 경우만 Spotify 정보 가져오기
    -> 안나오는 경우가 많아서 spotify에 있는 정보를 전체를 넣는다.

    다음과 같은 케이스가 있어서 일단 다 넣었다...
    눈의 꽃(드라마 "미안하다 사랑한다")
    눈의 꽃 - 미안하다, 사랑한다 (Original Television Soundtrack)
    """
    item = data["tracks"]["items"][0]
    track_id = item["id"]
    track_name = item["name"]
    track_artist = ", ".join(artist["name"] for artist in item["artists"])
    album_image_url_300 = item["album"]["images"][1]["url"]
    album_image_url_64 = item["album"]["images"][2]["url"]
    is_playable = item["is_playable"]
    preview_play_url = item["preview_url"]
    popularity = item["popularity"]
    return [
        track_id,
        track_name,
        track_artist,
        album_image_url_300,
        album_image_url_64,
        is_playable,
        preview_play_url,
        popularity,
    ]

def extract_spotify_track(line: list, access_token: dict) -> list:
    """
    Spotify 제목, 가수를 기준으로 조회한다.
    track id와 노래 정보, 앨범 커버, 음악 미리 듣기 등을 수집한다.
    가사 정보와 합친다.
    """

    url = "https://api.spotify.com/v1/search"
    parse_title = parse_string_title(line[chart_header_dict["title"]])
    parse_artist = parse_string_artist(line[chart_header_dict["artist"]])

    params = {
        "q": f"track={parse_title}?artist={parse_artist}",
        "type": "track",
        "market": "KR",
        "locale": "ko-KR",
        "limit": 20,
        "offset": 0,
    }

    # 초기화
    retries = 0
    max_retries = 5

    while retries < max_retries:

        response = requests.get(url, headers=access_token, params=params)
        data = response.json()
        if response.status_code == 200:
            title = line[chart_header_dict["title"]]
            artist = line[chart_header_dict["artist"]]
            # pprint.pprint(data)
            try:
                logger.info(f"[SUCCESS] :: {title} - {artist}")
                spotify_info = change_json_to_list(title, data)
            except Exception as e:
                # data json에 해당하는 값이 없을 경우
                logger.info(
                    f"[MISS] :: {line[chart_header_dict['title']]} - {line[chart_header_dict['artist']]}"
                )

            return line + spotify_info  # Spotify 조회 정보

        elif response.status_code == 429:
            retry_after = json.loads(response.headers)["Retry-After"]
            time.sleep(int(retry_after))
            print(f"time sleep {retry_after}")
            retries += 1
        else:
            # Spotify에 데이터가 없는 경우
            error_q.put(["error"] + line)
            logger.info(
                f"[ERROR] :: {line[chart_header_dict['title']]} - {line[chart_header_dict['artist']]}"
            )

def change_header_dict(header: list) -> dict:
    """
    저장한 헤더 값이 변경 될 것이기 때문에 함수
    """
    return {header_name: idx for idx, header_name in enumerate(header)}

def add_lists_to_csv(file_path, lists) -> None:
    """
    만들어둔 csv 파일에 list 추가
    """
    with open(file_path, "a", encoding="utf-8-sig") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(lists)

def run_thread(start, end, data_q, error_q, token_queue) -> None:

    count = 0
    thread_extract_list = []
    for idx, line in enumerate(chart_data_list[start:end]):
        access_token = token_queue.get()
        try:
            # spotify 데이터 수집
            spotify_info = extract_spotify_track(line, access_token)
            thread_extract_list.append(spotify_info)  # Thread 단위로 list 추가
            count += 1  # track count
            data_q.put(1)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            error_lineno = exc_tb.tb_lineno
            error_q.put(line + [e, error_lineno])
            thread_extract_list.append([])
            count += 1
        token_queue.put(access_token)
    add_lists_to_csv(spotify_extract_data_path, thread_extract_list)
    logger.info(f"THREAD DONE || track count :: {count}")


if __name__ == "__main__":

    logger = Logger().get_logger()

    # DATA_PATH = "./data/kysing/"
    DATA_PATH = "data/melon/"
    ES_BULK_PATH = "bulk/"
    SPOTIFY_PATH = "data/spotify/"
    ERROR_PATH = "data/error/"
    current_directory_path = "/" + "/".join(os.path.realpath(__file__).split("/")[:-1])

    ################################
    #       Client 정보 입력
    ################################
    # 파일 열기
    with open('spotify_token.json', 'r') as file:
        # JSON 데이터를 Python 딕셔너리로 변환
        spotify_tokens = json.load(file)

    token_queue = queue.Queue()
    for client_id, client_secret in spotify_tokens.values():
        token_queue.put(get_spotify_access_token(client_id, client_secret))


    ################################
    #        header파일 열기
    ################################
    spotify_header = [
        "track_id",
        "track_name",
        "track_artist",
        "album_image_url_300",
        "album_image_url_64",
        "is_playable",
        "preview_play_url",
        "popularity",
    ]
    m_chart_header = [
        "code","title","artist","lyric"
    ]
    unique_header = ["Unnamed: 0", "title", "singer", "year", "month", "song_id"]

    spotify_header_dict = change_header_dict(spotify_header)

    chart_header_dict = change_header_dict(m_chart_header)


    ################################
    #       csv 파일 열기
    ################################

    """"
    일단 한개 csv 파일만
    """
    chart_data_list = []

    with open(
        "data/melon/melon_chart.csv", "r", encoding="utf-8-sig"
    ) as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        for line in csvreader:
            chart_data_list.append(line)

    ################################
    #       csv 파일 쓰기
    ################################
    spotify_extract_data_path = SPOTIFY_PATH + "melon_chart_new.csv"

    with open(spotify_extract_data_path, "w", encoding="utf-8-sig") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(m_chart_header + spotify_header)

    #################################
    #       Thread
    #################################
    data_q = queue.Queue()
    error_q = queue.Queue()

    thread_count = 20
    thread_list = []

    work = len(chart_data_list) // thread_count

    for i in range(thread_count):
        start = i * work

        if i == thread_count - 1:
            end = len(chart_data_list)
        else:
            end = (i + 1) * work
        thread_list.append(
            threading.Thread(
                target=run_thread, args=(start, end, data_q, error_q, token_queue)
            )
        )

    [thread.start() for thread in thread_list]
    [thread.join() for thread in thread_list]

    data_count = data_q.qsize()
    error_count = error_q.qsize()

    if error_count != 0:
        os.makedirs(ERROR_PATH, exist_ok=True)
        with open(
            ERROR_PATH + "error_spotify_data.csv", "w", encoding="utf-8-sig"
        ) as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["track_key", "error_msg", "error_lineno"])

            while not error_q.empty():
                csvwriter.writerow([error_q.get()])

    print("===============================")
    print(f"total_target_count :: {len(chart_data_list)}")
    print(f"data_count :: {data_count}")
    print(f"error_count :: {error_count}")
    print(f"total_data_count :: {data_count + error_count}")
    print("================================")
    print("         종료        ")
