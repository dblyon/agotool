#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
A list of commonly used multiple correction routines
"""
from __future__ import print_function
from __future__ import absolute_import
import sys
import random
import fisher
import numpy as np
from ratio_dbl import count_terms


class AbstractCorrection(object):

    def __init__(self, pvals, a=.05):
        self.pvals = self.corrected_pvals = np.array(pvals)
        self.n = len(self.pvals)    # number of multiple tests
        self.a = a                  # type-1 error cutoff for each test
        self.set_correction()

    def set_correction(self):
        # the purpose of multiple correction is to lower the alpha
        # instead of the canonical value (like .05)
        pass


class Bonferroni(AbstractCorrection):
    """
    >>> Bonferroni([0.01, 0.01, 0.03, 0.05, 0.005], a=0.05).corrected_pvals
    array([ 0.05 ,  0.05 ,  0.15 ,  0.25 ,  0.025])
    """
    def set_correction(self):
        self.corrected_pvals *= self.n


class Sidak(AbstractCorrection):
    """http://en.wikipedia.org/wiki/Bonferroni_correction
    >>> Sidak([0.01, 0.01, 0.03, 0.05, 0.005], a=0.05).corrected_pvals
    array([ 0.04898974,  0.04898974,  0.14696923,  0.24494871,  0.02449487])
    """

    def set_correction(self):
        if self.n != 0:
            correction = self.a * 1. / (1 - (1 - self.a) ** (1. / self.n))
        else:
            correction = 1
        self.corrected_pvals *= correction


class HolmBonferroni(AbstractCorrection):

    """http://en.wikipedia.org/wiki/Holm-Bonferroni_method
    given a list of pvals, perform the Holm-Bonferroni correction
    and return the indexes from original list that are significant.
    (cant use p-value as that may be repeated.)
    >>> HolmBonferroni([0.01, 0.01, 0.03, 0.05, 0.005], a=0.05).corrected_pvals
    array([ 0.04 ,  0.04 ,  0.06 ,  0.05 ,  0.025])
    """
    def set_correction(self):
        if len(self.pvals):
            idxs, correction = list(zip(*self.generate_significant()))
            idxs = list(idxs)
            self.corrected_pvals[idxs] *= correction

    def generate_significant(self):

        pvals = self.pvals
        pvals_idxs = list(zip(pvals, list(range(len(pvals)))))
        pvals_idxs.sort()

        lp = len(self.pvals)

        from itertools import groupby
        for pval, idxs in groupby(pvals_idxs, lambda x: x[0]):
            idxs = list(idxs)
            for p, i in idxs:
                if p * 1. / lp < self.a:
                    yield (i, lp)
            lp -= len(idxs)


class FDR(object):
    def __init__(self, p_val_distribution, results, a=.05):
        self.corrected_pvals = fdr = []
        for rec in results:
            q = (sum(1 for x in p_val_distribution if x < rec.p_uncorrected)
                 * 1.0 / len(p_val_distribution))
            fdr.append(q)


"""
Generate a p-value distribution based on re-sampling, as described in:
http://www.biomedcentral.com/1471-2105/6/168
"""


# def calc_qval(study_count, study_n, pop_count, pop_n, pop, assoc, term_pop, obo_dag, T=500):
#     print(("Generate p-value distribution for FDR "
#            "based on resampling (this might take a while)"), file=sys.stderr)
#     distribution = []
#     for i in range(T):
#         new_study = random.sample(pop, study_n)
#         new_term_study = count_terms(new_study, assoc, obo_dag)
#         smallest_p = 1
#         for term, study_count in list(new_term_study.items()):
#             pop_count = term_pop[term]
#             p = fisher.pvalue_population(study_count, study_n, pop_count, pop_n)
#             if p.two_tail < smallest_p:
#                 smallest_p = p.two_tail
#         distribution.append(smallest_p)
#         if i % 10  == 0:
#             print("Sample {0} / {1}: p-value {2}".\
#                         format(i, T, smallest_p), file=sys.stderr)
#     return distribution

def calc_qval_dbl(study_n, pop_n, pop, assoc, term_pop, obo_dag, T=500):
    """
    :param study_n: Integer (number of ANs from sample frequency)
    :param pop_n: Integer (number of ANs from background frequency = sample freq.)
    :param pop:
    :param assoc:
    :param term_pop:
    :param obo_dag:
    :param T:
    :return:
    """
    distribution = []
    for i in range(T):
        new_study = random.sample(pop, study_n) # add pop and study
        new_term_study = count_terms(new_study, assoc, obo_dag)[0] #!!!
        smallest_p = 1
        for term, study_count in list(new_term_study.items()):
            pop_count = term_pop[term]
            a = study_count
            col_1 = study_n
            r1 = study_count + pop_count
            n = study_n + pop_n
            p = fisher.pvalue_population(a, col_1, r1, n)
            if p.two_tail < smallest_p:
                smallest_p = p.two_tail
        distribution.append(smallest_p)
        if i % 10  == 0:
            print("Sample {0} / {1}: p-value {2}".\
                        format(i, T, smallest_p), file=sys.stderr)
    return distribution


def BenjaminiHochberg(pvals, num_total_tests):
    '''
    expects a sorted (ascending) list of uncorrected p-values
    and the total number of tests
    http://stats.stackexchange.com/questions/870/multiple-hypothesis-testing-correction-with-benjamini-hochberg-p-values-or-q-va
    http://projecteuclid.org/DPubS?service=UI&version=1.0&verb=Display&handle=euclid.aos/1074290335
    :param pvals: ListOfFloat
    :param num_total_tests: Integer
    :return: ListOfFloat
    '''
    p_values = np.array(pvals)
    p_values_corrected = []
    prev_bh_value = 0
    for i, p_value in enumerate(p_values):
        bh_value = p_value * num_total_tests / (i + 1)
        # Sometimes this correction can give values greater than 1,
        # so we set those values at 1
        bh_value = min(bh_value, 1)
        # To preserve monotonicity in the values, we take the
        # maximum of the previous value or this one, so that we
        # don't yield a value less than the previous.
        bh_value = max(bh_value, prev_bh_value)
        prev_bh_value = bh_value
        p_values_corrected.append(bh_value)
    return p_values_corrected


# def calc_benjamini_hochberg_corrections(p_values, num_total_tests):
#     """
#     Calculates the Benjamini-Hochberg correction for multiple hypothesis
#     testing from a list of p-values *sorted in ascending order*.
#
#     See
#     http://en.wikipedia.org/wiki/False_discovery_rate#Independent_tests
#     for more detail on the theory behind the correction.
#
#     **NOTE:** This is a generator, not a function. It will yield values
#     until all calculations have completed.
#
#     :Parameters:
#     - `p_values`: a list or iterable of p-values sorted in ascending
#       order
#     - `num_total_tests`: the total number of tests (p-values)
#
#     """
#     prev_bh_value = 0
#     for i, p_value in enumerate(p_values):
#         bh_value = p_value * num_total_tests / (i + 1)
#         # Sometimes this correction can give values greater than 1,
#         # so we set those values at 1
#         bh_value = min(bh_value, 1)
#         # To preserve monotonicity in the values, we take the
#         # maximum of the previous value or this one, so that we
#         # don't yield a value less than the previous.
#         bh_value = max(bh_value, prev_bh_value)
#         prev_bh_value = bh_value
#         yield bh_value


if __name__ == '__main__':
    import doctest
    doctest.testmod()
