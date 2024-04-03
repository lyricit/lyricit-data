"""
kysing crawler

get kysing chart by genre track ids, artist names, track titles
"""

import sys

import requests
from bs4 import BeautifulSoup


# File Location 
DATA_PATH = "./data/kysing/"
header = ["index", "song_number","title","artist","lyrics","composer","written","release_date"]


def crawl_genre(genre_num : int) : 
    import csv
    
    f = open(DATA_PATH + f"kysing_chart_genre{genre_num}_data.csv", "w", encoding = "utf-8-sig")
    writer = csv.writer(f)
    writer.writerow(header)


    # genre query field가 조건에 따라 변경된다.
    if genre_num == 0 : 
        genre_num = ""
    if genre_num == 8 : 
        q_genre_string = "gb=8"
    else :
        q_genre_string = "genre="
        if genre_num == 0 :
            q_genre_string += ""
        else :
            q_genre_string += "{:02}".format(genre_num)
        
    
    # page num 
    for page_num in range(1,3) :
        response = requests.get(f'https://kysing.kr/genre-polular/?{q_genre_string}&range={page_num}')
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        chart_list = soup.find_all("ul", class_ = "popular_chart_list")
        
        for idx, chart in enumerate(chart_list) : 
            
            chart_number = chart.find("li", class_ = "popular_chart_num").text
            if chart_number == "곡번호" :   # 첫번째 테이블이라면 넘기기
                continue
            
            chart_rank = 50+idx if page_num == 2 else idx
            
            song_number = chart.find("li", class_ = "popular_chart_num").text
            chart_info = chart.find("li", class_ = "popular_chart_tit")              # 제목, 가수, 가사를 포함하는 정보
            song_title = chart_info.find("span", class_ = "tit").text.strip()
            song_artist = chart_info.find("span", class_ = "tit mo-art").text.strip()
            song_lyrics = processing_lyric(chart_info.find('div', class_='LyricsCont').text.strip())
            song_composer = chart.find("li", class_ = "popular_chart_cmp").text.strip()
            song_written = chart.find("li", class_= "popular_chart_wrt").text.strip()
            song_release = chart.find("li", class_ = "popular_chart_rel").text
            print(f'[{chart_rank}/100] ({song_number}) {song_title} - {song_artist}')
            writer.writerow([chart_rank, song_number,song_title, song_artist, song_lyrics, song_composer, song_written, song_release])
            
        
    f.close() # csv 종료

def processing_lyric(lyric : str) -> str :
    lines = lyric.split('\n')
    return '\n'.join(lines[2:])
    
        
if __name__ == "__main__" :
    
    GENRE_CNT = 9
    for genre_num in range(GENRE_CNT) : 
        if genre_num == 7 : continue # 외국 노래 인기곡
        crawl_genre(genre_num)