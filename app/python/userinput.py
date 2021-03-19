import pandas as pd
import sys, os
import numpy as np
from collections import defaultdict
from io import StringIO # from StringIO import StringIO
from itertools import zip_longest # from itertools import izip_longest
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import tools, variables, query
import colnames as cn

if variables.PD_WARNING_OFF:
    pd.options.mode.chained_assignment = None


DEFAULT_MISSING_BIN = -1
NUM_BINS = 100

class Userinput:
    """
    expects 2 arrays,
    foregroundfreq: Pandas DataFrame 1column
    backgrndfreq: 2D array/Pandas DataFrame, with backgrnd_an, backgrnd_int

    enrichment_method is one of: "abundance_correction", "compare_samples", "compare_groups", "characterize_foreground"
     - abundance_correction: Foreground vs Background abundance corrected
     - compare_samples: Foreground vs Background (no abundance correction)
     - compare_groups: Foreground(replicates) vs Background(replicates), --> foreground_n and background_n need to be set
     - characterize_foreground: Foreground only
     #     ui = userinput.Userinput(pqo_STRING, foreground_string=fg, background_string=bg, enrichment_method=enrichment_method)
    """
    def __init__(self, pqo, fn=None, foreground_string=None, background_string=None,
            num_bins=NUM_BINS, decimal='.', args_dict=None): # foreground_n=None, background_n=None,
        self.pqo = pqo
        self.fn = fn
        self.foreground_string = foreground_string
        self.background_string = background_string
        self.decimal = decimal
        self.num_bins = num_bins
        self.col_foreground = "foreground"
        self.col_background = "background"
        self.col_intensity = "intensity"
        self.enrichment_method = args_dict["enrichment_method"]
        self.foreground_n = None
        self.background_n = None
        self.default_missing_bin = DEFAULT_MISSING_BIN
        self.args_dict = clean_args_dict(args_dict)
        self.args_dict = o_or_u_or_both_to_number(self.args_dict)
        self.check = False
        self.df_orig, self.decimal, self.check_parse = self.parse_input()
        if self.check_parse:
            try:
                self.foreground, self.background, self.check_cleanup = self.cleanupforanalysis(self.df_orig, self.col_foreground, self.col_background, self.col_intensity)
            except KeyError:
                self.args_dict["ERROR Input"] = "Please check if your column headers are correct ('foreground', 'background', and optionally 'intensity')"
                self.check_cleanup = False
        else:
            self.check_cleanup = False
        if self.check_parse and self.check_cleanup:
            self.check = True

    def parse_input(self):
        if self.enrichment_method not in variables.enrichment_methods:
            return False, False, False
        if self.enrichment_method == "genome": # check if user provided Taxid is available as Reference Proteome
            # adds error message if is_taxid_valid is False
            taxid, is_taxid_valid = query.check_if_TaxID_valid_for_GENOME_and_try_2_map_otherwise(self.args_dict["taxid"], self.pqo, self.args_dict)
            if is_taxid_valid:
                self.args_dict["taxid"] = taxid
            else:
                return False, False, False

        is_copypaste = self.check_if_copy_and_paste()
        if is_copypaste: # copy&paste field
            self.fn = StringIO()
            self.foreground_string = self.remove_header_if_present(self.foreground_string.replace("\r\n", "\n"), self.col_foreground)
            if self.enrichment_method not in {"characterize_foreground", "genome"}:
                self.background_string = self.remove_header_if_present(self.background_string.replace("\r\n", "\n"), self.col_background)
            if self.enrichment_method == "abundance_correction":
                is_abundance_correction = self.fast_check_is_abundance_correction(self.background_string)
                if is_abundance_correction:
                    header = '{}\t{}\t{}\n'.format(self.col_foreground, self.col_background, self.col_intensity)
                else:
                    return False, False, False
            elif self.enrichment_method in {"compare_samples", "compare_groups"}:
                header = '{}\t{}\n'.format(self.col_foreground, self.col_background)
            elif self.enrichment_method in {"characterize_foreground", "genome"}:
                header = '{}\n'.format(self.col_foreground)
            else:
                return False, False, False
            self.fn.write(header)
            if self.enrichment_method not in {"characterize_foreground", "genome"}:
                for a, b in zip_longest(self.foreground_string.split("\n"), self.background_string.split("\n"), fillvalue="\t"):
                    self.fn.write(a.strip() + "\t" + b.strip() + "\n")
            else:
                self.fn.write(self.foreground_string)
            self.fn.seek(0)
        try: # use file
            df_orig, decimal, check_parse = self.check_decimal(self.fn)
        except:
            print("userinput line 100 something wrong")
            return False, False, False
        return df_orig, decimal, check_parse

    def check_if_copy_and_paste(self):
        try:
            if len(self.foreground_string) > 0:  # use copy & paste field
                return True
            else:
                return False
        except TypeError: # NoneType (not None)
            return False

    def cleanupforanalysis(self, df, col_foreground, col_background, col_intensity):
        check_cleanup = True
        self.background = None

        ### remove rows consisting of only NaNs
        df = df[-df.isnull().all(axis=1)]

        ### remove NaNs from foregroundfrequency and backgroundfrequency AN-cols
        self.foreground = df.loc[pd.notnull(df[col_foreground]), [col_foreground]]

        ### check if foreground empty
        if self.foreground.shape[0] == 0:
            self.args_dict["ERROR foreground empty"] = "Please check the foreground you've provided. It seems we can't find anything to parse."
            return self.foreground, self.background, False

        if self.enrichment_method == "abundance_correction": # abundance_correction
            self.background = df[[col_background, col_intensity]]
            # set default missing value for NaNs
            self.default_missing_bin = min(self.background[col_intensity]) - 1
            self.background.loc[pd.isnull(df[col_background]), col_intensity] = self.default_missing_bin
        elif self.enrichment_method in {"compare_samples", "compare_groups"}:
            try:
                self.background = df.loc[pd.notnull(df[col_background]), [col_background]]
            except KeyError:
                self.args_dict["ERROR background empty"] = "Please check the background you've provided. It seems we can't find anything to parse."
                return self.foreground, self.background, False
        else:
            pass

        ### check if background is empty
        if self.enrichment_method not in {"characterize_foreground", "genome"}:
            if self.background.shape[0] == 0:
                self.args_dict["ERROR background empty"] = "Please check the background you've provided. It seems the Background is empty."
                return self.foreground, self.background, False

        ### remove splice variant appendix and drop duplicates
        try:
            self.foreground[col_foreground] = self.foreground[col_foreground].apply(self.remove_spliceVariant)
        except AttributeError: # np.nan can't be split
            return self.foreground, self.background, False
        if self.enrichment_method != "compare_groups":
            self.foreground.drop_duplicates(subset=col_foreground, inplace=True)
        self.foreground.index = range(0, len(self.foreground))
        if self.enrichment_method not in {"characterize_foreground", "genome"}:
            try:
                self.background[col_background] = self.background[col_background].apply(self.remove_spliceVariant)
            except AttributeError:
                return self.foreground, self.background, False
            if self.enrichment_method != "compare_groups":
                self.background = self.background.drop_duplicates(subset=col_background)

        if self.enrichment_method == "abundance_correction":
            ### map abundance from protein groups to all individual proteins, if individual protein not with standalone abundance
            self.background = self.map_proteinGroup_abundance_2_individual_protein(self.background)
            ### map abundance from background to foreground, set default missing value for NaNs
            cond = pd.isnull(self.background[col_intensity])
            self.background.loc[cond, col_intensity] = self.default_missing_bin
            an_2_intensity_dict = self.create_an_2_intensity_dict(zip(self.background[col_background], self.background[col_intensity]), self.default_missing_bin)
            self.foreground["intensity"] = self.map_intensities_2_foreground(self.foreground[col_foreground], an_2_intensity_dict)

        ### map obsolete Accessions to primary ANs, by replacing secondary ANs with primary ANs
        if variables.VERSION_ == "UniProt":
            self.Secondary_2_Primary_IDs_dict_user = query.map_secondary_2_primary_ANs(self.get_all_individual_AN(), Secondary_2_Primary_IDs_dict=None, read_from_flat_files=False) # don't read from flat file unless ABSOLUTELY necessary, VERY slow
            self.Secondary_2_Primary_IDs_dict_fg = query.map_secondary_2_primary_ANs(self.get_foreground_an_set(), Secondary_2_Primary_IDs_dict=self.Secondary_2_Primary_IDs_dict_user, read_from_flat_files=False)
            self.foreground[col_foreground] = self.foreground[col_foreground].apply(replace_secondary_and_primary_IDs, args=(self.Secondary_2_Primary_IDs_dict_fg, False))
            if self.enrichment_method not in {"characterize_foreground", "genome"}:
                self.Secondary_2_Primary_IDs_dict_bg = query.map_secondary_2_primary_ANs(self.get_background_an_set(), self.Secondary_2_Primary_IDs_dict_user)
                self.background[col_background] = self.background[col_background].apply(replace_secondary_and_primary_IDs, args=(self.Secondary_2_Primary_IDs_dict_bg, False))

        ### sort values for iter bins
        if self.enrichment_method == "abundance_correction":
            cond = self.foreground["intensity"] > self.default_missing_bin
            if sum(cond) == 0:  # render info_check_input.html
                check_cleanup = False
            self.foreground = self.foreground.sort_values(["intensity", "foreground"])
            self.background = self.background.sort_values(["intensity", "background"])
        return self.foreground, self.background, check_cleanup

    def map_proteinGroup_abundance_2_individual_protein(self, background):
        background_set = self.get_background_an_set()
        proteins_2_add, abundances_2_add = [], []
        for arr in background[[self.col_background, self.col_intensity]].values:
            protein_split = arr[0].split(";")
            if len(protein_split) > 1:
                for protein in protein_split:
                    if protein not in background_set:
                        proteins_2_add.append(protein)
                        abundances_2_add.append(arr[1])
        return background.append(pd.DataFrame.from_dict({self.col_background: proteins_2_add, self.col_intensity: abundances_2_add}), ignore_index=True)

    def translate_primary_back_to_secondary(self, df):
        if len(self.Secondary_2_Primary_IDs_dict_fg) > 0:
            df[cn.FG_IDs] = df[cn.FG_IDs].apply(replace_secondary_and_primary_IDs, args=(self.Secondary_2_Primary_IDs_dict_fg, True))
        if self.enrichment_method == "compare_samples" and len(self.Secondary_2_Primary_IDs_dict_bg) > 0:
            cond = df[cn.BG_IDs].notnull()
            df.loc[cond, cn.BG_IDs] = df.loc[cond, cn.BG_IDs].apply(replace_secondary_and_primary_IDs, args=(self.Secondary_2_Primary_IDs_dict_bg, True))
        return df

    def check_decimal(self, fn):
        """
        test if userinput uses ',' or '.' as a decimal separator
        and if 3 columns for abundance_correction exist
        return df attribute, and set check_parse to False
        :param fn: FileName
        :return: (DF_orig, Decimal(a String), check_parse(a Boolean))
        """
        decimal = "."
        check_parse = False
        df_orig = None

        try:
            df_orig = pd.read_csv(fn, sep='\t', decimal=decimal)
            check_parse = True
        except pd.errors.ParserError:
            return df_orig, decimal, check_parse

        df_orig = self.change_column_names(df_orig)
        if self.enrichment_method == "abundance_correction":
            if len({self.col_background, self.col_intensity, self.col_foreground}.intersection(set(df_orig.columns.tolist()))) == 3:
                try:
                    np.histogram(df_orig.loc[pd.notnull(df_orig[self.col_intensity]), self.col_intensity], bins=10)
                    check_parse = True
                    return df_orig, decimal, check_parse
                except TypeError:
                    pass
                try:
                    if not isinstance(fn, str):
                        fn.seek(0)
                    decimal = ","
                    df_orig = pd.read_csv(fn, sep='\t', decimal=decimal)
                    np.histogram(df_orig.loc[pd.notnull(df_orig[self.col_intensity]), self.col_intensity], bins=10)
                    check_parse = True
                    return df_orig, decimal, check_parse
                except TypeError:
                    check_parse = False
        return df_orig, decimal, check_parse

    @staticmethod
    def remove_header_if_present(input_string, foreground_or_background):
        if foreground_or_background == "foreground":
            if input_string.split("\n")[0].lower() == "foreground":
                return "\n".join(input_string.split("\n")[1:])
        else:
            if input_string.split("\n")[0].lower() == "background\tintensity":
                return "\n".join(input_string.split("\n")[1:])
        return input_string

    @staticmethod
    def fast_check_is_abundance_correction(background_string):
        try:
            string_split = background_string.split("\n", 1)[0].split("\t")
        except AttributeError:
            return False
        try:
            float(string_split[1].replace(",", "."))
        except (IndexError, ValueError) as _:
            return False
        return True

    @staticmethod
    def change_column_names(df):
        """
        :param df: Pandas DataFrame
        :return: Pandas DataFrame
        """
        df = df.rename(columns={colname: colname.lower() for colname in df.columns.tolist()})
        potential_colnames_2_rename = {"population": "background",
                                       "population_an": "background",
                                       "population_int": "background_intensity",
                                       "population_intensity": "background_intensity",
                                       "sample": "foreground",
                                       "sample_an": "foreground"}
        return df.rename(columns=potential_colnames_2_rename)

    @staticmethod
    def create_an_2_intensity_dict(list_of_tuples, default_missing_bin=DEFAULT_MISSING_BIN):
        """
        notnull values are assigned a default of -1, in order to count them in an extra bin
        e.g.
        [('P00330', '10,6690378'),
         ('P02407;P14127', '10,64061061'),
         ...]
        --> an_2_intensity_dict["P02407"] = 10,64061061
        :param list_of_tuples: ListOfTuples(ANs_string, Intensity_float)
        :param default_missing_bin: Float
        :return: Dict (key=AN, val=Float)
        """
        an_2_intensity_dict = defaultdict(lambda: default_missing_bin)
        for ans, int_ in list_of_tuples:
            for an in ans.split(";"):
                an_2_intensity_dict[an] = int_
        return an_2_intensity_dict

    @staticmethod
    def remove_spliceVariant(string_):
        """
        remove UniProt isoform appendix, but prevent removing part of ENSP
        removes appendix for splice variants from accession numbers and sorts protein groups
        :param string_: String
        :return: String
        """
        list_2_return = []
        for ele in string_.split(";"):
            if not "." in ele: # to remove isoform appendix for UniProt
                list_2_return.append(ele.split("-")[0])
            else: # for STRING identifiers / ENSPs
                list_2_return.append(ele)
        return ";".join(list_2_return)

    @staticmethod
    def map_intensities_2_foreground(foreground_series, an_2_intensity_dict):
        """
        foreground proteinGroups with abundance data
        first AN in proteinGroup used to lookup abundance values from background
        :return: Series
        """
        # foreground proteinGroups with intensities
        intensity_foreground = []
        for proteinGroup in foreground_series:
            an_first_in_proteinGroup = proteinGroup.split(";")[0]
            intensity_foreground.append(an_2_intensity_dict[an_first_in_proteinGroup])
        return pd.Series(intensity_foreground, name="intensity")

    def get_foreground_an_set(self):
        """
        get_foreground_an_set --> proteinGroups and individual proteins
        get_all_individual_foreground_ANs --> only individual proteins (proteinGroups split into individual proteins)
        get_an_redundant_foreground --> everything but NaNs, even redundant proteins
        """
        return set(self.foreground[self.col_foreground].values)

    def get_all_individual_foreground_ANs(self):
        """
        split proteinGroups into individual proteins
        """
        return tools.commaSepCol2uniqueFlatList(self.foreground, self.col_foreground, sep=";", unique=True)

    def get_all_individual_background_ANs(self):
        return tools.commaSepCol2uniqueFlatList(self.background, self.col_background, sep=";", unique=True)

    def get_background_an_set(self):
        return set(self.background[self.col_background].values)

    def get_an_redundant_foreground(self):
        # return self.foreground[self.col_foreground].tolist()
        return self.foreground[self.col_foreground].values

    def get_an_redundant_background(self):
        # return self.background[self.col_background].tolist()
        return self.background[self.col_background].values

    def get_all_individual_AN(self):
        """
        return all unique AccessionNumber provided by the user
        :return: ListOfString
        """
        # if self.enrichment_method == "rank_enrichment":
        #     ans = tools.commaSepCol2uniqueFlatList(self.population_df, self.col_population, sep=";", unique=True)
        # else:
        ans = tools.commaSepCol2uniqueFlatList(self.foreground, self.col_foreground, sep=";", unique=True)
        if self.enrichment_method not in {"characterize_foreground", "genome", "rank_enrichment"}:
            ans += tools.commaSepCol2uniqueFlatList(self.background, self.col_background, sep=";", unique=True)
        return list(set(ans))

    def get_all_unique_proteinGroups(self):
        proteinGroup_list = []
        proteinGroup_list += self.foreground[self.col_foreground].tolist()
        if self.enrichment_method not in {"characterize_foreground", "genome"}:
            proteinGroup_list += self.background[self.col_background].tolist()
        return list(set(proteinGroup_list))

    def get_foreground_n(self):
        """
        "abundance_correction", "compare_samples", "enrichment_method", "characterize_foreground"
        :return: Int
        """
        if self.enrichment_method in {"abundance_correction", "compare_samples", "characterize_foreground", "genome"}:
            try:
                return len(self.foreground)
            except AttributeError:
                return -1
        elif self.enrichment_method == "compare_groups": # redundancies within group, therefore n set by user, but this only describes replicates
            return self.args_dict["foreground_replicates"] # * len(self.get_foreground_an_set())
        else:
            raise StopIteration # DEBUG, case should not happen

    def get_background_n(self):
        """
        "abundance_correction", "compare_samples", "compare_groups", "characterize_foreground"
        :return: Int
        """
        if self.enrichment_method == "genome":
            try:
                return self.pqo.taxid_2_proteome_count[self.args_dict["taxid"]]
            except KeyError:
                self.args_dict["ERROR taxid"] = "taxid:".format(self.args_dict["taxid"])
        elif self.enrichment_method == "abundance_correction": # same as foreground
            return len(self.foreground)
        elif self.enrichment_method == "compare_samples": # simply background to compare to
            return len(self.background)
        elif self.enrichment_method == "compare_groups": # redundancies within group, therefore n set by user
            # return self.background_n *  len(self.background)
            return self.args_dict["background_replicates"] # * len(self.get_background_an_set())
        elif self.enrichment_method == "characterize_foreground": # only for foreground, not background
            return None
        else:
            raise StopIteration # DEBUG, case should not happen

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
        # take subset of foreground with proper abundance values and create bins
        cond = self.foreground[self.col_intensity] > self.default_missing_bin
        bins = pd.cut(self.foreground.loc[cond, self.col_intensity], bins=self.num_bins, retbins=True)[1]
        # missing bin was already added when cleaning up data, but cut foreground abundances into e.g. 100 bins
        # and the missing abundance proteins into a separate bin
        bins = np.insert(bins, 0, min(bins) - 1)  # bins = [DEFAULT_MISSING_BIN - 1] + list(bins)
        # cut foreground and background into bins
        groups_fg = self.foreground.groupby(pd.cut(self.foreground[self.col_intensity], bins=bins))
        groups_bg = self.background.groupby(pd.cut(self.background[self.col_intensity], bins=bins))
        for group_fg, group_bg in zip(groups_fg, groups_bg):
            proteinGroups_foreground = group_fg[1][self.col_foreground]
            proteinGroups_background = group_bg[1][self.col_background]
            len_proteinGroups_foreground = len(proteinGroups_foreground)
            len_proteinGroups_background = len(proteinGroups_background)
            try:
                correction_factor = len_proteinGroups_foreground / len_proteinGroups_background
            except ZeroDivisionError:
                # since the foreground is assumed to be a proper subset of the background, anything in the foreground must also be in the background
                # therefore any foreground protein that can't be mapped to a background-intensity will still be counted and get a default correction
                # factor of 1
                correction_factor = 1
                proteinGroups_background = proteinGroups_foreground
            correction_factor = min(correction_factor, 1)
            yield proteinGroups_background.tolist(), correction_factor

    def check_if_fg_proper_subset_of_proteome(self):
        fg_set = self.get_foreground_an_set()
        proteins_of_taxid_set = self.pqo.taxid_2_proteins_dict[self.args_dict["taxid"]]
        if len(fg_set - proteins_of_taxid_set) == 0:
            return True
        else:
            return False


class REST_API_input(Userinput):

    def __init__(self, pqo, args_dict):
            # foreground_string=None, background_string=None, background_intensity=None,
            # num_bins=NUM_BINS, enrichment_method="abundance_correction", foreground_n=None, background_n=None):
        # super().__init__(pqo, args_dict=args_dict)
        self.pqo = pqo
        self.df_orig = pd.DataFrame()
        self.args_dict = args_dict
        self.foreground_string = args_dict["foreground"]
        self.background_string = args_dict["background"]
        self.background_intensity = args_dict["background_intensity"]
        try:
            background_intensity = args_dict["intensity"]
            if background_intensity is not None:
                self.background_intensity = background_intensity
        except KeyError:
            pass # in case "intensity" instead of "background_intensity" is being used
        try:
            self.population_string = args_dict["population"] # ? deprecated ?
        except KeyError:
            self.population_string = None
        try:
            self.abundance_ratio = args_dict["abundance_ratio"] # deprecated
        except KeyError:
            self.abundance_ratio = None
        self.num_bins = args_dict["num_bins"]
        self.enrichment_method = args_dict["enrichment_method"]
        self.foreground_n = args_dict["foreground_n"]
        self.background_n = args_dict["background_n"]
        self.col_foreground = "foreground"
        self.col_background = "background"
        self.col_intensity = "intensity"
        self.col_population = "population"
        self.col_abundance_ratio = "abundance_ratio"
        self.check = False
        self.check_cleanup = False
        self.args_dict = o_or_u_or_both_to_number(self.args_dict)
        self.df_orig, self.decimal, self.check_parse = self.parse_input()
        if self.check_parse:
            self.foreground, self.background, self.check_cleanup = self.cleanupforanalysis(self.df_orig, self.col_foreground, self.col_background, self.col_intensity)
        if self.check_parse and self.check_cleanup:
            self.check = True

    def parse_input(self):
        check_parse = False
        decimal = "."
        df_orig = pd.DataFrame()

        if self.enrichment_method not in variables.enrichment_methods:
            return False, False, False
        if self.enrichment_method == "genome": # check if user provided Taxid is available as Reference Proteome
            # adds error message if is_taxid_valid is False
            taxid, is_taxid_valid = query.check_if_TaxID_valid_for_GENOME_and_try_2_map_otherwise(self.args_dict["taxid"], self.pqo, self.args_dict)
            if is_taxid_valid:
                self.args_dict["taxid"] = taxid
            else:
                return False, False, False


        if self.enrichment_method != "genome": # ignore background if "genome"
            if self.background_string is not None:
                replaced = pd.Series(self._replace_and_split(self.background_string))
                if replaced is not None:
                    df_orig[self.col_background] = replaced
                else:
                    return df_orig, decimal, check_parse

        if self.enrichment_method == "abundance_correction":
            try:
                if "." in self.background_intensity:
                    pass
                elif "," in self.background_intensity:
                    decimal = ","
                    # replace comma with dot, work with consistently the same DF, but report the results to the user using the their settings
                    self.background_intensity = self.background_intensity.replace(",", ".")
            except TypeError: # self.background_intensity is None
                self.args_dict["ERROR_abundance_correction"] = "ERROR: enrichment_method 'abundance_correction' selected but no 'background_intensity' provided"
                return df_orig, decimal, check_parse
            else: # other checks could be done, but is this really necessary?
                pass
            try:
                replaced = pd.Series(self._replace_and_split(self.background_intensity), dtype=float)
                if replaced is not None:
                    df_orig[self.col_intensity] = replaced
                else:
                    return df_orig, decimal, check_parse
            except ValueError:
                return df_orig, decimal, check_parse
        # elif self.enrichment_method == "rank_enrichment":
        #     try:
        #         if "." in self.abundance_ratio:
        #             pass
        #         elif "," in self.abundance_ratio:
        #             decimal = ","
        #             # replace comma with dot, work with consistently the same DF, but report the results to the user using the their settings
        #             self.abundance_ratio = self.abundance_ratio.replace(",", ".")
        #     except TypeError: # self.background_intensity is None
        #         self.args_dict["ERROR_rank_enrichment"] = "ERROR: 'rank_enrichment' selected but no 'abundance_ratio' provided"
        #         return df_orig, decimal, check_parse
        #     try:
        #         replaced = pd.Series(self._replace_and_split(self.abundance_ratio), dtype=float)
        #         if replaced is not None:
        #             df_orig[self.col_abundance_ratio] = replaced
        #         else:
        #             return df_orig, decimal, check_parse
        #     except ValueError:
        #         return df_orig, decimal, check_parse
        #
        #     # statement need to be here rather than at top of function in order to not cut off the Series at the length of the existing Series in the DF
        #     replaced = pd.Series(self._replace_and_split(self.population_string))
        #     if replaced is not None:
        #         df_orig[self.col_population] = replaced
        #     else:
        #         return df_orig, decimal, check_parse
        #     check_parse = True
        #     return df_orig, decimal, check_parse

        else:
            df_orig[self.col_intensity] = DEFAULT_MISSING_BIN

        # statement need to be here rather than at top of function in order to not cut off the Series at the length of the existing Series in the DF
        replaced = pd.Series(self._replace_and_split(self.foreground_string))
        if replaced is not None:
            df_orig[self.col_foreground] = replaced
        else:
            return df_orig, decimal, check_parse
        check_parse = True
        return df_orig, decimal, check_parse

    @staticmethod
    def _replace_and_split(string_):
        try:
            return string_.replace("\r\n", "%0d").replace("\r", "%0d").replace("\n", "%0d").split("%0d")
        except AttributeError: # None
            return None

def replace_secondary_and_primary_IDs(ans_string, secondary_2_primary_dict, invert_dict=False):
    if invert_dict:
        dict_2_use = {v: k for k, v in secondary_2_primary_dict.items()}
    else:
        dict_2_use = secondary_2_primary_dict
    ids_2_return = []
    # throws error is None --> check here or at calling function?
    for id_ in ans_string.split(";"):  # if proteinGroup
        if id_ in dict_2_use:
            ids_2_return.append(dict_2_use[id_])
        else:
            ids_2_return.append(id_)
    return ";".join(ids_2_return)

def stringify_for_Userinput(list_of_proteins, list_of_abundances=None):
    if list_of_abundances is None:
        if list_of_proteins is None:
            return ""
        else:
            return "\n".join(list_of_proteins)
    else:
        string_2_return = ""
        for an, inte in zip(list_of_proteins, list_of_abundances):
            string_2_return += an + "\t" + str(inte) + "\n"
        return string_2_return.strip()

def o_or_u_or_both_to_number(args_dict):
    if args_dict["o_or_u_or_both"] == "overrepresented":
        o_or_u_or_both = 1
    elif args_dict["o_or_u_or_both"] == "both":
        o_or_u_or_both = 0
    elif args_dict["o_or_u_or_both"] == "underrepresented":
        o_or_u_or_both = 2
    else:
        args_dict["ERROR o_or_u_or_both"] = "You've provided '{}' which is not a valid option. Please use 'overrepreseted', 'underrepresented', or 'both'.".format(args_dict["o_or_u_or_both"])
        o_or_u_or_both = -1
    args_dict["o_or_u_or_both_encoding"] = o_or_u_or_both
    return args_dict

def clean_args_dict(args_dict):
    dict_2_return = defaultdict(lambda: None)
    for key, val in args_dict.items():
        if type(val) == str:
            dict_2_return[key] = string_2_properType(val)
        else:
            dict_2_return[key] = val
    dict_2_return["FDR_cutoff"], is_valid = zero_one_or_None_to_1(dict_2_return["FDR_cutoff"])
    if not is_valid:
        dict_2_return["ERROR FDR_cutoff"] = "We can't interpret the FDR_cutoff {} you've provided, please check your input.".format(dict_2_return["FDR_cutoff"])
    dict_2_return["p_value_cutoff"], is_valid = zero_one_or_None_to_1(dict_2_return["p_value_cutoff"])
    if not is_valid:
        dict_2_return["ERROR p_value_cutoff"] = "We can't interpret the p_value_cutoff {} you've provided, please check your input.".format(dict_2_return["p_value_cutoff"])
    if args_dict["filter_PMID_top_n"] == 0:
        dict_2_return["filter_PMID_top_n"] = None
    if args_dict["go_slim_subset"] == "basic":
        dict_2_return["go_slim_subset"] = None
    return dict_2_return

def zero_one_or_None_to_1(FDR_cutoff):
    if FDR_cutoff is None:
        return 1, True
    else:
        if isinstance(FDR_cutoff, str):
            try:
                FDR_cutoff = float(FDR_cutoff)
            except:
                pass
    if FDR_cutoff == 0 or FDR_cutoff >= 1:
        return 1, True
    else:
        return FDR_cutoff, True

def string_2_properType(string_):
    string_ = string_.strip().lower()
    if string_.lower() == "true" or string_ == "1":
        return True
    elif string_.lower() == "false" or string_ == "0":
        return False
    elif string_.lower() == "none":
        return None
    else:
        return string_

if __name__ == "__main__":
    # # fn = r'/Users/dblyon/modules/cpr/metaprot/Perio_vs_CH_Bacteria.txt'
    # # fn = r'/Users/dblyon/modules/cpr/metaprot/CompareGroups_test.txt'
    # # fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_proteinGroups.txt'
    # # foreground_n = 10.0
    # # background_n = 20.0
    # # proteinGroup = True
    # # ui = UserInput_compare_groups(proteinGroup, fn, foreground_n, background_n)
    # # foreground_an = ui.get_foreground_an()
    # # # backgound_an = ui.get_background_an()
    # # all_unique_an = ui.get_all_unique_ans()
    # # # print len(foreground_an), len(backgound_an), len(all_unique_an)
    # # print len(foreground_an), len(all_unique_an)
    # fn = r"/Users/dblyon/modules/cpr/agotool/static/data/exampledata/exampledata_yeast_Foreground_Background.txt"
    # fn = r"/Users/dblyon/modules/cpr/agotool/static/data/exampledata/exampledata_yeast_Intensity_Sample_Population.txt"
    # fn = r"/Users/dblyon/modules/cpr/agotool/static/data/exampledata/DEBUG.txt"
    # fn = r"/Users/dblyon/Downloads/Data for agotool 2017-01-30.txt"
    # fn = r"/Users/dblyon/Downloads/1A_Data_for_web_tool_test_AbundaceCorrection_fUbi.txt"
    # # import db_config
    # # ECHO = False
    # # TESTING = False
    # # DO_LOGGING = False
    # # connection = db_config.Connect(echo=ECHO, testing=TESTING, do_logging=DO_LOGGING)
    #
    # import io
    # fn = io.open(fn, mode='r')
    # ui = Userinput(fn=fn, foreground_string=None,
    #     background_string=None, col_foreground='foreground',
    #     col_background='background', col_intensity='intensity',
    #     num_bins=100, decimal='.', enrichment_method="abundance_correction")#, connection=connection)
    # # print(ui.iter_bins().next())

    ## testing UserInput
    # example1: foreground is proper subset of background, everything has an abundance value
    # df_test = pd.DataFrame()
    # df_test["background"] = pd.Series(['Q9UHI6', 'Q13075', 'A6NDB9', 'A6NFR9', 'O95359', 'D6RGG6', 'Q9BRQ0', 'P09629', 'Q9Y6G5', 'Q96KG9', 'Q8WXE0', 'Q6VB85', 'P13747', 'Q9UQ03', 'Q8N8S7'])
    # df_test["background_intensity"] = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10] + [1] * 5, dtype=float)
    # df_test["foreground"] = pd.Series(['Q9UHI6', 'Q13075', 'A6NDB9', 'A6NFR9', 'O95359', 'D6RGG6', 'Q9BRQ0', 'P09629', 'Q9Y6G5', 'Q96KG9'])
    # df_test = df_test.sort_values(["intensity", "background"])
    #
    # in_ = "%0d".join([str(ele) for ele in df_test.loc[df_test.intensity.notnull(), "intensity"].tolist()])
    # fg = "%0d".join(df_test.loc[df_test.foreground.notnull(), "foreground"].tolist())
    # bg = "%0d".join(df_test.loc[df_test.background.notnull(), "background"].tolist())
    # pqo = None
    # pqo = query.PersistentQueryObject()
    # ui = REST_API_input(pqo=pqo, foreground_string=fg, background_string=bg, background_intensity=in_, num_bins=10)

    # every AN from foreground present, nothing is downweighed, since same abundance
    # counter = 1
    # for ans, weight_fac in ui.iter_bins():
    #     print(counter, ans, weight_fac)
    #     counter += 1

    # foreground_almost_empty = pd.Series(name="foreground", data={0: np.nan, 1: "Q9UHI6", 2: np.nan})
    # background_no_intensity = pd.DataFrame({'background': {0: 'P13747', 1: 'Q6VB85', 2: 'Q8N8S7', 3: 'Q8WXE0', 4: 'Q9UHI6', 5: 'Q9UQ03', 6: 'Q13075', 7: 'A6NDB9', 8: 'A6NFR9', 9: 'O95359', 10: 'D6RGG6', 11: 'Q9BRQ0', 12: 'P09629', 13: 'Q9Y6G5', 14: 'Q96KG9'}, 'intensity': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan, 5: np.nan, 6: np.nan, 7: np.nan, 8: np.nan, 9: np.nan, 10: np.nan, 11: np.nan, 12: np.nan, 13: np.nan, 14: np.nan}})
    # "compare_samples"
    # contiguous = False
    # foreground_n = 100
    # foreground_input = sorted(get_random_human_ENSP(foreground_n, joined_for_web=False, contiguous=contiguous))
    # enrichment_method = "abundance_correction"  # "characterize_foreground" "abundance_correction" "compare_samples" "genome" "compare_groups"
    # fn_userinput = r"/Users/dblyon/modules/cpr/agotool/data/exampledata/Example_1.1_Yeast_acetylation_without_abundance.txt"
        #Example_3_Niu_PlasmaCirrhosis_compare_samples.txt" #compare_groups_v2.txt" # ExampleData_for_testing.txt" # Example_Yeast_acetylation_abundance_correction.txt
    # fn_userinput = r"/Users/dblyon/Downloads/ExampleData.txt"
    # from_file = False  # read user input from file
    # args_dict = {}
    # args_dict["enrichment_method"] = enrichment_method
    # args_dict["taxid"] = 9606
    # args_dict["FDR_cutoff"] = 0.05
    # args_dict["p_value_cutoff"] = 0.01
    # args_dict["limit_2_entity_type"] = None  # "-20;-25;-26" #"-20;-25;-21" # "-20;-21;-22;-23;-25;-26" # None #"-21;-22;-23"
    # args_dict["filter_PMID_top_n"] = 100
    # args_dict["filter_foreground_count_one"] = True
    # args_dict["filter_parents"] = True
    # args_dict["go_slim_subset"] = None  # "generic"
    # args_dict["o_or_u_or_both"] = "overrepresented"  # "both" "underrepresented"
    # args_dict["multiple_testing_per_etype"] = True
    # args_dict["privileged"] = True
    # args_dict["score_cutoff"] = 0
    # args_dict["foreground_replicates"] = 10
    # args_dict["background_replicates"] = 10
    # taxid = args_dict["taxid"]
    # # pqo = query.PersistentQueryObject_STRING(low_memory=True)
    # pqo = None
    # # background_input = query.get_proteins_of_taxid(taxid, read_from_flat_files=True)
    # # ui = Userinput(pqo, fn=None, foreground_string=stringify_for_Userinput(foreground_input), background_string=stringify_for_Userinput(background_input), args_dict=args_dict)
    # # ui = Userinput(pqo, fn_userinput, args_dict=args_dict)
    # # import pdb
    # # pdb.set_trace()
    #
    # # import requests
    # # from io import StringIO
    # # import pandas as pd
    # #
    # # # url_ = r"https://agotool.org/api"
    # # # url_ = r"http://localhost:5911/api"
    # # # fg = '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263%0d511145.b1264%0d511145.b1812%0d511145.b2551%0d511145.b3117%0d511145.b3772%0d511145.b1015%0d511145.b2585'
    # # # result = requests.post(url_, params={"output_format": "tsv", "enrichment_method": "genome",
    # # #                                      "taxid": "511145", "caller_identity": "11_0", "STRING_beta": True, 'FDR_cutoff': '0.05'},
    # # #                        data={'foreground': '511145.b1261%0d511145.b1260%0d511145.b1263%0d511145.b1262', 'background': '511145.b1260%0d511145.b1263%0d511145.b1262%0d511145.b1812%0d511145.b1261'})
    # # params = {'taxid': '511145', 'output_format': 'json', 'enrichment_method': 'compare_samples', 'FDR_cutoff': '0.05', 'caller_identity': '11_0', 'STRING_beta': True}
    # # for key, val in params.items():
    # #     args_dict[key] = val
    # # data = {'foreground': "511145.b1261%0d511145.b1260%0d511145.b1263", 'background': '511145.b1260%0d511145.b1263%0d511145.b1262%0d511145.b1812%0d511145.b1261'}
    # # ui = Userinput(pqo, fn=None, foreground_string=data["foreground"], background_string=data["background"], args_dict=args_dict)
    # # import pdb
    # # pdb.set_trace()
    # # result = requests.post(url_, params, data)
    # # result.text
    #
    # ###
    # # params = {'taxid': 559292, 'output_format': 'tsv', 'enrichment_method': 'genome', 'FDR_cutoff': '0.05', 'caller_identity': '11_0', 'STRING_beta': True}
    # # for key, val in params.items():
    # #     args_dict[key] = val
    # # fn_userinput = r"/Users/dblyon/modules/cpr/agotool/data/exampledata/Example_1_Yeast_acetylation_foreground_only.txt"
    # # class Y:
    # #     def __init__(self):
    # #         pass
    # # pqo = Y()
    # # pqo.taxid_2_proteome_count = {559292: 1234}
    # # ui = Userinput(pqo, fn=fn_userinput, foreground_string=None, background_string=None, args_dict=args_dict)
    # # import pdb
    # # pdb.set_trace()
    # fn_userinput = r"/Users/dblyon/Downloads/agotoolquestions/ClpP2up_KEimputed_aGOtool.txt"
    # ui = Userinput(pqo, fn=fn_userinput, foreground_string=None, background_string=None, args_dict=args_dict)
    # # print(ui.background["intensity"].min())
    # # print(ui.foreground["intensity"].min())
    # # print(ui.df_orig.head())
    # for bin in ui.iter_bins():
    #     print(bin)
    pqo = None
    args_dict_temp = {'FDR_cutoff': None, 'alpha': 0.05, 'foreground': '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263%0d511145.b1264%0d511145.b1812%0d511145.b2551%0d511145.b3117%0dnan%0dnan%0dnan%0dnan', 'background': '511145.b1260%0d511145.b1261%0d511145.b1262%0d511145.b1263%0d511145.b1264%0d511145.b1812%0d511145.b2551%0d511145.b3117%0d511145.b3360%0d511145.b3772%0d511145.b4388%0dnan', 'background_intensity': None, 'population': None, 'abundance_ratio': None, 'foreground_n': None, 'background_n': None, 'caller_identity': None, 'enrichment_method': 'abundance_correction', 'fold_enrichment_for2background': 0, 'go_slim_or_basic': 'basic', 'identifiers': None, 'indent': 'True', 'limit_2_entity_type': None, 'multitest_method': 'benjamini_hochberg', 'num_bins': 100, 'o_or_u_or_both': 'overrepresented', 'output_format': 'tsv', 'p_value_uncorrected': 0, 'organism': None, 'species': None, 'taxid': None, 'filter_PMID_top_n': 100, 'filter_foreground_count_one': False, 'filter_parents': False,
     'go_slim_subset': None, 'intensity': '1.0%0d2.0%0d3.0%0d4.0%0d5.0%0d6.0%0d7.0%0d8.0%0d9.0%0d10.0%0d11.0%0dnan', 'ERROR_abundance_correction': "ERROR: enrichment_method 'abundance_correction' selected but no 'background_intensity' provided"}
    ui = REST_API_input(pqo, args_dict=args_dict_temp)
    print(ui.df_orig.head(3))
    print(ui.check_parse, ui.check_cleanup)




