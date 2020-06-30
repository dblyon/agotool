import sys, os #, json
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import pandas as pd
from pandas import testing as pd_testing
import pytest, random
import math
from scipy import stats
# import numpy as np
# from itertools import islice
from io import StringIO
import requests
import conftest

import variables #, query


#### settings / parameters
url_local = r"http://127.0.0.1:10112/api"
# url_local = r"http://agotool.meringlab.org/api"
correlation_coefficient_min_threhold = 0.99
p_value_min_threshold = 1e-20

def test_random_contiguous_input_yields_results():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=100, UniProt_ID=False, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "foreground": fg_string, "enrichment_method": "genome", "taxid": 9606})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    is_true = df.shape[0] > 0
    if not is_true:
        response = requests.post(url_local, params={"output_format": "tsv", "foreground": fg_string, "enrichment_method": "genome", "taxid": 9606, "FDR_cutoff": 1, "p_value_uncorrected": 1})
        df = pd.read_csv(StringIO(response.text), sep='\t')
        assert df.shape[0] > 0

### tests for enrichment_method genome
def test_FG_count_not_larger_than_FG_n():
    num_ENSPs = 100
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=num_ENSPs, UniProt_ID=False, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    is_true = df.shape[0] > 0
    if not is_true:
        response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "FDR_cutoff": 1, "p_value_uncorrected": 1},
            data={"foreground": fg_string})
        df = pd.read_csv(StringIO(response.text), sep='\t')
        assert df.shape[0] > 0
    df["FG_n"] = num_ENSPs
    cond = df["foreground_count"] <= df["FG_n"]

def test_FG_count_not_larger_than_BG_count():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=200, UniProt_ID=False, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    is_true = df.shape[0] > 0
    if not is_true:
        response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "FDR_cutoff": 1, "p_value_uncorrected": 1},
            data={"foreground": fg_string})
        df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0
    cond = df["foreground_count"] <= df["background_count"]
    assert cond.all()

@pytest.mark.parametrize("i", range(25, 425, 25))
def test_genome_random_inputs(i):
    """
    genome sanity checks
    """
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=i, UniProt_ID=False, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    is_true = df.shape[0] > 0
    if not is_true:
        response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "FDR_cutoff": 1, "p_value_uncorrected": 1},
            data={"foreground": fg_string})
        df = pd.read_csv(StringIO(response.text), sep='\t')
        assert df.shape[0] > 0

    cond = df["foreground_count"] <= df["background_count"]
    assert cond.all()
    df["FG_n"] = i
    cond = df["foreground_count"] <= df["FG_n"]
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
    # fg_list = ["P69905", "P68871", "P02042", "P02100"]
    ENSP_list = ['9606.ENSP0000025159', '9606.ENSP0000032242', '9606.ENSP00000333994', '9606.ENSP00000369654', '9606.ENSP00000369586']
    fg_string = "%0d".join(ENSP_list)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    expected_terms = ["KW-0561", "KW-0349", "GO:0005344", "GO:0019825", "GO:0020037", "GO:0005833"]
    cond = df["term"].isin(expected_terms)
    assert len(expected_terms) == sum(cond)

#### STRING_example_MultipleProteins
###  - check valid result
###  - check result simlilar to expected static outcome of STRING v11.3 (includes PMID autoupdates) compare with stats.pearsonr
def test_STRING_example_MultipleProteins_1():
    """
    Escherichia coli str. K-12 substr. MG1655
    Taxonomy ID: 511145 (for references in articles please use NCBI:txid511145)
    Proteins/Genes:
    trpA 511145.b1260
    trpB 511145.b1261
    TRPC_ECOLI 511145.b1262
    trpD 511145.b1263
    organism: Escherichia coli K12_MG1655
    foreground 511145.b1262%0d511145.b1261%0d511145.b1263%0d511145.b1260

    ENSP_list = ["511145.b1260", "511145.b1261", "511145.b1262", "511145.b1263"]
    r = requests.post("https://string-db.org/api/tsv/enrichment",
                      params={"identifiers": "\r".join(ENSP_list),
                              "species": 511145, "caller_identity": "www.aweseome_app.org"})
    df = pd.read_csv(StringIO(r.text), sep='\t')
    dir_ = r"/Users/dblyon/modules/cpr/agotool/data/exampledata"
    fn_out = os.path.join(dir_, "STRING_v11.3_MultipleProteins_example_1.txt")
    df.to_csv(fn_out, sep="\t", header=True, index=False)

    ### STRING example 1
    # genome of E.coli vs '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263'
    # Aquarius update_ALL version
    curl "https://agotool.org/api?taxid=9606&output_format=tsv&enrichment_method=genome&taxid=511145&caller_identity=test&foreground=511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263" | head

    # Aquarius
    curl "http://agotool.meringlab.org/api?taxid=9606&output_format=tsv&enrichment_method=genome&taxid=511145&caller_identity=test&foreground=511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263" | head

    # When on Pisces
    curl "http://127.0.0.1:5912/api?taxid=9606&output_format=tsv&enrichment_method=genome&taxid=511145&caller_identity=test&foreground=511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263" | head
    curl "https://string-db.org/api/tsv/enrichment?identifiers=trpA%0dtrpB%0dtrpC%0dtrpE%0dtrpGD"
    """
    fn = os.path.join(variables.EXAMPLE_FOLDER, "STRING_v11.3_MultipleProteins_example_1.txt")
    df_string_orig = pd.read_csv(fn, sep='\t')

    ENSP_list = ["511145.b1260", "511145.b1261", "511145.b1262", "511145.b1263"]
    fg = "%0d".join(ENSP_list)
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 511145}, data={"foreground": fg})
    df_agotool = pd.read_csv(StringIO(result.text), sep='\t')

    test_suceeded = helper_compare_DataFrames_p_values(df_string_orig, df_agotool)
    assert test_suceeded

def test_STRING_example_MultipleProteins_2():
    """
    Proteins/Genes:
    ANP1_YEAST
    YJR075W
    VAN1
    OLE1
    MNN11
    organism: Saccharomyces cerevisiae
    4932.YGL055W%0d4932.YEL036C%0d4932.YJL183W%0d4932.YJR075W%0d4932.YML115C
    ENSP_list = ['4932.YGL055W', '4932.YEL036C', '4932.YJL183W', '4932.YJR075W', '4932.YML115C']
    r = requests.post("https://string-db.org/api/tsv/enrichment",
                      params={"identifiers": "\r".join(ENSP_list),
                              "species": 4932, "caller_identity": "www.aweseome_app.org"})
    df = pd.read_csv(StringIO(r.text), sep='\t')
    dir_ = r"/Users/dblyon/modules/cpr/agotool/data/exampledata"
    fn_out = os.path.join(dir_, "STRING_v11.3_MultipleProteins_example_2.txt")
    df.to_csv(fn_out, sep="\t", header=True, index=False)
    """
    fn = os.path.join(variables.EXAMPLE_FOLDER, "STRING_v11.3_MultipleProteins_example_2.txt")
    df_string_orig = pd.read_csv(fn, sep='\t')

    ENSP_list = ['4932.YGL055W', '4932.YEL036C', '4932.YJL183W', '4932.YJR075W', '4932.YML115C']
    fg = "%0d".join(ENSP_list)
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 4932}, data={"foreground": fg})
    df_agotool = pd.read_csv(StringIO(result.text), sep='\t')

    test_suceeded = helper_compare_DataFrames_p_values(df_string_orig, df_agotool)
    assert test_suceeded

def test_STRING_example_MultipleProteins_3():
    """
    Proteins/Genes:
    smoothened
    patched
    hedgehog
    cubitus interruptus
    organism: Drosophila melanogaster
    7227.FBpp0088443%0d7227.FBpp0077788%0d7227.FBpp0088245%0d7227.FBpp0099945
    ENSP_list = ['7227.FBpp0088443', '7227.FBpp0077788', '7227.FBpp0088245', '7227.FBpp0099945']
    r = requests.post("https://string-db.org/api/tsv/enrichment",
                      params={"identifiers": "\r".join(ENSP_list),
                              "species": 7227, "caller_identity": "www.aweseome_app.org"})
    df = pd.read_csv(StringIO(r.text), sep='\t')
    dir_ = r"/Users/dblyon/modules/cpr/agotool/data/exampledata"
    fn_out = os.path.join(dir_, "STRING_v11.3_MultipleProteins_example_3.txt")
    df.to_csv(fn_out, sep="\t", header=True, index=False)
    """
    fn = os.path.join(variables.EXAMPLE_FOLDER, "STRING_v11.3_MultipleProteins_example_3.txt")
    df_string_orig = pd.read_csv(fn, sep='\t')

    ENSP_list = ['7227.FBpp0088443', '7227.FBpp0077788', '7227.FBpp0088245', '7227.FBpp0099945']
    fg = "%0d".join(ENSP_list)
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 7227}, data={"foreground": fg})
    df_agotool = pd.read_csv(StringIO(result.text), sep='\t')

    test_suceeded = helper_compare_DataFrames_p_values(df_string_orig, df_agotool)
    assert test_suceeded

def test_Christian_example_1():
    """
    ENSP_list = ['9606.ENSP00000228682', '9606.ENSP00000249373', '9606.ENSP00000296575', '9606.ENSP00000297261', '9606.ENSP00000332353', '9606.ENSP00000379258']
    r = requests.post("https://string-db.org/api/tsv/enrichment",
                      params={"identifiers": "\r".join(ENSP_list),
                              "species": 9606, "caller_identity": "www.aweseome_app.org"})
    df = pd.read_csv(StringIO(r.text), sep='\t')
    dir_ = r"/Users/dblyon/modules/cpr/agotool/data/exampledata"
    fn_out = os.path.join(dir_, "STRING_v11.3_MultipleProteins_example_4.txt")
    df.to_csv(fn_out, sep="\t", header=True, index=False)
    """
    fn = os.path.join(variables.EXAMPLE_FOLDER, "STRING_v11.3_MultipleProteins_example_4.txt")
    df_string_orig = pd.read_csv(fn, sep='\t')

    ENSP_list = ['9606.ENSP00000228682', '9606.ENSP00000249373', '9606.ENSP00000296575', '9606.ENSP00000297261', '9606.ENSP00000332353', '9606.ENSP00000379258']
    fg = "%0d".join(ENSP_list)
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg})
    df_agotool = pd.read_csv(StringIO(result.text), sep='\t')

    test_suceeded = helper_compare_DataFrames_p_values(df_string_orig, df_agotool)
    assert test_suceeded

def helper_compare_DataFrames_p_values(df_string_orig, df_agotool):
    dfs = df_string_orig
    df = df_agotool
    dfs["term"] = dfs["term"].apply(lambda x: x.replace("GO.", "GO:"))
    df["log_p_value"] = df["p_value"].apply(lambda x: math.log(x) * -1)
    dfs["log_p_value"] = dfs["p_value"].apply(lambda x: math.log(x) * -1)
    df["log_FDR"] = df["FDR"].apply(lambda x: math.log(x) * -1)
    dfs["log_fdr"] = dfs["fdr"].apply(lambda x: math.log(x) * -1)
    dfm = df[["term", "p_value", "log_p_value", "log_FDR", "FDR"]].merge(dfs[["term", "p_value", "log_p_value", "log_fdr", "fdr"]], on="term")

    correlation_coefficient, p_value = stats.pearsonr(dfm["p_value_x"], dfm["p_value_y"])
    assert correlation_coefficient > correlation_coefficient_min_threhold
    assert p_value <= p_value_min_threshold

    correlation_coefficient, p_value = stats.pearsonr(dfm["FDR"], dfm["fdr"])
    assert correlation_coefficient > correlation_coefficient_min_threhold
    assert p_value <= p_value_min_threshold

    correlation_coefficient, p_value = stats.pearsonr(dfm["log_FDR"], dfm["log_fdr"])
    assert correlation_coefficient > correlation_coefficient_min_threhold
    assert p_value <= p_value_min_threshold

    correlation_coefficient, p_value = stats.pearsonr(dfm["log_p_value_x"], dfm["log_p_value_y"])
    assert correlation_coefficient > correlation_coefficient_min_threhold
    assert p_value <= p_value_min_threshold

    return True

def test_tsv_and_json_results_are_equal():
    ENSP_list = ["511145.b1260", "511145.b1261", "511145.b1262", "511145.b1263"]
    fg = "%0d".join(ENSP_list)
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 511145}, data={"foreground": fg})
    df_tsv = pd.read_csv(StringIO(result.text), sep='\t')
    result = requests.post(url_local, params={"output_format": "json", "enrichment_method": "genome", "taxid": 511145}, data={"foreground": fg})
    df_json = pd.read_json(result.text)
    pd_testing.assert_frame_equal(df_tsv, df_json)

def test_json_precision():
    fg = "9606.ENSP00000228682%0d9606.ENSP00000332353%0d9606.ENSP00000297261%0d9606.ENSP00000379258%0d9606.ENSP00000296575%0d9606.ENSP00000249373"
    result = requests.post(url_local, params={"output_format": "json", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg})
    term = "GO:0007224"
    df = pd.read_json(result.text)
    p_value = df.loc[df["term"] == term, "p_value"].values[0]
    assert p_value > 0
    assert p_value < 1e-10



####### tests from agotool.org that can't simply be ported to this version
# # genome and compare_samples should yield the same results if given the same input
# def test_genome_same_as_compare_samples():
#     fg_string = conftest.get_random_human_ENSP(num_ENSPs=200, UniProt_ID=True, contiguous=True, joined_for_web=True)
#     response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
#         data={"foreground": fg_string})
#     df_genome = pd.read_csv(StringIO(response.text), sep='\t')
#
#     bg_string = "%0d".join(conftest.UniProt_IDs_human_list)
#     response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "compare_samples", "taxid": 9606},
#         data={"foreground": fg_string, "background": bg_string})
#     df_compare_samples = pd.read_csv(StringIO(response.text), sep='\t')
#
#     assert df_compare_samples.shape[0] == df_genome.shape[0] # same number of rows but additional column of BG_IDs for compare_samples
#
#     cond_FG_count = df_compare_samples["FG_count"] == df_genome["FG_count"]
#     assert cond_FG_count.all()
#
#     cond_BG_count = df_compare_samples["BG_count"] == df_genome["BG_count"]
#     assert cond_BG_count.all()
#
#     cond_BG_n = df_compare_samples["BG_n"] == df_genome["BG_n"]
#     assert cond_BG_n.all()


# @pytest.mark.parametrize("i", range(50, 250, 50))
# def test_ENSP_vs_UniProtID(i):
#     """
#     check that ENSP and UniProtIDs give same results
#     """
#     UniProtID_list = random.sample(conftest.UniProt_IDs_human_list, i)
#     prim_2_sec_dict = query.map_primary_2_secondary_ANs(ids_2_map=UniProtID_list, Primary_2_Secondary_IDs_dict=None, read_from_flat_files=False, ENSPs_only=True)
#     fg_string = "%0d".join(prim_2_sec_dict.keys())
#     response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg_string})
#     df_UP = pd.read_csv(StringIO(response.text), sep='\t')
#
#     fg_string = "%0d".join(prim_2_sec_dict.values())
#     response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg_string})
#     df_ENSP = pd.read_csv(StringIO(response.text), sep='\t')
#
#     assert df_UP.shape[0] == df_ENSP.shape[0]
#
#     df_UP = df_UP.drop(columns=["FG_IDs"])
#     df_ENSP = df_ENSP.drop(columns=["FG_IDs"])
#     pd_testing.assert_frame_equal(df_UP, df_ENSP)

# examples from webpage need to work
# check p_value vs FDR
# def test_web_example_1():
#     df = pd.read_csv(os.path.join(variables.EXAMPLE_FOLDER, "Example_Yeast_acetylation_abundance_correction.txt"), sep='\t')
#     fg_id_string = "%0d".join(df.loc[df["Foreground"].notnull(), "Foreground"].tolist())
#     bg_id_string = "%0d".join(df["Background"].tolist())
#     bg_abundance_string = "%0d".join(df["Intensity"].astype(str).tolist())
#     response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "abundance_correction"},
#         data={"foreground": fg_id_string,
#               "background": bg_id_string,
#               "background_intensity": bg_abundance_string})
#     df = pd.read_csv(StringIO(response.text), sep='\t')
#     assert df.shape[0] > 50
#     assert df.groupby("category").count().shape[0] >= 5 # at least 5 categories with significant results, last time I checked (2020 04 01)
#     cond_FDR = df["p_value"] <= df["FDR"]
#     assert sum(cond_FDR) == len(cond_FDR)
#
# def test_web_example_2():
#     fg_string = "%0d".join(["P69905", "P68871", "P02042", "P02100"])
#     response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
#         data={"foreground": fg_string})
#     df = pd.read_csv(StringIO(response.text), sep='\t')
#     assert df.shape[0] > 100
#     assert df.groupby("category").count().shape[0] >= 9 # at least 9 categories with significant results, last time I checked (2020 04 01)
#     cond_FDR = df["p_value"] <= df["FDR"]
#     assert sum(cond_FDR) == len(cond_FDR)
#
# def test_web_example_3():
#     fg_string = "%0d".join(["Q9R117", "P33896", "O35664", "O35716", "P01575", "P42225", "P07351", "P52332", "Q9WVL2", "Q61179", "Q61716"])
#     bg_string = "%0d".join(query.get_proteins_of_taxid(10090, read_from_flat_files=True))
#     response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "compare_samples"},
#         data={"foreground": fg_string,
#               "background": bg_string})
#     df = pd.read_csv(StringIO(response.text), sep='\t')
#     assert df.shape[0] > 700
#     assert df.groupby("category").count().shape[0] >= 11  # at least 11 categories with significant results, last time I checked (2020 04 01)
#     cond_FDR = df["p_value"] <= df["FDR"]
#     assert sum(cond_FDR) == len(cond_FDR)
#
# def test_web_example_4():
#     fg_string = "MPRD_HUMAN"
#     response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "characterize_foreground", "filter_foreground_count_one": False},
#         data={"foreground": fg_string})
#     df = pd.read_csv(StringIO(response.text), sep='\t')
#     assert df.shape[0] > 1000
#     assert df.groupby("category").count().shape[0] >= 11  # at least 11 categories with significant results, last time I checked (2020 04 01)

# def test_taxid_species_mapping_1():
#     """
#     # 4932 Saccharomyces cerevisiae --> rank species
#     # 1337652 Saccharomyces cerevisiae 101S
#     # 559292 Saccharomyces cerevisiae S288C --> UniProt Ref prot
#     4932 is Saccharomyces cerevisiae with rank species
#     559292 is Saccharomyces cerevisiae S288C with rank 'no rank' --> used by UniProt Ref Prot
#     """
#     ENSPs = ['4932.YAR019C', '4932.YFR028C', '4932.YGR092W', '4932.YHR152W', '4932.YIL106W', '4932.YJL076W', '4932.YLR079W', '4932.YML064C', '4932.YMR055C', '4932.YOR373W', '4932.YPR119W']
#     fg = "%0d".join(ENSPs)
#     # UniProt reference proteomes uses "Saccharomyces cerevisiae S288C" with Taxid 559292 as a pan proteome instead of 4932 (TaxID on taxonomic rank of species).
#     result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 4932}, data={"foreground": fg})
#     df_4932 = pd.read_csv(StringIO(result.text), sep="\t")
#
#     result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 559292}, data={"foreground": fg})
#     df_559292 = pd.read_csv(StringIO(result.text), sep="\t")
#
#     result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 1337652}, data={"foreground": fg})
#     df_1337652 = pd.read_csv(StringIO(result.text), sep="\t")
#
#     pd_testing.assert_frame_equal(df_4932, df_559292)
#     pd_testing.assert_frame_equal(df_4932, df_1337652)
#     pd_testing.assert_frame_equal(df_559292, df_1337652)

# def test_taxid_species_mapping_2():
#     """
#     4896 is Schizosaccharomyces pombe with rank species
#     284812 is Schizosaccharomyces pombe 972h- with rank 'no rank' --> used by UniProt Ref Prot
#     """
#     fg_ids = ["1A1D_SCHPO","2AAA_SCHPO","2ABA_SCHPO","2AD1_SCHPO","2AD2_SCHPO","6PGD_SCHPO","6PGL_SCHPO","AAKB_SCHPO","AAKG_SCHPO","AAP1_SCHPO"]
#     fg = "%0d".join(fg_ids)
#     result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 284812}, data={"foreground": fg})
#     df_1 = pd.read_csv(StringIO(result.text), sep="\t")
#     result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 4896}, data={"foreground": fg})
#     df_2 = pd.read_csv(StringIO(result.text), sep="\t")
#     pd_testing.assert_frame_equal(df_1, df_2)

# def test_taxid_species_mapping_3():
#     """
#     # 511145 Escherichia coli str. K-12 substr. MG1655
#     # 562 E. coli --> rank species
#     # 83334 Escherichia coli O157:H7 --> UniProt Ref Prot
#
#     # https://www.uniprot.org/proteomes/?query=Escherichia+coli&sort=score
#     # 562 E. coli --> rank species
#     # 511145 Escherichia coli str. K-12 substr. MG1655 --> should match to 83333 not 83334!
#     # 83333 Escherichia coli K-12 --> UniProt Ref Prot (with 4391 proteins)
#     # 83334 Escherichia coli O157:H7 --> UniProt Ref Prot (with 5062 proteins)
#     {'taxid': '511145', 'output_format': 'json', 'foreground': '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263%0d511145.b1264%0d511145.b1812%0d511145.b2551%0d511145.b3117%0d511145.b3772%0d511145.b1015%0d511145.b2585', 'background': '', 'enrichment_method': 'genome', 'FDR_cutoff': '0.05', 'caller_identity': '11_0', 'STRING_beta': True}
#     """
#     fg = '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263%0d511145.b1264%0d511145.b1812%0d511145.b2551%0d511145.b3117%0d511145.b3772%0d511145.b1015%0d511145.b2585'
#     bg = ""
#     result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 511145, "caller_identity": "11_0", "STRING_beta": True, 'FDR_cutoff': '0.05'}, data={"foreground": fg, "background": bg})
#     df_1 = pd.read_csv(StringIO(result.text), sep="\t")
#     assert df_1.shape[0] > 0
#
#     # check that PMID "background_count" is larger than 0
#     ser = df_1.loc[df_1["etype"] == -56, "background_count"]
#     assert ser.shape[0] == ser[ser > 0].shape[0]
#
#     result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 83333, "caller_identity": "11_0", "STRING_beta": True, 'FDR_cutoff': '0.05'}, data={"foreground": fg, "background": bg})
#     df_2 = pd.read_csv(StringIO(result.text), sep="\t")
#     pd_testing.assert_frame_equal(df_1, df_2)

# def test_wrong_Taxid():
#     fg = '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263%0d511145.b1264%0d511145.b1812%0d511145.b2551%0d511145.b3117%0d511145.b3772%0d511145.b1015%0d511145.b2585'
#     result = requests.post(url_local, params={"output_format": "json", "enrichment_method": "genome", "taxid": 562, "caller_identity": "11_0", "STRING_beta": True, 'FDR_cutoff': '0.05'}, data={"foreground": fg})
#     results_json = json.loads(result.text)
#     keys_lower = [ele.lower() for ele in results_json.keys()]
#     assert "error taxid" in keys_lower

# @pytest.mark.parametrize("i", range(3))
# def test_compare_funEnum_consistency(i):
#     """
#     compare funcEnum from flatfile with funcEnum returned via API.
#     Randomly select Protein ID. query associated functions from file, compare with API
#     """
#     UniProtID = random.sample(conftest.UniProt_IDs_human_list, 1)[0]
#     response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "characterize_foreground", "filter_foreground_count_one": False}, data={"foreground": UniProtID})
#     df = pd.read_csv(StringIO(response.text), sep='\t')
#     for funcEnum, term in zip(df["funcEnum"], df["term"]):
#         assert conftest.funcEnum_2_funcName_dict[funcEnum] == term
