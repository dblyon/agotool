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
            self.fold_enrichment_study2pop = str(round(self.calc_fold_enrichemnt(self.perc_enrichment_study, self.perc_enrichment_pop), 2))
        else:
            self.fold_enrichment_study2pop = "-1"
        self.perc_enrichment_study = int(round(self.perc_enrichment_study * 100))
        self.perc_enrichment_pop = int(round(self.perc_enrichment_pop * 100))
        # self.study_count = str(self.study_count)
        # self.study_n = str(self.study_n)
        # self.pop_count = str(self.pop_count)
        # self.pop_n = str(self.pop_n)



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

    def get_attributes2write(self):
# id	enrichment	fold_enrichment	description	ratio_in_study	ratio_in_pop	p_uncorrected	p_bonferroni	p_holm	p_sidak	p_fdr	ANs_study	ANs_pop
# ....GO:0016624	e	3.84	oxidoreductase activity, acting on the aldehyde or oxo group of donors, disulfide as acceptor	5/1129	5/4337	0.0372	182	163	178	n.a.	P09624,P16387,P19955,P20967,P32473	P09624,P16387,P19955,P20967,P32473

        header_list = ['id', 'enrichment', 'perc_enrichment_study', 'perc_enrichment_pop', 'fold_enrichment_study2pop', 'study_count',
                       'study_n', 'pop_count', 'pop_n', 'description', 'p_uncorrected', 'p_bonferroni', 'p_holm', 'p_sidak', 'ANs_study', 'ANs_pop'] # 'p_fdr'
        return header_list

    def get_line2write(self, indent):
        attributes2write_list = self.get_attributes2write()
        if indent:
            attributes2write_list = ['dot_id' if x=='id' else x for x in attributes2write_list]
            dots = ''
            if self.goterm is not None:
                dots = "." * self.goterm.level
            self.dot_id = dots + self.id
        return self.get_attributes_formatted(attributes2write_list)

    def get_attributes_formatted(self, attributes_list):
        string2write = ""
        for attribute in attributes_list:
            attr2write = self.__dict__[attribute]
            if type(attr2write) == str:
                pass
            elif type(attr2write) == float:
                attr2write == str(round(attr2write, 2))
            elif type(attr2write) == int:
                attr2write == str(attr2write)
            else:
                try:
                    attr2write = str(attr2write)
                except:
                    attr2write = 'bubu'
            print(attr2write, type(attr2write))
            string2write += attr2write + '\t'
        return string2write.rstrip()


class GOEnrichmentStudy(object):
    """Runs Fisher's exact test, as well as multiple corrections
    """
    def __init__(self, ui, assoc_dict, obo_dag, alpha, methods, backtracking, randomSample, abcorr):
        self.ui = ui
        self.assoc_dict = assoc_dict
        self.obo_dag = obo_dag
        self.alpha = alpha
        self.methods = methods
        self.results = []
        self.backtracking = backtracking
        self.randomSample = randomSample
        self.abcorr = abcorr

        if self.backtracking: # add all parent GO-terms to assoc_dict
            self.obo_dag.update_association(self.assoc_dict)

        self.prepare_run()

    # def prepare_run(self):
    #     '''
    #     :return: None
    #     '''
    #     self.study_an_frset = self.ui.get_study_an_frset()
    #     self.term_study, self.go2ans_study_dict = ratio_dbl.count_terms(self.study_an_frset, self.assoc_dict, self.obo_dag)
    #     # study_n = len(self.study_an_frset)
    #     if self.abcorr:
    #         self.study_an_frset = self.ui.get_study_an_frset()
    #         self.term_study, self.go2ans_study_dict = ratio_dbl.count_terms(self.study_an_frset, self.assoc_dict, self.obo_dag)
    #         study_n = len(self.study_an_frset)
    #         if self.randomSample:
    #             self.pop_an_set = self.ui.get_population_an_set_random_sample()
    #             pop_n  = len(self.pop_an_set)
    #             self.term_pop, self.go2ans_pop_dict = ratio_dbl.count_terms(self.pop_an_set, self.assoc_dict, self.obo_dag)
    #         else:
    #             pop_n = len(self.study_an_frset)
    #             self.term_pop, self.go2ans_pop_dict = ratio_dbl.count_terms_abundance_corrected(self.ui, self.assoc_dict, self.obo_dag)
    #     else:
    #         self.study_an_frset = self.ui.get_study_an_frset_all()
    #         self.term_study, self.go2ans_study_dict = ratio_dbl.count_terms(self.study_an_frset, self.assoc_dict, self.obo_dag)
    #         study_n = len(self.study_an_frset)
    #         self.pop_an_set = self.ui.get_population_an_set_all()
    #         pop_n  = len(self.pop_an_set)
    #         self.term_pop, self.go2ans_pop_dict = ratio_dbl.count_terms(self.pop_an_set, self.assoc_dict, self.obo_dag)
    #     self.run_study_v2(self.term_study, self.term_pop, study_n, pop_n)

    def prepare_run(self): # study_n should be the same in genome vs. observed vs. abundance_corrected
        '''
        :return: None
        '''
        # self.study_an_frset = self.ui.get_study_an_frset()
        # self.term_study, self.go2ans_study_dict = ratio_dbl.count_terms(self.study_an_frset, self.assoc_dict, self.obo_dag)
        # if self.abcorr:
        #     self.study_an_frset = self.ui.get_study_an_frset()
        #     self.term_study, self.go2ans_study_dict = ratio_dbl.count_terms(self.study_an_frset, self.assoc_dict, self.obo_dag)
        #     study_n = len(self.study_an_frset)
        #     if self.randomSample:
        #         self.pop_an_set = self.ui.get_population_an_set_random_sample()
        #         pop_n  = len(self.pop_an_set)
        #         self.term_pop, self.go2ans_pop_dict = ratio_dbl.count_terms(self.pop_an_set, self.assoc_dict, self.obo_dag)
        #     else:
        #         pop_n = len(self.study_an_frset)
        #         self.term_pop, self.go2ans_pop_dict = ratio_dbl.count_terms_abundance_corrected(self.ui, self.assoc_dict, self.obo_dag)
        # else:
        #     self.study_an_frset = self.ui.get_study_an_frset()
        #     self.term_study, self.go2ans_study_dict = ratio_dbl.count_terms(self.study_an_frset, self.assoc_dict, self.obo_dag)
        #     study_n = len(self.study_an_frset)
        #     self.pop_an_set = self.ui.get_population_an_set_all()
        #     pop_n  = len(self.pop_an_set)
        #     self.term_pop, self.go2ans_pop_dict = ratio_dbl.count_terms(self.pop_an_set, self.assoc_dict, self.obo_dag)
        # self.run_study_v2(self.term_study, self.term_pop, study_n, pop_n)


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
            one_record = GOEnrichmentRecord(
                id=goid,
                p_uncorrected=p.two_tail,
                ratio_in_study=(study_count, study_n),
                ratio_in_pop=(pop_count, pop_n),
                ANs_study = (',').join(self.get_ans_from_goid(goid, study=True)),
                ANs_pop = (',').join(self.get_ans_from_goid(goid, study=False)))
            self.results.append(one_record)
        self.calc_multiple_corrections()

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
        study_n = pop_n = len(self.study_an_frset)
        # Init study_count and pop_count to handle empty sets
        study_count = pop_count = 0
        for goid, study_count in list(self.term_study.items()):
            pop_count = self.term_pop[goid]
            a = study_count
            col_1 = study_n
            r1 = study_count + pop_count
            n = study_n + pop_n
            p = fisher.pvalue_population(a, col_1, r1, n)
            try:
                fold_en = (float(study_count)/study_n) / (float(pop_count)/pop_n)
            except ZeroDivisionError:
                fold_en = -1
            one_record = GOEnrichmentRecord(
                id=goid,
                fold_enrichment= fold_en,
                p_uncorrected=p.two_tail,
                ratio_in_study=(study_count, study_n),
                ratio_in_pop=(pop_count, pop_n),
                ANs_study = (',').join(self.get_ans_from_goid(goid, study=True)),
                ANs_pop = (',').join(self.get_ans_from_goid(goid, study=False)))
            self.results.append(one_record)
        self.calc_multiple_corrections()

    def calc_multiple_corrections(self):
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
            elif method == "fdr":
                # get the empirical p-value distributions for FDR
                p_val_distribution = calc_qval_dbl(study_n, pop_n, self.pop_an_set, self.assoc_dict, self.term_pop, self.obo_dag)
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
        with open(fn_out, 'w') as fh_out:
            fh_out.write("# min_ratio={0} pval={1}".format(min_ratio, pval) + '\n')
            header2write = ('\t').join(self.results[0].get_attributes2write()) + '\n'
            fh_out.write(header2write)
            results_sorted_by_fold_enrichment_study2pop = sorted(self.results, key=lambda record: record.fold_enrichment_study2pop, reverse=True)
            for rec in results_sorted_by_fold_enrichment_study2pop:
                rec.update_remaining_fields(min_ratio=min_ratio)
                if pval is not None and rec.p_bonferroni > pval:
                    continue
                if rec.is_ratio_different:
                    fh_out.write(rec.get_line2write(indent=indent) + '\n')
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
