import pandas as pd
import numpy as np
from collections import defaultdict

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
    def __init__(self, user_input_fn=None, foreground_string=None, background_string=None,
            col_foreground_an='foreground_an', col_background_an='background_an', col_background_int='background_int',
            num_bins=100, decimal='.', method="abundance_correction"):

        self.user_input_fn = user_input_fn
        # !!! file name not file handle
        self.foreground_string = foreground_string
        self.background_string = background_string
        self.decimal = decimal
        self.num_bins = num_bins
        self.col_foreground_an = col_foreground_an
        self.col_background_an = col_background_an
        self.col_background_int = col_background_int
        self.method = method
        self.housekeeping_dict = {} # Infos for User
        self.parse_input()

    def parse_input(self):
        if self.user_input_fn is not None:
            is_abundance_correction, self.decimal = self.check_userinput(self.user_input_fn)

            if not is_abundance_correction:
                pass
                # switch for reporting that something went wrong to user, or automatically switch method
                # self.method = "compare_groups"
                # or "characterize study"

            self.df_orig = pd.read_csv(self.user_input_fn, sep="\t", decimal=self.decimal)
            self.cleanupforanalysis(self.df_orig, self.col_foreground_an, self.col_background_an, self.col_background_int)
        else: # do something cool ;)
            # parse text fields
            # self.bubu
            pass


    def cleanupforanalysis(self, df_orig, col_foreground_an, col_background_an, col_background_int):
        '''
        ToDo:
        summary stats on total number of ANs, redundancy, mapped to which species, 
        remove NaNs, remove duplicates, split protein groups, remove splice variant appendix
        create 2 DataFrames
        self.df_all: columns = [foreground_ans, background_ans]
        --> contains all AccessionNumbers regardless if intensity values present or not
        self.df_int: columns = [foreground_ans, background_ans, intensity]
        --> only if intensity value given
        :return: None
        '''
        self.foreground_ser = df_orig[col_foreground_an]
        self.background_df = df_orig[[col_background_an, col_background_int]]
        # housekeeping
        self.housekeeping_dict["Foreground_Number_of_entries_including_duplicates_and_NaNs"] = len(self.foreground_ser) # total number of entries, including duplicates and NaNs
        self.housekeeping_dict["Background_Number_of_entries_including_duplicates_and_NaNs"] = len(self.background_df)

        # remove NaNs from foregroundfrequency and backgroundfrequency AN-cols
        self.foreground_ser = self.foreground_ser[pd.notnull(self.foreground_ser)]
        self.background_df = self.background_df.loc[pd.notnull(self.background_df[self.col_background_an]), [col_background_an, col_background_int]]

        # remove splice variant appendix and drop duplicates
        self.foreground_ser = self.foreground_ser.apply(self.remove_spliceVariant)
        self.foreground_ser.drop_duplicates(inplace=True)
        self.background_df[self.col_background_an] = self.background_df[self.col_background_an].apply(self.remove_spliceVariant)
        self.background_df.drop_duplicates(subset=self.col_background_an, inplace=True)
        # housekeeping
        self.housekeeping_dict["Foreground_Number_of_entries_excluding_duplicates_and_NaNs"] = len(self.foreground_ser) # number of entries, excluding duplicates and NaNs
        self.housekeeping_dict["Background_Number_of_entries_excluding_duplicates_and_NaNs"] = len(self.background_df)

        # set default missing value for notnulls, and create lookup dict for abundances
        cond = pd.isnull(self.background_df[self.col_background_int])
        self.background_df.loc[cond, self.col_background_int] = DEFAULT_MISSING_BIN
        self.an_2_intensity_dict = self.create_an_2_intensity_dict(zip(self.background_df[self.col_background_an], self.background_df[self.col_background_int]))
        # housekeeping
        self.housekeeping_dict["Number_ANs_with_missing_abundance_values"] = sum(cond)

    def check_userinput(self, userinput_fh):
        """
        test if userinput uses ',' or '.' as a decimal separator
        and if 3 columns for abundance_correction exist
        :param userinput_fh: FileHandle
        :return: Tuple(Bool, String)
        """
        decimal = '.'
        df = pd.read_csv(userinput_fh, sep='\t', decimal=decimal)
        # userinput_fh.seek(0)
        if self.method == "abundance_correction":
            if len({self.col_background_an, self.col_background_int, self.col_foreground_an}.intersection(set(df.columns.tolist()))) == 3:
                try:
                    np.histogram(df.loc[pd.notnull(df[self.col_background_int]), self.col_background_int], bins=10)
                except TypeError:
                    try:
                        decimal = ','
                        df = pd.read_csv(userinput_fh, sep='\t', decimal=decimal)
                        # userinput_fh.seek(0)
                        np.histogram(df.loc[pd.notnull(df[self.col_background_int]), self.col_background_int], bins=10)
                    except TypeError:
                        return False, decimal
                return True, decimal
        else:
            if len({self.col_background_an, self.col_foreground_an}.intersection(set(df.columns.tolist()))) == 2:
                return True, decimal
        return False, decimal

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

    ###################################################
    #     foreground       |     background     |
    # -------------------------------------------------
    # +   a = foregr_count |   c = backgr_count |   r1
    # -------------------------------------------------
    # -     b              |       d            |   r2
    # -------------------------------------------------
    #     foregr_n         |     backgr_n       |    n


    def get_foreground_n(self):
        # get_study_n
        pass

    def get_background_n(self):
        # get_pop_n
        pass

    def get_sample_an(self):
        pass

# intensity values as array, for all proteins/proteinGroups

# protein groups only count as a single AN
# split intensity values of foreground into bins
# iterate over bins
    # correction factor = number ANs foreground in bin / number ANs background in bin
    # yield correction factor and ANs background


    def bbu(self):
        """
        foreground proteinGroups with intensities

        :return:
        """
        # foreground proteinGroups with intensities
        intensity_foreground = []
        for proteinGroup in self.foreground_ser:
            an_first_in_proteinGroup = proteinGroup.split(";")[0]
            intensity_foreground.append(self.an_2_intensity_dict[an_first_in_proteinGroup])
        self.foreground_df = pd.DataFrame(data=intensity_foreground, columns=["Int"])
        self.foreground_df["AN"] = self.foreground_ser

    def iter_bins(self):
        pass
        # hist = number of ANs in bin, bins = edges of the cuts
        # hist, bins = np.histogram(, bins=self.num_bins, density=False)

    def iter_bins_old(self):
        """
        for every bin, produce ans-background and weighting-factor of respective bin
        weighting-factor = number of foreground-ANs in bin / number background-ANs in bin
        :return: Tuple(ListOfSting, Float)
        """
        hist, bins = np.histogram(self.get_foreground_an_int()[self.col_background_int], bins=self.num_bins)
        for index, numinhist in enumerate(hist):
            num_ans = numinhist
            lower = bins[index]
            upper = bins[index + 1]
            ans_all_from_bin = self.get_random_an_from_bin(lower, upper, num_ans, get_all_ans=True)
            num_ans_all_from_bin = len(ans_all_from_bin)
            # if not num_ans_all_from_bin == 0:
            if num_ans_all_from_bin != 0:
                # weight_fac = float(numinhist) / len(ans_all_from_bin)
                weight_fac = float(numinhist) / num_ans_all_from_bin
            else:
                weight_fac = 0 #!!! debug
                print("Weight factor is Zero")
                raise StopIteration
            yield(ans_all_from_bin, weight_fac)

    def get_random_an_from_bin(self, lower, upper, num_ans=1, get_all_ans=False):
        '''
        produce a random number of AccessionNumbers within given boundaries of Intensity values
        where intensity >= lower and intensity < upper.
        option: get_all_ans returns all AccessionNumbers in bin
        :param lower: Float
        :param upper: Float
        :param num_ans: Integer
        :param get_all_ans: Boolean
        :return: ListOfString
        '''
        df = self.get_background_an_int()
        cond1 = df[self.col_background_int] >= lower
        cond2 = df[self.col_background_int] <= upper
        cond = cond1 & cond2
        ans_withinBounds = df.loc[cond, self.col_background_an]
        if len(ans_withinBounds) > 0:
            if get_all_ans:
                return sorted(ans_withinBounds)
            else:
                return sorted(np.random.choice(ans_withinBounds, size=num_ans, replace=False))
        else:
            return []


    def get_foreground_an_int(self):
        '''
        produce AccessionNumbers with corresponding Intensity of foreground/study
        :return: DataFrame
        '''
        return self.df_int.loc[pd.notnull(self.df_int[self.col_foreground_an]), [self.col_foreground_an, self.col_background_int]]

    def get_background_an_int(self):
        '''
        produce AccessionNumbers with corresponding Intensity of background/background
        :return: DataFrame
        '''
        return self.df_int[[self.col_background_an, self.col_background_int]]

    def concat_and_align_foreground_and_background(self, foreground_ser, background_df):
        '''
        expects a Series and a DataFrames each containing a column with non-redundant
        AccessionNumbers, concatenate by producing the union and aligning the ANs in rows
        :param foreground_ser: Pandas.Series
        :param background_df: Pandas.DataFrame
        :return: DataFrame
        '''
        foreground_ser.index = foreground_ser.tolist()
        background_df.index = background_df[self.col_background_an].tolist()
        return pd.concat([foreground_ser, background_df], axis=1)

    def get_random_background_ans(self):
        '''
        produce a randomly generated set of AccessionNumbers from background-frequency
        with the same intensity-distribution as foreground-frequency
        :return: ListOfString
        '''
        ans_random_list = []
        hist, bins = np.histogram(self.get_foreground_an_int()[self.col_background_int], bins=self.num_bins)
        for index, numinhist in enumerate(hist):
            num_ans = numinhist
            lower = bins[index]
            upper = bins[index+1]
            ans_random_list += self.get_random_an_from_bin(lower, upper, num_ans)
        return sorted(ans_random_list)




    def write_ans2file(self, ans_list, fn):
        with open(fn, 'w') as fh:
            for an in ans_list:
                fh.write(an + '\n')

    def get_foreground_an_frset(self):
        '''
        produce frozenset of AccessionNumbers of foreground frequency (study)
        if intensity value given
        :return: FrozenSet of Strings
        '''
        return frozenset(self.df_int.loc[pd.notnull(self.df_int[self.col_foreground_an]), self.col_foreground_an])

    def get_foreground_an_frset_all(self):
        '''
        produce Set of AccessionNumbers of original DataFrame, regardless of abundance data
        remove NaN
        :return: SetOfString
        '''
        return frozenset(self.df_all.loc[pd.notnull(self.df_all[self.col_foreground_an]), self.col_foreground_an])

    def get_foreground_an_frset_genome(self):
        '''
        produce all AccessionNumbers with intensity values in 'Observed' column
        :return: Frozenset of Strings
        '''
        col_background_an = 'Observed Proteome'
        ui2 = Userinput(self.user_input_fn, self.num_bins, col_foreground_an=self.col_foreground_an, col_background_an=col_background_an, col_background_int=self.col_background_int, decimal=self.decimal)
        return ui2.get_foreground_an_frset()

    def get_background_an_set(self):
        '''
        produce set of AccessionNumbers of background frequency (background)
        if intensity value given
        :return: Set of Strings
        '''
        return set(self.df_int[self.col_background_an])

    def get_background_an_all_set(self):
        '''
        produce Set of AccessionNumbers of original DataFrame, regardless of abundance data
        remove NaN
        :return: SetOfString
        '''
        return set(self.df_all[self.col_background_an])

    def get_background_an_set_random_foreground(self):
        '''
        produce a randomly generated set of AccessionNumbers from background-frequency
        with the same intensity-distribution as foreground-frequency
        :return: Set of Strings
        '''
        return set(self.get_random_background_ans())


class Userinput_noAbCorr(Userinput):

    def __init__(self, user_input_fn, num_bins=100, col_foreground_an='foreground_an', col_background_an='background_an', decimal='.'):
        self.user_input_fn = user_input_fn
        self.decimal = decimal
        self.df_orig = pd.read_csv(user_input_fn, sep="\t", decimal=self.decimal)
        self.set_num_bins(num_bins)
        self.col_foreground_an = col_foreground_an
        self.col_background_an = col_background_an
        self.cleanupforanalysis(self.df_orig, self.col_foreground_an, self.col_background_an)

    def cleanupforanalysis(self, df_orig, col_foreground_an, col_background_an):
        self.foreground_ser = df_orig[col_foreground_an]
        self.background_ser = df_orig[col_background_an]

        # remove duplicate AccessionNumbers and NaNs from foregroundfrequency and backgroundfrequency AN-cols
        cond = pd.notnull(self.foreground_ser)
        self.foreground_ser = self.foreground_ser.loc[cond, ].drop_duplicates()
        cond = pd.notnull(self.background_ser)
        self.background_ser = self.background_ser.loc[cond, ].drop_duplicates()

        # split AccessionNumber column into mulitple rows P63261;I3L4N8;I3L1U9;I3L3I0 --> correction: 1 row of first value
        # remove splice variant appendix from AccessionNumbers (if present) P04406-2 --> P04406
        self.foreground_ser = self.removeSpliceVariants_takeFirstEntryProteinGroups_Series(self.foreground_ser)
        self.background_ser = self.removeSpliceVariants_takeFirstEntryProteinGroups_Series(self.background_ser)

        # remove duplicate AccessionNumbers and NaNs from foregroundfrequency and backgroundfrequency AN-cols
        cond = pd.notnull(self.foreground_ser)
        self.foreground_ser = self.foreground_ser.loc[cond, ].drop_duplicates()
        cond = pd.notnull(self.background_ser)
        self.background_ser = self.background_ser.loc[cond, ].drop_duplicates()

    def get_foreground_an_frset(self):
        return frozenset(self.foreground_ser)

    def get_background_an_all_set(self):
        return set(self.background_ser)


class UserInput_compare_groups(object):

    def __init__(self, proteinGroup, user_input_fn, study_n, pop_n, col_foreground_an='foreground_an', col_background_an='background_an', decimal='.'):
        self.proteinGroup = proteinGroup
        self.user_input_fn = user_input_fn
        self.study_n = study_n
        self.pop_n = pop_n
        self.decimal = decimal
        self.df = pd.read_csv(user_input_fn, sep="\t", decimal=self.decimal)
        self.col_foreground_an = col_foreground_an
        self.col_background_an = col_background_an
        self.foreground_ser = self.df[col_foreground_an]
        self.background_ser = self.df[col_background_an]

        # remove NaNs from foregroundfrequency and backgroundfrequency AN-cols
        # DON'T REMOVE DUPLICATES
        self.foreground_ser = self.foreground_ser.dropna()
        if not self.proteinGroup:
            self.foreground_ser = self.foreground_ser.apply(self.grep_first_an_from_proteinGroup)

        self.background_ser = self.background_ser.dropna()
        if not self.proteinGroup:
            self.background_ser = self.background_ser.apply(self.grep_first_an_from_proteinGroup)

    def grep_first_an_from_proteinGroup(self, stringi_):
        try:
            return stringi_.split(";")[0]
        except IndexError:
            return stringi_

    def get_foreground_an(self):
        return self.foreground_ser

    def get_background_an(self):
        return self.background_ser

    def split_protGroups_into_unique_list(self, ans_list):
        temp_list = []
        for protgroup in ans_list:
            temp_list += protgroup.split(";")
        return sorted(set(temp_list))

    def get_all_unique_ans(self, foreground_background_all="all"):
        if foreground_background_all == "all":
            ans_list = self.foreground_ser.unique().tolist() + self.background_ser.unique().tolist()
        elif foreground_background_all == "foreground":
            ans_list = self.foreground_ser.unique().tolist()
        elif foreground_background_all == "background":
            ans_list = self.background_ser.unique().tolist()
        ans_list = sorted(set(ans_list))
        if self.proteinGroup: # split comma sep string of ANs into single ANs and make unique
            ans_list = self.split_protGroups_into_unique_list(ans_list)
        return ans_list

    def get_study_n(self):
        return self.study_n

    def get_pop_n(self):
        return self.pop_n


if __name__ == "__main__":
    fn = r'/Users/dblyon/modules/cpr/metaprot/Perio_vs_CH_Bacteria.txt'
    fn = r'/Users/dblyon/modules/cpr/metaprot/CompareGroups_test.txt'
    fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_proteinGroups.txt'
    study_n = 10.0
    pop_n = 20.0
    proteinGroup = True
    ui = UserInput_compare_groups(proteinGroup, fn, study_n, pop_n)
    foreground_an = ui.get_foreground_an()
    # backgound_an = ui.get_background_an()
    all_unique_an = ui.get_all_unique_ans()
    # print len(foreground_an), len(backgound_an), len(all_unique_an)
    print len(foreground_an), len(all_unique_an)




####### Dead Code RIP
# def removeSpliceVariants_splitProteinGrous_Series(self, series):
#     '''
#     remove splice variant appendix from AccessionNumbers (if present) P04406-2 --> P04406
#     split AccessionNumber column into mulitple rows P63261;I3L4N8;I3L1U9;I3L3I0 --> 4 rows of values
#     :param series: PandasSeries
#     :return: Series
#     '''
#     list2return = []
#     templist = []
#     for ele in series:
#         templist += ele.split(';')
#     for ele in templist:
#         ele_split = ele.split('-')
#         if len(ele_split) > 1:
#             list2return.append(ele_split[0])
#         else:
#             list2return.append(ele)
#     return pd.Series(list2return, name=series.name)
#
#
# def removeSpliceVariants_takeFirstEntryProteinGroups_Series(self, series):
#     list2return = []
#     templist = []
#     for ele in series:
#         ele_split = ele.split(';')
#         if len(ele_split) > 1:
#             templist.append(ele_split[0])
#         else:
#             templist.append(ele)
#     for ele in templist:
#         ele_split = ele.split('-')
#         if len(ele_split) > 1:
#             list2return.append(ele_split[0])
#         else:
#             list2return.append(ele)
#     return pd.Series(list2return, name=series.name)
#
#
# def removeSpliceVariants_takeFirstEntryProteinGrous_DataFrame(self, dataframe, colname_an, colname_int):
#     iterrows = dataframe[[colname_an, colname_int]].iterrows()
#     for row in iterrows:
#         index = row[0]
#         an_row = row[1][colname_an]
#         an_row_split_colon = an_row.split(';')
#         if len(an_row_split_colon) > 1:
#             an = an_row_split_colon[0]
#         else:
#             an = an_row
#         an_split_minus = an.split('-')
#         if len(an_split_minus) > 1:
#             an = an_split_minus[0]
#         else:
#             an = an
#         dataframe.loc[index, colname_an] = an
#     return dataframe
#
#
# def removeSpliceVariants_splitProteinGrous_DataFrame(self, dataframe, colname_an, colname_int):
#     '''
#     remove splice variant appendix from AccessionNumbers (if present) P04406-2 --> P04406
#     split AccessionNumber column into mulitple rows P63261;I3L4N8;I3L1U9;I3L3I0 --> 4 rows of values
#     copy abundance data when adding rows
#     :param series: PandasDataFrame
#     :return: Series
#     '''
#     df_new = self.splitProteinGroups_DataFrame(dataframe, colname_an, colname_int)
#     return self.removeSpliceVariants_DataFrame(df_new, colname_an, colname_int)
#
#
# def splitProteinGroups_DataFrame(self, dataframe, colname_an, colname_int):
#     ans2write_list = []
#     int2write_list = []
#     iterrows = dataframe[[colname_an, colname_int]].iterrows()
#     for row in iterrows:
#         index = row[0]
#         int_val = dataframe.loc[index, colname_int]
#         ans_row = row[1][colname_an]
#         ans_split_semicol = ans_row.split(';')
#         len_ans_split_semicol = len(ans_split_semicol)
#         if len_ans_split_semicol > 1:
#             ans2write_list += ans_split_semicol
#             int2write_list += [int_val] * len_ans_split_semicol
#         else:
#             ans2write_list.append(ans_row)
#             int2write_list.append(int_val)
#     return pd.DataFrame({colname_an: ans2write_list, colname_int: int2write_list})
#
#
# def removeSpliceVariants_DataFrame(self, dataframe, colname_an, colname_int):
#     # iterrows = dataframe[[colname_an, colname_int]].iterrows()
#     # for row in iterrows:
#     for index_, row in dataframe[[colname_an, colname_int]].iterrows():
#         index = row[0]
#         an_row = row[1][colname_an]
#         an_split_minus = an_row.split('-')
#         len_an_split_minus = len(an_split_minus)
#         if len_an_split_minus > 1:
#             dataframe.loc[index, colname_an] = an_split_minus[0]
#     return dataframe
