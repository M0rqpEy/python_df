import pandas as pd
import multiprocessing as mp
import numpy as np
import time
import polars as pl
from some_funcs import get_all_ind


list_all_ind = get_all_ind(16)
#""" # numpy
rows = 40
cols = 20
some_df = pd.DataFrame(
    data=np.random.randint(0,3+1, size=(rows,cols)),
    columns=[f"col{i}" for i in range(cols)]
)
start = time.time()
c = 1
np_data = some_df.to_numpy()
for i in range(0,some_df.shape[0] -10, 5):
    # print(c)
    c +=1
    for idx in list_all_ind:
        # print(some_df.iloc[i:i+10, idx])
        print(np_data[i:i+10, idx])
        # print(pl.DataFrame(np_data[i:i+10, idx]))
print(time.time() - start)
""" # polars
some_df = pl.DataFrame(
    data=np.random.randint(0,3+1, size=(20,20)),
    columns=[f"col{i}" for i in range(20)]
)
some_df = some_df.with_row_count("id")

start = time.time()
c = 1
for i in range(0, some_df.shape[0]-10, 5):
    # print(c)
    c +=1
    for idx in list_all_ind:
        # print(some_df.row(i))
        # print(some_df.slice(i, 10))
        # print(some_df[i:i+10, idx])
        print(some_df[i:i+10, idx])
print(time.time() - start)
"""
