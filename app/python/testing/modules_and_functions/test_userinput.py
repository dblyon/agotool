import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import pandas as pd
import numpy as np
from itertools import zip_longest
import pytest

import userinput, variables

TEST_FN_DIR = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), "test")

NUM_BINS = 100
DEFAULT_MISSING_BIN = -1

### empty DF, edge case
foreground_empty = pd.Series(name="foreground", data={0: np.nan, 1: np.nan, 2: np.nan})
background_empty = pd.DataFrame({"background": {0: np.nan, 1: np.nan, 2: np.nan},
                                 "intensity": {0: np.nan, 1: np.nan, 2: np.nan}})
foreground_empty_1 = pd.Series(dtype="float64")
background_empty_1 = pd.DataFrame()
foreground_empty_2 = [[], []]
background_empty_2 = [[], []]
foreground_empty_3 = []
background_empty_3 = []
foreground_empty_4 = None
background_empty_4 = None

foreground_almost_empty = pd.Series(name="foreground", data={0: np.nan, 1: "Q9UHI6", 2: np.nan})

### example0: nonesense AccessionNumbers, foreground is proper subset of background, everything has an abundance value
foreground_nonsense = pd.Series(name='foreground', data={0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'})
background_nonsense = pd.DataFrame({'background': {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O'},
                             'intensity': {0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 2.0, 7: 3.0, 8: 4.0, 9: 5.0, 10: 6.0, 11: 7.0, 12: 8.0, 13: 9.0, 14: 10.0}})

# without intensity values and nonsense ANs
foreground_no_intensity_nonsense = pd.Series(name='foreground', data={0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'})
background_no_intensity_nonsense = pd.DataFrame({'background': {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O'},
                             'intensity': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan, 5: np.nan, 6: np.nan, 7: np.nan, 8: np.nan, 9: np.nan, 10: np.nan, 11: np.nan, 12: np.nan, 13: np.nan, 14: np.nan}})
fg_bg_no_intensity_nonsense = [foreground_no_intensity_nonsense, background_no_intensity_nonsense]

# without intensity values
foreground_no_intensity = pd.Series(name='foreground', data={0: 'Q9UHI6', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9'})
background_no_intensity = pd.DataFrame({'background': {0: 'P13747', 1: 'Q6VB85', 2: 'Q8N8S7', 3: 'Q8WXE0', 4: 'Q9UHI6', 5: 'Q9UQ03', 6: 'Q13075', 7: 'A6NDB9', 8: 'A6NFR9', 9: 'O95359', 10: 'D6RGG6', 11: 'Q9BRQ0', 12: 'P09629', 13: 'Q9Y6G5', 14: 'Q96KG9'},
                             'intensity': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan, 5: np.nan, 6: np.nan, 7: np.nan, 8: np.nan, 9: np.nan, 10: np.nan, 11: np.nan, 12: np.nan, 13: np.nan, 14: np.nan}})
fg_bg_no_intensity = [foreground_no_intensity, background_no_intensity]

### example1: foreground is a proper subset of the background, everything has an abundance value
foreground_1 = pd.Series(name='foreground', data={0: 'Q9UHI6', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9'})
background_1 = pd.DataFrame({'background': {0: 'P13747', 1: 'Q6VB85', 2: 'Q8N8S7', 3: 'Q8WXE0', 4: 'Q9UHI6', 5: 'Q9UQ03', 6: 'Q13075', 7: 'A6NDB9', 8: 'A6NFR9', 9: 'O95359', 10: 'D6RGG6', 11: 'Q9BRQ0', 12: 'P09629', 13: 'Q9Y6G5', 14: 'Q96KG9'},
                             'intensity': {0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 2.0, 7: 3.0, 8: 4.0, 9: 5.0, 10: 6.0, 11: 7.0, 12: 8.0, 13: 9.0, 14: 10.0}})

### example2: foreground is a proper subset of the background, not everything has an abundance value
foreground_2 = pd.Series(name='foreground', data={0: 'Q9UHI6', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9'})
background_2 = pd.DataFrame({'background': {0: 'Q9UHI6', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9', 10: 'Q8WXE0', 11: 'Q6VB85', 12: 'P13747', 13: 'Q9UQ03', 14: 'Q8N8S7'},
                             'intensity': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0, 7: 8.0, 8: -1.0, 9: -1.0, 10: -1.0, 11: -1.0, 12: -1.0, 13: -1.0, 14: -1.0}})

### example3: foreground is not a proper subset of the background, not everything has an abundance value
foreground_3 = pd.Series(name='foreground', data={0: 'Q9UHI6', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9'})
background_3 = pd.DataFrame({'background': {0: 'ABC123', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9', 10: 'Q8WXE0', 11: 'Q6VB85', 12: 'P13747', 13: 'Q9UQ03', 14: 'Q8N8S7'},
                             'intensity': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0, 7: 8.0, 8: -1.0, 9: -1.0, 10: -1.0, 11: -1.0, 12: -1.0, 13: -1.0, 14: -1.0}})

### example4: foreground and background don't intersect at all
foreground_4 = pd.Series(name='foreground', data={0: 'Q9UHI6', 1: 'Q13075', 2: 'A6NDB9'})
background_4 = pd.DataFrame({'background': {0: 'ABC123', 1: 'BCD234', 2: 'CDE345'},
                             'intensity': {0: 1.0, 1: 2.0, 2: 3.0}})



fg_bg_meth_all = [pytest.mark.xfail((foreground_empty, background_empty, "abundance_correction"), strict=True),
                  pytest.mark.xfail((foreground_empty_2, background_empty_2, "abundance_correction")),
                  pytest.mark.xfail((foreground_empty_3, background_empty_3, "abundance_correction")),
                  pytest.mark.xfail((foreground_empty_4, background_empty_4, "abundance_correction")),
                  (foreground_nonsense, background_nonsense, "abundance_correction"),
                  (foreground_almost_empty, background_no_intensity, "compare_samples"),
                  (foreground_1, background_1, "abundance_correction"),
                  (foreground_2, background_2, "abundance_correction"),
                  (foreground_3, background_3, "abundance_correction")]

fg_bg_meth_all_ids = ["edge case, empty DFs with NaNs",
                    "edge case: nested empty list",
                    "edge case: empty list",
                    "edge case: None",
                    "edge case: nonsense ANs",
                    "foreground almost empty, many NaNs",
                    "example1: foreground is proper subset of background, everything has an abundance value",
                    "example2: foreground is proper subset of background, not everything has an abundance value",
                    "example3: foreground is not a proper subset of background, not everything has an abundance value"]

@pytest.fixture(params=fg_bg_meth_all, ids=fg_bg_meth_all_ids)
def fixture_fg_bg_meth_all(request):
    return request.param


fg_bg_meth_expected_cases_DFs = [(foreground_1, background_1, "abundance_correction"),
                                 (foreground_2, background_2, "abundance_correction"),
                                 (foreground_3, background_3, "abundance_correction")]

fg_bg_meth_expected_cases_ids = ["example1: foreground is proper subset of background, everything has an abundance value",
                                 "example2: foreground is proper subset of background, not everything has an abundance value",
                                 "example3: foreground is not a proper subset of background, not everything has an abundance value"]

@pytest.fixture(params=fg_bg_meth_expected_cases_DFs, ids=fg_bg_meth_expected_cases_ids)
def fixture_fg_bg_meth_expected_cases(request):
    return request.param


fg_bg_meth_edge_cases_DFs = [pytest.mark.xfail((foreground_empty, background_empty, "abundance_correction")),
                        pytest.mark.xfail((foreground_empty_2, background_empty_2, "abundance_correction")),
                        pytest.mark.xfail((foreground_empty_3, background_empty_3, "abundance_correction")),
                        pytest.mark.xfail((foreground_empty_4, background_empty_4, "abundance_correction")),
                        (foreground_nonsense, background_nonsense, "abundance_correction"),
                        (foreground_almost_empty, background_no_intensity, "compare_samples")]

fg_bg_meth_edge_cases_ids = ["edge case, empty DFs with NaNs",
                            "edge case: nested empty list",
                            "edge case: empty list",
                            "edge case: None",
                            "edge case: nonsense ANs",
                            "foreground almost empty, many NaNs"]

@pytest.fixture(params=fg_bg_meth_edge_cases_DFs, ids=fg_bg_meth_edge_cases_ids)
def fixture_fg_bg_edge_cases(request):
    return request.param


fg_bg_iter_bins_DFs = [pytest.mark.xfail((foreground_empty, background_empty, "abundance_correction"), strict=True),
                                pytest.mark.xfail((foreground_empty_2, background_empty_2, "abundance_correction")),
                                pytest.mark.xfail((foreground_empty_3, background_empty_3, "abundance_correction")),
                                pytest.mark.xfail((foreground_empty_4, background_empty_4, "abundance_correction")),
                                (foreground_nonsense, background_nonsense, "abundance_correction"),
                                (foreground_1, background_1, "abundance_correction"),
                                (foreground_2, background_2, "abundance_correction"),
                                (foreground_3, background_3, "abundance_correction")]

fg_bg_iter_bins_ids = ["edge case, empty DFs with NaNs",
                    "edge case: nested empty list",
                    "edge case: empty list",
                    "edge case: None",
                    "edge case: nonsense ANs",
                    "example1: foreground is proper subset of background, everything has an abundance value",
                    "example2: foreground is proper subset of background, not everything has an abundance value",
                    "example3: foreground is not a proper subset of background, not everything has an abundance value"]

@pytest.fixture(params=fg_bg_iter_bins_DFs, ids=fg_bg_iter_bins_ids)
def fixture_fg_bg_iter_bins(request):
    return request.param
#
# # ToDo #!!!
# # def test_compare_file_2_copypaste_2_RestAPI():
# #     assert 1 == 2

def test_ui_API_check(pqo, fixture_fg_bg_meth_all):
    foreground, background, enrichment_method = fixture_fg_bg_meth_all
    fg = format_for_REST_API(foreground[foreground.notnull()])
    bg = format_for_REST_API(background.loc[background.background.notnull(), "background"])
    in_ = format_for_REST_API(background.loc[background.intensity.notnull(), "intensity"])

    ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=NUM_BINS, enrichment_method=enrichment_method)
    assert ui.check_parse == True
    assert ui.check_cleanup == True
    assert ui.check == True

def test_check_parse_and_cleanup_FN_point(pqo):
    fn_example_data = os.path.join(variables.EXAMPLE_FOLDER, "ExampleData.txt")
    ui = userinput.Userinput(pqo=pqo, fn=fn_example_data, num_bins=NUM_BINS)
    assert ui.check_parse == True
    assert ui.check_cleanup == True
    assert ui.check == True

def test_check_parse_and_cleanup_FN_comma(pqo):
    fn_example_data = os.path.join(variables.EXAMPLE_FOLDER, "HeLa_Ubi_exampledata.txt")
    ui = userinput.Userinput(pqo=pqo, fn=fn_example_data, num_bins=NUM_BINS)
    assert ui.check_parse == True
    assert ui.check_cleanup == True
    assert ui.check == True

def test_check_parse_and_cleanup_FN_missing(pqo):
    fn_example_data = os.path.join(variables.EXAMPLE_FOLDER, "This_does_not_exist_and_therefore_can_not_be_parsed.txt")
    ui = userinput.Userinput(pqo=pqo, fn=fn_example_data, num_bins=NUM_BINS)
    assert ui.check_parse == False
    assert ui.check_cleanup == False
    assert ui.check == False

@pytest.mark.parametrize("foreground, background, enrichment_method", [(foreground_4, background_4, "abundance_correction")])
def test_check_parse_and_fail_cleanup_0(foreground, background, enrichment_method, pqo):
    fg = "\n".join(foreground[foreground.notnull()].tolist())
    bg = "\n".join(background.loc[background.background.notnull(), "background"].tolist())
    ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=bg, num_bins=NUM_BINS, enrichment_method=enrichment_method)
    assert ui.check_parse == False
    assert ui.check_cleanup == False
    assert ui.check == False

# @pytest.mark.parametrize("foreground, background, enrichment_method", [(foreground_4, background_4, "abundance_correction")])
# def test_check_parse_and_fail_cleanup_1(foreground, background, enrichment_method, pqo):
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     bg = "\n".join(background.loc[background.background.notnull(), "background"].tolist())
#     in_ = [str(ele) for ele in background.loc[background.intensity.notnull(), "intensity"].tolist()]
#     background_string = ""
#     for ele in zip(bg, in_):
#         an, in_ = ele
#         background_string += an + "\t" + in_ + "\n"
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=background_string, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#     assert ui.check_parse == True
#     assert ui.check_cleanup == False
#     assert ui.check == False
#
# @pytest.mark.parametrize("foreground, background, enrichment_method", [(foreground_empty, background_1, "compare_samples"), (foreground_1, background_empty, "compare_samples")])
# def test_check_parse_and_fail_cleanup_2(foreground, background, enrichment_method, pqo):
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     bg = "\n".join(background.loc[background.background.notnull(), "background"].tolist())
#     in_ = [str(ele) for ele in background.loc[background.intensity.notnull(), "intensity"].tolist()]
#     background_string = ""
#     for ele in zip(bg, in_):
#         an, in_ = ele
#         background_string += an + "\t" + in_ + "\n"
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=background_string, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#     assert ui.check_parse == True
#     assert ui.check_cleanup == False
#     assert ui.check == False
#
#
#
# fg_bg_0 = [(foreground_1, background_1, "compare_samples"),
#            (foreground_1, background_1, "compare_groups"),
#            (foreground_1, background_1, "compare_samples")]
#
# # example_1: foreground is a proper subset of the background, everything has an abundance value, one row of NaNs
# # example_2: same as example_1 with "," instead of "." as decimal delimiter
# ### FileName_EnrichmentMethod
# fn_em_0 = [(os.path.join(TEST_FN_DIR, "example_1.txt"), "compare_samples"),
#            (os.path.join(TEST_FN_DIR, "example_1.txt"), "compare_groups"),
#            (os.path.join(TEST_FN_DIR, "example_1.txt"), "characterize_foreground"),
#            pytest.mark.xfail((os.path.join(TEST_FN_DIR, "example_1.txt"), "unknown_method")),
#            (os.path.join(TEST_FN_DIR, "example_2.txt"), "compare_samples"),
#            (os.path.join(TEST_FN_DIR, "example_2.txt"), "compare_groups"),
#            (os.path.join(TEST_FN_DIR, "example_2.txt"), "characterize_foreground"),
#            pytest.mark.xfail((os.path.join(TEST_FN_DIR, "example_2.txt"), "unknown_method")),
#            pytest.mark.xfail((os.path.join(TEST_FN_DIR, "file_does_not_exist.txt"), "compare_samples"))]
#
# # @pytest.mark.factory
# @pytest.mark.parametrize("fn, enrichment_method", fn_em_0)
# def test_factory(fn, enrichment_method, pqo):
#     ui_1 = get_ui_copy_and_paste(pqo=pqo, fn=fn, enrichment_method=enrichment_method)
#     test_check_parse_cleanup_check(ui_1, check_parse=True, check_cleanup=True, check=True)
#     assert ui_1.foreground.shape == (10, 1)
#     if enrichment_method != "characterize_foreground":
#         assert ui_1.background.shape == (15, 1)
#
#     ui_2 = get_ui_fn(pqo=pqo, fn=fn, enrichment_method=enrichment_method)
#     test_check_parse_cleanup_check(ui_2, check_parse=True, check_cleanup=True, check=True)
#     assert ui_2.foreground.shape == (10, 1)
#     if enrichment_method != "characterize_foreground":
#         assert ui_2.background.shape == (15, 1)
#
#     ui_3 = get_ui_fn(pqo=pqo, fn=fn, enrichment_method=enrichment_method)
#     test_check_parse_cleanup_check(ui_3, check_parse=True, check_cleanup=True, check=True)
#     assert ui_3.foreground.shape == (10, 1)
#     if enrichment_method != "characterize_foreground":
#         assert ui_3.background.shape == (15, 1)
#
#     ### Check if the results are equal regardless if file, copy&paste, or REST-API
#     assert ui_1.foreground.equals(ui_2.foreground)
#     assert ui_2.foreground.equals(ui_3.foreground)
#     if enrichment_method == "characterize_foreground":
#         assert ui_1.background is None
#         assert ui_2.background is None
#         assert ui_3.background is None
#     else:
#         assert ui_1.background.equals(ui_2.background)
#         assert ui_2.background.equals(ui_3.background)
#
#
# fn_em_1 = [(os.path.join(TEST_FN_DIR, "example_1.txt"), "abundance_correction"),
#            (os.path.join(TEST_FN_DIR, "example_2.txt"), "abundance_correction"),
#            pytest.mark.xfail((os.path.join(TEST_FN_DIR, "file_does_not_exist.txt"), "compare_samples"))]
# # example_1: foreground is a proper subset of the background, everything has an abundance value, one row of NaNs
# # example_2: same as above with "," instead of "." as decimal delimiter
#
# # @pytest.mark.factory
# @pytest.mark.parametrize("fn, enrichment_method", fn_em_1)
# def test_factory_abundance(fn, enrichment_method, pqo):
#     ui_1 = get_ui_copy_and_paste(pqo=pqo, fn=fn, enrichment_method=enrichment_method, with_abundance=True)
#     test_check_parse_cleanup_check(ui_1, check_parse=True, check_cleanup=True, check=True)
#     assert ui_1.foreground.shape == (10, 2)
#     assert ui_1.background.shape == (15, 2)
#
#     ui_2 = get_ui_fn(pqo=pqo, fn=fn, enrichment_method=enrichment_method)
#     test_check_parse_cleanup_check(ui_2, check_parse=True, check_cleanup=True, check=True)
#     assert ui_2.foreground.shape == (10, 2)
#     assert ui_2.background.shape == (15, 2)
#
#     ui_3 = get_ui_rest_api(pqo=pqo, fn=fn, enrichment_method=enrichment_method, with_abundance=True)
#     test_check_parse_cleanup_check(ui_3, check_parse=True, check_cleanup=True, check=True)
#     assert ui_3.foreground.shape == (10, 2)
#     assert ui_3.background.shape == (15, 2)
#
#     ### Check if the results are equal regardless if file, copy&paste, or REST-API
#     assert ui_1.foreground.equals(ui_2.foreground)
#     assert ui_2.foreground.equals(ui_3.foreground)
#     if enrichment_method == "characterize_foreground":
#         assert ui_1.background is None
#         assert ui_2.background is None
#         assert ui_3.background is None
#     else:
#         assert ui_1.background.equals(ui_2.background)
#         assert ui_2.background.equals(ui_3.background)
#
# @pytest.mark.parametrize("fn, enrichment_method", [(os.path.join(TEST_FN_DIR, "example_5.txt"), "abundance_correction")])
# def test_protein_groups(fn, enrichment_method, pqo):
#     pass
#
# @pytest.mark.parametrize("foreground, background, enrichment_method", fg_bg_0)
# def test_check_parse_with_copy_and_paste_0(foreground, background, enrichment_method, pqo):
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     bg = "\n".join(background.loc[background.background.notnull(), "background"].tolist())
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=bg, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#     assert ui.check_parse == True
#     assert ui.foreground.shape == (10, 1)
#
#
# fg_bg_1 = [(foreground_1, background_1, "abundance_correction")]
#
# @pytest.mark.parametrize("foreground, background, enrichment_method", fg_bg_1)
# def test_check_parse_with_copy_and_paste_1(foreground, background, enrichment_method, pqo):
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     bg = background.loc[background.background.notnull(), "background"].tolist()
#     in_ = [str(ele) for ele in background.loc[background.intensity.notnull(), "intensity"].tolist()]
#     background_string = ""
#     for ele in zip_longest(bg, in_, fillvalue=np.nan):
#         an, in_ = ele
#         background_string += an + "\t" + str(in_) + "\n"
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=background_string, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#     assert ui.check_parse == True
#     assert ui.foreground.shape == (10, 2)
#
#
# @pytest.mark.parametrize("foreground, background, enrichment_method", [(foreground_1, background_1, "compare_samples")])
# def test_check_parse_and_cleanup_copy_and_paste_2(foreground, background, enrichment_method, pqo):
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     bg = "\n".join(background.loc[background.background.notnull(), "background"].tolist())
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=bg, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#     assert ui.check_parse == True
#
#
# edge_cases_0 = [(foreground_empty, background_empty, "abundance_correction")] #,
#                 # (foreground_empty_1, background_empty_1, "abundance_correction"),
#                 # (foreground_empty_2, background_empty_2, "abundance_correction")]
#
# @pytest.mark.parametrize("foreground, background, enrichment_method", edge_cases_0)
# def test_check_parse_and_cleanup_copy_and_paste_0(foreground, background, enrichment_method, pqo):
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     bg = "\n".join(background.loc[background.background.notnull(), "background"].tolist())
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=bg, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#     assert ui.check_parse == False
#     assert ui.check_cleanup == False
#     assert ui.check == False
#
# fg_bg_meth_cp_abu = [pytest.mark.xfail((foreground_empty, background_empty, "abundance_correction"), strict=True),
#       pytest.mark.xfail((foreground_empty_2, background_empty_2, "abundance_correction")),
#       pytest.mark.xfail((foreground_empty_3, background_empty_3, "abundance_correction")),
#       pytest.mark.xfail((foreground_empty_4, background_empty_4, "abundance_correction")),
#       (foreground_nonsense, background_nonsense, "abundance_correction"),
#       (foreground_1, background_1, "abundance_correction"),
#       (foreground_2, background_2, "abundance_correction"),
#       (foreground_3, background_3, "abundance_correction")]
#
# @pytest.mark.parametrize("foreground, background, enrichment_method", fg_bg_meth_cp_abu)
# def test_check_parse_and_cleanup_copy_and_paste_1(foreground, background, enrichment_method, pqo):
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     bg = background.loc[background.background.notnull(), "background"].tolist()
#     in_ = [str(ele) for ele in background.loc[background.intensity.notnull(), "intensity"].tolist()]
#     background_string = ""
#     for ele in zip_longest(bg, in_, fillvalue=np.nan):
#         an, in_ = ele
#         background_string += an + "\t" + str(in_) + "\n"
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=background_string, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#     assert ui.check_parse == True
#     assert ui.check_cleanup == True
#     assert ui.check == True
#
# # @pytest.mark.parametrize("foreground, background, enrichment_method", [(foreground_almost_empty, background_no_intensity, "compare_samples")])
# # def test_check_parse_and_cleanup_copy_and_paste_2(foreground, background, enrichment_method, pqo):
# #     fg = "\n".join(foreground[foreground.notnull()].tolist())
# #     bg = background.loc[background.background.notnull(), "background"].tolist()
# #     in_ = [str(ele) for ele in background.loc[background.intensity.notnull(), "intensity"].tolist()]
# #     background_string = ""
# #     for ele in zip_longest(bg, in_, fillvalue=np.nan):
# #         an, in_ = ele
# #         background_string += an + "\t" + str(in_) + "\n"
# #     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=background_string, num_bins=NUM_BINS, enrichment_method=enrichment_method)
# #     assert ui.check_parse == True
# #     assert ui.check_cleanup == False
# #     assert ui.check == False
#
#
# def test_iter_bins_API_input(pqo, fixture_fg_bg_iter_bins):
#     foreground, background, enrichment_method = fixture_fg_bg_iter_bins
#     fg = format_for_REST_API(foreground[foreground.notnull()])
#     bg = format_for_REST_API(background.loc[background.background.notnull(), "background"])
#     in_ = format_for_REST_API(background.loc[background.intensity.notnull(), "intensity"])
#
#     ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#     counter = 0
#     for ans, weight_fac in ui.iter_bins():
#         # every weighting factor is a float
#         assert type(weight_fac) == float
#         counter += 1
#     number_of_bins_used = pd.cut(ui.foreground["intensity"], bins=100, retbins=False).drop_duplicates().shape[0]
#     assert counter == number_of_bins_used
#
# def test_iter_bins_API_input_missing_bin(pqo, fixture_fg_bg_iter_bins):
#     """
#     this test only works if ANs fall within separate bins,
#     e.g. for negative example:
#        background  intensity foreground
#     0           A        1.0          A
#     1           B        1.0          B
#     2           C        1.0          C
#     """
#     foreground, background, enrichment_method = fixture_fg_bg_iter_bins
#     fg = format_for_REST_API(foreground[foreground.notnull()])
#     bg = format_for_REST_API(background.loc[background.background.notnull(), "background"])
#     in_ = format_for_REST_API(background.loc[background.intensity.notnull(), "intensity"])
#
#     ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#     counter = 0
#     for ans, weight_fac in ui.iter_bins():
#         # every weighting factor is a float
#         assert type(weight_fac) == float
#         counter += 1
#     # since integers instead of floats are being used for test data, the number of unique bins can be determined by sets
#     num_iterations_expected = len({int(ele) for ele in ui.foreground["intensity"].tolist()})
#     assert counter == num_iterations_expected
#
#
#
# ### test cleanup for analysis for all 4 different enrichment methods
# ### via class REST_API_input
# def test_cleanupforanalysis_abundance_correction_REST_API(pqo, fixture_fg_bg_meth_expected_cases):
#     """
#     using fixture_fg_bg_meth_all
#     python/test_userinput.py::test_cleanupforanalysis_abundance_correction_REST_API[edge case, empty DFs with NaNs] XPASS
#     XPASS: should fail but passes.
#     --> should not be tested at all, but doesn't matter
#     """
#     foreground, background, _ = fixture_fg_bg_meth_expected_cases
#     enrichment_method = "abundance_correction"
#     foreground_n = None
#     background_n = None
#     fg = format_for_REST_API(foreground)
#     bg = format_for_REST_API(background["background"])
#     in_ = format_for_REST_API(background["intensity"])
#     ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=NUM_BINS,
#         enrichment_method=enrichment_method, foreground_n=foreground_n, background_n=background_n)
#
#     # no NaNs where ANs are expected
#     foreground = ui.foreground[ui.col_foreground]
#     assert sum(foreground.isnull()) == 0
#     assert sum(foreground.notnull()) > 0
#     background = ui.background[ui.col_background]
#     assert sum(background.isnull()) == 0
#     assert sum(background.notnull()) > 0
#
#     # every AN has an abundance val
#     foreground_intensity = ui.foreground[ui.col_intensity]
#     assert sum(foreground_intensity.isnull()) == 0
#     assert sum(foreground_intensity.notnull()) > 0
#     background_intensity = ui.background[ui.col_intensity]
#     assert sum(background_intensity.isnull()) == 0
#     assert sum(background_intensity.notnull()) > 0
#
#     # foreground and background are strings and abundance values are floats
#     assert isinstance(foreground.iloc[0], str)
#     assert isinstance(background.iloc[0], str)
#     assert isinstance(foreground_intensity.iloc[0], float)
#     assert isinstance(background_intensity.iloc[0], float)
#
#     # no duplicates
#     assert foreground.duplicated().any() == False
#     assert background.duplicated().any() == False
#
#     # sorted abundance values
#     assert non_decreasing(foreground_intensity.tolist()) == True
#     assert non_decreasing(background_intensity.tolist()) == True
#
# def test_cleanupforanalysis_characterize_foreground_REST_API(pqo, fixture_fg_bg_meth_expected_cases):
#     """
#     python/test_userinput.py::test_cleanupforanalysis_characterize_foreground_REST_API[edge case, empty DFs with NaNs] XPASS
#     """
#     foreground, background, _ = fixture_fg_bg_meth_expected_cases
#     enrichment_method = "characterize_foreground"
#     foreground_n = None
#     background_n = None
#     fg = format_for_REST_API(foreground)
#     bg = None
#     in_ = None
#     ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=NUM_BINS,
#         enrichment_method=enrichment_method, foreground_n=foreground_n, background_n=background_n)
#
#     # no NaNs where ANs are expected
#     foreground = ui.foreground[ui.col_foreground]
#     assert sum(foreground.isnull()) == 0
#     assert sum(foreground.notnull()) > 0
#
#     # foreground
#     assert isinstance(foreground.iloc[0], str)
#
#     # no duplicates
#     assert foreground.duplicated().any() == False
#
# def test_cleanupforanalysis_compare_samples_REST_API(pqo, fixture_fg_bg_meth_expected_cases):
#     """
#     python/test_userinput.py::test_cleanupforanalysis_compare_samples_REST_API[edge case, empty DFs with NaNs] XPASS
#     """
#     foreground, background, _ = fixture_fg_bg_meth_expected_cases
#     enrichment_method = "compare_samples"
#     foreground_n = None
#     background_n = None
#     fg = format_for_REST_API(foreground)
#     bg = format_for_REST_API(background["background"])
#     in_ = None
#     ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=NUM_BINS,
#         enrichment_method=enrichment_method, foreground_n=foreground_n, background_n=background_n)
#
#     # no NaNs where ANs are expected
#     foreground = ui.foreground[ui.col_foreground]
#     assert sum(foreground.isnull()) == 0
#     assert sum(foreground.notnull()) > 0
#     background = ui.background[ui.col_background]
#     assert sum(background.isnull()) == 0
#     assert sum(background.notnull()) > 0
#
#     # foreground and background are strings
#     assert isinstance(foreground.iloc[0], str)
#     assert isinstance(background.iloc[0], str)
#
#     # no duplicates
#     assert foreground.duplicated().any() == False
#     assert background.duplicated().any() == False
#
# def test_cleanupforanalysis_compare_groups_REST_API(pqo, fixture_fg_bg_meth_all):
#     foreground, background, _ = fixture_fg_bg_meth_all
#     enrichment_method = "compare_groups"
#     foreground_n = None
#     background_n = None
#     fg = format_for_REST_API(foreground)
#     bg = "%0d".join(background.loc[:, "background"].tolist())
#     in_ = None
#     ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=NUM_BINS,
#         enrichment_method=enrichment_method, foreground_n=foreground_n, background_n=background_n)
#
#     # no NaNs where ANs are expected
#     foreground = ui.foreground[ui.col_foreground]
#     assert sum(foreground.isnull()) == 0
#     assert sum(foreground.notnull()) > 0
#     background = ui.background[ui.col_background]
#     assert sum(background.isnull()) == 0
#     assert sum(background.notnull()) > 0
#
#     # foreground and background are strings
#     assert isinstance(foreground.iloc[0], str)
#     assert isinstance(background.iloc[0], str)
#
#     # if there were duplicates in the original input they should still be preserved in the cleaned up DF
#     # not equal because of splice variants
#     # remove NaNs from df_orig
#     foreground_df_orig = ui.df_orig[ui.col_foreground]
#     background_df_orig = ui.df_orig[ui.col_background]
#     assert foreground.duplicated().sum() >= foreground_df_orig[foreground_df_orig.notnull()].duplicated().sum()
#     assert background.duplicated().sum() >= background_df_orig[background_df_orig.notnull()].duplicated().sum()
#
# ### via class Userinput
# def test_cleanupforanalysis_abundance_correction_Userinput(pqo, fixture_fg_bg_meth_all):
#     foreground, background, enrichment_method = fixture_fg_bg_meth_all
#     if enrichment_method != "abundance_correction":
#         # assert 1 == 1
#         return None
#
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     bg = background.loc[background.background.notnull(), "background"].tolist()
#     in_ = [str(ele) for ele in background.loc[background.intensity.notnull(), "intensity"].tolist()]
#     background_string = ""
#     for ele in zip(bg, in_):
#         an, in_ = ele
#         background_string += an + "\t" + in_ + "\n"
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=background_string, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#
#     # no NaNs where ANs are expected
#     foreground = ui.foreground[ui.col_foreground]
#     assert sum(foreground.isnull()) == 0
#     assert sum(foreground.notnull()) > 0
#     background = ui.background[ui.col_background]
#     assert sum(background.isnull()) == 0
#     assert sum(background.notnull()) > 0
#
#     # every AN has an abundance val
#     foreground_intensity = ui.foreground[ui.col_intensity]
#     assert sum(foreground_intensity.isnull()) == 0
#     assert sum(foreground_intensity.notnull()) > 0
#     background_intensity = ui.background[ui.col_intensity]
#     assert sum(background_intensity.isnull()) == 0
#     assert sum(background_intensity.notnull()) > 0
#
#     # foreground and background are strings and abundance values are floats
#     assert isinstance(foreground.iloc[0], str)
#     assert isinstance(background.iloc[0], str)
#     assert isinstance(foreground_intensity.iloc[0], float)
#     assert isinstance(background_intensity.iloc[0], float)
#
#     # no duplicates
#     assert foreground.duplicated().any() == False
#     assert background.duplicated().any() == False
#
#     # sorted abundance values
#     assert non_decreasing(foreground_intensity.tolist()) == True
#     assert non_decreasing(background_intensity.tolist()) == True
#
# def test_cleanupforanalysis_characterize_foreground_Userinput(pqo, fixture_fg_bg_meth_all):
#     foreground, background, _ = fixture_fg_bg_meth_all
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     enrichment_method = "characterize_foreground"
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=None, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#
#     # no NaNs where ANs are expected
#     foreground = ui.foreground[ui.col_foreground]
#     assert sum(foreground.isnull()) == 0
#     assert sum(foreground.notnull()) > 0
#
#     # foreground
#     assert isinstance(foreground.iloc[0], str)
#
#     # no duplicates
#     assert foreground.duplicated().any() == False
#
# def test_cleanupforanalysis_compare_samples_Userinput(pqo, fixture_fg_bg_meth_all):
#     enrichment_method = "compare_samples"
#     foreground, background, _ = fixture_fg_bg_meth_all
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     bg = "\n".join(background.loc[background.background.notnull(), "background"].tolist())
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=bg, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#
#     # no NaNs where ANs are expected
#     foreground = ui.foreground[ui.col_foreground]
#     assert sum(foreground.isnull()) == 0
#     assert sum(foreground.notnull()) > 0
#     background = ui.background[ui.col_background]
#     assert sum(background.isnull()) == 0
#     assert sum(background.notnull()) > 0
#
#     # foreground and background are strings
#     assert isinstance(foreground.iloc[0], str)
#     assert isinstance(background.iloc[0], str)
#
#     # no duplicates
#     assert foreground.duplicated().any() == False
#     assert background.duplicated().any() == False
#
# def test_cleanupforanalysis_compare_groups_Userinput(pqo, fixture_fg_bg_meth_all):
#     enrichment_method = "compare_groups"
#     foreground, background, _ = fixture_fg_bg_meth_all
#     fg = "\n".join(foreground[foreground.notnull()].tolist())
#     bg = "\n".join(background.loc[background.background.notnull(), "background"].tolist())
#     ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=bg, num_bins=NUM_BINS, enrichment_method=enrichment_method)
#
#     # no NaNs where ANs are expected
#     foreground = ui.foreground[ui.col_foreground]
#     assert sum(foreground.isnull()) == 0
#     assert sum(foreground.notnull()) > 0
#     background = ui.background[ui.col_background]
#     assert sum(background.isnull()) == 0
#     assert sum(background.notnull()) > 0
#
#     # foreground and background are strings
#     assert isinstance(foreground.iloc[0], str)
#     assert isinstance(background.iloc[0], str)
#
#     # if there were duplicates in the original input they should still be preserved in the cleaned up DF
#     # not equal because of splice variants
#     # remove NaNs from df_orig
#     foreground_df_orig = ui.df_orig[ui.col_foreground]
#     background_df_orig = ui.df_orig[ui.col_background]
#     assert foreground.duplicated().sum() >= foreground_df_orig[foreground_df_orig.notnull()].duplicated().sum()
#     assert background.duplicated().sum() >= background_df_orig[background_df_orig.notnull()].duplicated().sum()
#
### helper functions
def non_decreasing(L):
    """
    https://stackoverflow.com/questions/4983258/python-how-to-check-list-monotonicity
    """
    return all(x<=y for x, y in zip(L, L[1:]))

def format_for_REST_API(pd_series):
    return "%0d".join([str(ele) for ele in pd_series.tolist()])

def get_ui_copy_and_paste(pqo, fn, enrichment_method, with_abundance=False, num_bins=NUM_BINS):
    df = pd.read_csv(fn, sep='\t')
    fg = "\n".join(df.loc[df["foreground"].notnull(), "foreground"].tolist())
    if not with_abundance:
        bg = "\n".join(df.loc[df["background"].notnull(), "background"].tolist())
        return userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=bg, num_bins=num_bins, enrichment_method=enrichment_method)
    else:
        bg = df.loc[df["background"].notnull(), "background"].tolist()
        in_ = [str(ele) for ele in df.loc[df["intensity"].notnull(), "intensity"].tolist()]
        background_string = ""
        for ele in zip(bg, in_):
            an, in_ = ele
            background_string += an + "\t" + in_ + "\n"
        return userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=background_string, num_bins=num_bins, enrichment_method=enrichment_method)

def get_ui_rest_api(pqo, fn, enrichment_method, with_abundance=False, num_bins=NUM_BINS):
    df = pd.read_csv(fn, sep='\t')
    fg = format_for_REST_API(df.loc[df["foreground"].notnull(), "foreground"])
    bg = format_for_REST_API(df.loc[df["background"].notnull(), "background"])
    in_ = format_for_REST_API(df.loc[df["intensity"].notnull(), "intensity"])
    if with_abundance:
        return userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, enrichment_method=enrichment_method)
    else:
        return userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, enrichment_method=enrichment_method, num_bins=num_bins)

def get_ui_fn(pqo, fn, enrichment_method, num_bins=NUM_BINS):
    return userinput.Userinput(pqo=pqo, fn=fn, enrichment_method=enrichment_method, num_bins=num_bins)

@pytest.mark.skip(reason="this test is being used internally, but will fail if run on its own since 'ui' is not a fixture but a parameter")
def test_check_parse_cleanup_check(ui, check_parse=True, check_cleanup=True, check=True):
    assert ui.check_parse == check_parse
    assert ui.check_cleanup == check_cleanup
    assert ui.check == check