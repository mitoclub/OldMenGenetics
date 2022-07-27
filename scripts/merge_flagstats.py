import os
import glob
import numpy as np
import pandas as pd

path_to_dir = "data/interim/mapping_stats/"
path_to_out = "data/processed/flagstats.csv"

data = []
for fname in os.listdir(path_to_dir):
    fp = os.path.join(path_to_dir, fname)
    sample = fname.removesuffix(".txt")
    with open(fp) as fin:
        one_data = {"Sample": sample}
        for line in fin:
            row = line.strip().split("\t")
            value, column = row[0], row[2]
            one_data[column] = value.replace("%", "")
        data.append(one_data)

df = pd.DataFrame(data)
df.to_csv(path_to_out, index=None)
