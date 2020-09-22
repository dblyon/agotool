import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."))) # to get from API to python directory
import pandas as pd
import numpy as np

import variables

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
df = df[df["deprecated"] == False] # skip TextMining Scores tables
version_current = max(df["version"])
version_previous = version_current - 1
cond_previous = df["version"] == version_previous
cond_current = df["version"] == version_current
cond_not_binary = df["binary"] == False


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
        assert num_lines_current >= num_lines_previous

def test_compare_file_size():
    # for every file, compare previous vs current size of file
    for fn in sorted(df["fn"].unique()):
        cond_fn = df["fn"] == fn
        cond_fnp = cond_previous & cond_fn
        cond_fnc = cond_current & cond_fn
        if sum(cond_fnp) == 0:
            print("{} not present in previous version".format(fn))
        if sum(cond_fnc) == 0:
            print("{} not present in current version".format(fn))
        size_previous = df.loc[cond_fnp, "size"].values[0]
        size_current = df.loc[cond_fnc, "size"].values[0]
        assert size_current >= size_previous

        
