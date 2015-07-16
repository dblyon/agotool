import sys
import unittest
import obo_parser

sys.path.append('/Users/dblyon/modules/cpr/goterm/agotool/static/python')
import cluster_filter
from unittest import TestCase
import pandas as pd
import numpy as np
from os.path import expanduser


class TestFilter(TestCase):
    """
    # example 1
    # before
    # .....GO:0031326	5.33e-05 # term
    # ...GO:0019222	0.00324 # parent
    # ......GO:2001141	5.46e-05 # child
    # .....GO:0010556	0.000122 # sister
    # after
    # .....GO:0031326	5.33e-05 # term
    # .....GO:0010556	0.000122 # sister

    # example 2
    # before
    # ...GO:0016021	1.23e-10 # term
    # ....GO:0031361	1.23e-09 # child
    # ....GO:0031224	1.23e-08 # parent
    # ....GO:0044425	1.23e-08 # parent
    # ....GO:0031360	1.23e-11 # sibling
    # after
    # ...GO:0016021	1.23e-10 # term
    # ....GO:0031360	1.23e-11 # sibling

    #example 3
    # before
    # GO:0008150	0.00141 # blacklist BP
    # GO:0005575	0.00453 # blacklist CP
    # GO:0003674	0.000145 # blacklist MF
    # after
    # None of the above

    # example ABC
    # A = parent to B and C
    # B and C are siblings
    # p-value sorted order:
    # CBA --> CB
    # CAB --> CB
    # ABC --> A
    """
    @classmethod
    def setUpClass(cls):
        fn = r'/Users/dblyon/modules/cpr/goterm/agotool/static/data/OBO/go-basic.obo'
        go_dag = obo_parser.GODag(obo_file=fn)
        cls._cf = cluster_filter.Filter(go_dag)
        # files to test before and after filtering
        cls._fn_indent = r'/Users/dblyon/modules/cpr/goterm/agotool/static/python/test/Results_TestFilter_indent.txt'
        cls._fn_indent_after = r'/Users/dblyon/modules/cpr/goterm/agotool/static/python/test/Results_TestFilter_indent_after.txt'
        cls._fn_NoIndent = r'/Users/dblyon/modules/cpr/goterm/agotool/static/python/test/Results_TestFilter_NoIndent.txt'
        cls._fn_NoIndent_after = r'/Users/dblyon/modules/cpr/goterm/agotool/static/python/test/Results_TestFilter_NoIndent_after.txt'
        cls._fn_ABC = r'/Users/dblyon/modules/cpr/goterm/agotool/static/python/test/Results_TestFilter_ABC.txt'
        cls._fn_ABC_after = r'/Users/dblyon/modules/cpr/goterm/agotool/static/python/test/Results_TestFilter_ABC_after.txt'
        cls._fn_CAB = r'/Users/dblyon/modules/cpr/goterm/agotool/static/python/test/Results_TestFilter_CAB.txt'
        cls._fn_CAB_after = r'/Users/dblyon/modules/cpr/goterm/agotool/static/python/test/Results_TestFilter_CAB_after.txt'
        cls._fn_CBA = r'/Users/dblyon/modules/cpr/goterm/agotool/static/python/test/Results_TestFilter_CBA.txt'
        cls._fn_CBA_after = r'/Users/dblyon/modules/cpr/goterm/agotool/static/python/test/Results_TestFilter_CBA_after.txt'

    def get_header_results(self, fn):
        results = []
        with open(fn, 'r') as fh:
            for line in fh:
                res2append = line.strip().split('\t')
                if len(res2append) > 1:
                    results.append(res2append)
        header = results[0]
        results = results[1:]
        return header, results

    def test_filter_term_lineage_indent(self):
        fn_before = self._fn_indent
        fn_after = self._fn_indent_after
        header_b, results_b = self.get_header_results(fn_before)
        header_a, results_a = self.get_header_results(fn_after)
        indent = True
        computed = self._cf.filter_term_lineage(header_b, results_b, indent)
        expected = results_a
        self.assertEqual(computed, expected)

    def test_filter_term_lineage_NoIndent(self):
        fn_before = self._fn_NoIndent
        fn_after = self._fn_NoIndent_after
        header_b, results_b = self.get_header_results(fn_before)
        header_a, results_a = self.get_header_results(fn_after)
        indent = False
        computed = self._cf.filter_term_lineage(header_b, results_b, indent)
        expected = results_a
        self.assertEqual(computed, expected)

    def test_filter_term_lineage_ident_ABC(self):
        fn_before = self._fn_ABC
        fn_after = self._fn_ABC_after
        header_b, results_b = self.get_header_results(fn_before)
        header_a, results_a = self.get_header_results(fn_after)
        indent = True
        computed = self._cf.filter_term_lineage(header_b, results_b, indent)
        expected = results_a
        self.assertEqual(computed, expected)

    def test_filter_term_lineage_ident_CAB(self):
        fn_before = self._fn_CAB
        fn_after = self._fn_CAB_after
        header_b, results_b = self.get_header_results(fn_before)
        header_a, results_a = self.get_header_results(fn_after)
        indent = True
        computed = self._cf.filter_term_lineage(header_b, results_b, indent)
        expected = results_a
        self.assertEqual(computed, expected)

    def test_filter_term_lineage_ident_CBA(self):
        fn_before = self._fn_CBA
        fn_after = self._fn_CBA_after
        header_b, results_b = self.get_header_results(fn_before)
        header_a, results_a = self.get_header_results(fn_after)
        indent = True
        computed = self._cf.filter_term_lineage(header_b, results_b, indent)
        expected = results_a
        self.assertEqual(computed, expected)



suite = unittest.TestLoader().loadTestsFromTestCase(TestFilter)
unittest.TextTestRunner(verbosity=2).run(suite)
