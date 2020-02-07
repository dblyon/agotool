import numpy as np


def searchsorted_dbl(fg, bg):
    fg.sort()
    bg.sort()
    fg_bg = np.concatenate((fg, bg))
    fg_bg.sort()
    searchsorted_fg, searchsorted_bg = [], []
    fg_rank, bg_rank = 0, 0
    num_fg_vals, num_bg_vals = fg.shape[0], bg.shape[0]
    num_fg_bg_vals = fg_bg.shape[0]
    val_previous = -1
    for val in fg_bg:
        if val == val_previous:
            searchsorted_fg.append(fg_rank)
            continue
        if fg_rank == num_fg_vals:
            searchsorted_fg += [searchsorted_fg[-1]] * (num_fg_bg_vals-len(searchsorted_fg))
            break
        for fg_index in range(fg_rank, num_fg_vals):
            fg_val = fg[fg_index]
            if val < fg_val:
                searchsorted_fg.append(fg_rank)
                break
            else:
                fg_rank += 1
        val_previous = val
    return np.array(searchsorted_fg)#, np.array(searchsorted_bg)







if __name__ == "__main__":
    fg = np.random.randint(0, 5000000, 200)
    bg = np.random.randint(0, 5000000, 20000)
    # res_dbl_fg = searchsorted_dbl(fg, bg)
    fg_bg = np.concatenate((fg, bg))
    np.searchsorted(fg, fg_bg)
    # fg = np.arange(0, 5)
    # bg = np.arange(3, 10)
    # fg_bg = np.concatenate((fg, bg))
    # fg_bg.sort()
    # res = searchsorted_dbl(fg, fg_bg)
    # print(res)
    # fg = [0,1,1,2,2,2,4,5,6]
    # fg = np.array(fg)
    # bg = [0, 1, 1, 2, 2, 2, 4, 5, 6, 10,1000]
    # bg = np.array(bg)
    # res_dbl_fg = searchsorted_dbl(fg, bg)
    # fg_bg = np.concatenate((fg, bg))
    # fg_bg.sort()
    # res_np_fg = np.searchsorted(fg, fg_bg, side="right")
    # res_np_bg = np.searchsorted(bg, fg_bg, side="right")
    # print(res_np_fg)
    # print(fg_bg)
    # print(fg)
    # print(res_dbl_fg)
    # same = (res_dbl_fg == res_np_fg).all()
    # if not same:
    #     print(res_dbl_fg)
    #     print(res_np_fg)
    # assert (res_dbl_bg == res_np_bg).all()
    # np.random.seed(12345)
    # counter = 0
    # for num_iter in range(10000):
    #     fg = np.random.randint(0, 5000000, 200)
    #     bg = np.random.randint(0, 5000000, 20000)
    #     fg_bg = np.concatenate((fg, bg))
    #     fg_bg.sort()
    #     res_dbl = searchsorted_dbl(fg, bg)
    #     res_np = np.searchsorted(fg, fg_bg, side="right")
    #     same = (res_dbl_fg == res_np_fg).all()
    #     if not same:
    #         print(res_dbl_fg)
    #         print(res_np_fg)
    #         break
    #     else:
    #         counter += 1
    #     assert (res_dbl_fg == res_np_fg).all()
    # print(counter)

    # from scipy import stats
    # stats.ks_2samp()