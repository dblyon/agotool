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
from scipy import stats

class GOEnrichmentRecord(object):
    """Represents one result (from a single GOTerm) in the GOEnrichmentStudy
    """
    _fields = "id enrichment description ratio_in_study ratio_in_pop"\
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
        field_formatter = ["%s"] * 3 + ["%d/%d"] * 2 + ["%.3g"] * 5 + ["%s"] * 2
        assert len(field_data) == len(field_formatter)

        # default formatting only works for non-"n.a" data
        for i, f in enumerate(field_data):
            if f == "n.a.":
                field_formatter[i] = "%s"

        # print dots to show the level of the term
        dots = ""
        if self.goterm is not None and indent:
            dots = "." * self.goterm.level

        return dots + "\t".join(a % b for (a, b) in
                                zip(field_formatter, field_data))

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
        self.enrichment = 'e' if ((1.0 * study_count / study_n) >
                                  (1.0 * pop_count / pop_n)) else 'p'
        self.is_ratio_different = ratio_dbl.is_ratio_different(min_ratio, study_count,
                                                     study_n, pop_count, pop_n)


class GOEnrichmentStudy(object):
    """Runs Fisher's exact test, as well as multiple corrections
    """
    def __init__(self, study_an_frset, pop_an_set, assoc_dict, obo_dag, ui, alpha, methods, backtracking):

        self.study_an_frset = study_an_frset
        self.pop = pop_an_set
        self.assoc_dict = assoc_dict # dict: key=AN, val=set of go-terms
        self.obo_dag = obo_dag
        self.ui = ui
        self.alpha = alpha
        self.methods = methods
        self.results = []
        if backtracking:
            obo_dag.update_association(assoc_dict) # add all parent GO-terms to assoc_dict
        self.term_pop, self.go2ans_pop_dict = ratio_dbl.count_terms_abundance_corrected(ui, assoc_dict, obo_dag)

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

    def run_study(self):
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
        study_an_frset = self.study_an_frset
        results = self.results
        term_study, self.go2ans_study_dict = ratio_dbl.count_terms(study_an_frset, self.assoc_dict, self.obo_dag)
        pop_n = study_n = len(study_an_frset)

        # Init study_count and pop_count to handle empty sets
        study_count = pop_count = 0
        for goid, study_count in list(term_study.items()):
            pop_count = int(round(self.term_pop[goid]))
            # p = fisher.pvalue_population(study_count, study_n, pop_count, pop_n)
            a = study_count
            col_1 = study_n
            r1 = study_count + pop_count
            n = study_n + pop_n
            p = fisher.pvalue_population(a, col_1, r1, n)
            one_record = GOEnrichmentRecord(
                id=goid,
                p_uncorrected=p.two_tail,
                ratio_in_study=(study_count, study_n),
                ratio_in_pop=(pop_count, pop_n),
                ANs_study = (',').join(self.get_ans_from_goid(goid, study=True)),
                ANs_pop = (',').join(self.get_ans_from_goid(goid, study=False)))
            results.append(one_record)

        # Calculate multiple corrections
        pvals = [r.p_uncorrected for r in results]
        all_methods = ("bonferroni", "sidak", "holm", "benjamini_hochberg", "fdr")
        bonferroni, sidak, holm, fdr = None, None, None, None

        for method in self.methods:
            if method == "bonferroni":
                bonferroni = Bonferroni(pvals, self.alpha).corrected_pvals
            elif method == "sidak":
                sidak = Sidak(pvals, self.alpha).corrected_pvals
            elif method == "holm":
                holm = HolmBonferroni(pvals, self.alpha).corrected_pvals
            elif method == "fdr":
                # get the empirical p-value distributions for FDR
                # p_val_distribution = calc_qval(study_count, study_n,
                #                                pop_count, pop_n,
                #                                self.pop, self.assoc_dict,
                #                                self.term_pop, self.obo_dag)
                p_val_distribution = calc_qval_dbl(study_n, pop_n, self.pop, self.assoc_dict, self.term_pop, self.obo_dag)
                fdr = FDR(p_val_distribution,
                          results, self.alpha).corrected_pvals
            elif method == "benjamini_hochberg":
                pass

            else:
                raise Exception("multiple test correction methods must be "
                                "one of %s" % all_methods)

        all_corrections = (bonferroni, sidak, holm, fdr)

        for method, corrected_pvals in zip(all_methods, all_corrections):
            self.update_results(method, corrected_pvals)

        results.sort(key=lambda r: r.p_uncorrected)
        self.results = results

        for rec in results:
            # get go term for description and level
            rec.find_goterm(self.obo_dag)

        return results

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

    def write_summary2file(self, fn_out, min_ratio=None, indent=False, pval=0.05):
        '''
        as above just write to file instead of printing
        '''
        with open(fn_out, 'w') as fh_out:
            fh_out.write("# min_ratio={0} pval={1}".format(min_ratio, pval) + '\n')
            fh_out.write("\t".join(GOEnrichmentRecord()._fields) + '\n')
            # for rec in self.results: # sort by record.id, results=[record1, record2, ...]
            results_sorted_by_goterm  = sorted(self.results, key=lambda record: record.id)
            for rec in results_sorted_by_goterm:
                rec.update_remaining_fields(min_ratio=min_ratio)
                if pval is not None and rec.p_bonferroni > pval:
                    continue
                if rec.is_ratio_different:
                    fh_out.write(rec.__str__(indent=indent) + '\n')
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


