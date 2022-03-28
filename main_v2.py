import os
import pandas as pd
import numpy as np
import some_funcs as sf


def do_shit(f=None, char_f=None, v_h=None, v_a=None):
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
            filt_l = list(filter(lambda x: char_f in x, df_set.columns))
            data_r = row[filt_l].values

            df_h = df_set[ (df_set["HomeTeam"] == h_name) ]
            val_h = df_h.loc[df_h.index[-1]]
            data_h = val_h[filt_l].values

            df_a = df_set[ (df_set["AwayTeam"] == a_name) ]
            val_a = df_a.loc[df_a.index[-1]]
            data_a = val_a[filt_l].values

            count_h = sum(data_h == data_r)
            count_a = sum(data_a == data_r)

            if val_h["rez"] == v_h and val_a["rez"] == v_a:
            # if val_h["rez"] == v_h:
            # if val_a["rez"] == v_h:
                continue

            # c = 1 if char_f != "_" else 3
            # c = 6 if char_f != "_" else 10
            c = 3 if char_f != "_" else 8
            # c = 8 if char_f != "_" else 16
            # if count_h >= c:
            # if count_a >= c:
            if count_h + count_a <= c:
                rez_d[row["rez"]]+=1
    rez_0 = rez_d.get(0, 0)
    rez_1 = rez_d.get(1, 0)
    proc = rez_0 / (rez_0 + rez_1) if (rez_0 + rez_1) > 0 else 0
    if "19" in file_name and proc <= 0.66:
        return
    print(f"{file_name} => {rez_d} => {proc:.3f}")
    return rez_d


def main(many=None):
    if many:
        tot_list = os.listdir("./csv/pre_data")
        tot_list = list(filter(lambda x: "f2" in x, tot_list))
        # tot_list = list(filter(lambda x: "20" in x, tot_list))
        tot_list.sort()
        for char_f in ["HT", "AT","HM", "AM", "_s", "_m", "_"]:
            for val_h in [1,0]:
                for val_a in [1,0]:
                    print("===")
                    print(f"{char_f} {val_h} {val_a}")
                    for file_name in tot_list:
                        tot_rez = {1:0, 0:0}
                        rez_d = do_shit(file_name, char_f, val_h, val_a)
                        if rez_d is None:
                            break
                        rez_0 = rez_d.get(0, 0)
                        rez_1 = rez_d.get(1, 0)
                        tot_rez[1] += rez_1
                        tot_rez[0] += rez_0
                    # print(tot_rez)
    else:
        do_shit()



if __name__ == "__main__":
    main(many=True)
    # main()
