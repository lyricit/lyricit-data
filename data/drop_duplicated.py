"""
find not inserted data from es
"""
import pandas as pd
from track_elastic_search import ElasticAPI

def delete_duplicated() -> None:
    """
    delete duplicated data
    """
    df_melon = pd.read_csv("data/melon/melon_chart.csv")
    in_data = ElasticAPI.data_isin(["m"+str(i) for i in df_melon["code"]])
    in_dataset = []
    
    for i in in_data:
        in_dataset.append(int(i[1:]))
    
    not_in_data = set(df_melon["code"].values) - set(in_dataset)

    print("=====================================")
    print()
    print("Drop Duplicate Data..................")
    print(f"data decrease!!  {df_melon.shape[0]} {in_data} {len(not_in_data)}")
    print("=====================================")
    
    df_melon = df_melon[df_melon["code"].isin(not_in_data)]
    df_melon.to_csv("data/melon/melon_chart.csv", index=False)

if __name__ == "__main__":
    delete_duplicated()
    