import some_funcs as sf
import pandas as pd
import os
import numpy as np


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
        | data["file_name"].str.contains("20_21")
    )

    new_data = data[targ_mask]
    if new_data.empty:
        continue
    data = data[~targ_mask]
    if data.empty:
        continue
    m = data['proc'].mean()
    tot = data["rez_0"].sum() + data["rez_1"].sum()
    m_s = data["rez_0"].sum() / (data["rez_0"].sum() + data["rez_1"].sum())
    summ = data["rez_0"] + data["rez_1"]
    m_s_new = new_data["rez_0"].sum() / (new_data["rez_0"].sum() + new_data["rez_1"].sum())
    summ_new = new_data["rez_0"] + new_data["rez_1"]
    # if (
        # m_s >= 0.7
        # and tot >= 20
    # ):
    if (
        (summ_new >= 5).all()
        and m_s_new >= 0.74
    ):
    # if name == "(0, 7, 9, 10, 12)":
    # if "5, 3" in name and m >= 0.62:
    # if True:
    # if tot > 100:
        print("="*11)
        print(name)
        # print(data.iloc[:, 1:].sort_values("file_name"))
        print(new_data.iloc[:, 1:].sort_values("file_name"))
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
