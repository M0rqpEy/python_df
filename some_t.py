import pandas as pd
import math
import multiprocessing as mp
import numpy as np
import time
import polars as pl
from some_funcs import get_all_ind


list_all_ind = get_all_ind(16)
BUNCH = 15
MAX_PROCESSES = 11

def f(data, name_pr, d=None):
    for i in range(0, data.shape[0], 5):
        for idx in list_all_ind:
            rez = data[i:i+10, idx]
            un, count = np.unique(rez, axis=0, return_counts=True)
            rez = un[count>1]
            if rez.shape[0] > 0:
                print(rez)


def main():
    rows = 500
    cols = 20
    some_df = pl.DataFrame(
        data=np.random.randint(0,3+1, size=(rows, cols)),
        columns=[f"col{i}" for i in range(cols)]
    )
    some_df = some_df.with_row_count("id")
    print(some_df)
    np_data = some_df.to_numpy()
    bunch_x15 = math.ceil(np_data.shape[0] / BUNCH / MAX_PROCESSES)
    count_process = math.ceil(np_data.shape[0] / BUNCH / bunch_x15)

    print(f"count banch per process = {bunch_x15}")
    print(f"count_process = {count_process}")

    all_pr = []
    q = mp.Queue()
    #mp.set_start_method("spawn")
    with mp.Manager() as manager:
        d = manager.dict()
        c = 1
        for i in range(0, np_data.shape[0], bunch_x15 * BUNCH):
            # print(i,i+bunch_x15 * BUNCH)
            # print(np_data[i:i+bunch_x15 * BUNCH].shape)
            name = f"pr-{c}"
            pr = mp.Process(
                name=name,
                target=f,
                args=(np_data[i:(i + bunch_x15 * BUNCH)],name, d)
            )
            c += 1
            pr.start()
            all_pr.append(pr)

        for pr in all_pr:
            # rez.append(q.get())
            pr.join()
            print(f"close process = {pr.name}")


if __name__ == "__main__":
    start_t = time.time()
    main()
    print(time.time()-start_t)
