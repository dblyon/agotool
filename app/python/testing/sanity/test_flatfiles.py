import sys, os, datetime, pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."))) # to get from API to python directory
import pandas as pd
import numpy as np

import variables, tools

### adding files to deprecated list
# df["deprecated"] = False
# cond = df["fn"].isin(["Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN.txt", "Taxid_2_FunctionEnum_2_Scores_dict_UPS_FIN.p",
#                       "Protein_2_FunctionEnum_and_Score_table_UPS_FIN.txt", "rowIndex_2_ENSP_dict_UPS_FIN.p",
#                       "CSC_ENSPencoding_2_FuncEnum_UPS_FIN.npz", "ENSP_2_rowIndex_dict_UPS_FIN.p",
#                      "SparseMatrixCSC_ENSPencoding_vs_FuncEnum_UPS_FIN.npz"])
# df.loc[cond, "deprecated"] = True
# df.to_csv(LOG_DF_FILE_DIMENSIONS, sep="\t", header=True, index=False)

# check if files are similar size of larger than previously
# record status quo in table
# file_name date, size in MB, number of lines, comment
# read old table and add data to it
LOG_DF_FILE_DIMENSIONS = variables.LOG_DF_FILE_DIMENSIONS
df = pd.read_csv(LOG_DF_FILE_DIMENSIONS, sep="\t")
# df = df[df["deprecated"] == False] # skip TextMining Scores tables
version_current = max(df["version"])
version_previous = version_current - 1
cond_previous = df["version"] == version_previous
cond_current = df["version"] == version_current
cond_not_binary = df["binary"] == False

df["num_lines"] = df["num_lines"].astype("float")

def test_flatfiles_number_of_lines_similar_or_larger():
    # for every file, compare previous vs current number of lines
    for fn in sorted(df.loc[cond_not_binary, "fn"].unique()):
        cond_fn = df["fn"] == fn
        cond_fnp = cond_previous & cond_fn
        cond_fnc = cond_current & cond_fn
        if sum(cond_fnp) == 0:
            print("{} not present in previous version".format(fn))
        if sum(cond_fnc) == 0:
            print("{} not present in current version".format(fn))
        num_lines_previous = df.loc[cond_fnp, "num_lines"].values[0]
        num_lines_current = df.loc[cond_fnc, "num_lines"].values[0]
        # assert num_lines_current >= num_lines_previous
        try:
            assert num_lines_current >= num_lines_previous
        except AssertionError: # at least 95% of previous
            try:
                assert int(100 * num_lines_current / num_lines_previous) >= 70
            except AssertionError:
                print(f"{fn} fails line number assertion")
                raise StopIteration

def test_compare_file_size():
    # for every file, compare previous vs current size of file
    for fn in sorted(df["fn"].unique()):
        cond_fn = df["fn"] == fn
        cond_fnp = cond_previous & cond_fn
        cond_fnc = cond_current & cond_fn
        if sum(cond_fnp) == 0:
            print("{} not present in previous version".format(fn))
            continue
        if sum(cond_fnc) == 0:
            print("{} not present in current version".format(fn))
        size_previous = df.loc[cond_fnp, "size"].values[0]
        size_current = df.loc[cond_fnc, "size"].values[0]
        # assert size_current >= size_previous
        try:
            assert size_current >= size_previous
        except AssertionError: # at least 95% of previous
            try:
                assert int(100 * size_current / size_previous) >= 70
            except AssertionError:
                print(f"{fn} fails file size assertion")
                raise StopIteration

def test_checksum():
    """
    check on files for agotool flask PMID_autoupdates
    compares previously recorded checksum (from Phobos) to currently created checksum (on e.g. Pisces)
    """
    cond_md5 = df["md5"].notnull()
    cond_latestVersion = df["version"] == max(df["version"])
    df2compare = df[cond_md5 & cond_latestVersion]

    fn_list, binary_list, size_list, num_lines_list, date_list, md5_list = [], [], [], [], [], []
    for fn in sorted(os.listdir(variables.TABLES_DIR)):
        if fn == "Entity_types_table_UPS_FIN.txt":
            continue
        fn_abs_path = os.path.join(variables.TABLES_DIR, fn)
        if fn.endswith("UPS_FIN.txt"):
            binary_list.append(False)
            num_lines_list.append(tools.line_numbers(fn_abs_path))
        elif fn.endswith("UPS_FIN.p") or fn.endswith(".npy"):
            binary_list.append(True)
            num_lines_list.append(np.nan)
        else:
            continue
        fn_list.append(fn)
        size_list.append(os.path.getsize(fn_abs_path))
        timestamp = tools.creation_date(fn_abs_path)
        date_list.append(datetime.datetime.fromtimestamp(timestamp))
        md5_list.append(tools.md5(fn_abs_path))

    dflocal = pd.DataFrame()
    dflocal["fn"] = fn_list
    dflocal["binary"] = binary_list
    dflocal["size"] = size_list
    dflocal["num_lines"] = num_lines_list
    dflocal["date"] = date_list
    dflocal["md5"] = md5_list
    dfm = pd.concat([dflocal, df2compare])
    for fn, group in dfm.groupby("fn"):
        md5_arr = group["md5"].values
        assert md5_arr.shape == (2,)
        assert md5_arr[0] == md5_arr[1]

def test_new_version_was_created_no_later_than_x_days_ago(days=32):
    date_time_str = max(df["date"])
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    assert date_time_obj > datetime.datetime.now() - datetime.timedelta(days)

# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*3", 18)])
# def test_pytest_mark_parametrize(test_input, expected):
#     assert eval(test_input) == expected
