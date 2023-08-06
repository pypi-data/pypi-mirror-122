import pandas as pd
from importlib import resources


DATASETS = [
    "ae_com.parquet",
    "amazon_com.parquet",
    "btemptd_com.parquet",
    "calvinklein_com.parquet",
    "hankypanky_com.parquet",
    "macys_com.parquet",
    "shop_nordstrom_com.parquet",
    "us_topshop_com.parquet",
    "victoriassecret_com.parquet",
]

def load_lingerie():
    datasets = {}
    for dataset in DATASETS:
        with resources.path("eccd_datasets.lingerie", dataset) as df:
            datasets[dataset.split(".")[0]] = pd.read_parquet(df)

    return datasets

