import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
from scipy import stats
from scipy.stats import distributions
from fisher import pvalue
import numpy as np
import pandas as pd
from decimal import Decimal
import multiple_testing
from multiple_testing import Bonferroni, Sidak, HolmBonferroni, BenjaminiHochberg, BH_fast_v3
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
    def __init__(self, pqo, args_dict, ui, assoc_dict, enrichment_method="genome", entity_type="-51",
            o_or_u_or_both="overrepresented",
            multitest_method="benjamini_hochberg", alpha=0.05,
            association_2_count_dict_background=None, background_n=None,
            indent=False):
        self.pqo = pqo
        self.args_dict = args_dict
        self.ui = ui
        self.method = enrichment_method
        self.assoc_dict = assoc_dict
        # self.obo_dag = obo_dag
        self.alpha = alpha
        self.multitest_method = multitest_method
        self.results = []
        self.o_or_u_or_both = o_or_u_or_both
        self.entity_type = entity_type
        self.indent = indent # prepend GO-terms with a "." for each level

        ### prepare run for everyone but "rank_enrichment"
        if self.method != "rank_enrichment":
            self.an_set_foreground = self.ui.get_foreground_an_set()
            self.association_2_count_dict_foreground, self.association_2_ANs_dict_foreground, self.foreground_n = ratio.count_terms_v3(self.an_set_foreground, self.assoc_dict)

        if self.method == "genome":
            self.run_genome(association_2_count_dict_background, background_n)
        elif self.method == "rank_enrichment":
            self.df = self.run_rank_enrichment()
        elif self.method == "abundance_correction":
            self.run_abundance_correction()
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
        self.association_2_count_dict_background, self.association_2_ANs_dict_background = ratio.count_terms_abundance_corrected(self.ui, self.assoc_dict)
        self.df = self.run_study(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)

    def run_genome(self, association_2_count_dict_background, background_n):
        self.association_2_count_dict_background, self.background_n = association_2_count_dict_background, background_n
        self.df = self.run_study_genome(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)

    def get_result(self, FDR_cutoff=None, fold_enrichment_for2background=None, p_value_uncorrected=None):
        self.df = self.filter_results(self.df, FDR_cutoff, fold_enrichment_for2background, p_value_uncorrected)
        # if self.method != "characterize_foreground": # since no p-values available
        #     self.df["p_value"] = self.df["p_value"].apply(lambda x: "{:.2E}".format(Decimal(x)))
        #     self.df["FDR"] = self.df["FDR"].apply(lambda x: "{:.2E}".format(Decimal(x)))
        return self.df

    def run_compare_samples(self):
        self.an_set_background = self.ui.get_background_an_set()
        self.association_2_count_dict_background, self.association_2_ANs_dict_background, self.background_n = ratio.count_terms_v3(self.an_set_background, self.assoc_dict)
        self.df = self.run_study(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)

    def run_compare_groups(self):
        self.foreground_n = self.ui.get_foreground_n()
        self.background_n = self.ui.get_background_n()
        self.an_redundant_foreground = self.ui.get_an_redundant_foreground()
        self.an_redundant_background = self.ui.get_an_redundant_background()
        self.association_2_count_dict_foreground, self.association_2_ANs_dict_foreground, unused_an_count = ratio.count_terms_v3(self.an_redundant_foreground, self.assoc_dict)
        self.association_2_count_dict_background, self.association_2_ANs_dict_background, unused_an_count = ratio.count_terms_v3(self.an_redundant_background, self.assoc_dict)
        self.df = self.run_study(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)

    def run_characterize_foreground(self):
        self.an_redundant_foreground = self.ui.get_an_redundant_foreground()
        self.association_2_count_dict_foreground, self.association_2_ANs_dict_foreground, unused_an_count = ratio.count_terms_v3(self.an_redundant_foreground, self.assoc_dict)
        self.df = self.characterize_foreground(self.association_2_count_dict_foreground, self.foreground_n)

    def characterize_foreground(self, association_2_count_dict_foreground, foreground_n):
        term_list, description_list, foreground_ids_list, foreground_count_list, ratio_in_foreground_list = [], [], [], [], []
        for association, foreground_count in association_2_count_dict_foreground.items():
            term_list.append(association)
            # description_list.append(self.pqo.function_an_2_description_dict[association])
            ratio_in_foreground_list.append(self.calc_ratio(foreground_count, foreground_n))
            foreground_ids_list.append(';'.join(self.association_2_ANs_dict_foreground[association]))
            foreground_count_list.append(foreground_count)
        df = pd.DataFrame({"term": term_list, "ratio_in_foreground": ratio_in_foreground_list, "foreground_ids": foreground_ids_list, "foreground_count": foreground_count_list}) # "description": description_list,
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
            # description_list.append(self.pqo.function_an_2_description_dict[association])
            level_list.append(self.pqo.functerm_2_level_dict[association])

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
                           # "description": description_list,
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
           df["term"] = df["level"].apply(lambda x: int(x) * ".") + df["term"]
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
        term_list, description_list, p_value_list, foreground_count_list = [], [], [], []
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
                #p_val_uncorrected = stats.fisher_exact([[a, b], [c, d]], alternative='greater')[1]
                fisher_dict[(a, b, c, d)] = p_val_uncorrected
            term_list.append(association)
            p_value_list.append(p_val_uncorrected)
            # foreground_ids_list.append(';'.join(self.association_2_ANs_dict_foreground[association])) # !!! remove this and add infos after FDR filtering
            foreground_count_list.append(foreground_count)

        # create DataFrame from List compare time setup
        df = pd.DataFrame({"term": term_list,
                          "p_value": p_value_list,
                          # "foreground_ids": foreground_ids_list, # do later
                          "foreground_count": foreground_count_list})
        df = multiple_testing.BH_fast_v3(df)
        return df

    def run_study_genome_v2(self, association_2_count_dict_foreground, association_2_count_dict_background, foreground_n, background_n):
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
        len_dict = len(association_2_count_dict_foreground)
        term_arr = np.empty((len_dict,), dtype=np.dtype('U13')) # cat Functions_table_STRING.txt | cut -f 2 | awk '{print length, $0}' | sort -nr | head -1
        p_value_arr = np.zeros(shape=(len_dict, ), dtype="float64")
        foreground_count_arr = np.zeros(shape=(len_dict, ), dtype="int8")

        for i, (association, foreground_count) in enumerate(association_2_count_dict_foreground.items()):
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
                fisher_dict[(a, b, c, d)] = p_val_uncorrected
            term_arr[i] = association
            p_value_arr[i] = p_val_uncorrected
            foreground_count_arr[i] = foreground_count

        df = pd.DataFrame()
        df["term"] = term_arr
        df["p_value"] = p_value_arr
        df["foreground_count"] = foreground_count_arr
        df = multiple_testing.BH_fast_v3(df)
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

    def run_rank_enrichment(self):
        association_2_set_of_ratios_dict, association_2_ANs_dict, foldchanges_population = ratio.count_terms_fold_change_v4(self.ui.population_df, self.assoc_dict)
        if self.args_dict["compare_2_ratios_only"]:
            foldchanges_population = self.ui.population_df["abundance_ratio"].values
        foldchanges_population = np.sort(foldchanges_population)
        wilcoxon_dict = {}
        term_list, description_list, p_value_list, foreground_ids_list, foreground_count_list = [], [], [], [], []
        cles_list, over_under_represented_list = [], []
        for association, ratios_set in association_2_set_of_ratios_dict.items():
            ratios_set = np.sort(ratios_set)
            ratios_hash = hash(ratios_set.tostring())
            try:
                p_val_uncorrected, larger, cles_prob = wilcoxon_dict[ratios_hash]
            except KeyError:
                p_val_uncorrected, larger, cles_prob = mannwhitneyU(ratios_set, foldchanges_population)
                wilcoxon_dict[ratios_hash] = (p_val_uncorrected, larger, cles_prob)

            term_list.append(association)
            p_value_list.append(p_val_uncorrected)
            foreground_ids_list.append(';'.join(association_2_ANs_dict[association]))
            foreground_count_list.append(ratios_set.size)
            cles_list.append(cles_prob)
            over_under_represented_list.append(larger)
        df = pd.DataFrame({"term": term_list,
                          "p_value": p_value_list,
                          "foreground_ids": foreground_ids_list,
                          "foreground_count": foreground_count_list,
                          "effect_size": cles_list,
                          "overrepresented": over_under_represented_list})
        df = df.sort_values("p_value", ascending=True)
        df["FDR"] = BenjaminiHochberg(df["p_value"].values, df.shape[0], array=True)
        return df

def mannwhitneyU(x, y, use_continuity=True, alternative="two-sided"):
    """
    Mann Whitney U test
    :param x: sample(iterable)
    :param y: population(iterable
    :param use_continuity: Bool
    :param alternative: String
    :return: p_value, Bool, CLES_probability
    """
    U, pval = mannwhitneyu(y, x, use_continuity=use_continuity, alternative=alternative)
    if U > (len(x) * len(y)) / 2:
        larger = True # overrepresented
    else:
        larger = False # underrepresented
    cles_prob = cles(x, y)
    return pval, larger, cles_prob

def cles(lessers, greaters):
    """
    # code from https://github.com/ajschumacher/cles
    # explanation from https://janhove.github.io/reporting/2016/11/16/common-language-effect-sizes
    the probability that a score sampled at random from one distribution will be greater than a score sampled from some other distribution.

    Common-Language Effect Size
    Probability that a random draw from `greater` is in fact greater
    than a random draw from `lesser`.
    Args:
      lesser, greater: Iterables of comparables.
    """
    if len(lessers) == 0 and len(greaters) == 0:
        raise ValueError('At least one argument must be non-empty')
    # These values are a bit arbitrary, but make some sense.
    # (It might be appropriate to warn for these cases.)
    if len(lessers) == 0:
        return 1
    if len(greaters) == 0:
        return 0
    numerator = 0
    # lessers, greaters = sorted(lessers), sorted(greaters)
    lesser_index = 0
    for greater in greaters:
        while lesser_index < len(lessers) and lessers[lesser_index] < greater:
            lesser_index += 1
        numerator += lesser_index  # the count less than the greater
    denominator = len(lessers) * len(greaters)
    return float(numerator) / denominator

def mannwhitneyu(x, y, use_continuity=True, alternative=None):
    """
    Compute the Mann-Whitney rank test on samples x and y.

    Parameters
    ----------
    x, y : array_like
        Array of samples, should be one-dimensional.
    use_continuity : bool, optional
            Whether a continuity correction (1/2.) should be taken into
            account. Default is True.
    alternative : None (deprecated), 'less', 'two-sided', or 'greater'
            Whether to get the p-value for the one-sided hypothesis ('less'
            or 'greater') or for the two-sided hypothesis ('two-sided').
            Defaults to None, which results in a p-value half the size of
            the 'two-sided' p-value and a different U statistic. The
            default behavior is not the same as using 'less' or 'greater':
            it only exists for backward compatibility and is deprecated.

    Returns
    -------
    statistic : float
        The Mann-Whitney U statistic, equal to min(U for x, U for y) if
        `alternative` is equal to None (deprecated; exists for backward
        compatibility), and U for y otherwise.
    pvalue : float
        p-value assuming an asymptotic normal distribution. One-sided or
        two-sided, depending on the choice of `alternative`.

    Notes
    -----
    Use only when the number of observation in each sample is > 20 and
    you have 2 independent samples of ranks. Mann-Whitney U is
    significant if the u-obtained is LESS THAN or equal to the critical
    value of U.

    This test corrects for ties and by default uses a continuity correction.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Mann-Whitney_U_test

    .. [2] H.B. Mann and D.R. Whitney, "On a Test of Whether one of Two Random
           Variables is Stochastically Larger than the Other," The Annals of
           Mathematical Statistics, vol. 18, no. 1, pp. 50-60, 1947.

    """
    # if alternative is None:
    #     warnings.warn("Calling `mannwhitneyu` without specifying "
    #                   "`alternative` is deprecated.", DeprecationWarning)
    # x = np.asarray(x)
    # y = np.asarray(y)
    n1 = len(x)
    n2 = len(y)
    ranked = rankdata(np.concatenate((x, y)))
    rankx = ranked[0:n1]  # get the x-ranks
    u1 = n1*n2 + (n1*(n1+1))/2.0 - np.sum(rankx, axis=0)  # calc U for x
    u2 = n1*n2 - u1  # remainder is U for y
    T = tiecorrect(ranked)
    if T == 0:
        raise ValueError('All numbers are identical in mannwhitneyu')
    sd = np.sqrt(T * n1 * n2 * (n1+n2+1) / 12.0)

    meanrank = n1*n2/2.0 + 0.5 * use_continuity
    if alternative is None or alternative == 'two-sided':
        bigu = max(u1, u2)
    elif alternative == 'less':
        bigu = u1
    elif alternative == 'greater':
        bigu = u2
    else:
        raise ValueError("alternative should be None, 'less', 'greater' "
                         "or 'two-sided'")

    z = (bigu - meanrank) / sd
    if alternative is None:
        # This behavior, equal to half the size of the two-sided
        # p-value, is deprecated.
        p = distributions.norm.sf(abs(z))
    elif alternative == 'two-sided':
        p = 2 * distributions.norm.sf(abs(z))
    else:
        p = distributions.norm.sf(z)

    u = u2
    # This behavior is deprecated.
    if alternative is None:
        u = min(u1, u2)
    # return MannwhitneyuResult(u, p)
    return u, p

def rankdata(a, method='average'):
    """
    Assign ranks to data, dealing with ties appropriately.

    Ranks begin at 1.  The `method` argument controls how ranks are assigned
    to equal values.  See [1]_ for further discussion of ranking methods.

    Parameters
    ----------
    a : array_like
        The array of values to be ranked.  The array is first flattened.
    method : str, optional
        The method used to assign ranks to tied elements.
        The options are 'average', 'min', 'max', 'dense' and 'ordinal'.

        'average':
            The average of the ranks that would have been assigned to
            all the tied values is assigned to each value.
        'min':
            The minimum of the ranks that would have been assigned to all
            the tied values is assigned to each value.  (This is also
            referred to as "competition" ranking.)
        'max':
            The maximum of the ranks that would have been assigned to all
            the tied values is assigned to each value.
        'dense':
            Like 'min', but the rank of the next highest element is assigned
            the rank immediately after those assigned to the tied elements.
        'ordinal':
            All values are given a distinct rank, corresponding to the order
            that the values occur in `a`.

        The default is 'average'.

    Returns
    -------
    ranks : ndarray
         An array of length equal to the size of `a`, containing rank
         scores.

    References
    ----------
    .. [1] "Ranking", http://en.wikipedia.org/wiki/Ranking

    Examples
    --------
    >>> from scipy.stats import rankdata
    >>> rankdata([0, 2, 3, 2])
    array([ 1. ,  2.5,  4. ,  2.5])
    >>> rankdata([0, 2, 3, 2], method='min')
    array([ 1,  2,  4,  2])
    >>> rankdata([0, 2, 3, 2], method='max')
    array([ 1,  3,  4,  3])
    >>> rankdata([0, 2, 3, 2], method='dense')
    array([ 1,  2,  3,  2])
    >>> rankdata([0, 2, 3, 2], method='ordinal')
    array([ 1,  2,  4,  3])
    """
    if method not in ('average', 'min', 'max', 'dense', 'ordinal'):
        raise ValueError('unknown method "{0}"'.format(method))

    arr = np.ravel(np.asarray(a))
    algo = 'mergesort' if method == 'ordinal' else 'quicksort'
    sorter = np.argsort(arr, kind=algo)

    inv = np.empty(sorter.size, dtype=np.intp)
    inv[sorter] = np.arange(sorter.size, dtype=np.intp)

    if method == 'ordinal':
        return inv + 1

    arr = arr[sorter]
    obs = np.r_[True, arr[1:] != arr[:-1]]
    dense = obs.cumsum()[inv]

    if method == 'dense':
        return dense

    # cumulative counts of each unique value
    count = np.r_[np.nonzero(obs)[0], len(obs)]

    if method == 'max':
        return count[dense]

    if method == 'min':
        return count[dense - 1] + 1

    # average method
    return .5 * (count[dense] + count[dense - 1] + 1)

def tiecorrect(rankvals):
    """
    Tie correction factor for ties in the Mann-Whitney U and
    Kruskal-Wallis H tests.

    Parameters
    ----------
    rankvals : array_like
        A 1-D sequence of ranks.  Typically this will be the array
        returned by `stats.rankdata`.

    Returns
    -------
    factor : float
        Correction factor for U or H.

    See Also
    --------
    rankdata : Assign ranks to the data
    mannwhitneyu : Mann-Whitney rank test
    kruskal : Kruskal-Wallis H test

    References
    ----------
    .. [1] Siegel, S. (1956) Nonparametric Statistics for the Behavioral
           Sciences.  New York: McGraw-Hill.

    Examples
    --------
    >>> from scipy.stats import tiecorrect, rankdata
    >>> tiecorrect([1, 2.5, 2.5, 4])
    0.9
    >>> ranks = rankdata([1, 3, 2, 4, 5, 7, 2, 8, 4])
    >>> ranks
    array([ 1. ,  4. ,  2.5,  5.5,  7. ,  8. ,  2.5,  9. ,  5.5])
    >>> tiecorrect(ranks)
    0.9833333333333333

    """
    arr = np.sort(rankvals)
    idx = np.nonzero(np.r_[True, arr[1:] != arr[:-1], True])[0]
    cnt = np.diff(idx).astype(np.float64)

    size = np.float64(arr.size)
    return 1.0 if size < 2 else 1.0 - (cnt**3 - cnt).sum() / (size**3 - size)