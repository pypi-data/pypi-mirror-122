import pandas as pd
with open("train_list.txt") as fh: l_train = fh.readlines()
with open("test_list.txt") as fh: l_test = fh.readlines()
with open("val_list.txt") as fh: l_val = fh.readlines()

l_all = l_train + l_test + l_val

# from PIL import Image
# import io


rows = []
for l in l_all:
    l_ = l.strip()
    parts = l_.split("/")
    if len(parts) > 1:
        with open(l_, "rb") as fh:
            img = fh.read()
        if len(parts) == 3:
            dataset, coarse_cat, name = parts
            fine_cat = coarse_cat
        elif len(parts) == 4:
            dataset, coarse_cat, fine_cat, name = parts
        else:
            print(parts)

        rows.append((dataset, coarse_cat, fine_cat, img))

df = pd.DataFrame(rows, columns=["dataset", "coarse_cat", "finegrained_cat", "image_data"])
df.to_parquet("images.parquet", compression="gzip")

# Image.open(io.BytesIO(img)).show()
