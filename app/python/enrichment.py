import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
from scipy import stats
from fisher import pvalue
import numpy as np
import pandas as pd
from decimal import Decimal

from multiple_testing import Bonferroni, Sidak, HolmBonferroni, BenjaminiHochberg
import ratio


def modify_list(list_of_string, search, replace):
    if search in list_of_string:
        index = list_of_string.index(search)
        return list_of_string[:index] + [replace] + list_of_string[index+1:]
    else:
        return list_of_string

def modify_header(header_list):
    header_list = modify_list(header_list, 'over_under', 'over/under')
    return modify_list(header_list, 'p_benjamini_hochberg', 'FDR')


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
    def __init__(self, ui, assoc_dict, obo_dag, enrichment_method="genome", entity_type="-51",
            o_or_u_or_both="overrepresented",
            multitest_method="benjamini_hochberg", alpha=0.05,
            association_2_count_dict_background=None, background_n=None,
            indent=False):
        self.ui = ui
        self.method = enrichment_method
        self.assoc_dict = assoc_dict
        self.obo_dag = obo_dag
        self.alpha = alpha
        self.multitest_method = multitest_method
        self.results = []
        self.o_or_u_or_both = o_or_u_or_both
        self.entity_type = entity_type
        # self.FDR_cutoff = FDR_cutoff
        # self.fold_enrichment_for2background = fold_enrichment_for2background
        # self.p_value_uncorrected = p_value_uncorrected
        self.indent = indent # prepend GO-terms with a "." for each level

        ### prepare run
        self.an_set_foreground = self.ui.get_foreground_an_set()
        self.association_2_count_dict_foreground, self.association_2_ANs_dict_foreground, self.foreground_n = ratio.count_terms_v3(
            self.an_set_foreground, self.assoc_dict)
        # , obo_dag=self.obo_dag, entity_type=self.entity_type)

        # run_study_ = True
        if self.method == "abundance_correction":
            self.run_abundance_correction()
            # self.background_n = self.foreground_n
            # self.association_2_count_dict_background, self.association_2_ANs_dict_background = ratio.count_terms_abundance_corrected_manager(self.ui, self.assoc_dict, self.obo_dag, self.entity_type)
        elif self.method == "genome":
            self.run_genome(association_2_count_dict_background, background_n)
            # self.association_2_count_dict_background, self.association_2_ANs_dict_background, background_n = association_2_count_dict_background, association_2_ANs_dict_background, background_n
        elif self.method == "compare_samples":
            self.run_compare_samples()
            # self.an_set_background = self.ui.get_background_an_set()
            # self.association_2_count_dict_background, self.association_2_ANs_dict_background, background_n = ratio.count_terms_manager(self.an_set_background, self.assoc_dict, self.obo_dag, self.entity_type)
        elif self.method == "compare_groups":
            self.run_compare_groups()
            # self.foreground_n = self.ui.get_foreground_n()
            # self.background_n = self.ui.get_background_n()
            # self.an_redundant_foreground = self.ui.get_an_redundant_foreground()
            # self.an_redundant_background = self.ui.get_an_redundant_background()
            # self.association_2_count_dict_foreground, self.association_2_ANs_dict_foreground, unused_an_count = ratio.count_terms_manager(self.an_redundant_foreground, self.assoc_dict, self.obo_dag, self.entity_type)
            # self.association_2_count_dict_background, self.association_2_ANs_dict_background, unused_an_count = ratio.count_terms_manager(self.an_redundant_background, self.assoc_dict, self.obo_dag, self.entity_type)
        elif self.method == "characterize_foreground":
            self.run_characterize_foreground()
            # self.an_redundant_foreground = self.ui.get_an_redundant_foreground()
            # self.association_2_count_dict_foreground, self.association_2_ANs_dict_foreground, unused_an_count = ratio.count_terms_manager(self.an_redundant_foreground, self.assoc_dict, self.obo_dag, self.entity_type)
            # run_study_ = False
        else:
            raise NotImplementedError

        # if run_study_:
        #     self.run_study(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)
        # else:
        #     self.characterize_foreground(self.association_2_count_dict_foreground, self.foreground_n)

    def run_abundance_correction(self):
        self.background_n = self.foreground_n
        self.association_2_count_dict_background, self.association_2_ANs_dict_background = ratio.count_terms_abundance_corrected_manager(self.ui, self.assoc_dict, self.obo_dag, self.entity_type)
        self.df = self.run_study(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)

    def run_genome(self, association_2_count_dict_background, background_n):
        self.association_2_count_dict_background, self.background_n = association_2_count_dict_background, background_n
        self.df = self.run_study_genome(self.association_2_count_dict_foreground, self.association_2_count_dict_background, self.foreground_n, self.background_n)

    def get_result(self, output_format="json", FDR_cutoff=None, fold_enrichment_for2background=None, p_value_uncorrected=None):
        self.df = self.filter_results(self.df, FDR_cutoff, fold_enrichment_for2background, p_value_uncorrected)
        if self.method != "characterize_foreground": # since no p-values available
            self.df["p_uncorrected"] = self.df["p_uncorrected"].apply(lambda x: "{:.2E}".format(Decimal(x)))
        if output_format == "json":
            return self.df.to_json(orient='records')
        elif output_format == "tsv":
            return self.df.to_csv(sep="\t", header=True, index=False)
        # elif output_format == "web_table":
            # header: list of string
            # results: nested list of string (one list per row)
            # return self.df.columns.tolist(), self.df.values
        else:
            raise NotImplementedError

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
        # multitest = ("p_" + self.multitest_method, "%.3g")
        # attributes2add_list = [multitest, ('description', '%s'), ('ANs_foreground', '%s'), ('ANs_background', '%s')]
        # for association, foreground_count in association_2_count_dict_foreground.items():
        #     one_record = EnrichmentRecord(id_=association,
        #         p_uncorrected=np.nan,
        #         ratio_in_foreground=(foreground_count, foreground_n),
        #         ratio_in_background=(np.nan, np.nan),
        #         ANs_foreground=', '.join(self.get_ans_from_association(association, True)),
        #         ANs_background="NaN",
        #         attributes2add=attributes2add_list)
        #     self.results.append(one_record)
        # for rec in self.results:
        #     rec.find_goterm(self.obo_dag)
        id_list, description_list, ANs_foreground_list, foreground_count_list, ratio_in_foreground_list = [], [], [], [], []
        for association, foreground_count in association_2_count_dict_foreground.items():
            id_list.append(association)
            description_list.append(self.obo_dag[association].name)
            ratio_in_foreground_list.append((foreground_count, foreground_n))
            ANs_foreground_list.append(';'.join(self.association_2_ANs_dict_foreground[association]))
            foreground_count_list.append(foreground_count)
        df = pd.DataFrame({"id_": id_list, "description": description_list, "ratio_in_foreground": ratio_in_foreground_list, "ANs_foreground": ANs_foreground_list, "foreground_count": foreground_count_list})
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
        id_list, description_list, level_list, p_uncorrected_list, ANs_foreground_list = [], [], [], [], []
        foreground_count_list, background_count_list, foreground_n_list, background_n_list = [], [], [], []
        percent_associated_foreground, percent_associated_background, ANs_foreground_list, ANs_background_list= [], [], [], []
        # multitest = ("p_" + self.multitest_method, "%.3g")
        # attributes2add_list = [multitest, ('description', '%s'), ('ANs_foreground', '%s')]
        # if self.method not in {"abundance_correction", "genome"}:
        #     attributes2add_list.append(('ANs_background', '%s'))
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
                # enriched or overrepresented --> right_tail or greater (but foreground and background are switched)
                try:
                    p_val_uncorrected = fisher_dict[(a, b, c, d)]
                except KeyError:
                    # p_val_uncorrected = stats.fisher_exact([[a, b], [c, d]], alternative='less')[1]
                    if a == c and b == d:
                        p_val_uncorrected = 1
                    else:
                        p_val_uncorrected = pvalue(a, b, c, d).right_tail
                    fisher_dict[(a, b, c, d)] = p_val_uncorrected
            elif self.o_or_u_or_both == 'both':
                # both --> two_tail or two-sided
                try:
                    p_val_uncorrected = fisher_dict[(a, b, c, d)]
                except KeyError:
                    p_val_uncorrected = stats.fisher_exact([[a, b], [c, d]], alternative='two-sided')[1]
                    ### fisher_dict[(a, b, c, d)] = p_val_uncorrected # don't use this version (but the scipy version above) since accuracy drops too much
            elif self.o_or_u_or_both == 'underrepresented':
                # purified or underrepresented --> left_tail or less
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
            # one_record = EnrichmentRecord(
            #     id_=association,
            #     p_uncorrected=p_val_uncorrected,
            #     ratio_in_foreground=(foreground_count, foreground_n),
            #     ratio_in_background=(background_count, background_n),
            #     ANs_foreground = ';'.join(self.get_ans_from_association(association, True)),
            #     ANs_background = ';'.join(self.get_ans_from_association(association, False)),
            #     attributes2add=attributes2add_list)
            # self.results.append(one_record)
        # self.calc_multiple_corrections()
            id_list.append(association)
            description_list.append(self.obo_dag[association].name)
            level_list.append(self.obo_dag[association].level)
            p_uncorrected_list.append(p_val_uncorrected)
            percent_associated_foreground.append("{0:.2f}".format(round(self.calc_ratio(foreground_count, foreground_n), 2)))
            percent_associated_background.append("{0:.2f}".format(round(self.calc_ratio(background_count, background_n), 2)))
            ANs_foreground_list.append(';'.join(self.association_2_ANs_dict_foreground[association]))
            ANs_background_list.append(';'.join(self.association_2_ANs_dict_background[association]))
            foreground_count_list.append(foreground_count)
            background_count_list.append(background_count)
            foreground_n_list.append(foreground_n)
            background_n_list.append(background_n)

        df = pd.DataFrame({"id": id_list,
                           "description": description_list,
                           "level": level_list,
                           "p_uncorrected": p_uncorrected_list,
                           "percent_associated_foreground": percent_associated_foreground,
                           "percent_associated_background": percent_associated_background,
                           "ANs_foreground": ANs_foreground_list,
                           "ANs_background": ANs_background_list,
                           "foreground_count": foreground_count_list,
                           "background_count": background_count_list,
                           "foreground_n": foreground_n_list,
                           "background_n": background_n_list})
        if self.method in {"abundance_correction", "genome"}:
            df = df.drop("ANs_foreground", axis=1)
        if self.indent:
           df["id"] = df["background_count"].apply(lambda x: int(x) * ".") + df["id"]
        df = df.sort_values("p_uncorrected", ascending=True)
        corrected_pvals = self.calc_multiple_corrections_v2(df["p_uncorrected"].values, method_name=self.multitest_method, alpha=self.alpha, array=True)
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
        id_list, description_list, p_uncorrected_list, ANs_foreground_list, foreground_count_list = [], [], [], [], []
        for association, foreground_count in association_2_count_dict_foreground.items():
            background_count = association_2_count_dict_background[association]
            a = foreground_count # number of proteins associated with given GO-term
            b = foreground_n - foreground_count # number of proteins not associated with GO-term
            c = background_count
            d = background_n - background_count
            if d < 0:
                d = 0
            # enriched or overrepresented --> right_tail or greater (but foreground and background are switched)
            try:
                p_val_uncorrected = fisher_dict[(a, b, c, d)]
            except KeyError:
                p_val_uncorrected = pvalue(a, b, c, d).right_tail
                fisher_dict[(a, b, c, d)] = p_val_uncorrected
            id_list.append(association)
            description_list.append(self.obo_dag[association].name)
            p_uncorrected_list.append(p_val_uncorrected)
            ANs_foreground_list.append(';'.join(self.association_2_ANs_dict_foreground[association]))
            foreground_count_list.append(foreground_count)
        df = pd.DataFrame({"id": id_list,
                          "description": description_list,
                          "p_uncorrected": p_uncorrected_list,
                          "ANs_foreground": ANs_foreground_list,
                          "foreground_count": foreground_count_list})
        df = df.sort_values("p_uncorrected", ascending=True)
        df["FDR"] = BenjaminiHochberg(df["p_uncorrected"].values, df.shape[0], array=True)
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

    def calc_multiple_corrections(self):
        self.results.sort(key=lambda r: r.p_uncorrected)
        pvals = [r.p_uncorrected for r in self.results]
        all_methods = ("bonferroni", "sidak", "holm", "benjamini_hochberg", "fdr")
        method_name = self.multitest_method

        if method_name == 'benjamini_hochberg':
            corrected_pvals = BenjaminiHochberg(pvals, len(self.results))
        elif method_name == "bonferroni":
            corrected_pvals = Bonferroni(pvals, self.alpha).corrected_pvals
        elif method_name == "sidak":
            corrected_pvals = Sidak(pvals, self.alpha).corrected_pvals
        elif method_name == "holm":
            corrected_pvals = HolmBonferroni(pvals, self.alpha).corrected_pvals
        else:
            raise Exception("multiple test correction methods must be "
                            "one of %s" % all_methods)
        self.update_results(method_name, corrected_pvals)
        for rec in self.results:
            rec.find_goterm(self.obo_dag)

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

    def write_summary2file(self, fn_out, fold_enrichment_foreground_2_background, p_value_mulitpletesting, p_value_uncorrected, indent):
        multitest_method_name = "p_" + self.multitest_method
        with open(fn_out, 'w') as fh_out:
            if len(self.results) == 0:
                fh_out.write("""unfortunately no results to write to file\n\npossible reasons:\n   threshold of reports too high\n\
   either no/few IDs could be mapped to keywords (correct species selected?)\n   abundance data\
missing (but option selected)\n\n\nDon't hesitate to contact us for feedback or questions!""")
            else:
                header_list = modify_header(self.results[0].get_attributenames2write(self.o_or_u_or_both))
                header2write = '\t'.join(header_list) + '\n'
                fh_out.write(header2write)
                results_sorted_by_fold_enrichment_study2pop = sorted(self.results, key=lambda record: record.p_uncorrected)
                for rec in results_sorted_by_fold_enrichment_study2pop:
                    rec.update_remaining_fields()
                    if rec.fold_enrichment_study2pop >= fold_enrichment_foreground_2_background or fold_enrichment_foreground_2_background is None:
                        if rec.__dict__[multitest_method_name] <= p_value_mulitpletesting or p_value_mulitpletesting is None:
                            if rec.p_uncorrected <= p_value_uncorrected or p_value_uncorrected is None:
                                fh_out.write(rec.get_line2write(indent, self.o_or_u_or_both) + '\n')

    def write_summary2file_web(self, fold_enrichment_foreground_2_background, p_value_mulitpletesting, p_value_uncorrected, indent):
        multitest_method_name = "p_" + self.multitest_method
        results2write = []
        if len(self.results) == 0:
            header2write = """unfortunately no results to write to file\n\npossible reasons:\n   threshold of reports too high\n\
either no/few IDs could be mapped to keywords (correct species selected?)\n   abundance data\
missing (but option selected)\n\n\nDon't hesitate to contact us for feedback or questions!"""
        else:
            header_list = modify_header(self.results[0].get_attributenames2write(self.o_or_u_or_both))
            header2write = '\t'.join(header_list) + '\n'
            results_sorted_by_fold_enrichment_foreground_2_background = sorted(self.results, key=lambda record: record.p_uncorrected)
            for rec in results_sorted_by_fold_enrichment_foreground_2_background:
                rec.update_remaining_fields()
                if fold_enrichment_foreground_2_background is None or rec.fold_enrichment_foreground_2_background >= fold_enrichment_foreground_2_background:
                    if p_value_mulitpletesting is None or rec.__dict__[multitest_method_name] <= p_value_mulitpletesting:
                        if p_value_uncorrected is None or rec.p_uncorrected <= p_value_uncorrected:
                            res = rec.get_line2write(indent, self.o_or_u_or_both)
                            results2write.append(res)
        return header2write.rstrip(), results2write


class EnrichmentRecord(object):
    """
    Represents one result (from a single GOTerm) in the GOEnrichmentStudy
    """

    def __init__(self, id_, p_uncorrected, ratio_in_foreground, ratio_in_background,
                 ANs_foreground, ANs_background, attributes2add):
        self.attributes_list = [
            ('id_', '%s'), ('over_under', '%s'),
            ('perc_associated_foreground', "%0.3f"),('perc_associated_background', "%0.3f"),
            ('fold_enrichment_foreground_2_background', "%0.3f"),('foreground_count', '%s'),
            ('foreground_n', '%s'), ('background_count','%s'), ('background_n', '%s'),
            ('p_uncorrected', "%.3g")]
        self.id_ = id_
        self.p_uncorrected = p_uncorrected
        self.foreground_count, self.foreground_n = ratio_in_foreground
        self.background_count, self.background_n = ratio_in_background
        self.ANs_foreground = ANs_foreground
        self.ANs_background = ANs_background
        self.perc_associated_foreground = self.calc_fold_enrichment(
            self.foreground_count, self.foreground_n)
        self.perc_associated_background = self.calc_fold_enrichment(
            self.background_count, self.background_n)
        if self.perc_associated_foreground != -1 and self.perc_associated_background != -1:
            self.fold_enrichment_foreground_2_background = self.calc_fold_enrichment(
                self.perc_associated_foreground, self.perc_associated_background)
        else:
            self.fold_enrichment_foreground_2_background = "-1"
        self.perc_associated_foreground = self.perc_associated_foreground * 100
        self.perc_associated_background = self.perc_associated_background * 100
        self.attributes_list += attributes2add

    @staticmethod
    def calc_fold_enrichment(zaehler, nenner):
        try:
            fold_en = float(zaehler) / nenner
        except ZeroDivisionError:
            # fold_en = -1 #!!!
            # fold_en = 1000
            fold_en = np.inf
        return fold_en

    def find_goterm(self, go):
        try:
            self.goterm = go[self.id_]
            self.description = self.goterm.name
        except KeyError:
            pass
        except TypeError:
            # print("find_goterm", go, type(go), len(go))
            pass
    #     kegg_pseudo_dag: description=nam, goterm=id


    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def update_fields(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def update_remaining_fields(self):
        if self.perc_associated_foreground > self.perc_associated_background:
            self.over_under = 'o'
        else:
            self.over_under = 'u'

    def get_attributenames2write(self, o_or_u_or_both):
        if o_or_u_or_both == 'both':
            return [name_format[0] for name_format in self.attributes_list]
        else:
            list2return = []
            for ele in self.attributes_list:
                if ele[0] != 'over_under':
                    list2return.append(ele[0])
            return list2return

    def get_attributes_list(self, o_or_u_or_both):
        if o_or_u_or_both == 'both':
            return self.attributes_list
        else:
            list2return = []
            for ele in self.attributes_list:
                if ele[0] != 'over_under':
                    list2return.append(ele)
            return list2return

    def get_attribute_format_list(self, indent, o_or_u_or_both):
        if indent:
            attributes_list = [('dot_id', '%s') if x[0] == 'id_' else x for x in self.get_attributes_list(o_or_u_or_both)]
            dots = ''
            if self.goterm is not None:
                dots = "." * self.goterm.level
            self.dot_id = dots + self.id_
        else:
            attributes_list = self.get_attributes_list(o_or_u_or_both)
        return attributes_list

    def get_attribute_formatted(self, attr_form):
        attr, form = attr_form
        try:
            val = self.__dict__[attr]
            attr2write = (form % val) + '\t'
        except KeyError:
            attr2write = 'n.a.' + '\t'
        return attr2write

    def get_line2write(self, indent, o_or_u_or_both):
        line2write = ''
        attribute_format_list = self.get_attribute_format_list(indent, o_or_u_or_both)
        for attr_form in attribute_format_list:
            line2write += self.get_attribute_formatted(attr_form)
        return line2write.rstrip()

