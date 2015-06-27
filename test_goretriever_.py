import unittest, goretriever, find_enrichment
from os.path import expanduser
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
import pandas as pd
import numpy as np
import cPickle as pickle
from unittest import TestCase

home = expanduser("~")


__author__ = 'dblyon'


# class TestGoretriever(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     @classmethod
#     def setUpClass(cls):
#         # cls._gor = goretriever.Goretriever()
#         cls._gor = goretriever.Parser_UniProt_goa_ref()
#         fn_goa_ref = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/yeast/gene_association.goa_yeast'
#         cls._gor.parse_goa_ref(fn_goa_ref)
#
#         # ans_list_pickled_fn_v1 = r"C:\Users\dblyon\CloudStation\CPR\Brian_GO\UniProt_data\yeast\Yeast_AccessionNumbersList_v1.p"
#         # cls._ans_list_v1 = pickle.load(open(ans_list_pickled_fn_v1, "rb"))
#         # ans_list_pickled_fn_v2 = r"C:\Users\dblyon\CloudStation\CPR\Brian_GO\UniProt_data\yeast\Yeast_AccessionNumbersList_v2.p"
#         # cls._ans_list_v2 = pickle.load(open(ans_list_pickled_fn_v2, "rb"))
#
#     def test_get_goterms_from_an_1(self):
#         an = "P07261"
#         goterm_list = ['GO:0000433', 'GO:0000978', 'GO:0001077', 'GO:0005635', 'GO:0006351', 'GO:0034728', 'GO:0045944',
#                        'GO:0060963', 'GO:0061435', 'GO:0072363']
#         self.assertEqual(self._gor.get_goterms_from_an(an), goterm_list)
#
#     def test_get_goterms_from_an_2(self):
#         an = ""
#         self.assertEqual(self._gor.get_goterms_from_an(an), -1)
#
#     # def test_get_goterms_from_an_4(self):
#     #     """
#     #     test whether every AccessionNumber from Brian's enrichment experiment is present in an2go_dict
#     #     includes redundant entries
#     #     """
#     #     for an in self._ans_list_v1:
#     #         self.assertTrue(type(self._gor.get_goterms_from_an(an)), type([]))
#     #         # self.assertIs(self._gor.get_goterms_from_an(an), list, self._gor.get_goterms_from_an(an))
#     #         # self.assertTrue(len(self._gor.get_goterms_from_an(an)) >= 1)
#     #
#     # def test_get_goterms_from_an_5(self):
#     #     """
#     #     test whether every AccessionNumber from Brian's background experiment is present in an2go_dict
#     #     should not include redundant entries
#     #     """
#     #     for an in self._ans_list_v2:
#     #         self.assertTrue(type(self._gor.get_goterms_from_an(an)), type([]))
#     #         # self.assertIs(self._gor.get_goterms_from_an(an), list, an)
#     #         # self.assertTrue(len(self._gor.get_goterms_from_an(an)) >= 1)
#
#     def test_get_date(self):
#         date = "2015-04-27 09:59"
#         self.assertEqual(self._gor.get_date(), date)
#
#     def test_get_obolibrary(self):
#         url = "http://purl.obolibrary.org/obo/go/releases/2015-04-25/go.owl"
#         self.assertEqual(self._gor.get_obolibrary(), url)
#
#     # def test_pickle_unpickle(self):
#     #     """
#     #     is object working as expected if pickled and unpickled
#     #     """
#     #     fn_p = r'/Users/dblyon/modules/cpr/goterm/Test_pickle_goretriever.p'
#     #     self._gor.pickle(fn_p)
#     #     # gor2 = goretriever.Goretriever()
#     #     gor2 = goretriever.Parser_UniProt_goa_ref()
#     #     self.assertEqual(gor2.get_date(), "not set yet")
#     #     gor2.unpickle(fn_p)
#     #     self.assertEqual(gor2.get_date(), "2015-04-27 09:59")
#     #     an = "P07261"
#     #     goterm_list = ['GO:0000433', 'GO:0000978', 'GO:0001077', 'GO:0005635', 'GO:0006351', 'GO:0034728', 'GO:0045944',
#     #                    'GO:0060963', 'GO:0061435', 'GO:0072363']
#     #     self.assertEqual(gor2.get_goterms_from_an(an), goterm_list)
#
#
# # suite = unittest.TestLoader().loadTestsFromTestCase(TestGoretriever)
# # unittest.TextTestRunner(verbosity=2).run(suite)
#
#
# class TestParser_UniProt_goa_ref(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         goa_ref_fn = home + r'/modules/cpr/goterm/test/gene_association_test.goa_ref_yeast'
#         cls._gor_parser = goretriever.Parser_UniProt_goa_ref(goa_ref_fn)
#
#     def test_get_association_dict(self):
#         self.assertEqual.__self__.maxDiff = None
#
#         assoc_dict = {'A0A023PZB3': {'GO:0005739'},
#                       'A0A0B7P3V8': {'GO:0003676', 'GO:0015074'},
#                      'A2P2R3': {'GO:0003674', 'GO:0004360','GO:0005575','GO:0006048','GO:0006541','GO:0008150'},
#                      'A5Z2X5': {'GO:0003674', 'GO:0005575', 'GO:0008150', 'GO:0016021'},
#                      'D6VPM8': {'GO:0003674', 'GO:0005575', 'GO:0008150', 'GO:0016021'},
#                      'D6VTK4': {'GO:0000750', 'GO:0000755','GO:0004934','GO:0005887','GO:0030031','GO:0051260'},
#                      'I2HB70': {'GO:0003674', 'GO:0005575', 'GO:0008150'},
#                      'I2HB52': {'GO:0003674', 'GO:0005575', 'GO:0008150'}}
#         self.assertDictEqual(assoc_dict, self._gor_parser.get_association_dict())
#
# suite = unittest.TestLoader().loadTestsFromTestCase(TestParser_UniProt_goa_ref)
# unittest.TextTestRunner(verbosity=2).run(suite)








