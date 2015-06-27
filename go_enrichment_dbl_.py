#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
python %prog study.file population.file gene-association.file

This program returns P-values for functional enrichment in a cluster of
study genes using Fisher's exact test, and corrected for multiple testing
(including Bonferroni, Holm, Sidak, and false discovery rate)
"""
from __future__ import absolute_import
import fisher
from multiple_testing import Bonferroni, Sidak, HolmBonferroni, FDR, calc_qval_dbl
import ratio_dbl
from collections import defaultdict
import numpy

class GOEnrichmentRecord_old(object):
    """Represents one result (from a single GOTerm) in the GOEnrichmentStudy
    """
    _fields = "id enrichment fold_enrichment description ratio_in_study ratio_in_pop"\
              " p_uncorrected p_bonferroni p_holm p_sidak p_fdr ANs_study ANs_pop".split()

    def __init__(self, **kwargs):
        for f in self._fields:
            self.__setattr__(f, "n.a.")

        for k, v in kwargs.items():
            assert k in self._fields, "invalid field name %s" % k
            self.__setattr__(k, v)

        self.goterm = None  # the reference to the GOTerm

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __str__(self, indent=False):
        field_data = [self.__dict__[f] for f in self._fields]
        field_formatter = ["%s"] * 2 + ["%0.2f"] + ["%s"] + ["%d/%d"] * 2 + ["%.3g"] * 5 + ["%s"] * 2
        assert len(field_data) == len(field_formatter)
        # default formatting only works for non-"n.a" data
        for i, f in enumerate(field_data):
            if f == "n.a.":
                field_formatter[i] = "%s"
        # print dots to show the level of the term
        dots = ""
        if self.goterm is not None and indent:
            dots = "." * self.goterm.level
        return dots + "\t".join(a % b for (a, b) in zip(field_formatter, field_data))

    def __repr__(self):
        return "GOEnrichmentRecord(%s)" % self.id

    def find_goterm(self, go):
        if self.id in list(go.keys()):
            self.goterm = go[self.id]
            self.description = self.goterm.name

    def update_fields(self, **kwargs):
        for k, v in kwargs.items():
            assert k in self._fields, "invalid field name %s" % k
            self.__setattr__(k, v)

    def update_remaining_fields(self, min_ratio=None):
        study_count, study_n = self.ratio_in_study
        pop_count, pop_n = self.ratio_in_pop
        self.enrichment = 'e' if ((1.0 * study_count / study_n) > (1.0 * pop_count / pop_n)) else 'p'
        self.is_ratio_different = ratio_dbl.is_ratio_different(min_ratio, study_count, study_n, pop_count, pop_n)

class GOEnrichmentRecord(object):
    """
    Represents one result (from a single GOTerm) in the GOEnrichmentStudy
    """
    attributes_list = [('id', '%s'), ('enrichment', '%s'), ('perc_enrichment_study', "%0.1f"),
                   ('perc_enrichment_pop', "%0.1f"), ('fold_enrichment_study2pop', "%0.2f"),
                   ('study_count', '%s'), ('study_n', '%s'), ('pop_count','%s'), ('pop_n', '%s'),
                   ('description', '%s'), ('p_uncorrected', "%.3g"), ('p_bonferroni', "%.3g"),
                   ('p_holm', "%.3g"), ('p_sidak',"%.3g"), ('ANs_study', '%s'), ('ANs_pop', '%s'),
                   ('p_fdr', '%s')]

    def __init__(self, id, p_uncorrected, ratio_in_study, ratio_in_pop, ANs_study, ANs_pop):
        self.id = id
        self.p_uncorrected = p_uncorrected
        self.study_count, self.study_n = ratio_in_study
        self.pop_count, self.pop_n = ratio_in_pop
        self.ANs_study = ANs_study
        self.ANs_pop = ANs_pop
        self.perc_enrichment_study = self.calc_fold_enrichemnt(self.study_count, self.study_n)
        self.perc_enrichment_pop = self.calc_fold_enrichemnt(self.pop_count, self.pop_n)
        if self.perc_enrichment_study != -1 and self.perc_enrichment_pop != -1:
            self.fold_enrichment_study2pop = round(self.calc_fold_enrichemnt(self.perc_enrichment_study, self.perc_enrichment_pop), 2)
        else:
            self.fold_enrichment_study2pop = "-1"
        self.perc_enrichment_study = self.perc_enrichment_study * 100
        self.perc_enrichment_pop = self.perc_enrichment_pop * 100

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

    def update_remaining_fields(self, min_ratio=None):
        self.enrichment = 'e' if ((1.0 * self.study_count / self.study_n) > (1.0 * self.pop_count / self.pop_n)) else 'p'
        self.is_ratio_different = ratio_dbl.is_ratio_different(min_ratio, self.study_count, self.study_n, self.pop_count, self.pop_n)

    def get_attributenames2write(self, e_or_p_or_both):
        if e_or_p_or_both == None:
            return [name_format[0] for name_format in self.attributes_list]
        else:
            list2return = []
            for ele in self.attributes_list:
                if ele[0] != 'enrichment':
                    list2return.append(ele[0])
            return list2return

    def get_attributes_list(self, e_or_p_or_both):
        if e_or_p_or_both == None:
            return self.attributes_list
        else:
            list2return = []
            for ele in self.attributes_list:
                if ele[0] != 'enrichment':
                    list2return.append(ele)
            return list2return

    def get_attribute_format_list(self, indent, e_or_p_or_both):
        if indent:
            attributes_list = [('dot_id', '%s') if x[0] == 'id' else x for x in self.get_attributes_list(e_or_p_or_both)]
            dots = ''
            if self.goterm is not None:
                dots = "." * self.goterm.level
            self.dot_id = dots + self.id
        else:
            attributes_list = self.get_attributes_list(e_or_p_or_both)
        return attributes_list

    def get_attribute_formatted(self, attr_form):
        attr, form = attr_form
        try:
            val = self.__dict__[attr]
            attr2write = (form % val) + '\t'
        except KeyError:
            attr2write = 'n.a.' + '\t'
        return attr2write

    def get_line2write(self, indent, e_or_p_or_both):
        line2write = ''
        attribute_format_list = self.get_attribute_format_list(indent, e_or_p_or_both)
        for attr_form in attribute_format_list:
            line2write += self.get_attribute_formatted(attr_form)
        return line2write.rstrip()

class GOEnrichmentRecord_UPK(GOEnrichmentRecord):
    attributes_list = [('id', '%s'), ('enrichment', '%s'), ('perc_enrichment_study', "%0.1f"),
                   ('perc_enrichment_pop', "%0.1f"), ('fold_enrichment_study2pop', "%0.2f"),
                   ('study_count', '%s'), ('study_n', '%s'), ('pop_count','%s'), ('pop_n', '%s'),
                   ('p_uncorrected', "%.3g"), ('p_bonferroni', "%.3g"),
                   ('p_holm', "%.3g"), ('p_sidak',"%.3g"), ('ANs_study', '%s'), ('ANs_pop', '%s')]

    def get_attribute_format_list(self, e_or_p_or_both):
        return self.get_attributes_list(e_or_p_or_both)

    def get_line2write(self, e_or_p_or_both):
        line2write = ''
        attribute_format_list = self.get_attribute_format_list(e_or_p_or_both)
        for attr_form in attribute_format_list:
            line2write += self.get_attribute_formatted(attr_form)
        return line2write.rstrip()

class GOEnrichmentStudy(object):
    """Runs Fisher's exact test, as well as multiple corrections
    """
    def __init__(self, ui, assoc_dict, obo_dag, alpha, methods, backtracking, randomSample, abcorr, e_or_p_or_both):
        self.ui = ui
        self.assoc_dict = assoc_dict
        self.obo_dag = obo_dag
        self.alpha = alpha
        self.methods = methods
        self.results = []
        self.backtracking = backtracking
        self.randomSample = randomSample
        self.abcorr = abcorr
        self.e_or_p_or_both = e_or_p_or_both

        if self.backtracking: # add all parent GO-terms to assoc_dict
            self.obo_dag.update_association(self.assoc_dict)
        self.prepare_run()

    def prepare_run(self): # study_n should be the same in genome vs. observed vs. abundance_corrected
        '''
        :return: None
        '''
        if self.abcorr:
            self.study_an_frset = self.ui.get_sample_an_frset()
            self.term_study, self.go2ans_study_dict = ratio_dbl.count_terms(self.study_an_frset, self.assoc_dict, self.obo_dag)
            study_n = len(self.study_an_frset)

            if self.randomSample:
                self.pop_an_set = self.ui.get_background_an_set_random_sample()
                pop_n  = len(self.pop_an_set)
                self.term_pop, self.go2ans_pop_dict = ratio_dbl.count_terms(self.pop_an_set, self.assoc_dict, self.obo_dag)
            else:
                pop_n = len(self.study_an_frset)
                self.term_pop, self.go2ans_pop_dict = ratio_dbl.count_terms_abundance_corrected(self.ui, self.assoc_dict, self.obo_dag)

        else:
            if self.ui.col_background_an == 'Genome':
                self.study_an_frset = self.ui.get_sample_an_frset_genome()
            else:
                self.study_an_frset = self.ui.get_sample_an_frset()
            self.term_study, self.go2ans_study_dict = ratio_dbl.count_terms(self.study_an_frset, self.assoc_dict, self.obo_dag)
            study_n = len(self.study_an_frset)

            self.pop_an_set = self.ui.get_background_an_all_set()
            pop_n  = len(self.pop_an_set)
            self.term_pop, self.go2ans_pop_dict = ratio_dbl.count_terms(self.pop_an_set, self.assoc_dict, self.obo_dag)

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
            if self.e_or_p_or_both == 'enriched':
                p_val_uncorrected = p.right_tail
            elif self.e_or_p_or_both == 'purified':
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
        # Calculate multiple corrections
        pvals = [r.p_uncorrected for r in self.results]
        all_methods = ("bonferroni", "sidak", "holm", "benjamini_hochberg", "fdr")
        bonferroni, sidak, holm, fdr = None, None, None, None
        for method in self.methods:
            if method == "bonferroni":
                bonferroni = Bonferroni(pvals, self.alpha).corrected_pvals
            elif method == "sidak":
                sidak = Sidak(pvals, self.alpha).corrected_pvals
            elif method == "holm":
                holm = HolmBonferroni(pvals, self.alpha).corrected_pvals
            # elif method == "fdr":
            #     # get the empirical p-value distributions for FDR
            #     p_val_distribution = calc_qval_dbl(study_n, pop_n, self.pop_an_set, self.assoc_dict, self.term_pop, self.obo_dag)
            #     fdr = FDR(p_val_distribution,
            #               self.results, self.alpha).corrected_pvals
            elif method == "benjamini_hochberg":
                pass

            else:
                raise Exception("multiple test correction methods must be "
                                "one of %s" % all_methods)
        all_corrections = (bonferroni, sidak, holm, fdr)
        for method, corrected_pvals in zip(all_methods, all_corrections):
            self.update_results(method, corrected_pvals)
        self.results.sort(key=lambda r: r.p_uncorrected)
        # self.results = results
        for rec in self.results:
            # get go term for description and level
            rec.find_goterm(self.obo_dag)
        # return self.results

    def update_results(self, method, corrected_pvals):
        if corrected_pvals is None:
            return
        for rec, val in zip(self.results, corrected_pvals):
            rec.__setattr__("p_"+method, val)

    def print_summary(self, min_ratio=None, indent=False, pval=0.05):
        # Header contains parameters
        print("# min_ratio={0} pval={1}".format(min_ratio, pval))

        # field names for output
        print("\t".join(GOEnrichmentRecord()._fields))

        for rec in self.results:
            # calculate some additional statistics
            # (over_under, is_ratio_different)
            rec.update_remaining_fields(min_ratio=min_ratio)

            if pval is not None and rec.p_bonferroni > pval:
                continue

            if rec.is_ratio_different:
                print(rec.__str__(indent=indent))

    def write_summary2file_old(self, fn_out, min_ratio=None, indent=False, pval=0.05):
        '''
        as above just write to file instead of printing
        '''
        with open(fn_out, 'w') as fh_out:
            fh_out.write("# min_ratio={0} pval={1}".format(min_ratio, pval) + '\n')
            fh_out.write("\t".join(GOEnrichmentRecord()._fields) + '\n')
            # for rec in self.results: # sort by record.id, results=[record1, record2, ...]
            results_sorted_by_goterm  = sorted(self.results, key=lambda record: record.fold_enrichment, reverse=True)
            for rec in results_sorted_by_goterm:
                rec.update_remaining_fields(min_ratio=min_ratio)
                if pval is not None and rec.p_bonferroni > pval:
                    continue
                if rec.is_ratio_different:
                    fh_out.write(rec.__str__(indent=indent) + '\n')
        print("DONE :)") #!!!


    def write_summary2file(self, fn_out, min_ratio=None, indent=False, pval=0.05):
        # return self.results
        with open(fn_out, 'w') as fh_out:
            fh_out.write("# min_ratio={0} pval={1}".format(min_ratio, pval) + '\n')
            header2write = ('\t').join(self.results[0].get_attributenames2write(self.e_or_p_or_both)) + '\n'
            fh_out.write(header2write)
            results_sorted_by_fold_enrichment_study2pop = sorted(self.results, key=lambda record: record.fold_enrichment_study2pop, reverse=True)
            for rec in results_sorted_by_fold_enrichment_study2pop:
                rec.update_remaining_fields(min_ratio=min_ratio)
                if pval is not None and rec.p_bonferroni > pval:
                    continue
                if rec.is_ratio_different:
                    fh_out.write(rec.get_line2write(indent, self.e_or_p_or_both) + '\n')
        print("DONE :)") #!!!

class GOEnrichmentStudy_UPK(GOEnrichmentStudy):

    def __init__(self, ui, assoc_dict, alpha, methods, randomSample, abcorr, e_or_p_or_both):
        self.ui = ui
        self.assoc_dict = assoc_dict
        self.alpha = alpha
        self.methods = methods
        self.results = []
        self.randomSample = randomSample
        self.abcorr = abcorr
        self.e_or_p_or_both = e_or_p_or_both

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
            if self.e_or_p_or_both == 'enriched':
                p_val_uncorrected = p.right_tail
            elif self.e_or_p_or_both == 'purified':
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
        pvals = [r.p_uncorrected for r in self.results]
        all_methods = ("bonferroni", "sidak", "holm", "benjamini_hochberg", "fdr")
        bonferroni, sidak, holm, fdr = None, None, None, None
        for method in self.methods:
            if method == "bonferroni":
                bonferroni = Bonferroni(pvals, self.alpha).corrected_pvals
            elif method == "sidak":
                sidak = Sidak(pvals, self.alpha).corrected_pvals
            elif method == "holm":
                holm = HolmBonferroni(pvals, self.alpha).corrected_pvals
            # elif method == "fdr":
            #     # get the empirical p-value distributions for FDR
            #     p_val_distribution = calc_qval_dbl(study_n, pop_n, self.pop_an_set, self.assoc_dict, self.term_pop, self.obo_dag)
            #     fdr = FDR(p_val_distribution,
            #               self.results, self.alpha).corrected_pvals
            elif method == "benjamini_hochberg":
                pass

            else:
                raise Exception("multiple test correction methods must be "
                                "one of %s" % all_methods)
        all_corrections = (bonferroni, sidak, holm, fdr)
        for method, corrected_pvals in zip(all_methods, all_corrections):
            self.update_results(method, corrected_pvals)
        self.results.sort(key=lambda r: r.p_uncorrected)

    def write_summary2file(self, fn_out, min_ratio=None, pval=0.05):
        # return self.results
        with open(fn_out, 'w') as fh_out:
            fh_out.write("# min_ratio={0} pval={1}".format(min_ratio, pval) + '\n')
            header2write = ('\t').join(self.results[0].get_attributenames2write(self.e_or_p_or_both)) + '\n'
            fh_out.write(header2write)
            results_sorted_by_fold_enrichment_study2pop = sorted(self.results, key=lambda record: record.fold_enrichment_study2pop, reverse=True)
            for rec in results_sorted_by_fold_enrichment_study2pop:
                rec.update_remaining_fields(min_ratio=min_ratio)
                if pval is not None and rec.p_bonferroni > pval:
                    continue
                if rec.is_ratio_different:
                    fh_out.write(rec.get_line2write(self.e_or_p_or_both) + '\n')
        print("DONE :)") #!!!


















############################################################################################
############ testing goatools original fisher p-value caluculation
# #GO:0000030	p	mannosyltransferase activity	1/1159	39/4258	8.97e-05	0.443	0.419	0.432	n.a.
# #GO:0000062	e	fatty-acyl-CoA binding	1/1159	1/4258	0.272	1.35e+03	824	1.31e+03	n.a.
# #GO:0000075	p	cell cycle checkpoint	14/1159	56/4258	0.765	3.78e+03	749	3.68e+03	n.a.
#
# study = '14/1159'
# pop   = '56/4258'
# a, col_1 = study.split('/')
# r1, n = pop.split('/')
# a = int(a)
# col_1 = int(col_1)
# r1 = int(r1)
# n = int(n)
# col_2 = n - col_1
# b = r1 - a
# c = col_1 - a
# d = col_2 - b
# r2 = c + d
# assert n == col_1 + col_2
# assert n == r1 + r2
# print fisher.pvalue_population(a, col_1, r1, n)
# print fisher.pvalue(a, b, c, d)
# print scipy.stats.fisher_exact([[a, b], [c, d]])
############ testing goatools abundance corrected fisher p-value caluculation
# #GO:0000122	e	negative regulation of transcription from RNA polymerase II promoter
# #50/1159	21/1159	0.000635	3.14	3.08	3.06	n.a.
# import scipy, fisher
# study = '50/1159'
# pop   = '21/1159'
# a, col_1 = study.split('/')
# b, col_2 = pop.split('/')
# a = int(a)
# col_1 = int(col_1)
# b = int(b)
# col_2 = int(col_2)
# n = col_1 + col_2
# col_2 = n - col_1
# b = r1 - a
# c = col_1 - a
# d = col_2 - b
# r2 = c + d
# assert n == col_1 + col_2
# assert n == r1 + r2
# print fisher.pvalue_population(a, col_1, r1, n)
# print fisher.pvalue(a, b, c, d)
# print scipy.stats.fisher_exact([[a, b], [c, d]])
############################################################################################



                # try:
                #     study_ratio = float(study_count)/study_n
                #     pop_ratio = float(pop_count)/pop_n
                #     if pop_ratio == 0:
                #         fold_en = +inf
                #     elif study_ratio == 0:
                #         fold_en = _inf
                # except ZeroDivisionError:
                #     fold_en = -1
# None ...GO:0045239	e	0.6	0.2	3.84	7	1129	7	4337	tricarboxylic acid cycle enzyme complex	0.0138	8.31	7.54	8.1	P08417,P09624,P19262,P19955,P20967,P28241,P28834	P08417,P09624,P19262,P19955,P20967,P28241,P28834	n.a.
# enriched ...GO:0045239	0.6	0.2	3.84	7	1129	7	4337	tricarboxylic acid cycle enzyme complex	0.0138	8.31	7.8	8.1	P08417,P09624,P19262,P19955,P20967,P28241,P28834	P08417,P09624,P19262,P19955,P20967,P28241,P28834	n.a.
# purified ...GO:0045239	0.6	0.2	3.84	7	1129	7	4337	tricarboxylic acid cycle enzyme complex	0.997	602	27.9	587	P08417,P09624,P19262,P19955,P20967,P28241,P28834	P08417,P09624,P19262,P19955,P20967,P28241,P28834	n.a.
# Pvalue(left_tail=0.9971, right_tail=0.01376, two_tail=0.01376)
#
# None ....GO:0016023	p	0.3	1.0	0.26	3	1129	44	4337	cytoplasmic membrane-bounded vesicle	0.0109	6.6	6.03	6.43	P07560,P41810,P43555	P07560,P08004,P11075,P17065,P19524,P22146,P22213,P22804,P25560,P27351,P29465,P32486,P32803,P36122,P38221,P38261,P38312,P38682,P38856,P38869,P39704,P39727,P39980,P40955,P41810,P43555,P47018,P47102,P53039,P53173,P53309,P53337,P53633,P53845,P54837,Q00381,Q04322,Q04651,Q05359,Q08754,Q12344,Q12396,Q12674,Q3E834	n.a.
# enriched ....GO:0016023	0.3	1.0	0.26	3	1129	44	4337	cytoplasmic membrane-bounded vesicle	0.998	603	25	588	P07560,P41810,P43555	P07560,P08004,P11075,P17065,P19524,P22146,P22213,P22804,P25560,P27351,P29465,P32486,P32803,P36122,P38221,P38261,P38312,P38682,P38856,P38869,P39704,P39727,P39980,P40955,P41810,P43555,P47018,P47102,P53039,P53173,P53309,P53337,P53633,P53845,P54837,Q00381,Q04322,Q04651,Q05359,Q08754,Q12344,Q12396,Q12674,Q3E834	n.a.
# purified ....GO:0016023	0.3	1.0	0.26	3	1129	44	4337	cytoplasmic membrane-bounded vesicle	0.00688	4.15	3.99	4.05	P07560,P41810,P43555	P07560,P08004,P11075,P17065,P19524,P22146,P22213,P22804,P25560,P27351,P29465,P32486,P32803,P36122,P38221,P38261,P38312,P38682,P38856,P38869,P39704,P39727,P39980,P40955,P41810,P43555,P47018,P47102,P53039,P53173,P53309,P53337,P53633,P53845,P54837,Q00381,Q04322,Q04651,Q05359,Q08754,Q12344,Q12396,Q12674,Q3E834	n.a.
# Pvalue(left_tail=0.006879, right_tail=0.9984, two_tail=0.01093)