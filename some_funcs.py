import numpy as np
import pandas as pd
import settings


def get_all_ind(count_cols, start_idx):
    rez = []
    count = 0
    for i in range(1, count_cols+1):
        my_rec(i, start_idx, 16, rez, [], count)
    return rez


def my_rec(count_cols, start_range, all_cols, some_l, middle_l, c):
    """
    кінець діапазону залежить від початку:
        при початку з 0 - кінець  all_cols-count_cols+1
        при початку з 1 - кінець  all_cols-count_cols+2
    """
    for ind in range(start_range, all_cols-count_cols+1):
        if len(middle_l) > 0 and ind <= middle_l[-1]:
            continue
        middle_l.append(ind)
        if count_cols != 1:
            my_rec(count_cols-1, start_range+1, all_cols, some_l, middle_l, c)
        else:
            # print(middle_l)
            # c += 1
            # print(c)
            some_l.append(middle_l.copy())
            middle_l.pop()
    if len(middle_l) > 0:
        middle_l.pop()


def get_distinct_rows():
    # rez = some_df[some_df.is_duplicated()].distinct(keep="first")
    pass


def add_result_cols(df):
    """
    добавляння колонки з результатом "rez"
    """
    df["rez"] = df.loc[:, 'HT_FM_1h_s':'AT_FM_2h_s'].apply(
                        lambda x: int((x[0] + x[1]) > (x[2] + x[3])),  # k1-xk2
                        # lambda x: int(x.sum() > 2.5), #tb2.5
                        axis=1
                        )


def drop_fm_cols(df):
    """
    видалення 4 колонок, які містять дані результату зустрічі команд
    """
    df.drop(
        list(filter(lambda x: "_FM_" in x, df.columns)),
        axis="columns",
        inplace=True)


def get_list_data_multipr(all_gr_idx):
    COUNT_PROCESSES = 11
    rez = []
    _ = list(map(lambda _: rez.append([]), range(COUNT_PROCESSES)))
    idx = 0
    for gr in all_gr_idx:
        if not all(map(lambda el: el >= 10, gr)):
            continue
        if idx > COUNT_PROCESSES-1:
            idx = 0
        rez[idx].append(gr.to_list())
        idx += 1
    return rez


def get_mask(vals, idx, df_data):
    """
    отримання маски для фільтрації "numpy"
    """
    mask = df_data[:,  idx[0]] == vals[0]
    for col, val in zip(idx, vals):
        mask = mask & (df_data[:, col] == val)
    return mask


def get_chunks_df(gr_idx, df, target="numpy"):
    min_idx = min(gr_idx)
    max_idx = max(gr_idx)
    if target == "pandas":
        df_data = df.loc[min_idx-10:min_idx-1]
        df_target = df.loc[min_idx:max_idx]
        return df_data, df_target
    if target == "numpy":
        df_numpy = df.loc[:, "HT_HM_1h_s":].to_numpy()
        df_numpy_data = df_numpy[min_idx-10:min_idx, :]
        df_numpy_target = df_numpy[min_idx:max_idx+1, :]
        return df_numpy_data, df_numpy_target


def proc_data(df_data, target="numpy"):
    """
    обробка df_datа, фільтурвання дублікатів
    """
    total_rez = []
    all_idx = get_all_ind(16, 0)
    for idx in all_idx:
        if target == "numpy":
            data, count = np.unique(df_data[:, idx],
                                    return_counts=True,
                                    axis=0
                                    )
            uniq_dup_rows = data[count >= 2]
            if len(uniq_dup_rows) > 0:
                for dup_row in uniq_dup_rows:
                    mask = get_mask(dup_row, idx, df_data)
                    rez = df_data[mask]
                    rez_1 = rez[:, -1].sum()
                    rez_0 = rez.shape[0] - rez_1
                    total_rez.append([
                        idx,  # список індексів
                        dup_row.tolist(),  # список значень
                        len(idx),  # кількість вибраних колонок
                        rez_1,  # кількість результатів "1"
                        rez_0  # кількість результатів "0"
                    ])

        if target == "pandas":
            # todo!!!
            pass
    return total_rez


def create_rez_df_proc_data(data):
    rez_df = pd.DataFrame(
        data=data,
        columns=[
            "cols",
            "vals",
            "count_cols",
            "rez_1",
            "rez_0"
        ]
    )
    rez_df["proc"] = rez_df["rez_0"] / (rez_df["rez_0"] + rez_df["rez_1"])
    rez_df["tot_rows"] = rez_df["rez_0"] + rez_df["rez_1"]

    return rez_df


def proc_target_data(rez_df, df_target):
    r_l = []
    for proc in [0.74, 0.99]:
        s = rez_df[
            (rez_df["proc"] >= proc)
            & (rez_df["tot_rows"] >= settings.FILTER_PARAMS.get("MIN_COUNT_DUPL"))
        ]
        s = s.nlargest(
            settings.FILTER_PARAMS.get("COUNT_ROWS"),
            "count_cols"
        )
        for target_row in df_target:
            for _, data_row in s.iterrows():
                r = all(target_row[data_row["cols"]] == data_row["vals"])
                if r is True:
                    r_l.append([
                        target_row,
                        proc,
                    ])
                    break
    return r_l


def some_name_func(gr_idx, df, q=None):
    """
    основна обробка частин даних
    """
    r_d = {1: 0, 0: 0}
    r_l = []
    for idxs in gr_idx:
        df_data, df_target = get_chunks_df(idxs, df, target="numpy")
        print(idxs)
        rez_proc_data = proc_data(df_data, target="numpy")
        rez_df = create_rez_df_proc_data(rez_proc_data)
        r_l += proc_target_data(rez_df, df_target)

    if len(r_l) > 0:
        print("="*11)
        for i in r_l:
            print(i)
            r_d[i[0][-1]] += 1
        print("="*11)
    q.put(r_d)


def get_rez_dict(rez_l):
    r_d = {1: 0, 0: 0}
    for r in rez_l:
        r_d[1] += r.get(1)
        r_d[0] += r.get(0)
    print(r_d)
