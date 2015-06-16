import pandas as pd
import numpy as np
import os


class UserInput(object):
    """
    expects 2 arrays,
    samplefreq: Pandas DataFrame 1column
    backgrndfreq: 2D array/Pandas DataFrame, with backgrnd_an, backgrnd_int
    """
    def __init__(self, user_input_fn=None, num_bins=100, col_sample_an='sample_an', col_background_an='backgrnd_an', col_background_int='backgrnd_int', decimal='.'):
        home = os.path.expanduser('~')
        if not user_input_fn:
            user_input_fn = home + r"/CloudStation/CPR/Brian_GO/UserInput.txt"
        self.user_input_fn = user_input_fn
        self.decimal = decimal
        self.df_orig = pd.read_csv(user_input_fn, sep="\t", decimal=self.decimal) #!!! check file for this
        self.set_num_bins(num_bins)
        self.col_sample_an = col_sample_an
        self.col_background_an = col_background_an
        self.col_background_int = col_background_int
        self.cleanupforanalysis(self.df_orig, self.col_sample_an, self.col_background_an, self.col_background_int)

    def cleanupforanalysis(self, df_orig, col_sample_an, col_background_an, col_background_int):
        '''
        remove NaNs, remove duplicates, split protein groups, remove splice variant appendix
        create 2 DataFrames
        self.df_all: columns = [sample_ans, background_ans]
        --> contains all AccessionNumbers regardless if intensity values present or not
        self.df_int: columns = [sample_ans, background_ans, intensity]
        --> only if intensity value given
        :return: None
        '''
        self.sample_ser = df_orig[col_sample_an]
        self.background_df = df_orig[[col_background_an, col_background_int]]

        # remove duplicate AccessionNumbers and NaNs from samplefrequency and backgroundfrequency AN-cols
        cond = pd.notnull(self.sample_ser)
        self.sample_ser = self.sample_ser.loc[cond, ].drop_duplicates()
        cond = pd.notnull(self.background_df[col_background_an])
        self.background_df = self.background_df.loc[cond, [col_background_an, col_background_int]].drop_duplicates(subset=col_background_an)

        # split AccessionNumber column into mulitple rows P63261;I3L4N8;I3L1U9;I3L3I0 --> 4 rows of values
        # remove splice variant appendix from AccessionNumbers (if present) P04406-2 --> P04406
        # self.sample_ser = self.removeSpliceVariants_splitProteinGrous_Series(self.sample_ser)
        self.sample_ser = self.removeSpliceVariants_takeFirstEntryProteinGroups_Series(self.sample_ser)
        # self.background_df = self.removeSpliceVariants_splitProteinGrous_DataFrame(self.background_df, col_background_an, col_background_int)
        self.background_df = self.removeSpliceVariants_takeFirstEntryProteinGrous_DataFrame(self.background_df, col_background_an, col_background_int)

        # remove duplicate AccessionNumbers and NaNs from samplefrequency and backgroundfrequency AN-cols
        cond = pd.notnull(self.sample_ser)
        self.sample_ser = self.sample_ser.loc[cond, ].drop_duplicates()
        cond = pd.notnull(self.background_df[col_background_an])
        self.background_df = self.background_df.loc[cond, [col_background_an, col_background_int]].drop_duplicates(subset=col_background_an)

        # concatenate data
        self.df_all = self.concat_and_align_sample_and_background(self.sample_ser, self.background_df)

        # remove AccessionNumbers from sample and background-frequency without intensity values
        self.df_int  = self.df_all.loc[pd.notnull(self.df_all[col_background_int]), ]

    def removeSpliceVariants_splitProteinGrous_Series(self, series):
        '''
        remove splice variant appendix from AccessionNumbers (if present) P04406-2 --> P04406
        split AccessionNumber column into mulitple rows P63261;I3L4N8;I3L1U9;I3L3I0 --> 4 rows of values
        :param series: PandasSeries
        :return: Series
        '''
        list2return = []
        templist = []
        for ele in series:
            templist += ele.split(';')
        for ele in templist:
            ele_split = ele.split('-')
            if len(ele_split) > 1:
                list2return.append(ele_split[0])
            else:
                list2return.append(ele)
        return pd.Series(list2return, name = series.name)

    def removeSpliceVariants_takeFirstEntryProteinGroups_Series(self, series):
        list2return = []
        templist = []
        for ele in series:
            ele_split = ele.split(';')
            if len(ele_split) > 1:
                templist.append(ele_split[0])
            else:
                templist.append(ele)
        for ele in templist:
            ele_split = ele.split('-')
            if len(ele_split) > 1:
                list2return.append(ele_split[0])
            else:
                list2return.append(ele)
        return pd.Series(list2return, name = series.name)

    def removeSpliceVariants_takeFirstEntryProteinGrous_DataFrame(self, dataframe, colname_an, colname_int):
        iterrows = dataframe[[colname_an, colname_int]].iterrows()
        for row in iterrows:
            index = row[0]
            an_row = row[1][colname_an]
            an_row_split_colon = an_row.split(';')
            if len(an_row_split_colon) > 1:
                an = an_row_split_colon[0]
            else:
                an = an_row
            an_split_minus = an.split('-')
            if len(an_split_minus) > 1:
                an = an_split_minus[0]
            else:
                an = an
            dataframe.loc[index, colname_an] = an
        return dataframe


    def removeSpliceVariants_splitProteinGrous_DataFrame(self, dataframe, colname_an, colname_int):
        '''
        remove splice variant appendix from AccessionNumbers (if present) P04406-2 --> P04406
        split AccessionNumber column into mulitple rows P63261;I3L4N8;I3L1U9;I3L3I0 --> 4 rows of values
        copy abundance data when adding rows
        :param series: PandasDataFrame
        :return: Series
        '''
        df_new = self.splitProteinGroups_DataFrame(dataframe, colname_an, colname_int)
        return self.removeSpliceVariants_DataFrame(df_new, colname_an, colname_int)

    def splitProteinGroups_DataFrame(self, dataframe, colname_an, colname_int):
        ans2write_list = []
        int2write_list = []
        iterrows = dataframe[[colname_an, colname_int]].iterrows()
        for row in iterrows:
            index = row[0]
            int_val = dataframe.loc[index, colname_int]
            ans_row = row[1][colname_an]
            ans_split_semicol = ans_row.split(';')
            len_ans_split_semicol = len(ans_split_semicol)
            if len_ans_split_semicol > 1:
                ans2write_list += ans_split_semicol
                int2write_list += [int_val] * len_ans_split_semicol
            else:
                ans2write_list.append(ans_row)
                int2write_list.append(int_val)
        return pd.DataFrame({colname_an: ans2write_list, colname_int: int2write_list})

    def removeSpliceVariants_DataFrame(self, dataframe, colname_an, colname_int):
        iterrows = dataframe[[colname_an, colname_int]].iterrows()
        for row in iterrows:
            index = row[0]
            an_row = row[1][colname_an]
            an_split_minus = an_row.split('-')
            len_an_split_minus = len(an_split_minus)
            if len_an_split_minus > 1:
                dataframe.loc[index, colname_an] = an_split_minus[0]
        return dataframe

    def set_num_bins(self, num_bins):
        self.num_bins = num_bins

    def get_num_bins(self):
        return self.num_bins

    def get_sample_an_int(self):
        '''
        produce AccessionNumbers with corresponding Intensity of sample/study
        :return: DataFrame
        '''
        return self.df_int.loc[pd.notnull(self.df_int[self.col_sample_an]), [self.col_sample_an, self.col_background_int]]

    def get_background_an_int(self):
        '''
        produce AccessionNumbers with corresponding Intensity of background/population
        :return: DataFrame
        '''
        return self.df_int[[self.col_background_an, self.col_background_int]]

    def concat_and_align_sample_and_background(self, sample_ser, background_df):
        '''
        expects a Series and a DataFrames each containing a column with non-redundant
        AccessionNumbers, concatenate by producing the union and aligning the ANs in rows
        :param sample_ser: Pandas.Series
        :param background_df: Pandas.DataFrame
        :return: DataFrame
        '''
        sample_ser.index = sample_ser.tolist()
        background_df.index = background_df[self.col_background_an].tolist()
        return pd.concat([sample_ser, background_df], axis=1)

    def get_random_background_ans(self):
        '''
        produce a randomly generated set of AccessionNumbers from background-frequency
        with the same intensity-distribution as sample-frequency
        :return: ListOfString
        '''
        ans_random_list = []
        hist, bins = np.histogram(self.get_sample_an_int()[self.col_background_int], bins=self.get_num_bins())
        for index, numinhist in enumerate(hist):
            num_ans = numinhist
            lower = bins[index]
            upper = bins[index+1]
            ans_random_list += self.get_random_an_from_bin(lower, upper, num_ans)
        return sorted(ans_random_list)

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

    def iter_bins(self):
        """
        for every bin, produce ans-background and weighting-factor of respective bin
        :return: Tuple(ListOfSting, Float)
        """
        hist, bins = np.histogram(self.get_sample_an_int()[self.col_background_int], bins=self.get_num_bins())
        for index, numinhist in enumerate(hist):
            num_ans = numinhist
            lower = bins[index]
            upper = bins[index+1]
            ans_all_from_bin = self.get_random_an_from_bin(lower, upper, num_ans, get_all_ans=True) #!!!
            num_ans_all_from_bin = len(ans_all_from_bin)
            if not num_ans_all_from_bin == 0:
                weight_fac = float(numinhist) / len(ans_all_from_bin)
            else:
                weight_fac = 0 #!!!
            yield(ans_all_from_bin, weight_fac)

    def write_ans2file(self, ans_list, fn):
        with open(fn, 'w') as fh:
            for an in ans_list:
                fh.write(an + '\n')

    def get_sample_an_frset(self):
        '''
        produce frozenset of AccessionNumbers of sample frequency (study)
        if intensity value given
        :return: FrozenSet of Strings
        '''
        return frozenset(self.df_int.loc[pd.notnull(self.df_int[self.col_sample_an]), self.col_sample_an])

    def get_sample_an_frset_all(self):
        '''
        produce Set of AccessionNumbers of original DataFrame, regardless of abundance data
        remove NaN
        :return: SetOfString
        '''
        return frozenset(self.df_all.loc[pd.notnull(self.df_all[self.col_sample_an]), self.col_sample_an])

    def get_sample_an_frset_genome(self):
        '''
        produce all AccessionNumbers with intensity values in 'Observed' column
        :return: Frozenset of Strings
        '''
        col_background_an = 'Observed Proteome'
        ui2 = UserInput(self.user_input_fn, self.get_num_bins, col_sample_an=self.col_sample_an, col_background_an=col_background_an, col_background_int=self.col_background_int, decimal=self.decimal)
        return ui2.get_sample_an_frset()

    def get_background_an_set(self):
        '''
        produce set of AccessionNumbers of background frequency (population)
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

    def get_background_an_set_random_sample(self):
        '''
        produce a randomly generated set of AccessionNumbers from background-frequency
        with the same intensity-distribution as sample-frequency
        :return: Set of Strings
        '''
        return set(self.get_random_background_ans())















