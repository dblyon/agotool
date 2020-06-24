"""Define some fixtures to use in the project."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."))) # to get to python directory
import random
import pandas as pd
import numpy as np
import pytest
from itertools import islice

import query, userinput, variables


Protein_2_FunctionEnum_and_Score_table_UPS = variables.TABLES_DICT_SNAKEMAKE["Protein_2_FunctionEnum_and_Score_table"]
ENSP_2_tuple_funcEnum_score_dict = query.get_proteinAN_2_tuple_funcEnum_score_dict(read_from_flat_files=True, fn=Protein_2_FunctionEnum_and_Score_table_UPS)


@pytest.fixture(scope='session')
def get_something():
    """A session scope fixture."""
    return "Bubu was here"

# taxid_list = [9606, 10090, 4932, 511145, 1038869, 32051]
# taxname_list = ["Homo sapiens",
#                 "Mus musculus",
#                 "Saccharomyces cerevisiae",
#                 "Escherichia coli str. K-12 substr. MG1655",
#                 "Paraburkholderia mimosarum",
#                 "Synechococcus sp. WH 7803"]
#
# @pytest.fixture(params=taxid_list, ids=taxname_list, scope="session")
# def TaxIDs(request):
#     return request.param

@pytest.fixture(scope="session")
def random_foreground_background(): # used TaxIDs fixture previously, but now it it random on TaxID level as well
    for _ in range(10):
        taxid = random.choice(query.get_taxids()) # read_from_flat_files=True
        background = query.get_proteins_of_taxid(taxid)
        foreground = random.sample(background, 200)
        return foreground, background, taxid


### STRING examples
# Example #1 Protein name: trpA; Organism: Escherichia coli K12_MG1655
ENSPs_1 = ['511145.b1260', '511145.b1261', '511145.b1262', '511145.b1263', '511145.b1264', '511145.b1812', '511145.b2551', '511145.b3117', '511145.b3360', '511145.b3772', '511145.b4388']
taxid_1 = 511145
# Example #2 Protein name: CDC15; Organism: Saccharomyces cerevisiae
ENSPs_2 = ['4932.YAR019C', '4932.YFR028C', '4932.YGR092W', '4932.YHR152W', '4932.YIL106W', '4932.YJL076W', '4932.YLR079W', '4932.YML064C', '4932.YMR055C', '4932.YOR373W', '4932.YPR119W']
taxid_2 = 4932
# Example #3 Protein name: smoothened; Organism: Mus musculus
ENSPs_3 = ['10090.ENSMUSP00000001812', '10090.ENSMUSP00000002708', '10090.ENSMUSP00000021921', '10090.ENSMUSP00000025791', '10090.ENSMUSP00000026474', '10090.ENSMUSP00000030443', '10090.ENSMUSP00000054837', '10090.ENSMUSP00000084430', '10090.ENSMUSP00000099623', '10090.ENSMUSP00000106137', '10090.ENSMUSP00000107498']
taxid_3 = 10090
ids_ = ["Protein name: trpA; Organism: Escherichia coli K12_MG1655", "Protein name: CDC15; Organism: Saccharomyces cerevisiae", "Protein name: smoothened; Organism: Mus musculus"]

@pytest.fixture(params=[(ENSPs_1, taxid_1), (ENSPs_2, taxid_2), (ENSPs_3, taxid_3)], ids=ids_, scope="session")
def STRING_examples(request):
    """
    :return: Tuple(ENSPs_list, TaxID(str))
    """
    return request.param

def from_file_2_df(fn):
    """
    :param fn: String
    :return: Tuple(Series, DataFrame)
    """
    df = pd.read_csv(fn, sep='\t')
    foreground = df["foreground"]
    if "intensity" in df.columns.tolist():
        background = df[["background", "intensity"]]
    else:
        background = df[["background"]]
    return foreground, background


foreground_1, background_1 = from_file_2_df(os.path.join(variables.PYTEST_FN_DIR, "example_1_STRING.txt"))
foreground_2, background_2 = from_file_2_df(os.path.join(variables.PYTEST_FN_DIR, "example_2_STRING.txt"))
foreground_11, background_11 = from_file_2_df(os.path.join(variables.PYTEST_FN_DIR, "example_11_STRING.txt"))
foreground_3, background_3 = from_file_2_df(os.path.join(variables.PYTEST_FN_DIR, "example_3_STRING.txt"))
fg_bg_meth_expected_cases_DFs = [(foreground_1, background_1, "abundance_correction"),
                                 (foreground_2, background_2, "abundance_correction"),
                                 (foreground_11, background_11, "abundance_correction"),
                                 (foreground_3, background_3, "abundance_correction")]
fg_bg_meth_expected_cases_ids = ["example_1_STRING.txt: foreground is a proper subset of the background, everything has an abundance value, one row of NaNs",
                                 'example_2_STRING.txt: same as example_1_STRING.txt with "," instead of "." as decimal delimiter',
                                 "example_11_STRING.txt: foreground is a proper subset of the background, not everything has an abundance value",
                                 "example_3_STRING.txt: foreground is not a proper subset of the background, not everything has an abundance value"]

@pytest.fixture(params=fg_bg_meth_expected_cases_DFs, ids=fg_bg_meth_expected_cases_ids)
def fixture_fg_bg_meth_expected_cases(request):
    return request.param

@pytest.fixture(scope="session")
def args_dict():
    args_d = {}
    args_d["enrichment_method"] = "genome"
    args_d["taxid"] = 9606
    args_d["FDR_cutoff"] = 1.05
    args_d["p_value_cutoff"] = 1.01
    args_d["limit_2_entity_type"] = None  # "-20;-25;-26" #"-21;-22;-23;-51;-52;-53;-54;-55;-56-57;-58"
    args_d["filter_PMID_top_n"] = 100
    args_d["filter_foreground_count_one"] = True
    args_d["filter_parents"] = True
    args_d["go_slim_subset"] = None  # "generic"
    args_d["o_or_u_or_both"] = "both"  # "both" "underrepresented" "overrepresented"
    args_d["multiple_testing_per_etype"] = True
    args_d["privileged"] = False
    return args_d



# UniProt_IDs_human_list = sorted(query.get_proteins_of_taxid(9606, read_from_flat_files=True))
# ENSP_human_list = sorted(query.get_proteins_of_human())
#
# @pytest.fixture(scope="session")
# def UniProt_IDs_human():
#     return UniProt_IDs_human_list
#
# @pytest.fixture(scope="session")
# def ENSPs_human():
#     return ENSP_human_list

### preloaded objects --> put into conftest.py?
UniProt_IDs_human_list = sorted(query.get_proteins_of_taxid(9606, read_from_flat_files=True))
ENSP_human_list = sorted(query.get_proteins_of_human())
###

def get_random_human_ENSP(num_ENSPs=20, joined_for_web=False, contiguous=False, UniProt_ID=False, UniProt_IDs_human_list=UniProt_IDs_human_list, ENSP_human_list=ENSP_human_list):
    if UniProt_ID:
        IDs_2_sample = UniProt_IDs_human_list
    else:
        IDs_2_sample = ENSP_human_list
    max_index = len(IDs_2_sample)
    if not contiguous:
        if not joined_for_web:
            return random.sample(IDs_2_sample, num_ENSPs)
        else:
            return "%0d".join(random.sample(IDs_2_sample, num_ENSPs))
    else:
        start_pos = np.random.randint(0, max_index)
        if start_pos + num_ENSPs > max_index:
            start_pos = max_index - num_ENSPs
        stop_pos = start_pos + num_ENSPs
        if not joined_for_web:
            return list(islice(IDs_2_sample, start_pos, stop_pos))
        else:
            return "%0d".join(list(islice(IDs_2_sample, start_pos, stop_pos)))

### preload funcEnum to funcName table from flatfile
def get_funcEnum_2_funcName_dict():
    """
    0       -20     GOCC:0000015    Phosphopyruvate hydratase complex       -1      10
    1       -20     GOCC:0000109    Nucleotide-excision repair complex      -1      10
    2       -20     GOCC:0000110    Nucleotide-excision repair factor 1 complex     -1      11
    3       -20     GOCC:0000111    Nucleotide-excision repair factor 2 complex     -1      11
    """
    funcEnum_2_funcName_dict = {}
    Functions_table = variables.tables_dict["Functions_table"]
    with open(Functions_table, "r") as fh:
        for line in fh:
            ls = line.split("\t")
            funcEnum = int(ls[0])
            funcName = ls[2]
            funcEnum_2_funcName_dict[funcEnum] = funcName
    return funcEnum_2_funcName_dict

funcEnum_2_funcName_dict = get_funcEnum_2_funcName_dict()