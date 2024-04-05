"""
melon crawler

get today's melon chart track ids, artist names, track titles

"""

import sys, os

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

from dotenv import load_dotenv

# File Location 
load_dotenv()
data_path = os.getenv('DATA_PATH')


class Crawl:
    """
    crawler class
    """

    def run(self: any, data_path: str) -> None:
        """
        get track id, artist name, track title from melon site
        """

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            + "AppleWebKit/537.36 (KHTML, like Gecko) "
            + "Chrome/109.0.0.0 Safari/537.36"
        }

        url = "https://www.melon.com/chart/day/index.htm"

        response = requests.get(url, headers=headers, timeout=10)

        soup = bs(response.text, "lxml")
        get_time = soup.find_all("span", attrs={"class": "year"})[0].get_text()
        year, month, date = get_time.split(".")

        # song ids
        track_tags = soup.find_all("tr")
        track_ids = [
            int(track_tag["data-song-no"].strip()) for track_tag in track_tags[1:]
        ]

        # title ids
        title_tags = soup.find_all("div", attrs={"class": "ellipsis rank01"})
        titles = [title_tag.get_text().strip() for title_tag in title_tags]

        # singer ids
        artists_tags = soup.find_all("div", attrs={"class": "ellipsis rank02"})
        artists = [artists_tag.a.get_text().strip() for artists_tag in artists_tags]

        pd.DataFrame(
            {"code": track_ids, "title": titles, "artist": artists}
        ).to_csv(
            f"{data_path}/melon/melon_chart.csv",
            index=False,
            encoding="utf-8-sig",
        )


if __name__ == "__main__":

    app = Crawl()
    if len(sys.argv) != 2:
        print("-- spark home input need")
    else:
        app.run(sys.argv[1])
