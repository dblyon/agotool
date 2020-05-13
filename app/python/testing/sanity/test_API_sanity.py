import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import pandas as pd

from pandas import testing as pd_testing
import pytest, random
import numpy as np
from itertools import islice
from io import StringIO
import requests
import conftest

import variables, query

url_local = r"http://127.0.0.1:5911/api"


def test_random_contiguous_input_yields_results():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=100, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "foreground": fg_string, "enrichment_method": "genome", "taxid": 9606})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0

### tests for enrichment_method genome
def test_FG_count_not_larger_than_FG_n():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=100, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0
    cond = df["FG_count"] <= df["FG_n"]
    assert cond.all()

def test_FG_count_not_larger_than_BG_count():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=200, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0
    cond = df["FG_count"] <= df["BG_count"]
    assert cond.all()

# genome and compare_samples should yield the same results if given the same input
def test_genome_same_as_compare_samples():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=200, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
        data={"foreground": fg_string})
    df_genome = pd.read_csv(StringIO(response.text), sep='\t')

    bg_string = "%0d".join(conftest.UniProt_IDs_human_list)
    response = requests.post(url_local, params={"output_format": "tsv", "foreground": fg_string, "enrichment_method": "compare_samples", "taxid": 9606}, data={"foreground": fg_string, "background": bg_string})
    df_compare_samples = pd.read_csv(StringIO(response.text), sep='\t')

    cond_FG_count = df_compare_samples["FG_count"] == df_genome["FG_count"]
    assert cond_FG_count.all()

    cond_BG_count = df_compare_samples["BG_count"] == df_genome["BG_count"]
    assert cond_BG_count.all()

    cond_BG_n = df_compare_samples["BG_n"] == df_genome["BG_n"]
    assert cond_BG_n.all()

@pytest.mark.parametrize("i", range(25, 425, 25))
def test_genome_random_inputs(i):
    """
    genome sanity checks
    """
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=i, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0
    cond = df["FG_count"] <= df["BG_count"]
    assert cond.all()
    cond = df["FG_count"] <= df["FG_n"]
    assert cond.all()
    cond = df["BG_count"] <= df["BG_n"]
    assert cond.all()
    cond = df["FG_n"] <= df["BG_n"]
    assert cond.all()

def test_expected_terms_in_output():
    """
    check expected terms for specific input (e.g. reviewer query on Haemoglobin)
    # KW-0561, Oxygen transport
    # KW-0349, Heme
    # GO:0005344, oxygen carrier activity
    # GO:0019825, oxygen binding
    # GO:0020037, heme binding
    # GO:0005833, hemoglobin complex
    """
    fg_list = ["P69905", "P68871", "P02042", "P02100"]
    fg_string = "%0d".join(fg_list)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    expected_terms = ["KW-0561", "KW-0349", "GO:0005344", "GO:0019825", "GO:0020037", "GO:0005833"]
    cond = df["term"].isin(expected_terms)
    assert len(expected_terms) == sum(cond)

@pytest.mark.parametrize("i", range(50, 250, 50))
def test_ENSP_vs_UniProtID(i):
    """
    check that ENSP and UniProtIDs give same results
    """
    UniProtID_list = random.sample(conftest.UniProt_IDs_human_list, i)
    prim_2_sec_dict = query.map_primary_2_secondary_ANs(ids_2_map=UniProtID_list, Primary_2_Secondary_IDs_dict=None, read_from_flat_files=False, ENSPs_only=True)
    fg_string = "%0d".join(prim_2_sec_dict.keys())
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg_string})
    df_UP = pd.read_csv(StringIO(response.text), sep='\t')

    fg_string = "%0d".join(prim_2_sec_dict.values())
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg_string})
    df_ENSP = pd.read_csv(StringIO(response.text), sep='\t')

    assert df_UP.shape[0] == df_ENSP.shape[0]

    df_UP = df_UP.drop(columns=["FG_IDs"])
    df_ENSP = df_ENSP.drop(columns=["FG_IDs"])
    pd_testing.assert_frame_equal(df_UP, df_ENSP)

# examples from webpage need to work
def test_web_example_1():
    df = pd.read_csv(os.path.join(variables.EXAMPLE_FOLDER, "Example_1_Yeast_acetylation_abundance_correction.txt"), sep='\t')
    fg_id_string = "%0d".join(df.loc[df["Foreground"].notnull(), "Foreground"].tolist())
    bg_id_string = "%0d".join(df["Background"].tolist())
    bg_abundance_string = "%0d".join(df["Intensity"].astype(str).tolist())
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "abundance_correction"},
        data={"foreground": fg_id_string,
              "background": bg_id_string,
              "background_intensity": bg_abundance_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 50
    assert df.groupby("category").count().shape[0] >= 5 # at least 5 categories with significant results, last time I checked (2020 04 01)

def test_web_example_2():
    fg_string = "%0d".join(["P69905", "P68871", "P02042", "P02100"])
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 100
    assert df.groupby("category").count().shape[0] >= 9 # at least 9 categories with significant results, last time I checked (2020 04 01)

def test_web_example_3():
    fg_string = "%0d".join(["Q9R117", "P33896", "O35664", "O35716", "P01575", "P42225", "P07351", "P52332", "Q9WVL2", "Q61179", "Q61716"])
    bg_string = "%0d".join(query.get_proteins_of_taxid(10090, read_from_flat_files=True))
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "compare_samples"},
        data={"foreground": fg_string,
              "background": bg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 700
    assert df.groupby("category").count().shape[0] >= 11  # at least 11 categories with significant results, last time I checked (2020 04 01)

def test_web_example_4():
    fg_string = "MPRD_HUMAN"
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "characterize_foreground", "filter_foreground_count_one": False},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 1000
    assert df.groupby("category").count().shape[0] >= 11  # at least 11 categories with significant results, last time I checked (2020 04 01)

def test_taxid_species_mapping():
    ENSPs = ['4932.YAR019C', '4932.YFR028C', '4932.YGR092W', '4932.YHR152W', '4932.YIL106W', '4932.YJL076W', '4932.YLR079W', '4932.YML064C', '4932.YMR055C', '4932.YOR373W', '4932.YPR119W']
    fg = "%0d".join(ENSPs)
    # UniProt reference proteomes uses "Saccharomyces cerevisiae S288C" with Taxid 559292 as a pan proteome instead of 4932 (TaxID on taxonomic rank of species).
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 4932, "STRING_beta": False}, data={"foreground": fg})
    df_4932 = pd.read_csv(StringIO(result.text), sep="\t")
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 559292, "STRING_beta": False}, data={"foreground": fg})
    df_559292 = pd.read_csv(StringIO(result.text), sep="\t")
    pd_testing.assert_frame_equal(df_4932, df_559292)