import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
from scipy import stats
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
    """Runs Fisher's exact test, as well as multiple corrections
    """
    def __init__(self, ui, assoc_dict, obo_dag, alpha, backtracking, o_or_u_or_both, multitest_method, gocat_upk="all_GO"):
        self.ui = ui
        self.method = self.ui.method
        self.assoc_dict = assoc_dict
        self.obo_dag = obo_dag
        self.alpha = alpha
        self.multitest_method = multitest_method
        self.gocat_upk = gocat_upk
        self.results = []
        self.backtracking = backtracking
        self.o_or_u_or_both = o_or_u_or_both

        # prepare run
        self.an_set_foreground = self.ui.get_foreground_an_set()
        self.association_2_count_dict_foreground, self.association_2_ANs_dict_foreground, foreground_n = ratio.count_terms_v2(
            self.an_set_foreground, self.assoc_dict, self.obo_dag)

        if self.method == "abundance_correction":
            background_n = foreground_n
            self.association_2_count_dict_background, self.association_2_ANs_dict_background = ratio.count_terms_abundance_corrected(
                self.ui, self.assoc_dict, self.obo_dag)

        elif self.method == "compare_samples":
            self.an_set_background = self.ui.get_background_an_set()
            self.association_2_count_dict_background, self.association_2_ANs_dict_background, background_n = ratio.count_terms_v2(
                self.an_set_background, self.assoc_dict, self.obo_dag)

        else:
            raise StopIteration

        self.run_study(self.association_2_count_dict_foreground, self.association_2_count_dict_background, foreground_n, background_n)

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
        multitest = ("p_" + self.multitest_method, "%.3g")
        attributes2add_list = [multitest, ('description', '%s'), ('ANs_foreground', '%s')]
        if self.method != "abundance_correction":
            attributes2add_list.append(('ANs_pop', '%s'))
        for association, foreground_count in association_2_count_dict_foreground.items():
            background_count = association_2_count_dict_background[association]
            a = foreground_count
            b = foreground_n - foreground_count
            c = background_count
            d = background_n - background_count
            if d < 0:
                d = 0
            # Debug STOP

            if self.o_or_u_or_both == 'underrepresented':
                # purified or underrepresented --> left_tail or less
                try:
                    p_val_uncorrected = fisher_dict[(a, b, c, d)]
                except KeyError: # why not tuple instead of list #!!!
                    p_val_uncorrected  = stats.fisher_exact([[a, b], [c, d]], alternative='greater')[1]
                    fisher_dict[(a, b, c, d)] = p_val_uncorrected
            elif self.o_or_u_or_both == 'overrepresented':
                # enriched or overrepresented --> right_tail or greater
                try:
                    p_val_uncorrected = fisher_dict[(a, b, c, d)]
                except KeyError:
                    p_val_uncorrected = stats.fisher_exact([[a, b], [c, d]], alternative='less')[1]
                    fisher_dict[(a, b, c, d)] = p_val_uncorrected
            else:
                # both --> two_tail or two-sided
                try:
                    p_val_uncorrected = fisher_dict[(a, b, c, d)]
                except KeyError:
                    p_val_uncorrected  = stats.fisher_exact([[a, b], [c, d]], alternative='two-sided')[1]
                    fisher_dict[(a, b, c, d)] = p_val_uncorrected
            one_record = EnrichmentRecord(
                id_=association,
                p_uncorrected=p_val_uncorrected,
                ratio_in_foreground=(foreground_count, foreground_n),
                ratio_in_background=(background_count, background_n),
                ANs_foreground = ', '.join(self.get_ans_from_association(association, True)),
                ANs_background = ', '.join(self.get_ans_from_association(association, False)),
                attributes2add=attributes2add_list)
            self.results.append(one_record)
        self.calc_multiple_corrections()

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
        if method_name == "bonferroni":
            corrected_pvals = Bonferroni(pvals, self.alpha).corrected_pvals
        elif method_name == "sidak":
            corrected_pvals = Sidak(pvals, self.alpha).corrected_pvals
        elif method_name == "holm":
            corrected_pvals = HolmBonferroni(pvals, self.alpha).corrected_pvals
        elif method_name == 'benjamini_hochberg':
            corrected_pvals = BenjaminiHochberg(pvals, len(self.results))
        else:
            raise Exception("multiple test correction methods must be "
                            "one of %s" % all_methods)
        self.update_results(method_name, corrected_pvals)
        for rec in self.results:
            rec.find_goterm(self.obo_dag)

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
                results_sorted_by_fold_enrichment_study2pop = sorted(self.results, key=lambda record: record.fold_enrichment_study2pop, reverse=True)
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
            results_sorted_by_fold_enrichment_foreground_2_background = sorted(self.results, key=lambda record: record.fold_enrichment_foreground_2_background, reverse=True)
            for rec in results_sorted_by_fold_enrichment_foreground_2_background:
                rec.update_remaining_fields()
                # if rec.fold_enrichment_foreground_2_background >= fold_enrichment_foreground_2_background or fold_enrichment_foreground_2_background is None:
                if fold_enrichment_foreground_2_background is None or rec.fold_enrichment_foreground_2_background >= fold_enrichment_foreground_2_background:
                    # if rec.__dict__[multitest_method_name] <= p_value_mulitpletesting or p_value_mulitpletesting is None:
                    if p_value_mulitpletesting is None or rec.__dict__[multitest_method_name] <= p_value_mulitpletesting:
                        # if rec.p_uncorrected <= p_value_uncorrected or p_value_uncorrected is None:
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
        self.perc_associated_foreground = self.calc_fold_enrichemnt(
            self.foreground_count, self.foreground_n)
        self.perc_associated_background = self.calc_fold_enrichemnt(
            self.background_count, self.background_n)
        if self.perc_associated_foreground != -1 and self.perc_associated_background != -1:
            self.fold_enrichment_foreground_2_background = self.calc_fold_enrichemnt(
                self.perc_associated_foreground, self.perc_associated_background)
        else:
            self.fold_enrichment_foreground_2_background = "-1"
        self.perc_associated_foreground = self.perc_associated_foreground * 100
        self.perc_associated_background = self.perc_associated_background * 100
        self.attributes_list += attributes2add

    @staticmethod
    def calc_fold_enrichemnt(zaehler, nenner):
        try:
            fold_en = float(zaehler) / nenner
        except ZeroDivisionError:
            # fold_en = -1 #!!!
            fold_en = 1000
        return fold_en

    def find_goterm(self, go):
        try:
            self.goterm = go[self.id_]
            self.description = self.goterm.name
        except KeyError:
            pass

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
