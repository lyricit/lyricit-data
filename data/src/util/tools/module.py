
def read_csvfile(file_path: str) -> list :
    import pandas as pd

    df = pd.read_csv(file_path, header=None, skiprows=1)
    return df.tolist()

def exist_directory(file_path:str) -> bool : 
    import os

    if not os.path.isdir(file_path) : 
        os.makedirs(file_path)

def chunk_list(list:list, chunk_size:int) -> list :
    return [list[index : index + chunk_size] for index in range(0, len(list), chunk_size)]