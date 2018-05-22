import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import pandas as pd
import numpy as np
import pytest

import userinput, variables


### empty DF, edge case
foreground_empty = pd.DataFrame({"foreground": {0: np.nan, 1: np.nan, 2: np.nan},
                                 "intensity": {0: np.nan, 1: np.nan, 2: np.nan}})
background_empty = pd.DataFrame({"background": {0: np.nan, 1: np.nan, 2: np.nan},
                                 "intensity": {0: np.nan, 1: np.nan, 2: np.nan}})
foreground_empty_2 = [[], []]
background_empty_2 = [[], []]
foreground_empty_3 = []
background_empty_3 = []
foreground_empty_4 = None
background_empty_4 = None
### example0: nonesense AccessionNumbers, foreground is proper subset of background, everything has an abundance value
foreground_0 = pd.DataFrame({'foreground': {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'},
                             'intensity': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0, 7: 8.0, 8: 9.0, 9: 10.0}})
background_0 = pd.DataFrame({'background': {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O'},
                             'intensity': {0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 2.0, 7: 3.0, 8: 4.0, 9: 5.0, 10: 6.0, 11: 7.0, 12: 8.0, 13: 9.0, 14: 10.0}})

### example1: foreground is proper subset of background, everything has an abundance value
foreground_1 = pd.DataFrame({'foreground': {0: 'Q9UHI6', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9'},
                             'intensity': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0, 7: 8.0, 8: 9.0, 9: 10.0}})
background_1 = pd.DataFrame({'background': {0: 'P13747', 1: 'Q6VB85', 2: 'Q8N8S7', 3: 'Q8WXE0', 4: 'Q9UHI6', 5: 'Q9UQ03', 6: 'Q13075', 7: 'A6NDB9', 8: 'A6NFR9', 9: 'O95359', 10: 'D6RGG6', 11: 'Q9BRQ0', 12: 'P09629', 13: 'Q9Y6G5', 14: 'Q96KG9'},
                             'intensity': {0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 2.0, 7: 3.0, 8: 4.0, 9: 5.0, 10: 6.0, 11: 7.0, 12: 8.0, 13: 9.0, 14: 10.0}})
### example2: foreground is proper subset of background, not everything has an abundance value
foreground_2 = pd.DataFrame({'foreground': {0: 'Q9UHI6', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9'},
                             'intensity': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0, 7: 8.0, 8: -1.0, 9: -1.0}})
background_2 = pd.DataFrame({'background': {0: 'Q9UHI6', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9', 10: 'Q8WXE0', 11: 'Q6VB85', 12: 'P13747', 13: 'Q9UQ03', 14: 'Q8N8S7'},
                             'intensity': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0, 7: 8.0, 8: -1.0, 9: -1.0, 10: -1.0, 11: -1.0, 12: -1.0, 13: -1.0, 14: -1.0}})
### example3: foreground is not a proper subset of background, not everything has an abundance value
foreground_3 = pd.DataFrame({'foreground': {0: 'Q9UHI6', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9'},
                             'intensity': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0, 7: 8.0, 8: -1.0, 9: -1.0}})
background_3 = pd.DataFrame({'background': {0: 'ABC123', 1: 'Q13075', 2: 'A6NDB9', 3: 'A6NFR9', 4: 'O95359', 5: 'D6RGG6', 6: 'Q9BRQ0', 7: 'P09629', 8: 'Q9Y6G5', 9: 'Q96KG9', 10: 'Q8WXE0', 11: 'Q6VB85', 12: 'P13747', 13: 'Q9UQ03', 14: 'Q8N8S7'},
                             'intensity': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0, 7: 8.0, 8: -1.0, 9: -1.0, 10: -1.0, 11: -1.0, 12: -1.0, 13: -1.0, 14: -1.0}})

foreground_background_2_test = [pytest.mark.xfail((foreground_empty, background_empty)),
                                pytest.mark.xfail((foreground_empty_2, background_empty_2)),
                                pytest.mark.xfail((foreground_empty_3, background_empty_3)),
                                pytest.mark.xfail((foreground_empty_4, background_empty_4)),
                                (foreground_0, background_0),
                                (foreground_1, background_1),
                                (foreground_2, background_2),
                                (foreground_3, background_3)]

example_ids = ["edge case, empty DFs with NaNs",
               "edge case: nested empty list",
               "edge case: empty list",
               "edge case: None",
               "edge case: nonsense ANs",
               "example1: foreground is proper subset of background, everything has an abundance value",
               "example2: foreground is proper subset of background, not everything has an abundance value",
               "example3: foreground is not a proper subset of background, not everything has an abundance value"]

@pytest.fixture(params=foreground_background_2_test, ids=example_ids)
def params_fixture_foreground_background_2_test(request):
    return request.param


def test_ui_API_check(pqo, params_fixture_foreground_background_2_test):
    foreground, background = params_fixture_foreground_background_2_test
    num_bins = 100
    fg = "%0d".join(foreground.loc[foreground.foreground.notnull(), "foreground"].tolist())
    bg = "%0d".join(background.loc[background.background.notnull(), "background"].tolist())
    in_ = "%0d".join([str(ele) for ele in background.loc[background.intensity.notnull(), "intensity"].tolist()])
    ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=num_bins)
    assert ui.check == True

def test_Userinput_check_parse_and_cleanup_FN(pqo):
    fn_example_data = os.path.join(variables.EXAMPLE_FOLDER, "ExampleData.txt")
    ui = userinput.Userinput(pqo=pqo, fn=fn_example_data, num_bins=100)
    assert ui.check_parse == True
    assert ui.check_cleanup == True

def test_Userinput_check_parse_and_cleanup_copy_and_paste(pqo, params_fixture_foreground_background_2_test):
    foreground, background = params_fixture_foreground_background_2_test
    num_bins = 100
    fg = "\n".join(foreground.loc[foreground.foreground.notnull(), "foreground"].tolist())
    bg = background.loc[background.background.notnull(), "background"].tolist()
    in_ = [str(ele) for ele in background.loc[background.intensity.notnull(), "intensity"].tolist()]
    background_string = ""
    for ele in zip(bg, in_):
        an, in_ = ele
        background_string += an + "\t" + in_ + "\n"
    ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=background_string, num_bins=num_bins)
    assert ui.check_parse == True
    assert ui.check_cleanup == True

def test_iter_bins_API_input(pqo, params_fixture_foreground_background_2_test):
    foreground, background = params_fixture_foreground_background_2_test
    num_bins = 100
    # DEFAULT_MISSING_BIN = -1

    fg = "%0d".join(foreground.loc[foreground.foreground.notnull(), "foreground"].tolist())
    bg = "%0d".join(background.loc[background.background.notnull(), "background"].tolist())
    in_ = "%0d".join([str(ele) for ele in background.loc[background.intensity.notnull(), "intensity"].tolist()])
    ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=num_bins)

    counter = 0
    for ans, weight_fac in ui.iter_bins():
        # every weighting factor is a float
        assert type(weight_fac) == float
        counter += 1

    # every AN in foreground needs to have an abundance value
    #  --> but those with missing abundance vals are all in the same bin (and therefore only count once all together)
    # foreground proteins that don't exist in background (since foreground proper subset of background) mess up the count and need to be added
    #  --> all of them fall within the missing vals bin of the foreground, but the ANs don't appear in the background
    # missing_in_background = ui.get_foreground_an_set() - ui.get_background_an_set()
    # if len(missing_in_background) > 0:
    #     counter += 1

    # proteins with abundance info
    # cond = ui.foreground["intensity"] > DEFAULT_MISSING_BIN
    # number_of_proteins = foreground[cond].shape[0]

    # number_of_bins_used = len(pd.cut(foreground["intensity"], bins=num_bins, retbins=True)[1])
    number_of_bins_used = pd.cut(ui.foreground["intensity"], bins=100, retbins=False).drop_duplicates().shape[0]

    # if any proteins fall within missing bin count as one since they get grouped together
    # if sum(-cond) > 0:
    #     number_of_bins_used += 1
    assert counter == number_of_bins_used


### test cleanup for analysis for all 4 different enrichment methods
### via class REST_API_input
def test_cleanupforanalysis_abundance_correction_REST_API(pqo, params_fixture_foreground_background_2_test):
    foreground_input, background_input = params_fixture_foreground_background_2_test
    num_bins = 100
    enrichment_method = "abundance_correction"
    foreground_n = None
    background_n = None
    fg = "%0d".join(foreground_input.loc[:, "foreground"].tolist())
    bg = "%0d".join(background_input.loc[:, "background"].tolist())
    in_ = "%0d".join([str(ele) for ele in background_input.loc[:, "intensity"].tolist()])
    ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=num_bins,
        enrichment_method=enrichment_method, foreground_n=foreground_n, background_n=background_n)

    # no NaNs where ANs are expected
    foreground = ui.foreground[ui.col_foreground]
    assert sum(foreground.isnull()) == 0
    assert sum(foreground.notnull()) > 0
    background = ui.background[ui.col_background]
    assert sum(background.isnull()) == 0
    assert sum(background.notnull()) > 0

    # every AN has an abundance val
    foreground_intensity = ui.foreground[ui.col_intensity]
    assert sum(foreground_intensity.isnull()) == 0
    assert sum(foreground_intensity.notnull()) > 0
    background_intensity = ui.background[ui.col_intensity]
    assert sum(background_intensity.isnull()) == 0
    assert sum(background_intensity.notnull()) > 0

    # foreground and background are strings and abundance values are floats
    assert isinstance(foreground.iloc[0], str)
    assert isinstance(background.iloc[0], str)
    assert isinstance(foreground_intensity.iloc[0], float)
    assert isinstance(background_intensity.iloc[0], float)

    # no duplicates
    assert foreground.duplicated().any() == False
    assert background.duplicated().any() == False

    # sorted abundance values
    assert non_decreasing(foreground_intensity.tolist()) == True
    assert non_decreasing(background_intensity.tolist()) == True

def test_cleanupforanalysis_characterize_foreground_REST_API(pqo, params_fixture_foreground_background_2_test):
    foreground_input, background_input = params_fixture_foreground_background_2_test
    num_bins = 100
    enrichment_method = "characterize_foreground"
    foreground_n = None
    background_n = None
    fg = "%0d".join(foreground_input.loc[:, "foreground"].tolist())
    bg = None
    in_ = None
    ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=num_bins,
        enrichment_method=enrichment_method, foreground_n=foreground_n, background_n=background_n)

    # no NaNs where ANs are expected
    foreground = ui.foreground[ui.col_foreground]
    assert sum(foreground.isnull()) == 0
    assert sum(foreground.notnull()) > 0

    # foreground
    assert isinstance(foreground.iloc[0], str)

    # no duplicates
    assert foreground.duplicated().any() == False

def test_cleanupforanalysis_compare_samples_REST_API(pqo, params_fixture_foreground_background_2_test):
    foreground_input, background_input = params_fixture_foreground_background_2_test
    num_bins = 100
    enrichment_method = "compare_samples"
    foreground_n = None
    background_n = None
    fg = "%0d".join(foreground_input.loc[:, "foreground"].tolist())
    bg = "%0d".join(background_input.loc[:, "background"].tolist())
    in_ = None
    ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=num_bins,
        enrichment_method=enrichment_method, foreground_n=foreground_n, background_n=background_n)

    # no NaNs where ANs are expected
    foreground = ui.foreground[ui.col_foreground]
    assert sum(foreground.isnull()) == 0
    assert sum(foreground.notnull()) > 0
    background = ui.background[ui.col_background]
    assert sum(background.isnull()) == 0
    assert sum(background.notnull()) > 0

    # foreground and background are strings
    assert isinstance(foreground.iloc[0], str)
    assert isinstance(background.iloc[0], str)

    # no duplicates
    assert foreground.duplicated().any() == False
    assert background.duplicated().any() == False

def test_cleanupforanalysis_compare_groups_REST_API(pqo, params_fixture_foreground_background_2_test):
    foreground_input, background_input = params_fixture_foreground_background_2_test
    num_bins = 100
    enrichment_method = "compare_groups"
    foreground_n = None
    background_n = None
    fg = "%0d".join(foreground_input.loc[:, "foreground"].tolist())
    bg = "%0d".join(background_input.loc[:, "background"].tolist())
    in_ = None
    ui = userinput.REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=num_bins,
        enrichment_method=enrichment_method, foreground_n=foreground_n, background_n=background_n)

    # no NaNs where ANs are expected
    foreground = ui.foreground[ui.col_foreground]
    assert sum(foreground.isnull()) == 0
    assert sum(foreground.notnull()) > 0
    background = ui.background[ui.col_background]
    assert sum(background.isnull()) == 0
    assert sum(background.notnull()) > 0

    # foreground and background are strings
    assert isinstance(foreground.iloc[0], str)
    assert isinstance(background.iloc[0], str)

    # if there were duplicates in the original input they should still be preserved in the cleaned up DF
    # not equal because of splice variants
    # remove NaNs from df_orig
    foreground_df_orig = ui.df_orig[ui.col_foreground]
    background_df_orig = ui.df_orig[ui.col_background]
    assert foreground.duplicated().sum() >= foreground_df_orig[foreground_df_orig.notnull()].duplicated().sum()
    assert background.duplicated().sum() >= background_df_orig[background_df_orig.notnull()].duplicated().sum()

### via class Userinput
def test_cleanupforanalysis_abundance_correction_Userinput(pqo, params_fixture_foreground_background_2_test):
    foreground, background = params_fixture_foreground_background_2_test
    num_bins = 100
    fg = "\n".join(foreground.loc[foreground.foreground.notnull(), "foreground"].tolist())
    bg = background.loc[background.background.notnull(), "background"].tolist()
    in_ = [str(ele) for ele in background.loc[background.intensity.notnull(), "intensity"].tolist()]
    background_string = ""
    for ele in zip(bg, in_):
        an, in_ = ele
        background_string += an + "\t" + in_ + "\n"
    ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=background_string, num_bins=num_bins)

    # no NaNs where ANs are expected
    foreground = ui.foreground[ui.col_foreground]
    assert sum(foreground.isnull()) == 0
    assert sum(foreground.notnull()) > 0
    background = ui.background[ui.col_background]
    assert sum(background.isnull()) == 0
    assert sum(background.notnull()) > 0

    # every AN has an abundance val
    foreground_intensity = ui.foreground[ui.col_intensity]
    assert sum(foreground_intensity.isnull()) == 0
    assert sum(foreground_intensity.notnull()) > 0
    background_intensity = ui.background[ui.col_intensity]
    assert sum(background_intensity.isnull()) == 0
    assert sum(background_intensity.notnull()) > 0

    # foreground and background are strings and abundance values are floats
    assert isinstance(foreground.iloc[0], str)
    assert isinstance(background.iloc[0], str)
    assert isinstance(foreground_intensity.iloc[0], float)
    assert isinstance(background_intensity.iloc[0], float)

    # no duplicates
    assert foreground.duplicated().any() == False
    assert background.duplicated().any() == False

    # sorted abundance values
    assert non_decreasing(foreground_intensity.tolist()) == True
    assert non_decreasing(background_intensity.tolist()) == True

def test_cleanupforanalysis_characterize_foreground_Userinput(pqo, params_fixture_foreground_background_2_test):
    foreground, background = params_fixture_foreground_background_2_test
    num_bins = 100
    fg = "\n".join(foreground.loc[foreground.foreground.notnull(), "foreground"].tolist())
    enrichment_method = "characterize_foreground"
    ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=None, num_bins=num_bins, enrichment_method=enrichment_method)

    # no NaNs where ANs are expected
    foreground = ui.foreground[ui.col_foreground]
    assert sum(foreground.isnull()) == 0
    assert sum(foreground.notnull()) > 0

    # foreground
    assert isinstance(foreground.iloc[0], str)

    # no duplicates
    assert foreground.duplicated().any() == False

def test_cleanupforanalysis_compare_samples_Userinput(pqo, params_fixture_foreground_background_2_test):
    num_bins = 100
    enrichment_method = "compare_samples"
    foreground, background = params_fixture_foreground_background_2_test
    fg = "\n".join(foreground.loc[foreground.foreground.notnull(), "foreground"].tolist())
    bg = "\n".join(background.loc[background.background.notnull(), "background"].tolist())
    ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=bg, num_bins=num_bins, enrichment_method=enrichment_method)

    # no NaNs where ANs are expected
    foreground = ui.foreground[ui.col_foreground]
    assert sum(foreground.isnull()) == 0
    assert sum(foreground.notnull()) > 0
    background = ui.background[ui.col_background]
    assert sum(background.isnull()) == 0
    assert sum(background.notnull()) > 0

    # foreground and background are strings
    assert isinstance(foreground.iloc[0], str)
    assert isinstance(background.iloc[0], str)

    # no duplicates
    assert foreground.duplicated().any() == False
    assert background.duplicated().any() == False

def test_cleanupforanalysis_compare_groups_Userinput(pqo, params_fixture_foreground_background_2_test):
    num_bins = 100
    enrichment_method = "compare_groups"
    foreground, background = params_fixture_foreground_background_2_test
    fg = "\n".join(foreground.loc[foreground.foreground.notnull(), "foreground"].tolist())
    bg = "\n".join(background.loc[background.background.notnull(), "background"].tolist())
    ui = userinput.Userinput(pqo=pqo, foreground_string=fg, background_string=bg, num_bins=num_bins, enrichment_method=enrichment_method)

    # no NaNs where ANs are expected
    foreground = ui.foreground[ui.col_foreground]
    assert sum(foreground.isnull()) == 0
    assert sum(foreground.notnull()) > 0
    background = ui.background[ui.col_background]
    assert sum(background.isnull()) == 0
    assert sum(background.notnull()) > 0

    # foreground and background are strings
    assert isinstance(foreground.iloc[0], str)
    assert isinstance(background.iloc[0], str)

    # if there were duplicates in the original input they should still be preserved in the cleaned up DF
    # not equal because of splice variants
    # remove NaNs from df_orig
    foreground_df_orig = ui.df_orig[ui.col_foreground]
    background_df_orig = ui.df_orig[ui.col_background]
    assert foreground.duplicated().sum() >= foreground_df_orig[foreground_df_orig.notnull()].duplicated().sum()
    assert background.duplicated().sum() >= background_df_orig[background_df_orig.notnull()].duplicated().sum()




### helper functions
def non_decreasing(L):
    """
    https://stackoverflow.com/questions/4983258/python-how-to-check-list-monotonicity
    """
    return all(x<=y for x, y in zip(L, L[1:]))