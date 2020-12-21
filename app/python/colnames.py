### description
# this module is intended to be imported as
# from colnames import *
# The logic and flow:
# - column names as variables (in one central location)
# - lists of colnames for specific enrichment_methods --> determine sort order and omit columns
# - dicts to translate short to long names

##########################################
### column names (used in run_cythonized.pyx, run.py, runserver.py)
etype = "etype"
term = "term"
funcEnum = "funcEnum"
description = "description"
p_value = "p_value"
FDR = "FDR"
effect_size = "effect_size"
over_under = "over_under"
hierarchical_level = "hierarchical_level"
s_value = "s_value"
ratio_in_FG = "ratio_in_foreground"
ratio_in_BG = "ratio_in_background"
FG_IDs = "foreground_ids"
BG_IDs = "background_ids"
FG_count = "foreground_count"
BG_count = "background_count"
FG_n = "foreground_n"
BG_n = "background_n"
rank = "rank"
logFDR = "logFDR"
year = "year"
category = "category"
color = "color"
marker_line_width = "marker_line_width"
marker_line_color = "marker_line_color"
id_ = "id"
opacity = "opacity"
text_label = "text_label"
category_rank = "category_rank"
##########################################
### Column sort order and omitting columns
#####################
## run_cythonized.pyx
cols_2_return_run_enrichment_cy = [term, hierarchical_level, description, year, over_under, p_value, FDR, effect_size, ratio_in_FG, ratio_in_BG, FG_count, FG_n, BG_count, BG_n, FG_IDs, BG_IDs, s_value, rank, funcEnum, category, etype]
cols_2_return_run_characterize_foreground_cy = [etype, term, hierarchical_level, description, year, ratio_in_FG, FG_count, FG_n, FG_IDs, funcEnum, category, rank]
#####################

#################################################
# STRING REST API specific sort order and columns
cols_sort_order_characterize_foreground_STRING_API = [FG_count, FG_IDs, ratio_in_FG, term, etype, category, hierarchical_level, description, year]
# all other methods (except for characterize_foreground)
cols_sort_order_STRING_API = [term, hierarchical_level, p_value, FDR, category, etype, description, FG_count, BG_count, FG_IDs, year]
#################################################

######################
# aGOtool runserver.py
cols_sort_order_genome = [s_value, term, description, FDR, effect_size, category, over_under, hierarchical_level, year, FG_IDs, FG_count, FG_n, BG_count, BG_n, ratio_in_FG, ratio_in_BG, p_value, logFDR, rank, category_rank]
cols_sort_order_abundance_correction = cols_sort_order_genome
cols_sort_order_characterize_foreground = [ratio_in_FG, term, description, category, hierarchical_level, year, FG_IDs, FG_count, FG_n, rank, category_rank]
# "BG_IDs" only for compare_samples
cols_sort_order_compare_samples = [s_value, term, description, FDR, effect_size, category, over_under, hierarchical_level, year, FG_IDs, BG_IDs, FG_count, FG_n, BG_count, BG_n, ratio_in_FG, ratio_in_BG, p_value, logFDR, rank, category_rank]
# dict below determines column sort order for the tab separated file download
# but also used in plot_and_table.df_2_html_table_with_data_bars
enrichmentMethod_2_colsSortOrder_dict = {"genome": cols_sort_order_genome,
                                         "characterize_foreground": cols_sort_order_characterize_foreground,
                                         "compare_samples": cols_sort_order_compare_samples,
                                         "abundance_correction": cols_sort_order_abundance_correction, }
######################


##########################################
### dicts to translate names (if exist)
# STRING
colnames_2_rename_dict_STRING = {FG_count: "foreground_count",
                                 BG_count: "background_count",
                                 FG_IDs: "foreground_ids",
                                 ratio_in_FG: "ratio_in_foreground",
                                 FDR: "FDR",
                                 hierarchical_level: "hierarchical_level", }
# aGOtool website
colnames_2_rename_dict_aGOtool_web = {FG_count: "foreground count",
                                      BG_count: "background count",
                                      FG_IDs: "foreground ids",
                                      BG_IDs: "background ids",
                                      ratio_in_FG: "ratio in foreground",
                                      ratio_in_BG: "ratio in background",
                                      FDR: "false discovery rate",
                                      p_value: "p value",
                                      effect_size: "effect size",
                                      s_value: "s value",
                                      over_under: "over under",
                                      hierarchical_level: "hierarchical level",
                                      FG_n: "foreground n",
                                      BG_n: "background n", }

# aGOtool download csv file
colnames_2_rename_dict_aGOtool_file = {FG_count: "foreground_count",
                                      BG_count: "background_count",
                                      FG_IDs: "foreground_ids",
                                      BG_IDs: "background_ids",
                                      ratio_in_FG: "ratio_in_foreground",
                                      ratio_in_BG: "ratio_in_background",
                                      FDR: "false_discovery_rate", }

# aGOtool.js --> dict_per_category needs to have the same names as variables in this module
