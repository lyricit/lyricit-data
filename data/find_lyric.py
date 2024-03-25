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
        for s in soup.find("div", attrs={"class": "lyric"}):
            lyric += s.text.strip()
            lyric += "\n"
        lyric = lyric.replace("\n\n", "\n")

        return lyric


if __name__ == "__main__":
    app = Crawl()
    df = pd.read_csv("data/melon_chart.csv")
    df["lyric"] = df["track_id"].apply(lambda x: app.get_lyric(str(x)))
    df.to_csv("data/melon_chart.csv", index=False)
