import pandas as pd
from importlib import resources


def load_mercari():

    with resources.path("eccd_datasets.mercari", "mercari.parquet") as df:
        dataset = pd.read_parquet(df)

    return dataset

