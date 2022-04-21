import os
import pandas as pd
import numpy as np
import some_funcs as sf


def do_shit(f=None, count=None, char_f=None, v_h=None, v_a=None):
    rez_d = {1:0, 0:0}
    file_name = f if f else "pre_data_19_20_e1.csv"
    df_data = pd.read_csv(f"csv/pre_data/{file_name}")
    sf.add_result_cols(df_data)
    sf.drop_fm_cols(df_data)
    char_f = char_f if char_f else "_"
    for ind, row in df_data.iterrows():
        h_name = row["HomeTeam"]
        a_name = row["AwayTeam"]
        df_set = df_data.loc[:ind-1]
        if (h_name in df_set["HomeTeam"].values
            and a_name in df_set["AwayTeam"].values
        ):
            # filt_l = list(filter(lambda x: char_f in x, df_set.columns))
            filt_l = list(filter(lambda x: "_" in x, df_set.columns))
            data_r = row[filt_l].values

            df_h = df_set[
                (df_set["HomeTeam"] == h_name)
                |(df_set["AwayTeam"] == h_name)
            ]
            val_h = df_h.loc[df_h.index[-1]]
            data_h = val_h[filt_l].values

            df_a = df_set[
                (df_set["AwayTeam"] == a_name)
                |(df_set["HomeTeam"] == a_name)
            ]
            val_a = df_a.loc[df_a.index[-1]]
            data_a = val_a[filt_l].values

            count_h = (sum(data_h == data_r)
                       if val_h["rez"] == 0 else -sum(data_h == data_r))
            count_a = (sum(data_a == data_r)
                       if val_a["rez"] == 0 else -sum(data_a == data_r))

            # if val_h["rez"] != v_h and val_a["rez"] != v_a:
            # if val_h["rez"] != v_h:
            # if val_a["rez"] == v_h:
                # continue

            # c = 1 if char_f != "_" else 3
            # c = 6 if char_f != "_" else 10
            # c = 6 if char_f != "_" else 2
            # top4ik
            # c = 11 if char_f != "_" else 20
            # if count_h == count:
            # if count_a == count:
            if count_h + count_a == count:
                rez_d[row["rez"]]+=1
    rez_0 = rez_d.get(0, 0)
    rez_1 = rez_d.get(1, 0)
    proc = rez_0 / (rez_0 + rez_1) if (rez_0 + rez_1) > 0 else 0
    if "19" in file_name:
        if proc <= 0.69 or (rez_0 + rez_1) < 10:
            return
    return rez_d


def main():
    tot_list = os.listdir("./csv/pre_data")
    # tot_list = list(filter(lambda x: "e0" in x, tot_list))
    # tot_list = list(filter(lambda x: "19" in x, tot_list))
    # tot_list.sort()
    uniq_chap = list(set(map( lambda x: x.split("_")[-1], tot_list)))
    for chap in uniq_chap:
        r_target = {1:0, 0:0}
        print(f"{'+'*15} {chap}")
        target_files = list(filter(lambda x: f"{'_'+chap}" in x, tot_list))
        target_files.sort()
        # for char_f in ["HT", "AT","HM", "AM", "_s", "_m", "_"]:
        # for char_f in ["_"]:
            # for val_h in [1,0]:
                # for val_a in [1,0]:
        for count in range(-22, 32):
            m_r_target = {}
            tot_rez = {1:0, 0:0}
            # print(f"{char_f} {val_h} {val_a}")
            l_w_rez = []
            for file_name in target_files:
                # rez_d = do_shit(file_name, char_f, val_h, val_a)
                rez_d = do_shit(file_name, count)
                if rez_d is None:
                    break

                rez_0 = rez_d.get(0, 0)
                rez_1 = rez_d.get(1, 0)
                proc = rez_0 / (rez_0 + rez_1) if (rez_0 + rez_1) > 0 else 0
                # print(f"{file_name} => {rez_d} => {proc:.3f}")
                l_w_rez.append(f"{file_name} => {rez_d} => {proc:.3f}")
                if "20" in file_name:
                    tot_rez[1] += rez_1
                    tot_rez[0] += rez_0
                if "_22" in file_name:
                    m_r_target = {**rez_d}

            t_rez_0 = tot_rez.get(0, 0)
            t_rez_1 = tot_rez.get(1, 0)
            if (t_rez_0 + t_rez_1) == 0:
                continue
            proc = t_rez_0 / (t_rez_0 + t_rez_1)
            # if proc <= 0.69 or (t_rez_0 + t_rez_1) <= 10:
                # continue
            r_target[1] += m_r_target.get(1, 0)
            r_target[0] += m_r_target.get(0, 0)
            print("===")
            print(count)
            [print(x) for x in l_w_rez]
            print(f"{tot_rez} => {proc:.3f}")
        print(f" toto => {r_target}")
        print()


if __name__ == "__main__":
    main()
