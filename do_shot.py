import pandas as pd
# import numpy as np
# import polars as pl
import some_funcs as sf
import time


def main():
    df = pd.read_csv("/home/q/papka/sameshit/exp_1/data/data_19_20_d1.csv")
    sf.add_result_cols(df)
    sf.drop_fm_cols(df)

    gr = df.groupby("Date")
    total_list = sf.get_list_data_multipr(gr.groups.values())


    # тест. вивід в термінал
    sf.some_name_func(total_list[0], df)

if __name__ == "__main__":
    start_t = time.perf_counter()
    main()
    print(f"time = {(time.perf_counter() - start_t):.3f} s")
