import os
import shutil
import zipfile
from pathlib import Path

from libpysal.examples import load_example

Path("data/baltimore").mkdir(parents=True, exist_ok=True)
Path("data/berlin").mkdir(parents=True, exist_ok=True)
Path("data/california").mkdir(parents=True, exist_ok=True)

baltim = load_example("baltim")
berlin = load_example("berlin")
for file in baltim.get_file_list():
    shutil.copy(file, "data/baltimore")

for file in berlin.get_file_list():
    shutil.copy(file, "data/berlin")

for file in os.listdir("data/berlin"):
    if file.endswith(".zip"):
        with zipfile.ZipFile(os.path.join("data/berlin", file), 'r') as zip_ref:
            zip_ref.extractall("data/berlin")
        os.remove(os.path.join("data/berlin", file))
