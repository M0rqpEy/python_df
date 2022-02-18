import some_funcs as sf
import pandas as pd
import os
import numpy as np


cols = ['params', 'rez_1', 'rez_0', 'proc', 'file_name']
f_df = pd.DataFrame(data=[], columns=cols)
filtred_list = filter(
    # lambda x: "21_22" not in x,
    # lambda x: "19_20" in x,
    lambda x: x,
    os.listdir("./csv/post_data/")
)
for f in filtred_list:
    print(f)
    df_data = pd.read_csv(f"./csv/post_data/{f}")
    df_data["file_name"] = f
    f_df = pd.concat([f_df, df_data], ignore_index=False)

grs = f_df.groupby("params")
for name, data in grs:
    m = data['proc'].mean()
    # if m >= 0.68:
    # if (data["proc"] > 0.55).all():
    # if name == "(0.84, 3, 3)":
    if "5, 3" in name and m >= 0.62:
    # if True:
        print("="*11)
        print(name)
        print(data.iloc[:, 1:].sort_values("file_name"))
        print(f"mean = {m:.2f}")
        print(
            f"+{data['rez_0'].sum()}"
            f"-{data['rez_1'].sum()}"
        )
        print("="*11)
