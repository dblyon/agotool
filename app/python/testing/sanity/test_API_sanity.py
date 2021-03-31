import sys, os #, json
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import pandas as pd
from pandas import testing as pd_testing
import pytest
import math
from scipy import stats
from io import StringIO
import requests
import conftest

import variables
import query


#### settings / parameters
# url_local = r"http://127.0.0.1:10114/api"
# url_local = variables.pytest_url_local
# url_local = conftest.get_url()
# url_local = r"http://agotool.meringlab.org/api"
correlation_coefficient_min_threhold = 0.95
p_value_min_threshold = 1e-8

def test_random_contiguous_input_yields_results(url_local):
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=100, UniProt_ID=False, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "foreground": fg_string, "enrichment_method": "genome", "taxid": 9606})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    is_true = df.shape[0] > 0
    if not is_true:
        response = requests.post(url_local, params={"output_format": "tsv", "foreground": fg_string, "enrichment_method": "genome", "taxid": 9606, "FDR_cutoff": 1, "p_value_uncorrected": 1})
        df = pd.read_csv(StringIO(response.text), sep='\t')
        assert df.shape[0] > 0

### tests for enrichment_method genome
def test_FG_count_not_larger_than_FG_n(url_local):
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
    assert cond.all()

def test_FG_count_not_larger_than_BG_count(url_local):
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

def test_FG_count_not_larger_than_BG_count_v2(url_local):
    ENSP_list = ["511145.b1260", "511145.b1261", "511145.b1262", "511145.b1263"]
    fg_string = "%0d".join(ENSP_list)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 511145},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    is_true = df.shape[0] > 0
    if not is_true:
        response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 511145, "FDR_cutoff": 1, "p_value_uncorrected": 1},
            data={"foreground": fg_string})
        df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0
    cond = df["foreground_count"] <= df["background_count"]
    assert cond.all()

@pytest.mark.parametrize("i", range(25, 425, 25))
def test_genome_random_inputs(i, url_local):
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

def test_expected_terms_in_output(url_local):
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
def test_STRING_example_MultipleProteins_1(url_local):
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

def test_STRING_example_MultipleProteins_2(url_local):
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

def test_STRING_example_MultipleProteins_3(url_local):
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

def test_Christian_example_1(url_local):
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

def test_tsv_and_json_results_are_equal(url_local):
    ENSP_list = ["511145.b1260", "511145.b1261", "511145.b1262", "511145.b1263"]
    fg = "%0d".join(ENSP_list)
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 511145}, data={"foreground": fg})
    df_tsv = pd.read_csv(StringIO(result.text), sep='\t')
    result = requests.post(url_local, params={"output_format": "json", "enrichment_method": "genome", "taxid": 511145}, data={"foreground": fg})
    df_json = pd.read_json(result.text)
    pd_testing.assert_frame_equal(df_tsv, df_json)

def test_json_precision(url_local):
    fg = "9606.ENSP00000228682%0d9606.ENSP00000332353%0d9606.ENSP00000297261%0d9606.ENSP00000379258%0d9606.ENSP00000296575%0d9606.ENSP00000249373"
    result = requests.post(url_local, params={"output_format": "json", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg})
    term = "GO:0007224"
    df = pd.read_json(result.text)
    p_value = df.loc[df["term"] == term, "p_value"].values[0]
    assert p_value > 0
    assert p_value < 1e-10

# def test_equality_of_Lineage_dict_flatFile_vs_pickled():
#     """
#     only pickled object rsynced to Aquarius... for local test
#     """
#     lineage_dict_v1 = query.get_lineage_dict_enum(as_array=False, read_from_flat_files=False, from_pickle=True)
#     lineage_dict_v2 = query.get_lineage_dict_enum(as_array=False, read_from_flat_files=True, from_pickle=False)
#     assert lineage_dict_v1 == lineage_dict_v2

def test_filter_parents_redundancy_STRING_clusters(url_local):
    fg = '9606.ENSP00000228872%0d9606.ENSP00000262643%0d9606.ENSP00000266970%0d9606.ENSP00000267163%0d9606.ENSP00000274026%0d9606.ENSP00000311083%0d9606.ENSP00000362082%0d9606.ENSP00000384849%0d9606.ENSP00000429089' # cdk2 homo sapiens
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": fg})
    df = pd.read_csv(StringIO(result.text), sep='\t')
    cond = df["term"] == "CL:12482"
    assert sum(cond) == 1
    cond = df["term"] == "CL:12477"
    assert sum(cond) == 0

def test_STRING_v115(url_local):
    ensps = ['9606.ENSP00000258149', '9606.ENSP00000262367', '9606.ENSP00000263253', '9606.ENSP00000266970', '9606.ENSP00000269305', '9606.ENSP00000278616', '9606.ENSP00000302564', '9606.ENSP00000341957', '9606.ENSP00000356150', '9606.ENSP00000372023', '9606.ENSP00000384849']
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606}, data={"foreground": "%0d".join(ensps)})
    df = pd.read_csv(StringIO(result.text), sep='\t')
    etype_set = set(df["etype"].unique())
    assert -58 not in etype_set
    assert -20 not in etype_set
    assert -25 not in etype_set
    assert -26 not in etype_set
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "limit_2_entity_type": "-78;-58;-57;-56;-55;-54;-53;-52;-51;-26;-25;-23;-22;-21;-20"}, data={"foreground": "%0d".join(ensps)})
    df1 = pd.read_csv(StringIO(result.text), sep='\t')
    etype_set = set(df1["etype"].unique())
    assert -58 in etype_set
    assert -20 in etype_set
    assert -25 in etype_set
    assert -26 in etype_set
    result = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606, "limit_2_entity_type": False}, data={"foreground": "%0d".join(ensps)})
    df2 = pd.read_csv(StringIO(result.text), sep='\t')
    pd_testing.assert_frame_equal(df1, df2)

def test_genome_and_compare_samples_are_identical(url_local):
    ENSP_list = ["511145.b1260", "511145.b1261", "511145.b1262", "511145.b1263"]
    fg_string = "%0d".join(ENSP_list)
    bg_string = "%0d".join(query.get_ENSPs_of_taxid("511145"))
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 511145},
        data={"foreground": fg_string})
    df1 = pd.read_csv(StringIO(response.text), sep='\t')
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "compare_samples", "taxid": 511145},
        data={"foreground": fg_string, "background": bg_string})
    df2 = pd.read_csv(StringIO(response.text), sep='\t')

    correlation_coefficient_min_threhold = 0.99
    p_value_min_threshold = 1e-20

    df1["log_p_value"] = df1["p_value"].apply(lambda x: math.log(x) * -1)
    df2["log_p_value"] = df2["p_value"].apply(lambda x: math.log(x) * -1)

    df1["log_FDR"] = df1["FDR"].apply(lambda x: math.log(x) * -1)
    df2["log_FDR"] = df2["FDR"].apply(lambda x: math.log(x) * -1)
    dfm = df1[["term", "p_value", "log_p_value", "log_FDR", "FDR"]].merge(df2[["term", "p_value", "log_p_value", "log_FDR", "FDR"]], on="term")

    correlation_coefficient, p_value = stats.pearsonr(dfm["p_value_x"], dfm["p_value_y"])
    assert correlation_coefficient > correlation_coefficient_min_threhold
    assert p_value <= p_value_min_threshold

    correlation_coefficient, p_value = stats.pearsonr(dfm["FDR_x"], dfm["FDR_y"])
    assert correlation_coefficient > correlation_coefficient_min_threhold
    assert p_value <= p_value_min_threshold

    correlation_coefficient, p_value = stats.pearsonr(dfm["log_FDR_x"], dfm["log_FDR_y"])
    assert correlation_coefficient > correlation_coefficient_min_threhold
    assert p_value <= p_value_min_threshold

    correlation_coefficient, p_value = stats.pearsonr(dfm["log_p_value_x"], dfm["log_p_value_y"])
    assert correlation_coefficient > correlation_coefficient_min_threhold
    assert p_value <= p_value_min_threshold


