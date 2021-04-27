import sys, os, json #, argparse
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
import colnames as cn

PYTEST_FN_DIR = variables.PYTEST_FN_DIR


# argparse_parser = argparse.ArgumentParser()
# argparse_parser.add_argument("IP", help="IP address without port, e.g. '127.0.0.1' (is also the default)", type=str, default="127.0.0.1", nargs='?')
# argparse_parser.add_argument("port", help="port number, e.g. '10110' (is also the default)", type=str, default="5911", nargs='?')
#
# args = argparse_parser.parse_args()
# def error_(parser):
#     sys.stderr.write("The arguments passed are invalid.\nPlease check the input parameters.\n\n")
#     parser.print_help()
#     sys.exit(2)
# for arg in sorted(vars(args)):
#     if getattr(args, arg) is None:
#         error_(argparse_parser)
#
#
# url_local = r"http://{}:{}/api".format(args.IP, args.port)
# print("url_local: {}".format(url_local))
# url_local = r"http://127.0.0.1:5911/api"
url_local_API_orig = variables.url_local_API_orig
url_local_API_STRING_style = variables.url_local_API_STRING_style

def test_random_contiguous_input_yields_results():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=100, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "foreground": fg_string,
                                                "enrichment_method": "genome", "taxid": 9606, "caller_identity": "PyTest"})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    is_true = df.shape[0] > 0
    if not is_true:
        response = requests.post(url_local_API_orig,
            params={"output_format": "tsv", "foreground": fg_string, "enrichment_method": "genome",
                    "taxid": 9606, "FDR_cutoff": 1, "p_value_cutoff": 1, "caller_identity": "PyTest"})
        df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0

### tests for enrichment_method genome
def test_FG_count_not_larger_than_FG_n():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=100, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "caller_identity": "PyTest"},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    is_true = df.shape[0] > 0
    if not is_true:
        response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "FDR_cutoff": 1, "p_value_cutoff": 1, "caller_identity": "PyTest"}, data={"foreground": fg_string})
        df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0
    cond = df[cn.FG_count] <= df[cn.FG_n]
    assert cond.all()

def test_FG_count_not_larger_than_BG_count():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=200, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "caller_identity": "PyTest"},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    is_true = df.shape[0] > 0
    if not is_true:
        response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "FDR_cutoff": 1, "p_value_cutoff": 1, "caller_identity": "PyTest"}, data={"foreground": fg_string})
        df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0
    cond = df[cn.FG_count] <= df[cn.BG_count]
    assert cond.all()

# genome and compare_samples should yield the same results if given the same input
def test_genome_same_as_compare_samples():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=200, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "caller_identity": "PyTest"},
        data={"foreground": fg_string})
    df_genome = pd.read_csv(StringIO(response.text), sep='\t')

    bg_string = "%0d".join(conftest.UniProt_IDs_human_list)
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "compare_samples", "taxid": 9606, "caller_identity": "PyTest"},
        data={"foreground": fg_string, "background": bg_string})
    df_compare_samples = pd.read_csv(StringIO(response.text), sep='\t')

    assert df_compare_samples.shape[0] == df_genome.shape[0] # same number of rows but additional column of BG_IDs for compare_samples

    cond_FG_count = df_compare_samples[cn.FG_count] == df_genome[cn.FG_count]
    assert cond_FG_count.all()

    cond_BG_count = df_compare_samples[cn.BG_count] == df_genome[cn.BG_count]
    assert cond_BG_count.all()

    cond_BG_n = df_compare_samples[cn.BG_n] == df_genome[cn.BG_n]
    assert cond_BG_n.all()

@pytest.mark.parametrize("i", range(25, 425, 25))
def test_genome_random_inputs(i):
    """
    genome sanity checks
    """
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=i, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome",
                                                "taxid": 9606, "caller_identity": "PyTest"},
                                        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    if df.shape[0] == 0:
        response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome",
                                                    "taxid": 9606, "FDR_cutoff": 1, "p_value_cutoff": 1, "caller_identity": "PyTest"},
                                            data={"foreground": fg_string})
        df = pd.read_csv(StringIO(response.text), sep='\t')
        assert df.shape[0] > 0
    cond = df[cn.FG_count] <= df[cn.BG_count]
    assert cond.all()
    cond = df[cn.FG_count] <= df[cn.FG_n]
    assert cond.all()
    cond = df[cn.BG_count] <= df[cn.BG_n]
    assert cond.all()
    cond = df[cn.FG_n] <= df[cn.BG_n]
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
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "caller_identity": "PyTest"}, data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    # expected_terms = ["KW-0561", "KW-0349", "GO:0005344", "GO:0019825", "GO:0020037", "GO:0005833"]
    expected_terms = ["KW-0561", "KW-0349", "GO:0005344", "GO:0019825", "GO:0020037", "GO:0005833"]
    cond = df[cn.term].isin(expected_terms)
    assert len(expected_terms) == sum(cond)

@pytest.mark.parametrize("i", range(50, 250, 50))
def test_ENSP_vs_UniProtID(i):
    """
    check that ENSP and UniProtIDs give same results
    """
    UniProtID_list = random.sample(conftest.UniProt_IDs_human_list, i)
    prim_2_sec_dict = query.map_primary_2_secondary_ANs(ids_2_map=UniProtID_list, Primary_2_Secondary_IDs_dict=None, read_from_flat_files=False, ENSPs_only=True)
    fg_string = "%0d".join(prim_2_sec_dict.keys())
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "caller_identity": "PyTest"}, data={"foreground": fg_string})
    df_UP = pd.read_csv(StringIO(response.text), sep='\t')

    fg_string = "%0d".join(prim_2_sec_dict.values())
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "caller_identity": "PyTest"}, data={"foreground": fg_string})
    df_ENSP = pd.read_csv(StringIO(response.text), sep='\t')

    assert df_UP.shape[0] == df_ENSP.shape[0]

    df_UP = df_UP.drop(columns=[cn.FG_IDs])
    df_ENSP = df_ENSP.drop(columns=[cn.FG_IDs])
    pd_testing.assert_frame_equal(df_UP, df_ENSP)

# examples from webpage need to work
# check p_value vs FDR
def test_web_example_1():
    df = pd.read_csv(os.path.join(variables.EXAMPLE_FOLDER, "Example_Yeast_acetylation_abundance_correction.txt"), sep='\t')
    fg_id_string = "%0d".join(df.loc[df["Foreground"].notnull(), "Foreground"].tolist())
    bg_id_string = "%0d".join(df["Background"].tolist())
    bg_abundance_string = "%0d".join(df["Intensity"].astype(str).tolist())
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "abundance_correction", "caller_identity": "PyTest"},
        data={"foreground": fg_id_string,
              "background": bg_id_string,
              "background_intensity": bg_abundance_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 35
    assert df.groupby(cn.category).count().shape[0] >= 2 # GOCC from TM no longer gives hits
    cond_FDR = df[cn.p_value] <= df[cn.FDR]
    assert sum(cond_FDR) == len(cond_FDR)

def test_web_example_2():
    fg_string = "%0d".join(["P69905", "P68871", "P02042", "P02100"])
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "caller_identity": "PyTest"},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 100
    assert df.groupby(cn.category).count().shape[0] >= 9 # at least 9 categories with significant results, last time I checked (2020 04 01)
    cond_FDR = df[cn.p_value] <= df[cn.FDR]
    assert sum(cond_FDR) == len(cond_FDR)

def test_web_example_3():
    fg_string = "%0d".join(["Q9R117", "P33896", "O35664", "O35716", "P01575", "P42225", "P07351", "P52332", "Q9WVL2", "Q61179", "Q61716"])
    bg_string = "%0d".join(query.get_proteins_of_taxid(10090, read_from_flat_files=True))
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "compare_samples", "caller_identity": "PyTest"},
        data={"foreground": fg_string,
              "background": bg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] >= 190 # changed due to altering TextMining discretization hyperparameters
    assert df.groupby(cn.category).count().shape[0] >= 10  # at least 11 categories with significant results, last time I checked (2021 03 01)
    # changed after discretizing TM scores
    cond_FDR = df[cn.p_value] <= df[cn.FDR]
    assert sum(cond_FDR) == len(cond_FDR)

def test_web_example_4():
    fg_string = "MPRD_HUMAN"
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "characterize_foreground", "filter_foreground_count_one": False, "caller_identity": "PyTest"},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 200
    assert df.groupby(cn.category).count().shape[0] >= 9  # at least 11 categories with significant results, last time I checked (2020 04 01)

def test_taxid_species_mapping_1():
    """
    # 4932 Saccharomyces cerevisiae --> rank species
    # 1337652 Saccharomyces cerevisiae 101S
    # 559292 Saccharomyces cerevisiae S288C --> UniProt Ref prot
    4932 is Saccharomyces cerevisiae with rank species
    559292 is Saccharomyces cerevisiae S288C with rank 'no rank' --> used by UniProt Ref Prot
    """
    ENSPs = ['4932.YAR019C', '4932.YFR028C', '4932.YGR092W', '4932.YHR152W', '4932.YIL106W', '4932.YJL076W', '4932.YLR079W', '4932.YML064C', '4932.YMR055C', '4932.YOR373W', '4932.YPR119W']
    fg = "%0d".join(ENSPs)
    # UniProt reference proteomes uses "Saccharomyces cerevisiae S288C" with Taxid 559292 as a pan proteome instead of 4932 (TaxID on taxonomic rank of species).
    result = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 4932, "caller_identity": "PyTest"}, data={"foreground": fg})
    df_4932 = pd.read_csv(StringIO(result.text), sep="\t")

    result = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 559292, "caller_identity": "PyTest"}, data={"foreground": fg})
    df_559292 = pd.read_csv(StringIO(result.text), sep="\t")

    result = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 1337652, "caller_identity": "PyTest"}, data={"foreground": fg})
    df_1337652 = pd.read_csv(StringIO(result.text), sep="\t")

    pd_testing.assert_frame_equal(df_4932, df_559292)
    pd_testing.assert_frame_equal(df_4932, df_1337652)
    pd_testing.assert_frame_equal(df_559292, df_1337652)

def test_taxid_species_mapping_2():
    """
    4896 is Schizosaccharomyces pombe with rank species
    284812 is Schizosaccharomyces pombe 972h- with rank 'no rank' --> used by UniProt Ref Prot
    """
    fg_ids = ["1A1D_SCHPO","2AAA_SCHPO","2ABA_SCHPO","2AD1_SCHPO","2AD2_SCHPO","6PGD_SCHPO","6PGL_SCHPO","AAKB_SCHPO","AAKG_SCHPO","AAP1_SCHPO"]
    fg = "%0d".join(fg_ids)
    result = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 284812, "caller_identity": "PyTest"}, data={"foreground": fg})
    df_1 = pd.read_csv(StringIO(result.text), sep="\t")
    result = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 4896, "caller_identity": "PyTest"}, data={"foreground": fg})
    df_2 = pd.read_csv(StringIO(result.text), sep="\t")
    pd_testing.assert_frame_equal(df_1, df_2)

def test_taxid_species_mapping_3():
    """
    # 511145 Escherichia coli str. K-12 substr. MG1655
    # 562 E. coli --> rank species
    # 83334 Escherichia coli O157:H7 --> UniProt Ref Prot

    # https://www.uniprot.org/proteomes/?query=Escherichia+coli&sort=score
    # 562 E. coli --> rank species
    # 511145 Escherichia coli str. K-12 substr. MG1655 --> should match to 83333 not 83334!
    # 83333 Escherichia coli K-12 --> UniProt Ref Prot (with 4391 proteins)
    # 83334 Escherichia coli O157:H7 --> UniProt Ref Prot (with 5062 proteins)
    {'taxid': '511145', 'output_format': 'json', 'foreground': '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263%0d511145.b1264%0d511145.b1812%0d511145.b2551%0d511145.b3117%0d511145.b3772%0d511145.b1015%0d511145.b2585', 'background': '', 'enrichment_method': 'genome', 'FDR_cutoff': '0.05', 'caller_identity': '11_0', 'STRING_beta': True}
    """
    fg = '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263%0d511145.b1264%0d511145.b1812%0d511145.b2551%0d511145.b3117%0d511145.b3772%0d511145.b1015%0d511145.b2585'
    bg = ""
    result = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 511145, "caller_identity": "PyTest", "STRING_beta": True, 'FDR_cutoff': '0.05'}, data={"foreground": fg, "background": bg})
    df_1 = pd.read_csv(StringIO(result.text), sep="\t")
    assert df_1.shape[0] > 0

    # check that PMID "background_count" is larger than 0
    ser = df_1.loc[df_1[cn.etype] == -56, "background_count"]
    assert ser.shape[0] == ser[ser > 0].shape[0]

    result = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 83333, "caller_identity": "PyTest", "STRING_beta": True, 'FDR_cutoff': '0.05'}, data={"foreground": fg, "background": bg})
    df_2 = pd.read_csv(StringIO(result.text), sep="\t")
    pd_testing.assert_frame_equal(df_1, df_2)

def test_taxid_species_mapping_4():
    """
    561 --> Escherichia --> shouldn't work since not on species level
    562 --> Escherichia coli --> works since it get's mapped to a UniProt Reference Proteome via TaxidSpecies_2_TaxidProteome_dict
    511145 --> Escherichia coli str. K-12 substr. MG1655 --> works since it get's mapped to a UniProt Reference Proteome via TaxidSpecies_2_TaxidProteome_dict
    562 should map to 83334 (max num proteins)
    511145 should both map 83333 since this is closer in the lineage/tree
    """
    fg = '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263%0d511145.b1264%0d511145.b1812%0d511145.b2551%0d511145.b3117%0d511145.b3772%0d511145.b1015%0d511145.b2585'
    result = requests.post(url_local_API_orig, params={"output_format": "json", "enrichment_method": "genome", "taxid": 562, "caller_identity": "PyTest", "STRING_beta": True, 'FDR_cutoff': '0.05'}, data={"foreground": fg})
    df_json_1 = pd.read_json(result.text)
    assert df_json_1.shape[0] > 10

    result = requests.post(url_local_API_orig, params={"output_format": "json", "enrichment_method": "genome", "taxid": 83334, "caller_identity": "PyTest", "STRING_beta": True, 'FDR_cutoff': '0.05'}, data={"foreground": fg})
    df_json_2 = pd.read_json(result.text)
    assert df_json_2.shape[0] > 10

    result = requests.post(url_local_API_orig, params={"output_format": "json", "enrichment_method": "genome", "taxid": 511145, "caller_identity": "PyTest", "STRING_beta": True, 'FDR_cutoff': '0.05'}, data={"foreground": fg})
    df_json_3 = pd.read_json(result.text)
    assert df_json_3.shape[0] > 10

    result = requests.post(url_local_API_orig, params={"output_format": "json", "enrichment_method": "genome", "taxid": 83333, "caller_identity": "PyTest", "STRING_beta": True, 'FDR_cutoff': '0.05'}, data={"foreground": fg})
    df_json_4 = pd.read_json(result.text)
    assert df_json_4.shape[0] > 10
    pd_testing.assert_frame_equal(df_json_1, df_json_2)
    pd_testing.assert_frame_equal(df_json_3, df_json_4)


def test_wrong_Taxid_1():
    """
    561 --> Escherichia --> shouldn't work since not on species level
    """
    fg = '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263%0d511145.b1264%0d511145.b1812%0d511145.b2551%0d511145.b3117%0d511145.b3772%0d511145.b1015%0d511145.b2585'
    result = requests.post(url_local_API_orig, params={"output_format": "json", "enrichment_method": "genome", "taxid": 561, "caller_identity": "PyTest", "STRING_beta": True, 'FDR_cutoff': '0.05'}, data={"foreground": fg})
    results_json = json.loads(result.text)
    keys_lower = [ele.lower() for ele in results_json.keys()]
    assert "error taxid" in keys_lower

def test_compare_samples_works_without_error():
    """
    Damian problematic call
    {'taxid': '511145', 'output_format': 'json', 'enrichment_method': 'compare_samples', 'FDR_cutoff': '0.05', 'caller_identity': '11_0', 'STRING_beta': True}
{'foreground': '511145.b1261%0d511145.b1260%0d511145.b1263%0d511145.b1262', 'background': '511145.b1260%0d511145.b1263%0d511145.b1262%0d511145.b1812%0d511145.b1261'}
    """
    params = {'taxid': '511145', 'output_format': 'json', 'enrichment_method': 'compare_samples', 'FDR_cutoff': '1.05', 'caller_identity': 'PyTest', 'STRING_beta': True}
    data = {'foreground': '511145.b1261%0d511145.b1260%0d511145.b1263%0d511145.b1262', 'background': '511145.b1260%0d511145.b1263%0d511145.b1262%0d511145.b1812%0d511145.b1261'}
    result = requests.post(url_local_API_orig, params=params, data=data)
    result_json = json.loads(result.text)
    assert len(result_json) > 10

@pytest.mark.parametrize("i", range(3))
def test_compare_funEnum_consistency(i):
    """
    compare funcEnum from flatfile with funcEnum returned via API.
    Randomly select Protein ID. query associated functions from file, compare with API
    """
    UniProtID = random.sample(conftest.UniProt_IDs_human_list, 1)[0]
    response = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "characterize_foreground", "filter_foreground_count_one": False, "caller_identity": "PyTest"},
        data={"foreground": UniProtID})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    for funcEnum, term in zip(df[cn.funcEnum], df[cn.term]):
        assert conftest.funcEnum_2_funcName_dict[funcEnum] == term

### abundance correction tests
def test_abundance_correction_with_intensity_instead_of_background_intensity(random_abundance_correction_foreground_background):
    foreground, background, intensity, taxid = random_abundance_correction_foreground_background
    params = {'taxid': taxid, 'output_format': 'tsv', 'enrichment_method': 'abundance_correction', 'FDR_cutoff': '1.0', "caller_identity": "PyTest"}
    # should be "background_intensity" instead of "intensity" but nonetheless this should work
    data = {'foreground': "%0d".join(foreground), 'background': "%0d".join(background), "intensity": "%0d".join(intensity)}
    response = requests.post(url_local_API_orig, params=params, data=data)
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert (df[cn.FG_n] == df[cn.BG_n]).all()
    assert (df[cn.FG_count] <= df[cn.FG_n]).all()
    assert (df[cn.BG_count] <= df[cn.BG_n]).all()

def test_random_abundance_correction(random_abundance_correction_foreground_background):
    """
    fg_n == bg_n
    fg_count == bg_count

    this can't be guaranteed because of the correction factor
    assert (df[cn.FG_count] <= df[cn.BG_count]).all()
    """
    foreground, background, intensity, taxid = random_abundance_correction_foreground_background
    params = {'taxid': taxid, 'output_format': 'tsv', 'enrichment_method': 'abundance_correction', 'FDR_cutoff': '1.0', "caller_identity": "PyTest"}
    # should be "background_intensity" instead of "intensity" but nonetheless this should work
    data = {'foreground': "%0d".join(foreground), 'background': "%0d".join(background), "intensity": "%0d".join(intensity)}
    # addiontally testing that "intensity" maps to "background_intensity"
    response = requests.post(url_local_API_orig, params=params, data=data)
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert (df[cn.FG_n] == df[cn.BG_n]).all()
    assert (df[cn.FG_count] <= df[cn.FG_n]).all()
    assert (df[cn.BG_count] <= df[cn.BG_n]).all()

def test_abundance_correction_fg_equals_bg(random_abundance_correction_foreground_background):
    """
    no enrichment expected, but counts should be equal for
    fg_n == bg_n
    fg_count == bg_count
    """
    _, background, intensity, taxid = random_abundance_correction_foreground_background
    params = {'taxid': taxid, 'output_format': 'tsv', 'enrichment_method': 'abundance_correction', 'FDR_cutoff': '1.0', "caller_identity": "PyTest"}
    ### use background as foreground on purpose
    data = {'foreground': "%0d".join(background), 'background': "%0d".join(background), "background_intensity": "%0d".join(intensity)}
    response = requests.post(url_local_API_orig, params=params, data=data)
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert (df[cn.FG_count] == df[cn.BG_count]).all()
    assert (df[cn.FG_n] == df[cn.BG_n]).all()
    assert (df[cn.FG_count] <= df[cn.FG_n]).all()
    assert (df[cn.BG_count] <= df[cn.BG_n]).all()

# def test_abundance_correction_impute_values(random_abundance_correction_foreground_background):
def test_abundance_correction_impute_values(random_abundance_correction_foreground_background_human):
    """
    pytest failed on
    20210427
    20210425

    self = Empty DataFrame
    Columns: [{"ERROR_UserInput":"ERROR_UserInput: Something went wrong parsing your input, please check y..."organism":9606,"output_format":"tsv","p_value_cutoff":1.0,"population":null,"species":9606,"taxid":1922782}]

    self = Empty DataFrame
    Columns: [{"ERROR_UserInput":"ERROR_UserInput: Something went wrong parsing your input, please check y..."organism":9606,"output_format":"tsv","p_value_cutoff":1.0,"population":null,"species":9606,"taxid":1923608}]

    keep observing if this fails or others
    """
    foreground, background, intensity, taxid = random_abundance_correction_foreground_background_human
    params = {'taxid': taxid, 'output_format': 'tsv', 'enrichment_method': 'abundance_correction',
              'FDR_cutoff': 1, 'p_value_cutoff': 1, "caller_identity": "PyTest",
              "filter_foreground_count_one": False, "filter_parents": False}

    ### background a bit bigger than foreground
    bg_1 = foreground + background[:100]
    in_1 = intensity[:len(bg_1)] #[str(ele) for ele in np.random.normal(size=len(bg_1))]
    data = {'foreground': "%0d".join(foreground), 'background': "%0d".join(bg_1), "background_intensity": "%0d".join(in_1)}
    response = requests.post(url_local_API_orig, params=params, data=data)
    df_1 = pd.read_csv(StringIO(response.text), sep='\t').sort_values([cn.term, "description"]).reset_index(drop=True)

    ### add genome with imputed values (the same for all)
    bg_2 = bg_1 + list(set(background) - set(bg_1))
    value_2_impute = min([float(ele) for ele in in_1]) - 1
    in_2 = in_1 + [str(value_2_impute)]*(len(bg_2) - len(bg_1))
    data = {'foreground': "%0d".join(foreground), 'background': "%0d".join(bg_2), "background_intensity": "%0d".join(in_2)}
    response = requests.post(url_local_API_orig, params=params, data=data)
    df_2 = pd.read_csv(StringIO(response.text), sep='\t')
    df_2_sub = df_2[df_2[cn.term].isin(df_1[cn.term])].sort_values([cn.term, "description"]).reset_index(drop=True)
    assert df_1.shape[0] == df_2_sub.shape[0]
    assert (df_1[cn.FG_count] == df_2_sub[cn.FG_count]).all()
    assert (df_1[cn.BG_n] == df_2_sub[cn.BG_n]).all()
    # since imputed values don't affect correction_factor, the BG counts should only increase
    assert (df_1[cn.BG_count] <= df_2_sub[cn.BG_count]).all()

def test_tsv_and_json_results_are_equal():
    ENSP_list = ["511145.b1260", "511145.b1261", "511145.b1262", "511145.b1263"]
    fg = "%0d".join(ENSP_list)
    result = requests.post(url_local_API_orig, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 511145, "caller_identity": "PyTest"}, data={"foreground": fg})
    df_tsv = pd.read_csv(StringIO(result.text), sep='\t')
    result = requests.post(url_local_API_orig, params={"output_format": "json", "enrichment_method": "genome", "taxid": 511145, "caller_identity": "PyTest"}, data={"foreground": fg})
    df_json = pd.read_json(result.text)
    pd_testing.assert_frame_equal(df_tsv, df_json)

def test_json_precision():
    fg = "9606.ENSP00000228682%0d9606.ENSP00000332353%0d9606.ENSP00000297261%0d9606.ENSP00000379258%0d9606.ENSP00000296575%0d9606.ENSP00000249373"
    result = requests.post(url_local_API_orig, params={"output_format": "json", "enrichment_method": "genome", "taxid": 9606, "caller_identity": "PyTest"}, data={"foreground": fg})
    term = "GO:0007224"
    df = pd.read_json(result.text)
    p_value = df.loc[df["term"] == term, "p_value"].values[0]
    assert p_value > 0
    assert p_value <= 9.9388e-7

def test_STRING_style_API_species_gets_mapped_to_taxid():
    response = requests.post(url_local_API_STRING_style + "/json/enrichment?species=9606&identifiers=9606.ENSP00000326366%0A9606.ENSP00000263094%0A9606.ENSP00000340820%0A9606.ENSP00000260408%0A9606.ENSP00000252486%0A9606.ENSP00000355747%0A9606.ENSP00000338345%0A9606.ENSP00000260197%0A9606.ENSP00000315130%0A9606.ENSP00000284981&caller_identity=PyTest")
    df1 = pd.read_json(response.text)
    del df1["preferredNames"]
    response = requests.post(url_local_API_STRING_style + "/json/enrichment?taxid=9606&identifiers=9606.ENSP00000326366%0A9606.ENSP00000263094%0A9606.ENSP00000340820%0A9606.ENSP00000260408%0A9606.ENSP00000252486%0A9606.ENSP00000355747%0A9606.ENSP00000338345%0A9606.ENSP00000260197%0A9606.ENSP00000315130%0A9606.ENSP00000284981&caller_identity=PyTest")
    df2 = pd.read_json(response.text)
    del df2["preferredNames"]
    pd_testing.assert_frame_equal(df1, df2, check_dtype=False)
    assert df1.shape[0] > 10  # should get a lot more rows

    response = requests.post(url_local_API_STRING_style + "/tsv/enrichment?taxid=9606&identifiers=9606.ENSP00000326366%0A9606.ENSP00000263094%0A9606.ENSP00000340820%0A9606.ENSP00000260408%0A9606.ENSP00000252486%0A9606.ENSP00000355747%0A9606.ENSP00000338345%0A9606.ENSP00000260197%0A9606.ENSP00000315130%0A9606.ENSP00000284981&caller_identity=PyTest")
    df3 = pd.read_csv(StringIO(response.text), sep='\t')
    del df3["preferredNames"]
    del df3["inputGenes"]
    del df2["inputGenes"]
    pd_testing.assert_frame_equal(df3, df2, check_dtype=False)

@pytest.mark.xfail
def test_STRING_style_API_species_gets_mapped_to_taxid_2():
    """
    the results should differ and NOT be the same because different Taxids were used
    """
    response = requests.post(url_local_API_STRING_style + "/json/enrichment?species=9606&identifiers=9606.ENSP00000326366%0A9606.ENSP00000263094%0A9606.ENSP00000340820%0A9606.ENSP00000260408%0A9606.ENSP00000252486%0A9606.ENSP00000355747%0A9606.ENSP00000338345%0A9606.ENSP00000260197%0A9606.ENSP00000315130%0A9606.ENSP00000284981&caller_identity=PyTest")
    df1 = pd.read_json(response.text)
    response = requests.post(url_local_API_STRING_style + "/json/enrichment?species=10090&identifiers=9606.ENSP00000326366%0A9606.ENSP00000263094%0A9606.ENSP00000340820%0A9606.ENSP00000260408%0A9606.ENSP00000252486%0A9606.ENSP00000355747%0A9606.ENSP00000338345%0A9606.ENSP00000260197%0A9606.ENSP00000315130%0A9606.ENSP00000284981&caller_identity=PyTest")
    df2 = pd.read_json(response.text)
    pd_testing.assert_frame_equal(df1, df2)

def test_STRING_style_API_functional_annotation():
    """
    json and tsv should yield the same results
    default argument for functional_annotation filter_foreground_count_one should be False
    """
    response = requests.post(url_local_API_STRING_style + "/tsv/functional_annotation?filter_foreground_count_one=False&identifiers=P69905%0dP68871%0dP02042%0dP02100&caller_identity=PyTest")
    df1 = pd.read_csv(StringIO(response.text), sep='\t')
    response = requests.post(url_local_API_STRING_style + "/tsv/functional_annotation?identifiers=P69905%0dP68871%0dP02042%0dP02100&caller_identity=PyTest")
    df2 = pd.read_csv(StringIO(response.text), sep='\t')
    pd_testing.assert_frame_equal(df1, df2)

def test_STRING_style_API_foreground_count_one_genome():
    """
    default argument for functional_annotation filter_foreground_count_one should be Truetest_STRING_style_API_foreground_count_one_genome():
    """
    response = requests.post(url_local_API_STRING_style + "/tsv/enrichment?filter_foreground_count_one=True&species=9606&identifiers=9606.ENSP00000326366%0A9606.ENSP00000263094%0A9606.ENSP00000340820%0A9606.ENSP00000260408%0A9606.ENSP00000252486%0A9606.ENSP00000355747%0A9606.ENSP00000338345%0A9606.ENSP00000260197%0A9606.ENSP00000315130%0A9606.ENSP00000284981&caller_identity=PyTest")
    df1 = pd.read_csv(StringIO(response.text), sep='\t')
    response = requests.post(url_local_API_STRING_style + "/tsv/enrichment?&species=9606&identifiers=9606.ENSP00000326366%0A9606.ENSP00000263094%0A9606.ENSP00000340820%0A9606.ENSP00000260408%0A9606.ENSP00000252486%0A9606.ENSP00000355747%0A9606.ENSP00000338345%0A9606.ENSP00000260197%0A9606.ENSP00000315130%0A9606.ENSP00000284981&caller_identity=PyTest")
    df2 = pd.read_csv(StringIO(response.text), sep='\t')
    pd_testing.assert_frame_equal(df1, df2)

def test_STRING_style_API_Nadya_example_1():
    """
    %0A and %0d should both work as separators
    """
    response = requests.post(url_local_API_STRING_style + "/json/enrichment?species=9606&identifiers=9606.ENSP00000326366%0A9606.ENSP00000263094%0A9606.ENSP00000340820%0A9606.ENSP00000260408%0A9606.ENSP00000252486%0A9606.ENSP00000355747%0A9606.ENSP00000338345%0A9606.ENSP00000260197%0A9606.ENSP00000315130%0A9606.ENSP00000284981&caller_identity=PyTest")
    df1 = pd.read_json(response.text)
    response = requests.post(url_local_API_STRING_style + "/json/enrichment?species=9606&identifiers=9606.ENSP00000326366%0d9606.ENSP00000263094%0d9606.ENSP00000340820%0d9606.ENSP00000260408%0d9606.ENSP00000252486%0d9606.ENSP00000355747%0d9606.ENSP00000338345%0d9606.ENSP00000260197%0d9606.ENSP00000315130%0d9606.ENSP00000284981&caller_identity=PyTest")
    df2 = pd.read_json(response.text)
    pd_testing.assert_frame_equal(df1, df2)


# http://0.0.0.0:5912/api/json/enrichment?species=9606&identifiers=9606.ENSP00000326366%0A9606.ENSP00000263094%0A9606.ENSP00000340820%0A9606.ENSP00000260408%0A9606.ENSP00000252486%0A9606.ENSP00000355747%0A9606.ENSP00000338345%0A9606.ENSP00000260197%0A9606.ENSP00000315130%0A9606.ENSP00000284981&caller_identity=string_app_v1_7_0
#
# http://0.0.0.0:5912/api/tsv/?output_format=tsv&enrichment_method=genome&taxid=9606&caller_identity=test&foreground=P69905%0dP68871%0dP02042%0dP02100
# http://0.0.0.0:5912/api/tsv/enrichment?species=9606&identifiers=P69905%0dP68871%0dP02042%0dP02100&caller_identity=string_app_v1_7_0


# def test filter_foreground_count_one should be True for functional_annotation and False for genome by default



# if __name__ == "__main__":
    # foreground, background, intensity, taxid = random_abundance_correction_foreground_background
    # params = {'taxid': taxid, 'output_format': 'tsv', 'enrichment_method': 'abundance_correction', 'FDR_cutoff': '1.0'}
    # # should be "background_intensity" instead of "intensity" but nonetheless this should work
    # data = {'foreground': "%0d".join(foreground), 'background': "%0d".join(background), "intensity": "%0d".join(intensity)}
    # response = requests.post(url_local, params=params, data=data)
    # df = pd.read_csv(StringIO(response.text), sep='\t')
    # assert (df[cn.FG_n] == df[cn.BG_n]).all()
    # assert (df[cn.FG_count] <= df[cn.FG_n]).all()
    # assert (df[cn.BG_count] <= df[cn.BG_n]).all()