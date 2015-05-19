import unittest, goretriever
import cPickle as pickle
__author__ = 'dblyon'


class TestGoretriever(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        cls._gor = goretriever.Goretriever()
        fn = r"C:\Users\dblyon\CloudStation\CPR\Brian_GO\UniProt_data\yeast\gene_association.goa_yeast"
        cls._gor.parse_goa_ref(fn)
        # ans_list_pickled_fn = r"C:\Users\dblyon\CloudStation\CPR\Brian_GO\UniProt_data\yeast\SaccharomycesCerevisiae_UP_20150519_AccessionNumbersList.p"
        # ans_list_pickled_fn = r"C:\Users\dblyon\CloudStation\CPR\Brian_GO\UniProt_data\yeast\SaccharomycesCerevisiae_SwissProt_20150519_AccessionNumbersList.p"
        ans_list_pickled_fn_v1 = r"C:\Users\dblyon\CloudStation\CPR\Brian_GO\UniProt_data\yeast\Yeast_AccessionNumbersList_v1.p"
        cls._ans_list_v1 = pickle.load(open(ans_list_pickled_fn_v1, "rb"))
        ans_list_pickled_fn_v2 = r"C:\Users\dblyon\CloudStation\CPR\Brian_GO\UniProt_data\yeast\Yeast_AccessionNumbersList_v2.p"
        cls._ans_list_v2 = pickle.load(open(ans_list_pickled_fn_v2, "rb"))

    def test_get_goterms_from_an_1(self):
        an="P07261"
        goterm_list = ['GO:0000433','GO:0000978','GO:0001077','GO:0005635','GO:0006351','GO:0034728','GO:0045944','GO:0060963','GO:0061435','GO:0072363']
        self.assertEqual(self._gor.get_goterms_from_an(an), goterm_list)

    def test_get_goterms_from_an_2(self):
        an=""
        self.assertEqual(self._gor.get_goterms_from_an(an), -1)

    # def test_get_goterms_from_an_3(self):
    #     """
    #     test whether every AccessionNumber from UniProt (SP and Tr) is present in an2go_dict
    #     """
    #     for an in self._ans_list:
    #         self.assertIs(self._gor.get_goterms_from_an(an), list, an)
    #         self.assertTrue(len(self._gor.get_goterms_from_an(an)) >= 1)

    def test_get_goterms_from_an_4(self):
        """
        test whether every AccessionNumber from Brian's enrichment experiment is present in an2go_dict
        includes redundant entries
        """
        for an in self._ans_list_v1:
            self.assertTrue(type(self._gor.get_goterms_from_an(an)), type([]))
            #self.assertIs(self._gor.get_goterms_from_an(an), list, self._gor.get_goterms_from_an(an))
            #self.assertTrue(len(self._gor.get_goterms_from_an(an)) >= 1)

    def test_get_goterms_from_an_5(self):
        """
        test whether every AccessionNumber from Brian's background experiment is present in an2go_dict
        should not include redundant entries
        """
        for an in self._ans_list_v2:
            self.assertTrue(type(self._gor.get_goterms_from_an(an)), type([]))
            # self.assertIs(self._gor.get_goterms_from_an(an), list, an)
            # self.assertTrue(len(self._gor.get_goterms_from_an(an)) >= 1)

    def test_get_date(self):
        date = "2015-04-27 09:59"
        self.assertEqual(self._gor.get_date(), date)

    def test_get_obolibrary(self):
        url = "http://purl.obolibrary.org/obo/go/releases/2015-04-25/go.owl"
        self.assertEqual(self._gor.get_obolibrary(), url)

    def test_pickle_unpickle(self):
        """
        is object working as expected if pickled and unpickled
        """
        fn_p = r"C:\Users\dblyon\code\goweb\Test_pickle_goretriever.p"
        self._gor.pickle(fn_p)
        gor2 = goretriever.Goretriever()
        self.assertEqual(gor2.get_date(), "not set yet")
        gor2.unpickle(fn_p)
        self.assertEqual(gor2.get_date(), "2015-04-27 09:59")
        an="P07261"
        goterm_list = ['GO:0000433','GO:0000978','GO:0001077','GO:0005635','GO:0006351','GO:0034728','GO:0045944','GO:0060963','GO:0061435','GO:0072363']
        self.assertEqual(gor2.get_goterms_from_an(an), goterm_list)





suite = unittest.TestLoader().loadTestsFromTestCase(TestGoretriever)
unittest.TextTestRunner(verbosity=2).run(suite)