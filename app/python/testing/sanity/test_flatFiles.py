import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."))) # to get from API to python directory
import pandas as pd
import numpy as np

import variables



# check if files are similar size of larger than previously
# record status quo in table
# file_name date, size in MB, number of lines, comment
# read old table and add data to it
LOG_DF_FILE_DIMENSIONS = variables.LOG_DF_FILE_DIMENSIONS
df = pd.read_csv(LOG_DF_FILE_DIMENSIONS, sep="\t")
version_current = max(df["version"])
version_previous = version_current - 1
cond_previous = df["version"] == version_previous
cond_current = df["version"] == version_current
cond_not_binary = df["binary"] == False


def test_flatfiles_number_of_lines_similar_or_larger():
    # for every file, compare previous vs current number of lines
    for fn in sorted(df.loc[cond_not_binary, "fn"].unique()):
        cond_fn = df["fn"] == fn
        num_lines_previous = df.loc[cond_previous & cond_fn, "num_lines"].values[0]
        num_lines_current = df.loc[cond_current & cond_fn, "num_lines"].values[0]
        assert num_lines_current >= num_lines_previous

def test_compare_file_size():
    # for every file, compare previous vs current size of file
    for fn in sorted(df["fn"].unique()):
        cond_fn = df["fn"] == fn
        size_previous = df.loc[cond_previous & cond_fn, "size"].values[0]
        size_current  = df.loc[cond_current & cond_fn, "size"].values[0]
        assert size_current >= size_previous