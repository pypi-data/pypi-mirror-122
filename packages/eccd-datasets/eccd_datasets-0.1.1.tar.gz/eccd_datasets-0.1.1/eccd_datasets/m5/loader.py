import pandas as pd
from importlib import resources

DATASETS = [
        "calendar",
        "sales",
        "sell_prices",
]

def load_m5():
    datasets = {}
    for dataset in DATASETS:
        with resources.path("eccd_datasets.m5", dataset + ".parquet") as df:
            datasets[dataset] = pd.read_parquet(df)

    return datasets

