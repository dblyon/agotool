import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
from scipy import stats
from scipy.stats import distributions
from fisher import pvalue
import numpy as np
import pandas as pd
from decimal import Decimal
from collections import defaultdict
from multiple_testing import Bonferroni, Sidak, HolmBonferroni, BenjaminiHochberg
import ratio
from celery import Celery


@celery.task
class EnrichmentStudy_genome(object):
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
    def __init__(self, args_dict, assoc_dict, foreground, association_2_count_dict_background, background_n):
        self.args_dict = args_dict
        an_set_foreground = foreground
        # self.assoc_dict = assoc_dict
        # self.alpha = alpha
        # self.multitest_method = multitest_method
        # self.results = []
        # self.indent = indent # prepend GO-terms with a "." for each level
        # self.association_2_count_dict_background = association_2_count_dict_background
        # self.background_n = background_n

        association_2_count_dict_foreground, association_2_ANs_dict_foreground, foreground_n =  ratio.count_terms_v3(an_set_foreground, assoc_dict)
        self.df = self.run_study_genome(association_2_count_dict_foreground, association_2_count_dict_background, foreground_n, background_n)

    def get_result(self, FDR_cutoff=None, fold_enrichment_for2background=None, p_value_uncorrected=None):
        self.df = self.filter_results(self.df, FDR_cutoff, fold_enrichment_for2background, p_value_uncorrected)
        # self.df["p_value"] = self.df["p_value"].apply(lambda x: "{:.2E}".format(Decimal(x)))
        # self.df["FDR"] = self.df["FDR"].apply(lambda x: "{:.2E}".format(Decimal(x)))
        return self.df

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
                #p_val_uncorrected = stats.fisher_exact([[a, b], [c, d]], alternative='greater')[1]
                fisher_dict[(a, b, c, d)] = p_val_uncorrected
            term_list.append(association)
            p_value_list.append(p_val_uncorrected)
            foreground_ids_list.append(';'.join(self.association_2_ANs_dict_foreground[association]))
            foreground_count_list.append(foreground_count)
        df = pd.DataFrame({"term": term_list,
                          # "description": description_list,
                          "p_value": p_value_list,
                          "foreground_ids": foreground_ids_list,
                          "foreground_count": foreground_count_list})
        # df = df.sort_values("p_value", ascending=True)
        df["FDR"] = BenjaminiHochberg(df["p_value"].values, df.shape[0], array=True)
        return df

    @staticmethod
    def filter_results(df, FDR_cutoff=None, fold_enrichment_for2background=None, p_value_uncorrected=None):
        if FDR_cutoff is not None:
            df = df[df["FDR"] <= FDR_cutoff]
        if fold_enrichment_for2background is not None:
            df = df[df["fold_enrichment_for2background"] >= fold_enrichment_for2background]
        if p_value_uncorrected is not None:
            df = df[df["p_value_uncorrected"] <= p_value_uncorrected]
        return df


