### obsolete
# import os, datetime, sys
# import pandas as pd
# import numpy as np
#
# sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
# import tools
# import variables
#
# TEST_DIR = variables.TEST_DIR
# TABLES_DIR = variables.TABLES_DIR
# LOG_DIRECTORY = variables.LOG_DIRECTORY
#
# # - are all 10 tables there
# # - are all numpy files there
# # - is the size of the numpy files the same of larger?
# # - is the size of the tables the same or larger?
# # - number of lines roughly equal?
#
# def add_2_DF_file_dimensions_log():
#     """
#     read old log and add number of lines of flat files and bytes of data for binary files to log,
#     write to disk
#     :return: None
#     """
#     # read old table and add data to it
#     fn_log = os.path.join(LOG_DIRECTORY, "DF_file_dimensions.txt")
#     df_old = pd.read_csv(fn_log, sep="\t")
#
#     fn_list, binary_list, size_list, num_lines_list, date_list = [], [], [], [], []
#     for fn in sorted(os.listdir(TABLES_DIR)):
#         fn_abs_path = os.path.join(TABLES_DIR, fn)
#         if fn.endswith("UPS_FIN.txt"):
#             binary_list.append(False)
#             num_lines_list.append(tools.line_numbers(fn_abs_path))
#         elif fn.endswith("UPS_FIN.p") or fn.endswith("UPS_FIN.npz") or fn.endswith(".npy"):
#             binary_list.append(True)
#             num_lines_list.append(np.nan)
#         else:
#             continue
#         fn_list.append(fn)
#         size_list.append(os.path.getsize(fn_abs_path))
#         timestamp = tools.creation_date(fn_abs_path)
#         date_list.append(datetime.datetime.fromtimestamp(timestamp))
#
#     df = pd.DataFrame()
#     df["fn"] = fn_list
#     df["binary"] = binary_list
#     df["size"] = size_list
#     df["num_lines"] = num_lines_list
#     df["date"] = date_list
#     df["version"] = max(df_old["version"]) + 1
#     df = pd.concat([df_old, df])
#
#     df.to_csv(fn_log, sep="\t", header=True, index=False)
#
# if __name__ == "__main__":
#     add_2_DF_file_dimensions_log()