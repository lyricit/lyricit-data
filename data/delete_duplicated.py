"""
find not inserted data from es
"""
import pandas as pd
from track_elastic_search import ElasticAPI

def delete_duplicated() -> None:
    """
    delete duplicated data
    """
    df_melon = pd.read_csv("data/melon_chart.csv")
    new_data = ElasticAPI.data_isin(["m"+str(i) for i in df_melon["track_id"]])
    print(new_data)
    df_melon = df_melon[df_melon["track_id"].isin([int(i[1:]) for i in new_data])]
    df_melon.to_csv("data/melon_chart.csv", index=False)

if __name__ == "__main__":
    delete_duplicated()
    