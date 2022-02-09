def get_all_ind(count_cols):
    rez = []
    count = 0
    for i in range(1, count_cols+1):
        my_rec(i, 1, 16, rez, [], count)
    return rez


def my_rec(count_cols, start_range, all_cols, some_l, middle_l, c):
    for ind in range(start_range, all_cols-count_cols+2):
        if len(middle_l) > 0 and ind <= middle_l[-1]:
            continue
        middle_l.append(ind)
        if count_cols != 1:
            my_rec(count_cols-1, start_range+1, all_cols, some_l, middle_l, c)
        else:
            # print(middle_l)
            c += 1
            # print(c)
            some_l.append(middle_l.copy())
            middle_l.pop()
    if len(middle_l) > 0:
        middle_l.pop()


def get_distinct_rows():
    # rez = some_df[some_df.is_duplicated()].distinct(keep="first")
    pass
