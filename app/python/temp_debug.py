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




def KolmogorovSmirnov_sparse_cy_genome(funcEnum_2_score_2_rank_dict, foreground_n, background_n, fg_scores_matrix_data, fg_scores_matrix_indptr, p_values, cond_multitest, effectSizes, p_value_cutoff,funcEnum_count_foreground, funcEnum_count_background, over_under_int_arr, o_or_u_or_both_encoding, filter_foreground_count_one):

    fg_size_plus_bg_size = foreground_n + background_n
    fg_size_times_bg_size_times_mintwo = -2.0 * foreground_n * background_n
    len_fg_scores_matrix_indptr = fg_scores_matrix_indptr.shape[0]
    for funcEnum in range(len_fg_scores_matrix_indptr - 1):
        index_col_start_fg = fg_scores_matrix_indptr[funcEnum]
        index_col_stop_fg = fg_scores_matrix_indptr[funcEnum + 1]
        if index_col_start_fg == index_col_stop_fg:
            continue  # column is empty
        elif filter_foreground_count_one and (index_col_stop_fg - index_col_start_fg) == 1:
            continue
        else:
            fg_values = fg_scores_matrix_data[index_col_start_fg:index_col_stop_fg]

        try:
            score_2_rank_dict = funcEnum_2_score_2_rank_dict[funcEnum]
        except KeyError:
            print("KeyError funcEnum {} not in funcEnum_2_score_2_rank_dict".format(funcEnum))
            continue

        num_bg_vals = len(score_2_rank_dict)
        if num_bg_vals == 0:
            continue
        fg_values = np.sort(fg_values)
        num_fg_vals = fg_values.shape[0]
        num_zeros_2_fill_fg = foreground_n - num_fg_vals
        num_zeros_2_fill_bg = background_n - num_bg_vals
        fg_rank, D_max_abs = 0, 0

        while fg_rank < num_fg_vals:
            fg_val = fg_values[fg_rank]
            fg_cumulative = (fg_rank + num_zeros_2_fill_fg) / foreground_n

            try:
                bg_rank = score_2_rank_dict[fg_val]
            except KeyError:
                print("KeyError fg_val {} not in score_2_rank_dict".format(fg_val))
                continue

            bg_cumulative = (bg_rank + num_zeros_2_fill_bg + 1) / background_n
            D_current_abs = abs(fg_cumulative - bg_cumulative)
            if D_current_abs > D_max_abs:
                D_max_abs = D_current_abs

            fg_rank += 1
            fg_cumulative = (fg_rank + num_zeros_2_fill_fg) / foreground_n
            D_current_abs = abs(fg_cumulative - bg_cumulative)
            if D_current_abs > D_max_abs:
                D_max_abs = D_current_abs
        pvalue = math.exp(fg_size_times_bg_size_times_mintwo * D_max_abs * D_max_abs / fg_size_plus_bg_size)
        if o_or_u_or_both_encoding != 0:
            pvalue /= 2

        num_half_fg = int(round((num_fg_vals + num_zeros_2_fill_fg) / 2))  # index at half of fg
        if num_half_fg > num_zeros_2_fill_fg:
            median_index = int(num_half_fg - num_zeros_2_fill_fg)
            median_fg = fg_values[median_index]
        else:
            median_fg = 0
        num_half_bg = int(round((num_bg_vals + num_zeros_2_fill_bg) / 2))
        if num_half_bg > num_zeros_2_fill_bg:
            median_index = int(num_half_bg - num_zeros_2_fill_bg)
            median_bg = bg_values[median_index]
        else:
            median_bg = 0
        is_greater = median_fg > median_bg

        if pvalue <= p_value_cutoff:
            p_values[funcEnum] = pvalue
            effectSizes[funcEnum] = D_max_abs
            if is_greater:  # overrepresented
                over_under_int_arr[funcEnum] = 1
            else:  # underrepresented
                over_under_int_arr[funcEnum] = 2
        cond_multitest[funcEnum] = True
        funcEnum_count_foreground[funcEnum] = num_fg_vals
        funcEnum_count_background[funcEnum] = num_bg_vals

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