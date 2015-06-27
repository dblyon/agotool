import fisher, ratio
from multiple_testing import Bonferroni, Sidak, HolmBonferroni, BenjaminiHochberg
from collections import defaultdict


class GOEnrichmentRecord(object):
    """
    Represents one result (from a single GOTerm) in the GOEnrichmentStudy
    """
    attributes_list = [('id', '%s'), ('over_under', '%s'), ('perc_associated_study', "%0.3f"),
                   ('perc_associated_pop', "%0.3f"), ('fold_enrichment_study2pop', "%0.3f"),
                   ('study_count', '%s'), ('study_n', '%s'), ('pop_count','%s'), ('pop_n', '%s'), ('p_uncorrected', "%.3g")]

    def __init__(self, id, p_uncorrected, ratio_in_study, ratio_in_pop, ANs_study, ANs_pop):
        self.id = id
        self.p_uncorrected = p_uncorrected
        self.study_count, self.study_n = ratio_in_study
        self.pop_count, self.pop_n = ratio_in_pop
        self.ANs_study = ANs_study
        self.ANs_pop = ANs_pop
        self.perc_associated_study = self.calc_fold_enrichemnt(self.study_count, self.study_n)
        self.perc_associated_pop = self.calc_fold_enrichemnt(self.pop_count, self.pop_n)
        if self.perc_associated_study != -1 and self.perc_associated_pop != -1:
            self.fold_enrichment_study2pop = round(self.calc_fold_enrichemnt(self.perc_associated_study, self.perc_associated_pop), 2)
        else:
            self.fold_enrichment_study2pop = "-1"
        self.perc_associated_study = self.perc_associated_study * 100
        self.perc_associated_pop = self.perc_associated_pop * 100

    def calc_fold_enrichemnt(self, zaehler, nenner):
        try:
            fold_en = float(zaehler) / nenner
        except ZeroDivisionError:
            fold_en = -1
        return fold_en

    def find_goterm(self, go):
        if self.id in list(go.keys()):
            self.goterm = go[self.id]
            self.description = self.goterm.name

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def update_fields(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def update_remaining_fields(self):
        self.over_under = 'o' if ((1.0 * self.study_count / self.study_n) > (1.0 * self.pop_count / self.pop_n)) else 'u'

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
            attributes_list = [('dot_id', '%s') if x[0] == 'id' else x for x in self.get_attributes_list(o_or_u_or_both)]
            dots = ''
            if self.goterm is not None:
                dots = "." * self.goterm.level
            self.dot_id = dots + self.id
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


class GOEnrichmentRecord_UPK(GOEnrichmentRecord):
    attributes_list = [('id', '%s'), ('over_under', '%s'),
     ('perc_associated_study', "%0.3f"), ('perc_associated_pop', "%0.3f"),
     ('fold_enrichment_study2pop', "%0.3f"), ('study_count', '%s'),
     ('study_n', '%s'), ('pop_count','%s'), ('pop_n', '%s'), ('p_uncorrected', "%.3g")]

    def get_attribute_format_list(self, o_or_u_or_both):
        return self.get_attributes_list(o_or_u_or_both)

    def get_line2write(self, o_or_u_or_both):
        line2write = ''
        attribute_format_list = self.get_attribute_format_list(o_or_u_or_both)
        for attr_form in attribute_format_list:
            line2write += self.get_attribute_formatted(attr_form)
        return line2write.rstrip()


class GOEnrichmentStudy(object):
    """Runs Fisher's exact test, as well as multiple corrections
    """
    def __init__(self, ui, assoc_dict, obo_dag, alpha, backtracking, randomSample, abcorr, o_or_u_or_both, multitest_method):
        self.ui = ui
        self.assoc_dict = assoc_dict
        self.obo_dag = obo_dag
        self.alpha = alpha
        self.multitest_method = multitest_method
        GOEnrichmentRecord.attributes_list += [("p_" + self.multitest_method, "%.3g"), ('description', '%s'), ('ANs_study', '%s')]
        self.results = []
        self.backtracking = backtracking
        self.randomSample = randomSample
        self.abcorr = abcorr
        if not self.abcorr:
            GOEnrichmentRecord.attributes_list.append(('ANs_pop', '%s'))
        self.o_or_u_or_both = o_or_u_or_both
        if self.backtracking: # add all parent GO-terms to assoc_dict
            self.obo_dag.update_association(self.assoc_dict)
        self.prepare_run()

    def prepare_run(self): # study_n should be the same in genome vs. observed vs. abundance_corrected
        '''
        :return: None
        '''
        if self.abcorr:
            self.study_an_frset = self.ui.get_sample_an_frset()
            self.term_study, self.go2ans_study_dict = ratio.count_terms(self.study_an_frset, self.assoc_dict, self.obo_dag)
            study_n = len(self.study_an_frset)

            if self.randomSample:
                self.pop_an_set = self.ui.get_background_an_set_random_sample()
                pop_n  = len(self.pop_an_set)
                self.term_pop, self.go2ans_pop_dict = ratio.count_terms(self.pop_an_set, self.assoc_dict, self.obo_dag)
            else:
                pop_n = len(self.study_an_frset)
                self.term_pop, self.go2ans_pop_dict = ratio.count_terms_abundance_corrected(self.ui, self.assoc_dict, self.obo_dag)
        else:
            if self.ui.col_background_an == 'Genome':
                self.study_an_frset = self.ui.get_sample_an_frset_genome()
            else:
                self.study_an_frset = self.ui.get_sample_an_frset()
            self.term_study, self.go2ans_study_dict = ratio.count_terms(self.study_an_frset, self.assoc_dict, self.obo_dag)
            study_n = len(self.study_an_frset)

            self.pop_an_set = self.ui.get_background_an_all_set()
            pop_n  = len(self.pop_an_set)
            self.term_pop, self.go2ans_pop_dict = ratio.count_terms(self.pop_an_set, self.assoc_dict, self.obo_dag)

        self.run_study_v2(self.term_study, self.term_pop, study_n, pop_n)

    def get_ans_from_goid(self, goid, study):
        if study:
            if self.go2ans_study_dict.has_key(goid):
                return sorted(self.go2ans_study_dict[goid])
            else:
                return ''
        else:
            if self.go2ans_pop_dict.has_key(goid):
                return sorted(self.go2ans_pop_dict[goid])
            else:
                return ''

    def run_study_v2(self, term_study, term_pop, study_n, pop_n):
        """
        ###################################################
        # contingency table general variable names:
        #     sample  background  row-sum
        # -------------------------------
        # +   a       b           r1
        # -------------------------------
        # -   c       d           r2
        # -------------------------------
        #     col_1   col_2       n
        #
        # what we've got as input:
        #     sample            background    row-sum
        # ----------------------------------------------
        # +   study_count       pop_count     r1
        # ----------------------------------------------
        # -   c                 d             r2
        # ----------------------------------------------
        #     study_n           pop_n         n
        #
        # fisher.pvalue_population() expects:
        #  (a, col_1, r1, n)
        #  (study_count, study_n, study_count + pop_count, study_n + pop_n)
        #
        # equivalent results using the following methods:
        # fisher.pvalue_population(a, col_1, r1, n)
        # fisher.pvalue(a, b, c, d)
        # scipy.stats.fisher_exact([[a, b], [c, d]])
        ###################################################
        :return: results-object
        """
        # Init study_count and pop_count to handle empty sets
        study_count = pop_count = 0
        for goid, study_count in list(term_study.items()):
            pop_count = term_pop[goid]
            a = study_count
            col_1 = study_n
            r1 = study_count + pop_count
            n = study_n + pop_n
            p = fisher.pvalue_population(a, col_1, r1, n)
            # if significantly enriched --> right_tail
            # if significantly purified --> left_tail
            if self.o_or_u_or_both == 'underrepresented':
                p_val_uncorrected = p.right_tail
            elif self.o_or_u_or_both == 'overrepresented':
                p_val_uncorrected = p.left_tail
            else:
                p_val_uncorrected = p.two_tail
            one_record = GOEnrichmentRecord(
                id=goid,
                p_uncorrected=p_val_uncorrected,
                ratio_in_study=(study_count, study_n),
                ratio_in_pop=(pop_count, pop_n),
                ANs_study = (',').join(self.get_ans_from_goid(goid, study=True)),
                ANs_pop = (',').join(self.get_ans_from_goid(goid, study=False)))
            self.results.append(one_record)
        self.calc_multiple_corrections(study_n, pop_n)

    def calc_multiple_corrections(self, study_n, pop_n):
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

    def print_summary(self, min_ratio=None, indent=False, pval=0.05):
        print("# min_ratio={0} pval={1}".format(min_ratio, pval))
        print("\t".join(GOEnrichmentRecord()._fields))
        for rec in self.results:
            rec.update_remaining_fields(min_ratio=min_ratio)
            if pval is not None and rec.p_bonferroni > pval:
                continue
            if rec.is_ratio_different:
                print(rec.__str__(indent=indent))

    def write_summary2file(self, fn_out, fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent):
        multitest_method_name = "p_" + self.multitest_method
        with open(fn_out, 'w') as fh_out:
            if len(self.results) == 0:
                fh_out.write("""unfortunately no results to write to file\n\npossible reasons:\n   threshold of reports too high\n\
   either no/few IDs could be mapped to keywords (correct species selected?)\n   abundance data\
missing (but option selected)\n\n\nDon't hesitate to contact us for feedback or questions!""")
            else:
                header2write = ('\t').join(self.results[0].get_attributenames2write(self.o_or_u_or_both)) + '\n'
                fh_out.write(header2write)
                results_sorted_by_fold_enrichment_study2pop = sorted(self.results, key=lambda record: record.fold_enrichment_study2pop, reverse=True)
                for rec in results_sorted_by_fold_enrichment_study2pop:
                    rec.update_remaining_fields()
                    if rec.fold_enrichment_study2pop >= fold_enrichment_study2pop or fold_enrichment_study2pop is None:
                        if rec.__dict__[multitest_method_name] <= p_value_mulitpletesting or p_value_mulitpletesting is None:
                            if rec.p_uncorrected <= p_value_uncorrected or p_value_uncorrected is None:
                                fh_out.write(rec.get_line2write(indent, self.o_or_u_or_both) + '\n')

    def write_summary2file_web(self, fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent):
        multitest_method_name = "p_" + self.multitest_method
        results2write = []
        if len(self.results) == 0:
            header2write = """unfortunately no results to write to file\n\npossible reasons:\n   threshold of reports too high\n\
either no/few IDs could be mapped to keywords (correct species selected?)\n   abundance data\
missing (but option selected)\n\n\nDon't hesitate to contact us for feedback or questions!"""
        else:
            header2write = '\t'.join(self.results[0].get_attributenames2write(self.o_or_u_or_both)) + '\n'
            results_sorted_by_fold_enrichment_study2pop = sorted(self.results, key=lambda record: record.fold_enrichment_study2pop, reverse=True)
            for rec in results_sorted_by_fold_enrichment_study2pop:
                rec.update_remaining_fields()
                if rec.fold_enrichment_study2pop >= fold_enrichment_study2pop or fold_enrichment_study2pop is None:
                    if rec.__dict__[multitest_method_name] <= p_value_mulitpletesting or p_value_mulitpletesting is None:
                        if rec.p_uncorrected <= p_value_uncorrected or p_value_uncorrected is None:
                            res = rec.get_line2write(indent, self.o_or_u_or_both)
                            results2write.append(res)
        return header2write.rstrip(), results2write


class GOEnrichmentStudy_UPK(GOEnrichmentStudy):

    def __init__(self, ui, assoc_dict, alpha, randomSample, abcorr, o_or_u_or_both, multitest_method):
        self.ui = ui
        self.assoc_dict = assoc_dict
        self.alpha = alpha
        self.multitest_method = multitest_method
        GOEnrichmentRecord_UPK.attributes_list += [("p_" + self.multitest_method, "%.3g"), ('ANs_study', '%s')]
        self.results = []
        self.randomSample = randomSample
        self.abcorr = abcorr
        if not self.abcorr:
            GOEnrichmentRecord_UPK.attributes_list.append(('ANs_pop', '%s'))
        self.o_or_u_or_both = o_or_u_or_both
        self.prepare_run()

    def prepare_run(self):
        if self.abcorr:
            self.study_an_frset = self.ui.get_sample_an_frset()
            self.term_study, self.upk2ans_study_dict = self.count_upk(self.study_an_frset, self.assoc_dict)
            study_n = len(self.study_an_frset)
            if self.randomSample:
                self.pop_an_set = self.ui.get_background_an_set_random_sample()
                pop_n  = len(self.pop_an_set)
                self.term_pop, self.upk2ans_pop_dict = self.count_upk(self.pop_an_set, self.assoc_dict)
            else:
                pop_n = len(self.study_an_frset)
                self.term_pop, self.upk2ans_pop_dict = self.count_upk_abundance_corrected(self.ui, self.assoc_dict)
        else:
            if self.ui.col_background_an == 'Genome':
                self.study_an_frset = self.ui.get_sample_an_frset_genome()
            else:
                self.study_an_frset = self.ui.get_sample_an_frset()
            self.term_study, self.upk2ans_study_dict = self.count_upk(self.study_an_frset, self.assoc_dict)
            study_n = len(self.study_an_frset)
            self.pop_an_set = self.ui.get_background_an_all_set()
            pop_n  = len(self.pop_an_set)
            self.term_pop, self.upk2ans_pop_dict = self.count_upk(self.pop_an_set, self.assoc_dict)
        self.run_study(self.term_study, self.term_pop, study_n, pop_n)

    def count_upk(self, ans_set, assoc_dict):
        """
        count the number of terms in the study group
        produces defaultsdict: key=UPKeyword, val=Num of occurrences
        upk2ans_dict: key=UPKeyword, val=ListOfANs
        """
        upk2ans_dict = {}
        term_cnt = defaultdict(int)
        for an in (acnum for acnum in ans_set if acnum in assoc_dict):
            for upk in assoc_dict[an]:
                term_cnt[upk] += 1
                if not upk2ans_dict.has_key(upk):
                    upk2ans_dict[upk] = set([an])
                else:
                    upk2ans_dict[upk].update([an])
        return(term_cnt, upk2ans_dict)

    def count_upk_abundance_corrected(self, ui, assoc_dict):
        """
        produce abundance corrected counts of UPK of background frequency
        round floats to nearest integer
        UserInput-object includes ANs of sample, and background as well as abundance data
        :param ui: UserInput-object
        :param assoc_dict:  Dict with key=AN, val=set of GO-terms
        :return: DefaultDict(Float)
        """
        upk2ans_dict = {}
        term_cnt = defaultdict(float)
        for ans, weight_fac in ui.iter_bins(): # for every bin, produce ans-background and weighting-factor
            for an in ans: # for every AccessionNumber
                if assoc_dict.has_key(an):
                    upk_set = assoc_dict[an]
                    for upk in upk_set:
                        term_cnt[upk] += weight_fac
                        if not upk2ans_dict.has_key(upk):
                            upk2ans_dict[upk] = set([an])
                        else:
                            upk2ans_dict[upk].update([an])
        for upk in term_cnt:
            term_cnt[upk] = int(round(term_cnt[upk]))
        upk2ans2return = {}
        for upk in term_cnt:
            count = term_cnt[upk]
            if count >=1:
                upk2ans2return[upk] = upk2ans_dict[upk]
        return(term_cnt, upk2ans2return)

    def get_ans_from_upk(self, upk, study):
        if study:
            if self.upk2ans_study_dict.has_key(upk):
                return sorted(self.upk2ans_study_dict[upk])
            else:
                return ''
        else:
            if self.upk2ans_pop_dict.has_key(upk):
                return sorted(self.upk2ans_pop_dict[upk])
            else:
                return ''

    def run_study(self, term_study, term_pop, study_n, pop_n):
        """
        ###################################################
        # contingency table general variable names:
        #     sample  background  row-sum
        # -------------------------------
        # +   a       b           r1
        # -------------------------------
        # -   c       d           r2
        # -------------------------------
        #     col_1   col_2       n
        #
        # what we've got as input:
        #     sample            background    row-sum
        # ----------------------------------------------
        # +   study_count       pop_count     r1
        # ----------------------------------------------
        # -   c                 d             r2
        # ----------------------------------------------
        #     study_n           pop_n         n
        #
        # fisher.pvalue_population() expects:
        #  (a, col_1, r1, n)
        #  (study_count, study_n, study_count + pop_count, study_n + pop_n)
        #
        # equivalent results using the following methods:
        # fisher.pvalue_population(a, col_1, r1, n)
        # fisher.pvalue(a, b, c, d)
        # scipy.stats.fisher_exact([[a, b], [c, d]])
        ###################################################
        :return: results-object
        """
        # Init study_count and pop_count to handle empty sets
        study_count = pop_count = 0
        for upk, study_count in list(term_study.items()):
            pop_count = term_pop[upk]
            a = study_count
            col_1 = study_n
            r1 = study_count + pop_count
            n = study_n + pop_n
            p = fisher.pvalue_population(a, col_1, r1, n)
            if self.o_or_u_or_both == 'overrepresented':
                p_val_uncorrected = p.right_tail
            elif self.o_or_u_or_both == 'underrepresented':
                p_val_uncorrected = p.left_tail
            else:
                p_val_uncorrected = p.two_tail
            one_record = GOEnrichmentRecord_UPK(
                id=upk,
                p_uncorrected=p_val_uncorrected,
                ratio_in_study=(study_count, study_n),
                ratio_in_pop=(pop_count, pop_n),
                ANs_study = (',').join(self.get_ans_from_upk(upk, study=True)),
                ANs_pop = (',').join(self.get_ans_from_upk(upk, study=False)))
            self.results.append(one_record)
        self.calc_multiple_corrections(study_n, pop_n)

    def calc_multiple_corrections(self, study_n, pop_n):
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

    def write_summary2file_web(self, fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected):
        multitest_method_name = "p_" + self.multitest_method
        results2write = []
        if len(self.results) == 0:
            header2write = """unfortunately no results to write to file\n\npossible reasons:\n   threshold of reports too high\n\
either no/few IDs could be mapped to keywords (correct species selected?)\n   abundance data\
missing (but option selected)\n\n\nDon't hesitate to contact us for feedback or questions!"""
        else:
            header2write = ('\t').join(self.results[0].get_attributenames2write(self.o_or_u_or_both)) + '\n'
            results_sorted_by_fold_enrichment_study2pop = sorted(self.results, key=lambda record: record.fold_enrichment_study2pop, reverse=True)
            for rec in results_sorted_by_fold_enrichment_study2pop:
                rec.update_remaining_fields()
                if rec.fold_enrichment_study2pop >= fold_enrichment_study2pop or fold_enrichment_study2pop is None:
                    if rec.__dict__[multitest_method_name] <= p_value_mulitpletesting or p_value_mulitpletesting is None:
                        if rec.p_uncorrected <= p_value_uncorrected or p_value_uncorrected is None:
                            res = rec.get_line2write(self.o_or_u_or_both)
                            results2write.append(res)
        return header2write.rstrip(), results2write












