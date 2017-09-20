import sys, os
import pandas as pd
import numpy as np
from collections import defaultdict
from io import StringIO # from StringIO import StringIO
from itertools import zip_longest # from itertools import izip_longest
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import tools, query

# test for comma vs point separated intensity values
# test for " enclosed ANs, in general and for protein groups using these
# test for background protein group with abundance data, but foreground with single AN or different size of protein group
# Question for Lars/Jan: # test for background protein group with abundance data, but foreground with single AN or different size of protein group

DEFAULT_MISSING_BIN = -1

class Userinput(object):
    """
    expects 2 arrays,
    foregroundfreq: Pandas DataFrame 1column
    backgrndfreq: 2D array/Pandas DataFrame, with backgrnd_an, backgrnd_int
    """
    def __init__(self, fn=None, foreground_string=None, background_string=None,
            col_foreground='foreground', col_background='background', col_intensity='intensity',
            num_bins=100, decimal='.', method="abundance_correction", foreground_n=None, background_n=None):
        self.fn = fn
        self.foreground_string = foreground_string
        self.background_string = background_string
        self.decimal = decimal
        self.num_bins = num_bins
        self.col_foreground = col_foreground
        self.col_background = col_background
        self.col_intensity = col_intensity
        self.method = method # one of: "abundance_correction", "compare_samples", "compare_groups", "characterize"
        # abundance_correction: Foreground vs Background abundance corrected
        # compare_samples: Foreground vs Background (no abundance correction)
        # compare_groups: Foreground(replicates) vs Background(replicates), --> foreground_n and background_n need to be set
        # characterize: Foreground only
        self.foreground_n = foreground_n
        self.background_n = background_n
        self.housekeeping_dict = {} # Infos for Usere
        self.check = True
        self.parse_input()

    def parse_input(self):
        self.fn.read()
        if self.fn.tell() != 0:
            self.fn.seek(0)
        else: # use copy & paste field
            self.fn = StringIO()
            is_abundance_correction = self.fast_check_is_abundance_correction(self.background_string)
            if is_abundance_correction:
                header = 'foreground\tbackground\tintensity\r'
            else:
                header = 'foreground\tbackground\r'
            self.fn.write(header)
            for a, b in zip_longest(self.foreground_string.split("\r\n"), self.background_string.split("\r\n"), fillvalue="\t"):
                self.fn.write(a.strip() + "\t" + b.strip() + "\r")
            self.fn.seek(0)
        is_abundance_correction, self.decimal = self.check_userinput(self.fn)
        if is_abundance_correction:
            self.method = "abundance_correction"
        else:
            self.method = "compare_samples" # switch for reporting that something went wrong to user, or automatically switch method
        self.df_orig = self.change_column_names(self.df_orig)
        self.cleanupforanalysis(self.df_orig, self.col_foreground, self.col_background, self.col_intensity)

    def fast_check_is_abundance_correction(self, background_string):
        string_split = background_string.split("\n", 1)[0].split("\t")
        try:
            float(string_split[1])
        except (IndexError, ValueError) as err_:
            return False
        return True

    def change_column_names(self, df):
        """
        :param df_orig: Pandas DataFrame
        :return: Pandas DataFrame
        """
        cols = sorted(self.df_orig.columns.tolist())
        cols = [colname.lower() for colname in cols]
        if "population" in cols:
            df = self.rename_cols(df, [("population", "background")])
        if "population_an" in cols:
            df = self.rename_cols(df, [("population_an", "background")])
        if "population_int" in cols:
            df = self.rename_cols(df, [("population_int", "intensity")])
        if "sample" in cols:
            df = self.rename_cols(df, [("sample", "foreground")])
        if "sample_an" in cols:
            df = self.rename_cols(df, [("sample_an", "foreground")])
        return df

    @staticmethod
    def rename_cols(df, cols2rename_tuple):  # rename to list
        """
        rename old to new names and remove old columns
        :param df: DataFrame
        :param cols2rename_tuple: [(old1, new1), (old2, new2), ...]
        :return: DataFrame
        """
        for colstuple in cols2rename_tuple:
            old, new = colstuple
            df[new] = df[old]
            del df[old]
        return df

    def check_userinput(self, fh):
        """
        test if userinput uses ',' or '.' as a decimal separator
        and if 3 columns for abundance_correction exist
        set df attribute
        :param fh: FileHandle
        :return: Tuple(Bool, String)
        """
        decimal = '.'
        self.df_orig = pd.read_csv(fh, sep='\t', decimal=decimal)
        if self.method == "abundance_correction":
            if len({self.col_background, self.col_intensity, self.col_foreground}.intersection(set(self.df_orig.columns.tolist()))) == 3:
                try:
                    np.histogram(self.df_orig.loc[pd.notnull(self.df_orig[self.col_intensity]), self.col_intensity], bins=10)
                except TypeError:
                    try:
                        decimal = ','
                        fh.seek(0)
                        self.df_orig = pd.read_csv(fh, sep='\t', decimal=decimal)
                        np.histogram(self.df_orig.loc[pd.notnull(self.df_orig[self.col_intensity]), self.col_intensity], bins=10)
                    except TypeError:
                        return False, decimal
                return True, decimal
        else:
            if len({self.col_background, self.col_foreground}.intersection(set(self.df_orig.columns.tolist()))) == 2:
                return True, decimal
        return False, decimal

    def cleanupforanalysis(self, df, col_foreground, col_background, col_intensity):
        """
        ToDo:
        summary stats on total number of ANs, redundancy, mapped to which species,
        remove NaNs, remove duplicates, split protein groups, remove splice variant appendix
        create 2 DataFrames
        self.df_all: columns = [foreground_ans, background_ans]
        --> contains all AccessionNumbers regardless if intensity values present or not
        self.df_int: columns = [foreground_ans, background_ans, intensity]
        --> only if intensity value given
        :return: None
        """
        # housekeeping
        self.housekeeping_dict["Foreground_Number_of_entries_including_duplicates_and_NaNs"] = len(df[[col_foreground]]) # total number of entries, including duplicates and NaNs
        if self.method == "abundance_correction":
            self.housekeeping_dict["Background_Number_of_entries_including_duplicates_and_NaNs"] = len(df[[col_background, col_intensity]])
        else:
            self.housekeeping_dict["Background_Number_of_entries_including_duplicates_and_NaNs"] = len(df[[col_background]])

        # remove NaNs from foregroundfrequency and backgroundfrequency AN-cols
        self.foreground = df.loc[pd.notnull(df[col_foreground]), [col_foreground]]
        if self.method == "abundance_correction":
            self.background = df.loc[pd.notnull(df[col_background]), [col_background, col_intensity]]
        else:
            self.background = df.loc[pd.notnull(df[col_background]), [col_background]]

        # remove splice variant appendix and drop duplicates
        self.foreground[col_foreground] = self.foreground[col_foreground].apply(self.remove_spliceVariant)
        if self.method != "compare_groups":
            self.foreground.drop_duplicates(subset=col_foreground, inplace=True)
        self.foreground.index = range(0, len(self.foreground))
        self.background[col_background] = self.background[col_background].apply(self.remove_spliceVariant)
        if self.method != "compare_groups":
            self.background.drop_duplicates(subset=col_background, inplace=True)
        # housekeeping
        self.housekeeping_dict["Foreground_Number_of_entries_excluding_duplicates_and_NaNs"] = len(self.foreground) # number of entries, excluding duplicates and NaNs
        self.housekeeping_dict["Background_Number_of_entries_excluding_duplicates_and_NaNs"] = len(self.background)

        # set default missing value for notnulls, and create lookup dict for abundances
        if self.method == "abundance_correction":
            cond = pd.isnull(self.background[col_intensity])
            self.background.loc[cond, col_intensity] = DEFAULT_MISSING_BIN
            self.an_2_intensity_dict = self.create_an_2_intensity_dict(zip(self.background[col_background], self.background[col_intensity]))

            # housekeeping
            self.housekeeping_dict["Number_ANs_with_missing_abundance_values"] = sum(cond)

            self.foreground["intensity"] = self.map_intensities_2_foreground()

        ## map obsolete Accessions to primary ANs, by replacing secondary ANs with primary ANs
        secondary_2_primary_dict = query.map_secondary_2_primary_ANs(self.get_all_unique_ANs())
        if secondary_2_primary_dict: # not an empty dict
            df_sec_prim = pd.DataFrame().from_dict(secondary_2_primary_dict, orient="index").reset_index()
            df_sec_prim.columns = ["secondary", "primary"]
            self.housekeeping_dict["Seondary_2_Primary_ANs_DF"] = df_sec_prim # ANs that were replaced
        else:
            self.housekeeping_dict["Seondary_2_Primary_ANs_DF"] = None

        self.foreground[col_foreground] = self.foreground[col_foreground].apply(self.replace_secondary_with_primary_ANs, args=(secondary_2_primary_dict, ))
        if self.method != "characterize":
            self.background[col_background] = self.background[col_background].apply(self.replace_secondary_with_primary_ANs, args=(secondary_2_primary_dict,))

        ### sort values for iter bins
        if self.method == "abundance_correction":
            # self.background.sort_values(self.col_intensity, ascending=True, inplace=True)
            # self.foreground.sort_values(["intensity"], ascending=False, inplace=True)
            cond = self.foreground["intensity"] > DEFAULT_MISSING_BIN
            if sum(cond) == 0:  # render info_check_input.html
                self.check = False

    def replace_secondary_with_primary_ANs(self, ans_string, secondary_2_primary_dict):
        ans_2_return = []
        for an in ans_string.split(";"): # if proteinGroup
            if an in secondary_2_primary_dict:
                ans_2_return.append(secondary_2_primary_dict[an])
            else:
                ans_2_return.append(an)
        return ";".join(ans_2_return)

    @staticmethod
    def create_an_2_intensity_dict(list_of_tuples):
        """
        notnull values are assigned a default of -1, in order to count them in an extra bin
        e.g.
        [('P00330', '10,6690378'),
         ('P02407;P14127', '10,64061061'),
         ...]
        --> an_2_intensity_dict["P02407"] = 10,64061061
        :param list_of_tuples: ListOfTuples(ANs_string, Intensity_float)
        :return: Dict (key=AN, val=Float)
        """
        an_2_intensity_dict = defaultdict(lambda: DEFAULT_MISSING_BIN)
        for ans, int_ in list_of_tuples:
            for an in ans.split(";"):
                an_2_intensity_dict[an] = int_
        return an_2_intensity_dict

    @staticmethod
    def remove_spliceVariant(string_):
        """
        removes appendix for splice variants from accession numbers and sorts protein groups
        :param string_: String
        :return: String
        """
        return ";".join(sorted([ele.split("-")[0] for ele in string_.split(";")]))

    def map_intensities_2_foreground(self):
        """
        foreground proteinGroups with abundance data
        first AN in proteinGroup used to lookup abundance values from background
        :return: Series
        """
        # foreground proteinGroups with intensities
        intensity_foreground = []
        for proteinGroup in self.foreground[self.col_foreground]:
            an_first_in_proteinGroup = proteinGroup.split(";")[0]
            intensity_foreground.append(self.an_2_intensity_dict[an_first_in_proteinGroup])
        return pd.Series(intensity_foreground, name="intensity")

    def get_foreground_an_set(self):
        return set(self.foreground[self.col_foreground].tolist())

    def get_background_an_set(self):
        return set(self.background[self.col_background].tolist())

    def get_foreground_n(self):
        """
        "abundance_correction", "compare_samples", "method", "characterize"
        :return: Int
        """
        if self.method == "abundance_correction":
            return len(self.foreground)
        elif self.method == "compare_samples": # no abundance correction
            return len(self.foreground)
        elif self.method == "compare_groups": # redundancies within group, therefore n set by user
            return self.foreground_n
        elif self.method == "characterize":
            return len(self.foreground)
        else:
            raise StopIteration # debug, case should not happen

    def get_background_n(self):
        """
        "abundance_correction", "compare_samples", "method", "characterize"
        :return: Int
        """
        if self.method == "abundance_correction": # same as foreground
            return len(self.foreground)
        elif self.method == "compare_samples": # simply background to compare to
            return len(self.background)
        elif self.method == "compare_groups": # redundancies within group, therefore n set by user
            return self.background_n
        elif self.method == "characterize": # only for foreground, not background
            return None
        else:
            raise StopIteration # debug, case should not happen

    def get_sample_an(self):
        return self.foreground[self.col_foreground].tolist()

    def iter_bins(self):
        """
        map foreground proteinGroups to background abundance values,
        split foreground proteinGroups into bins based on abundance,
        calculate a correction factor for each bin (num proteinGroups foreground / num proteinGroups background),
        yield background proteinGroups and correction factor for each bin
        :return: Tuple(ListOfString(';' sep ANs), correction factor)
        """
        cond = self.foreground["intensity"] > DEFAULT_MISSING_BIN
        bins = pd.cut(self.foreground.loc[cond, "intensity"], bins=self.num_bins, retbins=True)[1]
        # bins = [DEFAULT_MISSING_BIN - 1] + list(bins) # ToDo investigate and fix
        # print(self.foreground.head())
        groups_fg = self.foreground.groupby(pd.cut(self.foreground["intensity"], bins=bins))
        groups_bg = self.background.groupby(pd.cut(self.background[self.col_intensity], bins=bins))
        for group_fg, group_bg in zip(groups_fg, groups_bg):
            # bins_fg = group_fg[0]
            # bins_bg = group_bg[0]
            # assert bins_fg == bins_bg
            proteinGroups_foreground = group_fg[1][self.col_foreground]
            proteinGroups_background = group_bg[1][self.col_background]
            len_proteinGroups_foreground = len(proteinGroups_foreground) * 1.0
            len_proteinGroups_background = len(proteinGroups_background) * 1.0
            try:
                correction_factor = len_proteinGroups_foreground / len_proteinGroups_background
            except ZeroDivisionError:
                # since the foreground is assumed to be a proper subset of the background, anything in the foreground must also be in the background
                correction_factor = 1
                proteinGroups_background = proteinGroups_foreground
            if len_proteinGroups_foreground == 0:
                continue
            # yield proteinGroups_background.tolist(), proteinGroups_foreground.tolist(), correction_factor, bins_fg
            yield proteinGroups_background.tolist(), correction_factor

    def get_all_unique_ANs(self):
        """
        return all unique AccessionNumber provided by the user
        :return: ListOfString
        """
        ans = tools.commaSepCol2uniqueFlatList(self.foreground, self.col_foreground, sep=";", unique=True)
        ans += tools.commaSepCol2uniqueFlatList(self.background, self.col_background, sep=";", unique=True)
        return list(set(ans))

    def get_all_unique_proteinGroups(self):
        proteinGroup_list = []
        proteinGroup_list += self.foreground[self.col_foreground].tolist()
        if self.method != "characterize":
            proteinGroup_list += self.background[self.col_background].tolist()
        return list(set(proteinGroup_list))


if __name__ == "__main__":
    # fn = r'/Users/dblyon/modules/cpr/metaprot/Perio_vs_CH_Bacteria.txt'
    # fn = r'/Users/dblyon/modules/cpr/metaprot/CompareGroups_test.txt'
    # fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_proteinGroups.txt'
    # foreground_n = 10.0
    # background_n = 20.0
    # proteinGroup = True
    # ui = UserInput_compare_groups(proteinGroup, fn, foreground_n, background_n)
    # foreground_an = ui.get_foreground_an()
    # # backgound_an = ui.get_background_an()
    # all_unique_an = ui.get_all_unique_ans()
    # # print len(foreground_an), len(backgound_an), len(all_unique_an)
    # print len(foreground_an), len(all_unique_an)
    fn = r"/Users/dblyon/modules/cpr/agotool/static/data/exampledata/exampledata_yeast_Foreground_Background.txt"
    fn = r"/Users/dblyon/modules/cpr/agotool/static/data/exampledata/exampledata_yeast_Intensity_Sample_Population.txt"
    fn = r"/Users/dblyon/modules/cpr/agotool/static/data/exampledata/debug.txt"
    fn = r"/Users/dblyon/Downloads/Data for agotool 2017-01-30.txt"

    import db_config
    ECHO = False
    TESTING = False
    DO_LOGGING = False
    connection = db_config.Connect(echo=ECHO, testing=TESTING, do_logging=DO_LOGGING)

    import io
    fn = io.open(fn, mode='r')
    ui = Userinput(fn=fn, foreground_string=None,
        background_string=None, col_foreground='foreground',
        col_background='background', col_intensity='intensity',
        num_bins=100, decimal='.', method="abundance_correction", connection=connection)
    # print(ui.iter_bins().next())

