import os
import pandas as pd
import numpy as np
import some_funcs as sf


def do_shit(f=None):
    rez_d = {1:0, 0:0}
    file_name = f if f else "pre_data_19_20_e1.csv"
    df_data = pd.read_csv(f"csv/pre_data/{file_name}")
    sf.add_result_cols(df_data)
    sf.drop_fm_cols(df_data)
    for char_f in ["HM", "AM", "_s", "_m",]:  # "_"]:
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

                # if val_h["rez"] != 0 and val_a["rez"] == 0:
                # if val_h["rez"] == 0:
                # if val_a["rez"] != 0:
                    # continue

                # if count_h >= 6:
                if count_a >= 7:
                # if count_h + count_a <= 11:
                    rez_d[row["rez"]]+=1
        rez_0 = rez_d.get(0, 0)
        rez_1 = rez_d.get(1, 0)
        proc = rez_0 / (rez_0 + rez_1) if (rez_0 + rez_1) > 0 else 0
        print(f"{char_f} {file_name} => {rez_d} => {proc:.3f}")
    return rez_d


def main(many=None):
    tot_rez = {1:0, 0:0}
    tot_list = os.listdir("./csv/pre_data")
    tot_list = list(filter(lambda x: "e0" in x, tot_list))
    tot_list.sort()
    if many:
        for file_name in tot_list:
            rez_d = do_shit(file_name)
            rez_0 = rez_d.get(0, 0)
            rez_1 = rez_d.get(1, 0)
            tot_rez[1] += rez_1
            tot_rez[0] += rez_0
        print("===")
        print(tot_rez)
    else:
        do_shit()



if __name__ == "__main__":
    main(many=True)
    # main()
