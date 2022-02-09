import pandas as pd
import numpy as np
import time
import polars as pl
# from some_funcs import get_all_ind


# list_all_ind = get_all_ind(16)
c = 0
for _ in range(500):
    some_df = pl.DataFrame(
        data=np.random.randint(0,3+1, size=(20,8)),
        columns=[f"col{i}" for i in range(8)]
    )
    rez = some_df[some_df.is_duplicated()].distinct(keep="first")
    if rez.shape[0] > 0:
        print(some_df)
        mask = some_df.is_duplicated()
        print(some_df[mask])
        print(rez)
        for i in rez.rows():

            print(list(i))
        c += 1
print(c)
