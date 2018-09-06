import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
from scipy import stats
from fisher import pvalue
import numpy as np
import pandas as pd
from decimal import Decimal

from multiple_testing import Bonferroni, Sidak, HolmBonferroni, BenjaminiHochberg
import ratio


class EnrichmentStudy(object):
    """
    ToDo: change examples on website
    add REST API examples
    unify output of genome method vs compare samples
    Runs Fisher's exact test, as well as multiple corrections
    abundance_correction: Foreground vs Background abundance corrected
    genome: Foreground vs Proteome (no abundance correction)
    compare_samples: Foreground vs Background (no abundance correction)
    compare_groups: Foreground(replicates) vs Background(replicates), --> foreground_n and background_n need to be set
    characterize_foreground: Foreground only
    """
    def __init__(self, pqo, args_dict, ui, assoc_dict, obo_dag, enrichment_method="genome", entity_type="-51",
            o_or_u_or_both="overrepresented",
            multitest_method="benjamini_hochberg", alpha=0.05,
            association_2_count_dict_background=None, background_n=None,
            indent=False):
        self.pqo = pqo
        self.args_dict = args_dict
        self.ui = ui
        self.method = enrichment_method
        self.assoc_dict = assoc_dict
        self.obo_dag = obo_dag
        self.alpha = alpha
        self.multitest_method = multitest_method
        self.results = []
        self.o_or_u_or_both = o_or_u_or_both
        self.entity_type = entity_type
        self.indent = indent # prepend GO-terms with a "." for each level

        ### prepare run
        self.an_set_foreground = self.ui.get_foreground_an_set()
        self.association_2_count_dict_foreground, self.association_2_ANs_dict_foreground, self.foreground_n = ratio.count_terms_v3(
            self.an_set_foreground, self.assoc_dict)
        if self.method == "abundance_correction":
            self.run_abundance_correction()
        elif self.method == "genome":
            self.run_genome(association_2_count_dict_background, background_n)
        elif self.method == "compare_samples":
            self.run_compare_samples()
        elif self.method == "compare_groups":
            self.run_compare_groups()
        elif self.method == "characterize_foreground":
            self.run_characterize_foreground()
        else:
            raise NotImplementedError

    def run_abundance_correction(self):
        self.background_n = self.foreground_n
        self.association_2_count_dict_background, self.association_2_ANs_dict_background = ratio.count_terms_abundance_corrected_manager(self.ui, self.assoc_dict, self.obo_dag, self.entity_type)
        self.df = self.run_study(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)

    def run_genome(self, association_2_count_dict_background, background_n):
        self.association_2_count_dict_background, self.background_n = association_2_count_dict_background, background_n
        self.df = self.run_study_genome(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)

    def get_result(self, FDR_cutoff=None, fold_enrichment_for2background=None, p_value_uncorrected=None):
        self.df = self.filter_results(self.df, FDR_cutoff, fold_enrichment_for2background, p_value_uncorrected)
        if self.method != "characterize_foreground": # since no p-values available
            self.df["p_value"] = self.df["p_value"].apply(lambda x: "{:.2E}".format(Decimal(x)))
            self.df["FDR"] = self.df["FDR"].apply(lambda x: "{:.2E}".format(Decimal(x)))
        return self.df

    def run_compare_samples(self):
        self.an_set_background = self.ui.get_background_an_set()
        self.association_2_count_dict_background, self.association_2_ANs_dict_background, self.background_n = ratio.count_terms_manager(self.an_set_background, self.assoc_dict, entity_type=self.entity_type)
        self.df = self.run_study(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)

    def run_compare_groups(self):
        self.foreground_n = self.ui.get_foreground_n()
        self.background_n = self.ui.get_background_n()
        self.an_redundant_foreground = self.ui.get_an_redundant_foreground()
        self.an_redundant_background = self.ui.get_an_redundant_background()
        self.association_2_count_dict_foreground, self.association_2_ANs_dict_foreground, unused_an_count = ratio.count_terms_manager(self.an_redundant_foreground, self.assoc_dict, self.obo_dag, self.entity_type)
        self.association_2_count_dict_background, self.association_2_ANs_dict_background, unused_an_count = ratio.count_terms_manager(self.an_redundant_background, self.assoc_dict, self.obo_dag, self.entity_type)
        self.df = self.run_study(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)

    def run_characterize_foreground(self):
        self.an_redundant_foreground = self.ui.get_an_redundant_foreground()
        self.association_2_count_dict_foreground, self.association_2_ANs_dict_foreground, unused_an_count = ratio.count_terms_manager(self.an_redundant_foreground, self.assoc_dict, self.obo_dag, self.entity_type)
        self.df = self.characterize_foreground(self.association_2_count_dict_foreground, self.foreground_n)

    def characterize_foreground(self, association_2_count_dict_foreground, foreground_n):
        term_list, description_list, foreground_ids_list, foreground_count_list, ratio_in_foreground_list = [], [], [], [], []
        for association, foreground_count in association_2_count_dict_foreground.items():
            term_list.append(association)
            description_list.append(self.obo_dag[association].name)
            ratio_in_foreground_list.append(self.calc_ratio(foreground_count, foreground_n))
            foreground_ids_list.append(';'.join(self.association_2_ANs_dict_foreground[association]))
            foreground_count_list.append(foreground_count)
        df = pd.DataFrame({"term": term_list, "description": description_list, "ratio_in_foreground": ratio_in_foreground_list, "foreground_ids": foreground_ids_list, "foreground_count": foreground_count_list})
        return df

    def run_study(self, association_2_count_dict_foreground, association_2_count_dict_background, foreground_n, background_n):
        """
        ###################################################
        # contingency table general variable names:
        #     foreground       |     background     |
        # -------------------------------------------------
        # +   a = foregr_count |   c = backgr_count |   r1
        # -------------------------------------------------
        # -     b              |       d            |   r2
        # -------------------------------------------------
        #     foregr_n         |     backgr_n       |    n

        # fisher.pvalue_population() expects:
        #  (a, col_1, r1, n)
        #  (foreground_count, foreground_n, foreground_count + background_count, foreground_n + background_n)

        # equivalent results using the following methods:
        # fisher.pvalue_population(a, col_1, r1, n)
        # fisher.pvalue(a, b, c, d)
        # scipy.stats.fisher_exact([[a, b], [c, d]])
        ###################################################
        :return: results-object
        """
        fisher_dict = {}
        term_list, description_list, level_list, p_value_list, foreground_ids_list = [], [], [], [], []
        foreground_count_list, background_count_list, foreground_n_list, background_n_list = [], [], [], []
        percent_associated_foreground, percent_associated_background, foreground_ids_list, background_ids_list= [], [], [], []
        if self.method == "compare_groups":
            foreground_n_2_multiply = foreground_n
            background_n_2_multiply = background_n
        for association, foreground_count in association_2_count_dict_foreground.items():
            background_count = association_2_count_dict_background[association]
            if self.method == "compare_groups":
                a = foreground_count # number of redundant proteins associated with GO-term
                foreground_n = len(self.association_2_ANs_dict_foreground[association]) * foreground_n_2_multiply # maximum number of proteins associated with GO-term
                try:
                    background_n = len(self.association_2_ANs_dict_background[association]) * background_n_2_multiply  # maximum number of proteins associated with GO-term
                except KeyError: # association only in foreground but not in background
                    pass
                b = foreground_n - foreground_count # maximum number of proteins associated with GO-term minus a
                c = background_count
                d = background_n - background_count
            else:
                a = foreground_count # number of proteins associated with given GO-term
                b = foreground_n - foreground_count # number of proteins not associated with GO-term
                c = background_count
                d = background_n - background_count
                if d < 0:
                    d = 0
            if self.o_or_u_or_both == 'overrepresented':
                ### enriched or overrepresented --> right_tail or greater (but foreground and background are switched)
                try:
                    p_val_uncorrected = fisher_dict[(a, b, c, d)]
                except KeyError:
                    ### p_val_uncorrected = stats.fisher_exact([[a, b], [c, d]], alternative='less')[1]
                    if a == c and b == d:
                        p_val_uncorrected = 1
                    else:
                        p_val_uncorrected = pvalue(a, b, c, d).right_tail
                    fisher_dict[(a, b, c, d)] = p_val_uncorrected
            elif self.o_or_u_or_both == 'both':
                ### both --> two_tail or two-sided
                try:
                    p_val_uncorrected = fisher_dict[(a, b, c, d)]
                except KeyError:
                    p_val_uncorrected = stats.fisher_exact([[a, b], [c, d]], alternative='two-sided')[1]
                    ### fisher_dict[(a, b, c, d)] = p_val_uncorrected # don't use this version (but the scipy version above) since accuracy drops too much
            elif self.o_or_u_or_both == 'underrepresented':
                ### purified or underrepresented --> left_tail or less
                try:
                    p_val_uncorrected = fisher_dict[(a, b, c, d)]
                except KeyError: # why not tuple instead of list #!!!
                    # p_val_uncorrected = stats.fisher_exact([[a, b], [c, d]], alternative='greater')[1]
                    if a == c and b == d:
                        p_val_uncorrected = 1
                    else:
                        p_val_uncorrected = pvalue(a, b, c, d).left_tail
                    fisher_dict[(a, b, c, d)] = p_val_uncorrected
            else:
                raise StopIteration
            term_list.append(association)
            # name_list.append(self.pqo.function_an_2_name_dict[association])
            # description_list.append(self.obo_dag[association].name)
            description_list.append(self.pqo.function_an_2_description_dict[association])
            level_list.append(self.obo_dag[association].level)
            p_value_list.append(p_val_uncorrected)
            percent_associated_foreground.append("{0:.2f}".format(round(self.calc_ratio(foreground_count, foreground_n), 2)))
            percent_associated_background.append("{0:.2f}".format(round(self.calc_ratio(background_count, background_n), 2)))
            try:
                foreground_ids_list.append(';'.join(self.association_2_ANs_dict_foreground[association]))
            except KeyError:
                foreground_ids_list.append('NaN')
            try:
                background_ids_list.append(';'.join(self.association_2_ANs_dict_background[association]))
            except KeyError:
                background_ids_list.append('NaN')
            foreground_count_list.append(foreground_count)
            background_count_list.append(background_count)
            foreground_n_list.append(foreground_n)
            background_n_list.append(background_n)

        df = pd.DataFrame({"term": term_list,
                           # "name": name_list,
                           "description": description_list,
                           "level": level_list,
                           "p_value": p_value_list,
                           "percent_associated_foreground": percent_associated_foreground,
                           "percent_associated_background": percent_associated_background,
                           "foreground_ids": foreground_ids_list,
                           "background_ids": background_ids_list,
                           "foreground_count": foreground_count_list,
                           "background_count": background_count_list,
                           "foreground_n": foreground_n_list,
                           "background_n": background_n_list})
        if self.method in {"abundance_correction", "genome"}:
            df = df.drop("foreground_ids", axis=1)
        if self.indent:
           df["term"] = df["background_count"].apply(lambda x: int(x) * ".") + df["id"]
        df = df.sort_values("p_value", ascending=True)
        corrected_pvals = self.calc_multiple_corrections_v2(df["p_value"].values, method_name=self.multitest_method, alpha=self.alpha, array=True)
        df["FDR"] = corrected_pvals
        return df

    @staticmethod
    def calc_ratio(zaehler, nenner):
        try:
            fold_en = zaehler/nenner
        except ZeroDivisionError:
            fold_en = np.inf
        return fold_en

    def run_study_genome(self, association_2_count_dict_foreground, association_2_count_dict_background, foreground_n, background_n):
        """
        ###################################################
        # contingency table general variable names:
        #     foreground       |     background     |
        # -------------------------------------------------
        # +   a = foregr_count |   c = backgr_count |   r1
        # -------------------------------------------------
        # -     b              |       d            |   r2
        # -------------------------------------------------
        #     foregr_n         |     backgr_n       |    n
        """
        fisher_dict = {}
        term_list, description_list, p_value_list, foreground_ids_list, foreground_count_list = [], [], [], [], []
        for association, foreground_count in association_2_count_dict_foreground.items():
            try:
                background_count = association_2_count_dict_background[association]
            except KeyError:
                self.args_dict["ERROR_association_2_count"] = "ERROR retrieving counts for association {} please contact david.lyon@uzh.ch with this error message".format(association)
                return None
                # background_count = np.nan
            a = foreground_count # number of proteins associated with given GO-term
            b = foreground_n - foreground_count # number of proteins not associated with GO-term
            c = background_count
            d = background_n - background_count
            if d < 0:
                d = 0
            ### enriched or overrepresented --> right_tail or greater (but foreground and background are switched)
            try:
                p_val_uncorrected = fisher_dict[(a, b, c, d)]
            except KeyError:
                p_val_uncorrected = pvalue(a, b, c, d).right_tail
                fisher_dict[(a, b, c, d)] = p_val_uncorrected
            term_list.append(association)
            # name_list.append(self.pqo.function_an_2_name_dict[association])
            #description_list.append(self.obo_dag[association].name)
            description_list.append(self.pqo.function_an_2_description_dict[association])
            p_value_list.append(p_val_uncorrected)
            foreground_ids_list.append(';'.join(self.association_2_ANs_dict_foreground[association]))
            foreground_count_list.append(foreground_count)
        df = pd.DataFrame({"term": term_list,
                          # "name": name_list,
                          "description": description_list,
                          # "definition": description_list,
                          "p_value": p_value_list,
                          "foreground_ids": foreground_ids_list,
                          "foreground_count": foreground_count_list})
        df = df.sort_values("p_value", ascending=True)
        df["FDR"] = BenjaminiHochberg(df["p_value"].values, df.shape[0], array=True)
        return df

    def get_ans_from_association(self, association, foreground):
        if foreground:
            if association in self.association_2_ANs_dict_foreground:
                return sorted(self.association_2_ANs_dict_foreground[association])
            else:
                return ''
        else:
            if association in self.association_2_ANs_dict_background:
                return sorted(self.association_2_ANs_dict_background[association])
            else:
                return ''

    @staticmethod
    def calc_multiple_corrections_v2(pvals_array, method_name="benjamini_hochberg", alpha=0.05, array=True):
        if method_name == 'benjamini_hochberg':
            corrected_pvals = BenjaminiHochberg(pvals_array, pvals_array.size)
        elif method_name == "bonferroni":
            corrected_pvals = Bonferroni(pvals_array, alpha, array=array).corrected_pvals
        elif method_name == "sidak":
            corrected_pvals = Sidak(pvals_array, alpha, array=array).corrected_pvals
        elif method_name == "holm":
            corrected_pvals = HolmBonferroni(pvals_array, alpha, array=array).corrected_pvals
        else:
            print("method_name: {}".format(method_name))
            raise NotImplementedError
        return corrected_pvals
    @staticmethod
    def filter_results(df, FDR_cutoff=None, fold_enrichment_for2background=None, p_value_uncorrected=None):
        if FDR_cutoff is not None:
            df = df[df["FDR"] <= FDR_cutoff]
        if fold_enrichment_for2background is not None:
            df = df[df["fold_enrichment_for2background"] >= fold_enrichment_for2background]
        if p_value_uncorrected is not None:
            df = df[df["p_value_uncorrected"] <= p_value_uncorrected]
        return df

    def update_results(self, method_name, corrected_pvals):
        if corrected_pvals is None:
            return
        for rec, val in zip(self.results, corrected_pvals):
            rec.__setattr__("p_" + method_name, val)

