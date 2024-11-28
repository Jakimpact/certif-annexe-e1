import os
from io import BytesIO

import duckdb
import pandas as pd
from PIL import Image 


# Variables 
parquet_folder = os.getenv("parquet_folder")
file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path).rsplit("/", 1)[0]
folder_path = dir_path + "/extracts/blobs/" + parquet_folder
images_path = folder_path + "/images"


# Récupération / visualisation des fichiers parquets
parquet_files = os.listdir(folder_path)
parquet_paths = [os.path.join(folder_path, file) for file in parquet_files if file.endswith(".parquet")]
parquets = duckdb.read_parquet(parquet_paths)
duckdb.sql("SELECT * FROM parquets LIMIT 5").show()

# Transformation des images bytes en png avec l'item id de l'image
os.makedirs(images_path, exist_ok=True)
df_images = duckdb.sql("SELECT image, item_ID FROM parquets").df()

test = df_images["image"][0]["bytes"]
test_path = images_path + "/" + df_images["item_ID"][0] + ".png"
img = Image.open(BytesIO(test))
img.save(test_path, format="PNG")

for index, row in df_images.iterrows():
    image_bytes = BytesIO(row["image"]["bytes"])
    image_path = images_path + "/" + row["item_ID"] + ".png"
    img = Image.open(image_bytes)
    img.save(image_path, format="PNG")

# Transformation des autres colonnes en csv
duckdb.sql("SELECT item_ID, query, title, position FROM parquets").write_csv((folder_path+"/images.csv"))

# Suppression des fichiers parquets
for parquet_path in parquet_paths:
    os.remove(parquet_path)