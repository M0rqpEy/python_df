import pandas as pd
import numpy as np
import datetime as dt
import time


COL_NAMES=[
    'HomeTeam',
    'AwayTeam',
    'Date',
    'HT_HM_1h_s',
    'HT_HM_1h_m',
    'HT_HM_2h_s',
    'HT_HM_2h_m',
    #
    'HT_AM_1h_s',
    'HT_AM_1h_m',
    'HT_AM_2h_s',
    'HT_AM_2h_m',
    ##
    'AT_HM_1h_s',
    'AT_HM_1h_m',
    'AT_HM_2h_s',
    'AT_HM_2h_m',
    #
    'AT_AM_1h_s',
    'AT_AM_1h_m',
    'AT_AM_2h_s',
    'AT_AM_2h_m',
    #
    'HT_FM_1h_s',
    'HT_FM_2h_s',
    'AT_FM_1h_s',
    'AT_FM_2h_s',
]

"""

*   B - Date = Match Date (dd/mm/yy)
*   D - HomeTeam = Home Team (к1)
*   E - AwayTeam = Away Team (к2)
*   F - FTHG = Full Time Home Team Goals
*   G - FTAG = Full Time Away Team Goals
*   I - HTHG = Half Time Home Team Goals
*   J - HTAG = Half Time Away Team Goals
*   HT - home team
*   AT - away team

*   HM - home match
*   AM - away match
*   1h - 1 half
*   2h - 2 half

*   s - score goal
*   m - miss a goal
*   FM - final match
"""

def get_all_df_from_exel(path_to_exel):
    """
    приймає шлях до ексел файлу,
    обробляє ексель, створює колонки для другого тайму,
    повертає словарь "{назва_дивізіону:датафрейм}"
    """
    df_dict = pd.read_excel(
        path_to_exel,
        sheet_name=None,  # імпорт певної робочої таблиці
        usecols='B,D,E,F,G,I,J',  # імпорт окремих колонок (B,D,E,F,G,I,J,)
    )

    for a_df in df_dict.keys():
        df_dict[a_df]['HT2HG'] = df_dict[a_df]['FTHG'] - df_dict[a_df]['HTHG']
        df_dict[a_df]['HT2AG'] = df_dict[a_df]['FTAG'] - df_dict[a_df]['HTAG']

    return df_dict


some_df = pd.DataFrame(
    data=[ ],
    columns=COL_NAMES)


def get_data_from_match(pd_s, name_team, match):
    """
    приймає pd_s - pd.Series,
            name_team - назву команди
            match - строка, 'home' або 'away'
    повертає список з 4 елементів:
        - гол забий 1 тайм
        - гол пропущений 1 тайм
        - гол забий 2 тайм
        - гол пропущений 2 тайм
    """

    s_1h = pd_s['HTHG']
    m_1h = pd_s['HTAG']
    s_2h = pd_s['HT2HG']
    m_2h = pd_s['HT2AG']
    if match == 'home':
        return [ s_1h, m_1h, s_2h, m_2h]
    elif match == 'away':
        return [ m_1h, s_1h, m_2h, s_2h]


def process_data(div_name, df_dict):
    rez_end = []
    a = df_dict[div_name]
    for s in a.index:
        Date = a.loc[s,'Date']
        HT_name = a.loc[s, 'HomeTeam']
        HT_home_mask = a.loc[:s-1,'HomeTeam'].isin([HT_name])
        HT_away_mask = a.loc[:s-1,'AwayTeam'].isin([HT_name])
        AT_name = a.loc[s, 'AwayTeam']
        AT_home_mask = a.loc[:s-1,'HomeTeam'].isin([AT_name])
        AT_away_mask = a.loc[:s-1,'AwayTeam'].isin([AT_name])
        #
        HT_FM_1h_s = a.loc[s, 'HTHG'],
        HT_FM_2h_s = a.loc[s, 'HT2HG'],
        AT_FM_1h_s = a.loc[s, 'HTAG'],
        AT_FM_2h_s = a.loc[s, 'HT2AG'],


        if (HT_home_mask.any() and HT_away_mask.any() and
            AT_home_mask.any() and AT_away_mask.any()):
            HT_home_match = a.iloc[ a.loc[:s-1][ HT_home_mask ].index[-1] ]
            HT_away_match = a.iloc[ a.loc[:s-1][ HT_away_mask ].index[-1] ]
            AT_home_match = a.iloc[ a.loc[:s-1][ AT_home_mask ].index[-1] ]
            AT_away_match = a.iloc[ a.loc[:s-1][ AT_away_mask ].index[-1] ]

            HT_home_rez = get_data_from_match(HT_home_match, HT_name, 'home')
            HT_away_rez = get_data_from_match(HT_away_match, HT_name, 'away')
            #
            AT_home_rez = get_data_from_match(AT_home_match, AT_name, 'home')
            AT_away_rez = get_data_from_match(AT_away_match, AT_name, 'away')
            rez = ([HT_name, AT_name, Date]
                + HT_home_rez
                + HT_away_rez
                + AT_home_rez
                + AT_away_rez
                + [HT_FM_1h_s[0], HT_FM_2h_s[0], AT_FM_1h_s[0], AT_FM_2h_s[0]])

            rez_end.append(rez)
            end = time.perf_counter()
    rez_df = pd.DataFrame(data=rez_end, columns=COL_NAMES)
    rez_df = rez_df.drop_duplicates()
    return rez_df
"""

for data in rez_end:
  some_df = some_df.append(
    dict(zip(COL_NAMES, data)
    ),
    ignore_index=True
   )


some_df =  some_df.drop_duplicates()
print(some_df)
exit()

name_csv = 'data_19_20_d1'
# name_csv = 'data_20_21_d1'
# name_csv = 'data_21_22_d1'
some_df.to_csv(
    f'/content/{name_csv}.csv',
    index=False

)
"""


def get_years_from_path_exel(path):
    a = "".join(list(filter(lambda x: x.isdigit(), path)))
    return a[:4][2:], a[4:][2:]


def do_work(df_dict):
    for key in df_dict.keys():
        print(key)
        rez_df = process_data(key, df_dict)
        print(rez_df)

        # break


TEMPLATE_FILENAME = "pre_data_{}_{}_{}.csv"


def main():
    # PATH_TO_EXEL = "/home/q/papka/sameshit/all-euro-data-2019-2020.xlsx"
    # PATH_TO_EXEL = "/home/q/papka/sameshit/all-euro-data-2020-2021.xlsx"
    PATH_TO_EXEL = "/home/q/papka/sameshit/all-euro-data-2021-2022.xlsx"
    df_dict = get_all_df_from_exel(PATH_TO_EXEL)
    for key in df_dict.keys():
        print(key)
        rez_df = process_data(key, df_dict)
        (s, e) = get_years_from_path_exel(PATH_TO_EXEL)
        file_name = TEMPLATE_FILENAME.format(s, e, key.lower())
        rez_df.to_csv(
            f"/home/q/languages/python/csv/pre_data/{file_name}",
            index=False
        )
        # print(file_name)


if __name__ == "__main__":
    main()
