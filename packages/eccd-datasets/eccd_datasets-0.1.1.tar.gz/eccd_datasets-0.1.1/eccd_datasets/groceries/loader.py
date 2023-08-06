import pandas as pd
from importlib import resources


def load_images():
    with resources.path("eccd_datasets.groceries", "images2.parquet") as df:
        return pd.read_parquet(df)



# def load_filelist(dataset):

#     col_names = ["Coarse Category", "Fine Category", "Name", "Image Data"]
#     dataset_list =  resources.read_text("eccd_datasets.groceries", f"{dataset}_list.txt")

#     rows = []
#     for line in dataset_list.split("\n"):
#         image_data = resources.read_binary("eccd_datasets.groceries", line)
#         parts = line.split("/")
#         if len(parts) > 1:
#             name = parts[-1]
#             fine_cat = parts[-2]
#             if len(parts) == 3:
#                 coarse_cat = fine_cat
#             else:
#                 coarse_cat = parts[-3]
#             rows.append((coarse_cat, fine_cat, name, path))
#     dataset = pd.DataFrame(rows, columns=col_names)
#     return dataset

        

