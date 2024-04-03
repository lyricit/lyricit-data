import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


class Crawl:
    """
    crawler class
    """

    def get_lyric(self: any, track_id: str) -> str:
        """
        get track id, artist name, track title from melon site
        """
        
        
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            + "AppleWebKit/537.36 (KHTML, like Gecko) "
            + "Chrome/109.0.0.0 Safari/537.36"
        }

        url = "https://www.melon.com/song/detail.htm?songId=" + track_id

        response = requests.get(url, headers=headers, timeout=10)
        soup = bs(response.text)
        lyric = ""
        if(soup.find("div", attrs={"class": "lyric"}) is not None):
            for s in soup.find("div", attrs={"class": "lyric"}):
                lyric += s.text.strip()
                lyric += "\n"
            lyric = lyric.replace("\n\n", "\n").replace("\n\n", "\n").replace("\n\n", "\n")
        print(track_id + " : " + lyric[:10] + "...")
        return lyric


if __name__ == "__main__":
    app = Crawl()
    df = pd.read_csv("data/melon/melon_chart.csv")
    
    df["lyric"] = df["code"].apply(lambda x: app.get_lyric(str(x)))
    print()
    print("===== Save to csv =====")
    df.to_csv("data/melon/melon_chart.csv", index=False)
