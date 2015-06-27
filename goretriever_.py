import cPickle as pickle
import pandas as pd
import numpy as np
from os.path import expanduser
home = expanduser("~")

__author__ = 'dblyon'


class Parser_UniProt_goa_ref(object):
    """
    formerly known as 'Goretriever'
    parse UniProt goa_ref files retrieved from ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/
    # e.g. gene_association.goa_ref_yeast
    # additional info http://www.geneontology.org/doc/GO.references
    produce list of GO-terms associated with given AccessionNumber
    """
    go_parents_name2num_dict = {"BP": "GO:0008150", "CP": "GO:0005575", "MF": "GO:0003674"}

    def __init__(self, goa_ref_fn=None):
        """
        :return: None
        """
        self.an2go_dict = {} # key=AccessionNumber val=ListOfStrings (GO-terms)
        self.date = "not set yet" # generation date
        self.obolibrary = "not yet set" # link to obo-library
        if not goa_ref_fn:
            goa_ref_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/yeast/gene_association.goa_ref_yeast'
        self.parse_goa_ref(goa_ref_fn)

    def parse_goa_ref(self, fn):
        """
        parse UniProt goa_ref file filling self.an2go_dict
        :param fn: raw String
        :return: None
        """
        fh = open(fn, "r")
        for line in fh:
            if line[0] == "!":
                if line[0:11] == "!Generated:":
                    self.date = line.replace("!Generated:", "").strip()
                elif line[0:12] == "!GO-version:":
                    self.obolibrary = line.replace("!GO-version:", "").strip()
            else:
                line_split = line.split("\t")
                if len(line_split) == 17:
                    an = line_split[1] # DB_Object_ID
                    goid = line_split[4] # GO_ID
                    if not self.an2go_dict.has_key(an):
                        self.an2go_dict[an] = [goid]
                    else:
                        self.an2go_dict[an].append(goid)
        self.remove_redundant_go_terms()
        fh.close()

    def get_goterms_from_an(self, an):
        """
        produce list of GO-terms associated with given AccessionNumber
        :param an: String
        :return: ListOfString
        """
        try:
            return self.an2go_dict[an]
        except KeyError:
            return -1 #!!!

    def get_goterms_from_an_limit2parent(self, an, go_parent, obo_dag):
        '''
        produce list of GO-terms associated with given AccessionNumber
        limit to child terms of given parent
        :param an: String
        :param go_parent: String
        :param obo_dag: GODag Instance
        :return: ListOfString
        '''
        goterms_list = self.get_goterms_from_an(an)
        if goterms_list == -1:
            return -1
        else:
            goterms_of_parent = []
            for goterm in goterms_list:
                if obo_dag[goterm].has_parent(self.go_parents_name2num_dict[go_parent]):
                    goterms_of_parent.append(goterm)
        if len(goterms_of_parent) >= 1:
            return goterms_of_parent
        else:
            return -1

    def get_ans(self):
        '''
        produce List of AccessionNumbers
        :return: ListOfString
        '''
        return sorted(self.an2go_dict)

    def get_date(self):
        """
        produce generation date of UniProt resource file
        :return: String
        """
        return self.date

    def get_obolibrary(self):
        """
        produce link to obo-library
        :return: String
        """
        return self.obolibrary

    def remove_redundant_go_terms(self):
        """
        remove redundant go-terms for each AccessionNumber if present
        and sort list of go-terms
        :return: None
        """
        for an in self.an2go_dict.keys():
            self.an2go_dict[an] = sorted(set(self.an2go_dict[an]))

    def pickle(self, fn_p):
        """
        pickle relevant attributes to given FileName
        :param fn_p: raw String
        :return: None
        """
        dict2pickle = {}
        dict2pickle["an2godict"] = self.an2go_dict
        dict2pickle["date"] = self.date
        dict2pickle["obolibrary"] = self.obolibrary
        pickle.dump(dict2pickle, open(fn_p, "wb"))
        del dict2pickle

    def unpickle(self, fn_p):
        """
        unpickle and set relevant attributes to instance
        :param fn_p: raw String
        :return: None
        """
        dict2pickle = pickle.load(open(fn_p, "rb"))
        self.an2go_dict = dict2pickle["an2godict"]
        self.date = dict2pickle["date"]
        self.obolibrary = dict2pickle["obolibrary"]
        del dict2pickle

    def write_association2file(self, fn_out):
        '''
        produce input file for goatools termed 'association'
        containing all AccessionNumbers of theoretical proteome and
        their corresponding GO-IDs
        e.g.:
        AN tab GO-id1;GO-id2;GO-id3
        ACD5	GO:0005575;GO:0003674;GO:0008219
        :param fn_out: rawString
        :return: None
        '''
        with open(fn_out, 'w') as fh_out:
            for an in self.get_ans():
                go_list = self.get_goterms_from_an(an)
                if go_list == -1:
                    pass # #!!! should there be a default value instead?
                else:
                    fh_out.write(an + '\t' + ';'.join(go_list) + '\n')

    def get_association_dict(self, go_parent, obo_dag):
        '''
        produce association_dictionary, containing all AccessionNumbers of theoretical proteome and
        their corresponding GO-IDs (most specific ones)
        do not report GO-ID without association
        assoc is a dict: key=AN, val=set of go-terms
        if go_parents given: limit the set of GO-terms to the given parent category
        obo_dag is a Dict: key=GO-term, val=GOTerm instance
        can be queried for parent term: obo_dag['GO:1990413'].has_parent('GO:0008150')
        # "BP" "GO:0008150"
        # "CP" "GO:0005575"
        # "MF" "GO:0003674"
        :param go_parent: String
        :param obo_dag: GODag Instance
        :return: Dict
        '''
        assoc_dict = {}
        for an in self.get_ans():
            if not assoc_dict.has_key(an):
                if go_parent:
                    goterms_list = self.get_goterms_from_an_limit2parent(an, go_parent, obo_dag)
                else:
                    goterms_list = self.get_goterms_from_an(an)
                if goterms_list != -1:
                    assoc_dict[an] = set(goterms_list)
            else:
                if go_parent:
                    goterms_set = set(self.get_goterms_from_an_limit2parent(an, go_parent, obo_dag))
                else:
                    goterms_set = set(self.get_goterms_from_an(an))
                if assoc_dict[an] != goterms_set:
                    print('Associations-dict: multiple entries of AN with diverging associations:')
                    print(an + ' ' + self.get_goterms_from_an(an))
        return assoc_dict



class UserInput(object):
    """
    expects 2 arrays,
    samplefreq: Pandas DataFrame 1column
    backgrndfreq: 2D array/Pandas DataFrame, with backgrnd_an, backgrnd_int
    """
    def __init__(self, user_input_fn=None, num_bins=100, col_sample_an='sample_an', col_background_an='backgrnd_an', col_background_int='backgrnd_int', decimal='.'):
        if not user_input_fn:
            user_input_fn = home + r"/CloudStation/CPR/Brian_GO/UserInput.txt"
        self.df_orig = pd.read_csv(user_input_fn, sep="\t", decimal=decimal) #!!! check file for this
        self.set_num_bins(num_bins)
        self.col_sample_an = col_sample_an
        self.col_background_an = col_background_an
        self.col_background_int = col_background_int
        self.cleanupforanalysis()
        # self.df_orig: unchanged
        # remove NaNs, duplicates, split, protein groups, remove splice variant appendix
        # self.df: aligned and only if intensity values exist

        # SAMPLE:
        # no NaNs, no duplicates, split protein groups, remove splice variant appendix
        # self.sample_ser_all: PandasSeries of AccessionNumbers
        # self.sample_ser_int: if abundance data present
        # BACKGROUND:
        # no NaNs, no duplicates, split protein groups, remove splice variant appendix
        # self.background_df_all: PandasDataFrame of AccessionNumber and Abundance data
        # self.background_df_int: if abundance data present
        # self.background_df_all_minsample: sample ANs removed
        # self.background_df_int_minsample: sample ANs removed
        # STUDY:
        # = self.sample_ser_int
        # POPULATION:
        # = self.background_df_int

    def cleanupforanalysis(self):
        '''
        reduce to non-redundant AccessionNumbers for sample and background-frequency (uses first observed row),
        remove ANs without GO-term(s)
        remove ANs without intensity-values
        concat and align data to single DataFrame
        :return: None
        '''
        self.sample_ser = self.df_orig[self.col_sample_an]
        self.background_df = self.df_orig[[self.col_background_an, self.col_background_int]]

        # remove duplicate AccessionNumbers and NaNs from samplefrequency and backgroundfrequency AN-cols
        cond = pd.notnull(self.sample_ser)
        self.sample_ser = self.sample_ser.loc[cond, ].drop_duplicates()
        cond = pd.notnull(self.background_df[self.col_background_an])
        self.background_df = self.background_df.loc[cond, [self.col_background_an, self.col_background_int]].drop_duplicates(subset=self.col_background_an)

        # split AccessionNumber column into mulitple rows P63261;I3L4N8;I3L1U9;I3L3I0 --> 4 rows of values
        # remove splice variant appendix from AccessionNumbers (if present) P04406-2 --> P04406
        self.sample_ser = self.removeSpliceVariants_splitProteinGrous_Series(self.sample_ser)
        self.background_df = self.removeSpliceVariants_splitProteinGrous_DataFrame(self.background_df, self.col_background_an, self.col_background_int)

        # remove duplicate AccessionNumbers and NaNs from samplefrequency and backgroundfrequency AN-cols
        cond = pd.notnull(self.sample_ser)
        self.sample_ser = self.sample_ser.loc[cond, ].drop_duplicates()
        self.set_sample_ser_all(self.sample_ser.copy())
        cond = pd.notnull(self.background_df[self.col_background_an])
        self.background_df = self.background_df.loc[cond, [self.col_background_an, self.col_background_int]].drop_duplicates(subset=self.col_background_an)
        self.set_background_df_all(self.background_df.copy())

        # concatenate data
        self.df = self.concat_and_align_sample_and_background(self.sample_ser, self.background_df)
        # remove AccessionNumbers from sample and background-frequency without intensity values
        self.df  = self.df.loc[pd.notnull(self.df[self.col_background_int]), ]
        # self.set_study(self.df.loc[pd.notnull(self.df[self.col_sample_an]), self.col_sample_an])
        self.set_sample_ser_int(self.df.loc[pd.notnull(self.df[self.col_sample_an]), self.col_sample_an])
        # self.set_population(self.df[[self.col_background_int, self.col_background_an]])
        self.set_background_df_int(self.df[[self.col_background_an, self.col_background_int]])

        # set background minus sample
        cond = self.get_background_df_all()[self.col_background_an].isin(self.get_sample_ser_all())
        self.set_background_df_all_minsample(self.get_background_df_all().loc[-cond, ].copy())
        cond = self.get_background_df_int()[self.col_background_an].isin(self.get_sample_ser_int())
        self.set_background_df_int_minsample(self.get_background_df_int().loc[-cond, ].copy())

    def set_sample_ser_all(self, series):
        self.sample_ser_all = series
        self.sample_ser_all.index = self.sample_ser_all.tolist()

    def get_sample_ser_all(self):
        return self.sample_ser_all

    def get_sample_list_all(self):
        return sorted(self.sample_ser_all)

    def set_sample_ser_int(self, series):
        self.sample_ser_int = series
        self.sample_ser_int.index = self.sample_ser_int.tolist()

    def get_sample_ser_int(self):
        return self.sample_ser_int

    def get_sample_list_int(self):
        return sorted(self.sample_ser_int)

    def set_background_df_all(self, df):
        self.background_df_all = df
        self.background_df_all.index = self.background_df_all[self.col_background_an].tolist()

    def get_background_df_all(self):
        return self.background_df_all

    def set_background_df_all_minsample(self, df):
        self.background_df_all_minsample = df
        self.background_df_all_minsample.index = self.background_df_all_minsample[self.col_background_an].tolist()

    def get_background_df_all_minsample(self):
        return self.background_df_all_minsample

    def set_background_df_int(self, df):
        self.background_df_int = df
        self.background_df_int.index = self.background_df_int[self.col_background_an].tolist()

    def get_background_df_int(self):
        return self.background_df_int

    def set_background_df_int_minsample(self, df):
        self.background_df_int_minsample = df
        self.background_df_int_minsample.index = self.background_df_int_minsample[self.col_background_an].tolist()

    def get_background_df_int_minsample(self):
        return self.background_df_int_minsample

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

    # def set_study(self, series):
    #     self.samplefreq_ser = series

    # def get_study(self):
    #     '''
    #     produce list of AccessionNumbers, sample frequency (termed 'study' in goatools)
    #     :return: ListOfString
    #     '''
    #     return sorted(self.samplefreq_ser.tolist())

    # def set_population(self, population):
    #     self.backgroundfreq_df = population

    # def get_population(self):
    #     '''
    #     produce list of AccessionNumbers, background frequency (termed 'population' in goatools)
    #     :return: ListOfString
    #     '''
    #     return sorted(self.backgroundfreq_df[self.col_background_an].tolist())

    def set_num_bins(self, num_bins):
        self.num_bins = num_bins

    def get_num_bins(self):
        return self.num_bins

    # def get_sample_an_int(self):
    #     '''
    #     produce AccessionNumbers with corresponding Intensity of sample/study
    #     :return: DataFrame
    #     '''
    #     return self.df.loc[pd.notnull(self.df[self.col_sample_an]), [self.col_sample_an, self.col_background_int]]

    def get_sample_int_an_int(self):
        '''
        produce AccessionNumbers with corresponding Intensity of sample/study
        :return: DataFrame
        '''
        return self.df.loc[pd.notnull(self.df[self.col_sample_an]), [self.col_sample_an, self.col_background_int]]


    # def get_background_an_int(self):
    #     '''
    #     produce AccessionNumbers with corresponding Intensity of background/population
    #     :return: DataFrame
    #     '''
    #     return self.df[[self.col_background_an, self.col_background_int]]

    # def get_df(self):
    #     '''
    #     return cleaned (non-redundant, aligned, no NANs) DataFrame
    #     columns: self.col_sample_an, backgrnd_an, backgrnd_int
    #     :return: DataFrame
    #     '''
    #     return self.df
    #
    # def get_df_orig(self):
    #     '''
    #     return original user input
    #     :return: DataFrame
    #     '''
    #     return self.df_orig

    # def write_goatools_input2file(self, fn_study, fn_pop):
    #     '''
    #     write input files for goatools termed study (sample-frequency) and population (background-frequency)
    #     consisting of AccessionNumbers (one per line)
    #     :param fn_study: rawString
    #     :param fn_pop: rawString
    #     :return: None
    #     '''
    #     with open(fn_study, 'w') as fh_study:
    #         for an in self.get_sample_ser_int():
    #             fh_study.write(an + '\n')
    #     with open(fn_pop, 'w') as fh_pop:
    #         for an in self.get_population():
    #             fh_pop.write(an + '\n')

    def remove_ans_without_go_or_int(self, gor):
        '''
        remove AccessionNumbers without GO-term or without intensity value
        change attributes of UserInput instance
        :param gor: goretriever instance
        :return: None
        '''
        ans_sample_filtered = []
        for an in self.get_sample_ser_int():
            goterm_list = gor.get_goterms_from_an(an)
            cond = self.backgroundfreq_df[self.col_background_an] == an
            intensity_valinlist = self.backgroundfreq_df.loc[cond, self.col_background_int].tolist()
            if goterm_list != -1 and len(intensity_valinlist) != 0:
                ans_sample_filtered += an

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
        # perc_hist = hist / float(sum(hist))
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
            ans_all_from_bin = self.get_random_an_from_bin(lower, upper, num_ans, get_all_ans=True)
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

    def get_sample_int_frset(self):
        '''
        produce frozenset of AccessionNumbers of sample frequency (study)
        :return: FrozenSet of Strings
        '''
        return frozenset(self.get_sample_ser_int())

    def get_background_int_set(self):
        '''
        produce set of AccessionNumbers of background frequency (population)
        :return: Set of Strings
        '''
        return set(self.get_background_df_int()[self.col_background_an])

    def get_background_an_set_random_sample(self):
        '''
        produce a randomly generated set of AccessionNumbers from background-frequency
        with the same intensity-distribution as sample-frequency
        :return: Set of Strings
        '''
        return set(self.get_random_background_ans())

    def get_background_all_set(self):
        '''
        produce Set of AccessionNumbers of original DataFrame, regardless of abundance data
        remove NaN
        :return: SetOfString
        '''
        return set(self.get_background_df_all()[self.col_background_an])
        # return set(self.df_orig.loc[pd.notnull(self.df_orig[self.col_background_an]), self.col_background_an].tolist())

    def get_sample_all_frset(self):
        '''
        produce Set of AccessionNumbers of original DataFrame, regardless of abundance data
        remove NaN
        :return: SetOfString
        '''
        return frozenset(self.get_sample_ser_all())
        # return set(self.df_orig.loc[pd.notnull(self.df_orig[self.col_sample_an]), self.col_sample_an].tolist())

if __name__ == "__main__":
    # pass

    ##### parse UniProt goa or goa_ref file and create input file for goatools (association-file)
    ##### with AN tab GO-IDs
    # gor = Parser_UniProt_goa_ref()
    # fn=r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/yeast/gene_association.goa_yeast'
    # fn=r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/human/gene_association.goa_ref_human'
    # gor.parse_goa_ref(fn)
    # #fn_out = r'/Users/dblyon/CloudStation/CPR/Brian_GO/goatools/data/association_goa_yeast'
    # fn_out = r'/Users/dblyon/CloudStation/CPR/Brian_GO/goatools/data/association_goa_ref_human'
    # gor.write_association2file(fn_out)

    #####
    ui = UserInput()
    ans_rand_list = ui.get_random_background_ans()
    fn_out = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/population_yeast_randomSample_test.txt'
    ui.write_ans2file(ans_rand_list, fn_out)
# %run find_enrichment_dbl.py --pval=0.5 /Users/dbl/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/study_test3.txt /Users/dbl/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/population_yeast /Users/dbl/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/association_goa_yeast --obo /Users/dbl/CloudStation/CPR/Brian_GO/go_rescources/go_obo/go-basic.obo --fn_out 'summary_test3.txt'



# class UpdateRescources(object):
#     """
#     retrieve updated resources from UniProt FTP and geneontology.org
#     ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/ --> e.g. gene_association.goa_ref_yeast
#     and e.g. http://purl.obolibrary.org/obo/go/releases/2015-04-25/go.owl
#     """
#
#     def __init__(self):
#         pass
