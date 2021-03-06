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
                        lambda x: int((x[0] + x[1]) > (x[2] + x[3])),  # п1|xп2
                        # lambda x: int((x[0] + x[1]) >= (x[2] + x[3])),  # п1x|п2
                        # lambda x: int((x[0] + x[1]) != (x[2] + x[3])),  # 12|н
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


def proc_data(df_data, selected_idx, target="numpy"):
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
                        selected_idx,  # вибрані індекси матчів
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
            "sel_idx",
            "count_cols",
            "rez_1",
            "rez_0"
        ]
    )
    rez_df["proc"] = rez_df["rez_0"] / (rez_df["rez_0"] + rez_df["rez_1"])
    rez_df["tot_rows"] = rez_df["rez_0"] + rez_df["rez_1"]

    return rez_df


def proc_target_data(rez_df, df_target, idxs):
    r_d = {}
    r_l = []
    for target_row, idx in zip(df_target, idxs):
        for _, data_row in rez_df.iterrows():
            r = all(
                target_row[data_row["cols"]] == data_row["vals"]
            )
            if r is True:
                # key = (
                    # proc,
                    # count_dupl,
                    # count_rows,
                    # col_name
                # )
                some_rez = data_row
                some_rez["rez"] = target_row[-1]
                some_rez["target_ind"] = idx
                # print(some_rez)
                r_l.append(some_rez)
                """
                continue
                key = tuple(data_row["cols"])
                if key not in r_d:
                    r_d[key] = [target_row]
                else:
                    r_d[key].append(target_row)
                """
                # break
    return r_l


def some_name_func(gr_idx, df, man_obj=None, pr_name=None):
    """
    основна обробка частин даних
    """
    r_d = {}
    r_l = []
    middle_d = {}
    for idxs in gr_idx:
        df_data, df_target = get_chunks_df(idxs, df, target="numpy")
        rez_proc_data = proc_data(df_data, idxs, target="numpy")
        rez_df = create_rez_df_proc_data(rez_proc_data)
        r_l += proc_target_data(rez_df, df_target, idxs)

    man_obj[pr_name] = r_l
    """
    if len(r_l) > 0:
        for d in r_l:
            for k, v in d.items():
                if k not in middle_d:
                    middle_d[k] = v
                else:
                    middle_d[k] += v
        for k, v in middle_d.items():
            # print("="*11)
            # print(k)
            rez_np = np.array(v)
            rez_1 = rez_np[:, -1].sum()
            rez_0 = rez_np.shape[0] - rez_1
            r_d[k] = {1: rez_1, 0: rez_0}
            # print(f"{rez_1=} || {rez_0=}")
            # print("="*11)

        # man_obj.put(r_d)
    """



def get_rez_dict(rez_d, file_name):
    final_rez_l = []
    r_d = {}
    for _, d in rez_d.items():
        for k, v in d.items():
            if k not in r_d:
                r_d[k] = v
            else:
                r_d[k][1] += v.get(1, 0)
                r_d[k][0] += v.get(0, 0)

    for k, v in r_d.items():
        proc = v[0] / (v[1] + v[0])
        # print(f"key = {k} == {v} proc= {proc}")
        final_rez_l.append([
            k,
            v.get(1, 0),
            v.get(0, 0),
            proc
        ])
        final_rez_df = pd.DataFrame(
            data=final_rez_l,
            columns=[
                "params",
                "rez_1",
                "rez_0",
                "proc",
            ])
        final_rez_df.to_csv(
            f"./csv/post_data/post_{file_name[4:]}",
            index=False
        )
        final_rez_df = final_rez_df.iloc[0:0]


def get_rez_dict_v2(rez_d, file_name):
    final_rez_l = []
    r_d = {}
    for _, l_w_series in rez_d.items():
        final_rez_l += l_w_series

    print(len(final_rez_l))
    final_rez_df = pd.DataFrame(data=final_rez_l)
    final_rez_df.to_csv(
        f"./csv/post_data/post_{file_name[4:]}",
        index=False
    )
    final_rez_df = final_rez_df.iloc[0:0]
