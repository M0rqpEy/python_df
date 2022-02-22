import some_funcs as sf
import pandas as pd
import os
import numpy as np


def do_stats():
    cols = ['params', 'rez_1', 'rez_0', 'proc', 'file_name']
    f_df = pd.DataFrame(data=[], columns=cols)
    filtred_list = filter(
        # lambda x: "21_22" not in x,
        # lambda x: "19_20" in x,
        # lambda x: "20_21" in x,
        # lambda x: "19_20_e1" in x,
        lambda x: x,
        os.listdir("./csv/post_data/")
    )
    for f in filtred_list:
        df_data = pd.read_csv(f"./csv/post_data/{f}")
        df_data["file_name"] = f
        f_df = pd.concat([f_df, df_data], ignore_index=True)

    rez_l = []
    grs = f_df.groupby("params")
    rez_d = {1: 0, 0: 0}
    for name, data in grs:
        targ_mask = (
            data["file_name"].str.contains("19")
            #| data["file_name"].str.contains("20_21")
        )

        new_data = data[targ_mask]
        if new_data.empty:
            continue
        m_s_new = new_data["rez_0"].sum() / (new_data["rez_0"].sum() + new_data["rez_1"].sum())
        summ_new = new_data["rez_0"] + new_data["rez_1"]

        mask = data["file_name"].str.contains("20_21")
        data = data[mask]
        if data.empty:
            continue
        m = data['proc'].mean()
        tot = data["rez_0"].sum() + data["rez_1"].sum()
        m_s = data["rez_0"].sum() / (data["rez_0"].sum() + data["rez_1"].sum())
        summ = data["rez_0"] + data["rez_1"]
        # if (
            # m_s >= 0.7
            # and tot >= 20
        # ):
        if (
            (summ_new >= 4).all()
            and m_s_new >= 0.7
        ):
        # if name == "(0, 7, 9, 10, 12)":
        # if "5, 3" in name and m >= 0.62:
        # if True:
        # if tot > 100:
            print("="*11)
            print(name)
            # print(data.iloc[:, 1:].sort_values("file_name"))
            # print(new_data.iloc[:, 1:].sort_values("file_name"))
            print(f"mean_sum = {m_s_new:.2f}")
            print(
                f"+{new_data['rez_0'].sum()}"
                f"-{new_data['rez_1'].sum()}"
            )
            print("*"*11)
            # print(f"mean = {m:.2f}")
            print(f"mean_sum = {m_s:.2f}")
            print(
                f"+{data['rez_0'].sum()}"
                f"-{data['rez_1'].sum()}"
            )
            print("="*11)
            rez_l.append(name)
            rez_d[1] += data["rez_1"].sum()
            rez_d[0] += data["rez_0"].sum()
    exit()
    print(rez_l)
    print(rez_d)
    a = pd.read_csv("./csv/post_data/post_data_21_22_e1.csv")
    b = a[a["params"].isin(rez_l)]
    print(b)
    print(
        f"+{b['rez_0'].sum()}"
        f"-{b['rez_1'].sum()}"
    )
    print(b["rez_0"].sum() / (b["rez_0"].sum() + b["rez_1"].sum()))


def do_tests():
    a = {}
    print(dir(a))

def do_stats_v2():
    for count_cols in range(2, 8+1):
        for tot_rows in range(2, 8+1):
            for proc in np.arange(0.69, 1.0, 0.05):
                print(
                    f"count_cols = {count_cols} "
                    f"proc = {proc:.3f} "
                    f"tot_rows = {tot_rows} "
                )
                for part_f in ["19_20", "20_21", "21_22"]:
                    final_0 = 0
                    final_1 = 0
                    for file_name in os.listdir("./csv/post_data/"):
                        if part_f not in file_name:
                            continue
                        a = pd.read_csv(f"./csv/post_data/{file_name}")
                        grs_by_sel_idx = a.groupby("sel_idx")
                        rez_d = do_shit_w_data(
                            grs_by_sel_idx, count_cols, proc, tot_rows
                        )
                        if rez_d == {}:
                            continue
                        rez_0 = rez_d.get(0, 0)
                        rez_1 = rez_d.get(1, 0)
                        tot_rez = rez_0 / (rez_0 + rez_1)
                        """
                        print(

                            f"  "
                            f"rez = +{rez_0:3} -{rez_1:3} "
                            f"= {tot_rez:.3f} "
                            f"{file_name} "
                        )
                        """
                        final_1 += rez_1
                        final_0 += rez_0

                    try:
                        final_proc = final_0 / (final_0 + final_1)
                    except ZeroDivisionError:
                        continue
                    # if final_proc <= 0.64 or (final_0 + final_1) <= 100:
                        # continue
                    print(
                        f"  "
                        f"{part_f} "
                        f"+{final_0}-{final_1} "
                        f" {final_proc:.3f}"
                    )
                print("="*11)


def do_shit_w_data(grs_by_sel_idx, count_cols, proc, tot_rows):
    rez_d = {}
    for i, (name, data) in enumerate(grs_by_sel_idx):
        # if i >= 5:
        # break
        for name_l2, data_l2 in data.groupby("target_ind"):
            mask = (
                (data_l2["count_cols"] == count_cols)
                & (data_l2["tot_rows"] == tot_rows)
            )
            data_l2_filt = data_l2[mask]
            if data_l2_filt.empty:
                continue
            tot = data_l2_filt["rez_0"].sum() + data_l2_filt["rez_1"].sum()
            m_s = data_l2_filt["rez_0"].sum() / (
                data_l2_filt["rez_0"].sum() + data_l2_filt["rez_1"].sum()
                )
            fin_rez = data_l2_filt['rez'].values[0]
            if m_s > proc:
                if fin_rez in rez_d:
                    rez_d[fin_rez] += 1
                else:
                    rez_d[fin_rez] = 1

    return rez_d


if __name__ == "__main__":
    # do_stats()
    do_stats_v2()
    # do_tests()
# ['cols', 'vals', 'sel_idx', 'count_cols', 'rez_1', 'rez_0',
# 'proc', 'tot_rows', 'rez', 'target_ind']
