# import sys, os
# sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
#
# import pytest
# import requests
# import ast
#
# import variables, cluster_filter
#
#
# def test_filter_parents_if_same_foreground(example_output_genome, pqo_STRING):
#     df = example_output_genome
#     df["level"] = df["id"].apply(lambda term: pqo_STRING.functerm_2_level_dict[term])
#     df_after = cluster_filter.filter_parents_if_same_foreground(dfi, pqo_STRING.functerm_2_level_dict))
#     # check that number of rows decreases or stays the same
#     assert example_output_genome.shape[0] >= df_after.shape[0]
#     assert sum(example_output_genome.duplicated()) == 0
#     assert sum(df_after.duplicated()) == 0
#
# def test_filter_parents_if_same_foreground_2(example_output_genome, pqo_STRING):
#     df = example_output_genome
#     df["level"] = df["id"].apply(lambda term: pqo_STRING.functerm_2_level_dict[term])
#     assert sum(example_output_genome.duplicated()) == 0
#     example_output_genome = cluster_filter.filter_parents_if_same_foreground(df, pqo_STRING.functerm_2_level_dict))
#     # check that number of rows decreases or stays the same
#     assert sum(example_output_genome.duplicated()) == 0
#
# def test_filter_parents_if_same_foreground_v2(example_output_genome, pqo_STRING):
#     df = example_output_genome
#     df["level"] = df["id"].apply(lambda term: pqo_STRING.functerm_2_level_dict[term])
#     df_after = cluster_filter.filter_parents_if_same_foreground_v2(example_output_genome)
#     # check that number of rows decreases or stays the same
#     assert example_output_genome.shape[0] >= df_after.shape[0]
#     assert sum(example_output_genome.duplicated()) == 0
#     assert sum(df_after.duplicated()) == 0
#
# def test_filter_parents_if_same_foreground_2_v2(example_output_genome, pqo_STRING):
#     df = example_output_genome
#     df["level"] = df["id"].apply(lambda term: pqo_STRING.functerm_2_level_dict[term])
#     assert sum(example_output_genome.duplicated()) == 0
#     example_output_genome = cluster_filter.filter_parents_if_same_foreground_v2(df)
#     # check that number of rows decreases or stays the same
#     assert sum(example_output_genome.duplicated()) == 0
#
