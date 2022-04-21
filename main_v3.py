import os
import pandas as pd
import numpy as np
import some_funcs as sf


def do_search(f=None):
    file_name = f if f else "pre_data_19_20_e2.csv"
    df_data = pd.read_csv(f"csv/pre_data/{file_name}")
    sf.add_result_cols(df_data)
    sf.drop_fm_cols(df_data)
    cols = df_data.columns[3:-1]
    print()
    print()
    print()
    for col_name in cols:
        for count in range(4):
            a = df_data[df_data[col_name] == count]
            r = a["rez"].value_counts(normalize=True).get(0, 0)
            r1 = a["rez"].count()


            if r > 0.69 and r1 >= 10:
                print(f"{col_name} => {count}")
                print(a["rez"].value_counts())
                print(a["rez"].value_counts(normalize=True))
                print("+"*11)


def do_check(f=None):
    file_name = f if f else "pre_data_20_21_e1.csv"
    df_data = pd.read_csv(f"csv/pre_data/{file_name}")
    sf.add_result_cols(df_data)
    sf.drop_fm_cols(df_data)
    cols = df_data.columns[3:-1]
    print()
    print()
    print()
    a = df_data[df_data["HT_AM_2h_m"] == 3]
    r = a["rez"].value_counts(normalize=True).get(0, 0)
    r1 = a["rez"].count()
    print(a["rez"].value_counts())
    print(a["rez"].value_counts(normalize=True))
    print("+"*11)


def main():
    # do_search()
    do_check()


if __name__ == "__main__":
    main()
