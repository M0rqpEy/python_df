import numpy as np


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
    df["rez"] = df.loc[:, 'HT_FM_1h_s':'AT_FM_2h_s'].apply(
                        lambda x: int((x[0] + x[1]) > (x[2] + x[3])),  # k1-xk2
                        # lambda x: int(x.sum() > 2.5), #tb2.5
                        axis=1
                        )


def drop_fm_cols(df):
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


def get_chunks_df(gr_idx, df):
    min_idx = min(gr_idx)
    max_idx = max(gr_idx)
    # df_data = df.loc[min_idx-10:min_idx-1]
    df_data = None
    # df_target = df.loc[min_idx:max_idx]
    df_target = None
    df_numpy = df.loc[:, "HT_HM_1h_s":].to_numpy()
    df_numpy_data = df_numpy[min_idx-10:min_idx, :]
    df_numpy_target = df_numpy[min_idx:max_idx+1, :]
    return df_data, df_numpy_data, df_target, df_numpy_target


def proc_data(df_data):
    all_idx = get_all_ind(16, 0)
    for idx in all_idx:
        data, count = np.unique(df_data[:, idx], return_counts=True, axis=0)
        data = data[count >= 2]
        if len(data) > 0:
            print(f"indexes = {idx}")
            print(df_data[:, idx])
            print(count)
            print(data)

def some_name_func(gr_idx, df):
    for idxs in gr_idx[-3:]:
        df_data, df_numpy_data, df_target, df_numpy_target = get_chunks_df(idxs, df)
        # print(idxs)
        # print(df_data)
        # print(df_target)
        print(df_numpy_data)
        print(df_numpy_target)
        rez_proc_data = proc_data(df_numpy_data)
        break
