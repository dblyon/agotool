"""Define some fixtures to use in the project."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."))) # to get to python directory
import random
import pandas as pd
# import numpy as np

import pytest

import query, userinput, variables


@pytest.fixture(scope='session')
def pqo():
    """
    get pqo (Persistent Query Object)
    """
    return query.PersistentQueryObject()

@pytest.fixture(scope='session')
def pqo_STRING():
    """
    get pqo (Persistent Query Object)
    """
    return query.PersistentQueryObject_STRING()

@pytest.fixture(scope='session')
def get_something():
    """A session scope fixture."""
    return "Bubu was here"


taxid_list = [9606, 10090, 4932, 511145,
              1038869, 32051]
taxname_list = ["Homo sapiens", "Mus musculus", "Saccharomyces cerevisiae", "Escherichia coli str. K-12 substr. MG1655",
                "Paraburkholderia mimosarum",
                "Synechococcus sp. WH 7803"]

@pytest.fixture(params=taxid_list, ids=taxname_list, scope="session")
def TaxIDs(request):
    return request.param

@pytest.fixture(scope="session")
def random_foreground_background(): # used TaxIDs fixture previously, but now it it random on TaxID level as well
    for _ in range(10):
        taxid = random.choice(query.get_taxids())
        background = query.get_proteins_of_taxid(taxid)
        foreground = random.sample(background, 200)
        return foreground, background, taxid

# @pytest.fixture(scope="session")
# def ui_genome(random_foreground_background):
#     foreground, background = random_foreground_background
#     ui = userinput.U


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
    args_dict = {'FDR_cutoff': None,
                 'alpha': 0.05,
                 'foreground': None,
                 'background': None,
                 'background_intensity': None,
                 'foreground_n': 10,
                 'background_n': 10,
                 'caller_identity': None,
                 'enrichment_method': 'genome',
                 'fold_enrichment_for2background': 0,
                 'go_slim_or_basic': 'basic',
                 'identifiers': None,
                 'indent': 'True',
                 'limit_2_entity_type': '-21;-22;-23;-51;-52;-53;-54;-55',
                 'multitest_method': 'benjamini_hochberg',
                 'num_bins': 100,
                 'o_or_u_or_both': 'overrepresented',
                 'output_format': 'tsv',
                 'p_value_uncorrected': 0,
                 'organism': None,
                 'species': None,
                 'taxid': None}
    return args_dict

@pytest.fixture(scope="session")
def example_output_genome():
    fn = os.path.join(variables.PYTEST_FN_DIR, "example_output_genome_STRING.txt")
    return pd.read_csv(fn, sep='\t')
