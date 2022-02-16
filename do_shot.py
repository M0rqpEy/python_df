import pandas as pd
# import numpy as np
# import polars as pl
import some_funcs as sf
import time
import multiprocessing as mp


def main():
    df = pd.read_csv("/home/q/papka/sameshit/exp_1/data/data_20_21_e1.csv")
    print(df.head(2).loc[:, "Date"])
    sf.add_result_cols(df)
    sf.drop_fm_cols(df)

    gr = df.groupby("Date")
    total_list = sf.get_list_data_multipr(gr.groups.values())

    # тест. вивід в термінал
    q = mp.Queue()
    all_prs = []
    for i, data in enumerate(total_list):
        pr = mp.Process(target=sf.some_name_func,
                        args=(data, df, q),
                        name=f"pr-{i}"
                        )
        pr.start()
        all_prs.append(pr)

    rez_l = []
    for pr in all_prs:
        rez = q.get()
        rez_l.append(rez)
        print(f"{pr.name} =  {rez}")
        pr.join()

    sf.get_rez_dict(rez_l)


if __name__ == "__main__":
    start_t = time.perf_counter()
    main()
    print(f"time = {(time.perf_counter() - start_t):.3f} s")
