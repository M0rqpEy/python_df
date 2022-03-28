import pandas as pd
import os
# import numpy as np
# import polars as pl
import some_funcs as sf
import time
import multiprocessing as mp


def do_work(file_name):
    # df = pd.read_csv("/home/q/papka/sameshit/exp_1/data/data_19_20_d1.csv")
    df = pd.read_csv(f"./csv/pre_data/{file_name}")
    sf.add_result_cols(df)
    sf.drop_fm_cols(df)

    # для тестів
    # df = df.loc[:150, :]

    gr = df.groupby("Date")
    total_list = sf.get_list_data_multipr(gr.groups.values())

    # тест. вивід в термінал
    q = mp.Queue()
    with mp.Manager() as manager:
        all_prs = []
        man_dict = manager.dict()
        for i, data in enumerate(total_list):
            pr_name = f"pr-{i}"
            pr = mp.Process(target=sf.some_name_func,
                            # args=(data, df, q),
                            args=(data, df, man_dict, pr_name),
                            name=pr_name
                            )
            pr.start()
            all_prs.append(pr)

        # while not q.empty():
            # q.get()
            # print("shit")

        rez_l = []
        for pr in all_prs:
            # rez = q.get()
            # rez_l.append(rez)
            # print(f"{pr.name} =  {rez}")
            pr.join()
        #print(man_dict)
        rez_d = {**man_dict}
        sf.get_rez_dict_v2(rez_d, file_name)
        rez_d = {}


def main():
    for file_name in os.listdir("./csv/pre_data"):
        # if "21_22" in file_name:
        if True:
            print(file_name)
            # continue
            do_work(file_name)
            print(f"done - {file_name}")
            # break


if __name__ == "__main__":
    start_t = time.perf_counter()
    main()
    print(f"time = {(time.perf_counter() - start_t):.3f} s")
