import sys, os, datetime, socket
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."))) # to get from API to python directory
import pandas as pd
import numpy as np

import variables, tools

HOSTNAME = socket.gethostname()

# check if files are similar size of larger than previously
# record status quo in table
# file_name date, size in MB, number of lines, comment
# read old table and add data to it
LOG_DF_FILE_DIMENSIONS = variables.LOG_DF_FILE_DIMENSIONS
LOG_DF_FILE_DIMENSIONS_GLOBAL_ENRICHMENT = variables.LOG_DF_FILE_DIMENSIONS_GLOBAL_ENRICHMENT
df = pd.read_csv(LOG_DF_FILE_DIMENSIONS, sep="\t")
version_current = max(df["version"])
version_previous = version_current - 1
cond_previous = df["version"] == version_previous
cond_current = df["version"] == version_current
cond_not_binary = df["binary"] == False

def create_DF_2_compare_global_enrichment():
    # only test on pisces, san, and aquarius
    if HOSTNAME not in {"pisces", "san.embl.de", "aquarius.meringlab.org"}:
        return pd.DataFrame()
    else:  # ToDo
        if HOSTNAME == "san.embl.de":
            GLOBAL_ENRICHMENT_DIR = r"/san/DB/dblyon/global_enrichment_v11"
        else:
            GLOBAL_ENRICHMENT_DIR = r"/home/dblyon/global_enrichment_v11"
    fn_list, binary_list, size_list, num_lines_list, date_list, md5_list = [], [], [], [], [], []
    fn_list_2_search = os.listdir(GLOBAL_ENRICHMENT_DIR)
    fn_list_2_search += os.listdir(os.path.join(GLOBAL_ENRICHMENT_DIR, "global_enrichment_data"))
    for fn in fn_list_2_search:
        if fn.endswith(".gz"):
            binary_list.append(True)
            num_lines_list.append(np.nan)
        elif fn.endswith(".tsv") or fn.endswith(".sql"):
            binary_list.append(False)
            num_lines_list.append(tools.line_numbers(fn))
        else:
            print(fn)
            continue
        size_list.append(os.path.getsize(fn))
        timestamp = os.path.getmtime(fn)
        date_list.append(datetime.datetime.fromtimestamp(timestamp))
        md5_list.append(tools.md5(fn))
        fn_list.append(os.path.basename(fn))
    dflocal = pd.DataFrame()
    dflocal["fn"] = fn_list
    dflocal["binary"] = binary_list
    dflocal["size"] = size_list
    dflocal["num_lines"] = num_lines_list
    dflocal["date"] = date_list
    dflocal["md5"] = md5_list
    dflocal["version"] = version_current_GE + 1

    cond_checksum = df_GE["checksum"].notnull()
    cond_latestVersion = df_GE["version"] == max(df_GE["version"])
    df2compare = df_GE[cond_checksum & cond_latestVersion]
    dfm = pd.concat([dflocal, df2compare])
    return dfm


df_GE = pd.read_csv(LOG_DF_FILE_DIMENSIONS_GLOBAL_ENRICHMENT, sep='\t')
version_current_GE = max(df_GE["version"])
version_local_GE = version_current_GE + 1
cond_local_GE = df_GE["version"] == version_local_GE
cond_current_GE = df_GE["version"] == version_current_GE
cond_not_binary_GE = df_GE["binary"] == False
dfm = create_DF_2_compare_global_enrichment()



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

def test_checksum():
    """
    compares previously recorded checksum (from Phobos) to currently created checksum (on e.g. Pisces)
    """
    cond_checksum = df["checksum"].notnull()
    cond_latestVersion = df["version"] == max(df["version"])
    df2compare = df[cond_checksum & cond_latestVersion]

    fn_list, binary_list, size_list, num_lines_list, date_list, checksum_list = [], [], [], [], [], []
    for fn in sorted(os.listdir(variables.TABLES_DIR)):
        fn_abs_path = os.path.join(variables.TABLES_DIR, fn)
        if fn.endswith("STS_FIN.txt"):
            binary_list.append(False)
            num_lines_list.append(tools.line_numbers(fn_abs_path))
        elif fn.endswith("STS_FIN.p"):
            binary_list.append(True)
            num_lines_list.append(np.nan)
        else:
            continue
        fn_list.append(fn)
        size_list.append(os.path.getsize(fn_abs_path))
        timestamp = tools.creation_date(fn_abs_path)
        date_list.append(datetime.datetime.fromtimestamp(timestamp))
        checksum_list.append(tools.md5(fn_abs_path))

    dflocal = pd.DataFrame()
    dflocal["fn"] = fn_list
    dflocal["binary"] = binary_list
    dflocal["size"] = size_list
    dflocal["num_lines"] = num_lines_list
    dflocal["date"] = date_list
    dflocal["checksum"] = checksum_list
    dfm = pd.concat([dflocal, df2compare])
    for fn, group in dfm.groupby("fn"):
        checksum_arr = group["checksum"].values
        assert checksum_arr.shape == (2,)
        assert checksum_arr[0] == checksum_arr[1]

def test_checksum_global_enrichment():
    for fn, group in dfm.groupby("fn"):
        checksum_arr = group["checksum"].values
        assert checksum_arr.shape == (2,)
        assert checksum_arr[0] == checksum_arr[1]

def test_flatfiles_number_of_lines_similar_or_larger_global_enrichment():
    # for every file, compare previous vs current number of lines
    for fn in sorted(dfm.loc[cond_not_binary_GE, "fn"].unique()):
        cond_fn = df_GE["fn"] == fn
        cond_fnl = cond_local_GE & cond_fn
        cond_fnc = cond_current_GE & cond_fn
        if sum(cond_fnl) == 0:
            print("{} not present in local version".format(fn))
        if sum(cond_fnc) == 0:
            print("{} not present in current version".format(fn))
        num_lines_local = df_GE.loc[cond_fnl, "num_lines"].values[0]
        num_lines_current = df_GE.loc[cond_fnc, "num_lines"].values[0]
        assert num_lines_current == num_lines_local

def test_compare_file_size_global_enrichment():
    # for every file, compare previous vs current size of file
    for fn in sorted(df_GE["fn"].unique()):
        cond_fn = df_GE["fn"] == fn
        cond_fnl = cond_local_GE & cond_fn
        cond_fnc = cond_current_GE & cond_fn
        if sum(cond_fnl) == 0:
            print("{} not present in local version".format(fn))
        if sum(cond_fnc) == 0:
            print("{} not present in current version".format(fn))
        size_local = df_GE.loc[cond_fnl, "size"].values[0]
        size_current = df_GE.loc[cond_fnc, "size"].values[0]
        assert size_current == size_local


### create DF_file_dimensions_log.txt for the first time
#import os, datetime, tools
## df_old = pd.read_csv(LOG_DF_FILE_DIMENSIONS, sep="\t")
#LOG_DF_FILE_DIMENSIONS = r"/home/dblyon/agotool_PMID_autoupdate/agotool/data/logs/DF_file_dimensions_log.txt"
#TABLES_DIR = r"/home/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables"
#fn_list, binary_list, size_list, num_lines_list, date_list = [], [], [], [], []
#stat = os.stat(LOG_DF_FILE_DIMENSIONS)
#timestamp = stat.st_mtime
#for fn in sorted(os.listdir(TABLES_DIR)):
#    fn_abs_path = os.path.join(TABLES_DIR, fn)
#    if fn.endswith("STS_FIN.txt"):
#        binary_list.append(False)
#        num_lines_list.append(tools.line_numbers(fn_abs_path))
#    elif fn.endswith("STS_FIN.p"):
#        binary_list.append(True)
#        num_lines_list.append(np.nan)
#    else:
#        continue
#    fn_list.append(fn)
#    size_list.append(os.path.getsize(fn_abs_path))
##     timestamp = tools.creation_date(fn_abs_path)
#    timestamp = stat.st_mtime
#    date_list.append(datetime.datetime.fromtimestamp(timestamp))
#df = pd.DataFrame()
#df["fn"] = fn_list
#df["binary"] = binary_list
#df["size"] = size_list
#df["num_lines"] = num_lines_list
#df["date"] = date_list
#df["version"] = 0
## df["version"] = max(df_old["version"]) + 1
## df = pd.concat([df_old, df])
#df.to_csv(LOG_DF_FILE_DIMENSIONS, sep="\t", header=True, index=False)