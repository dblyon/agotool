import unittest
import os
import sys

home = os.path.expanduser('~')
sys.path.append(home + r'/modules/cpr/goterm/agotool/static/python')
import go_enrichment
import go_retriever
import obo_parser
import userinput


class TestGOEnrichmentStudy(unittest.TestCase):
    '''
    made to check Fisher-Exact-Test using yeast data with different UserInput
    '''

    @classmethod
    def setUpClass(cls):
        cls._home = os.path.expanduser('~')
        cls._obo_dag = obo_parser.GODag(obo_file = cls._home + r'/modules/cpr/goterm/agotool/static/data/OBO/go-basic.obo')
        goa_ref_fn = cls._home + r'/modules/cpr/goterm/agotool/static/data/GOA/gene_association.goa_yeast'
        cls._assoc_dict = go_retriever.Parser_UniProt_goa_ref(goa_ref_fn = goa_ref_fn).get_association_dict("all_GO", cls._obo_dag)
        cls._alpha = 0.05
        cls._multitest_method = 'benjamini_hochberg'
        cls._abcorr = True
        cls._o_or_u_or_both = 'both'
        cls._num_bins = 100

    def test_run_study_1(self):
        '''
        study and population are equivalent
        therefore p-values should be 1
        '''
        userinput_fn = self._home + r'/modules/cpr/goterm/agotool/static/python/test/UserInput_test1.txt'
        ui = userinput.UserInput(userinput_fn, self._num_bins)
        backtracking = True
        randomSample = False
        gostudy = go_enrichment.GOEnrichmentStudy(
            ui, self._assoc_dict, self._obo_dag, self._alpha, backtracking, randomSample,
            self._abcorr, self._o_or_u_or_both, self._multitest_method)
        results = gostudy.results
        for result in results:
            self.assertAlmostEqual(1, result.__dict__['p_uncorrected'])

    def test_run_study_2(self):
        '''
        study and population are equivalent
        therefore p-values should be 1
        '''
        userinput_fn = self._home + r'/modules/cpr/goterm/agotool/static/python/test/UserInput_test1.txt'
        ui = userinput.UserInput(userinput_fn, self._num_bins)
        backtracking = False
        randomSample = False
        gostudy = go_enrichment.GOEnrichmentStudy(
            ui, self._assoc_dict, self._obo_dag, self._alpha, backtracking, randomSample,
            self._abcorr, self._o_or_u_or_both, self._multitest_method)
        results = gostudy.results
        for result in results:
            self.assertAlmostEqual(1, result.__dict__['p_uncorrected'])

    def test_run_study_3(self):
        '''
        study and population are equivalent
        therefore p-values should be 1
        '''
        userinput_fn = self._home + r'/modules/cpr/goterm/agotool/static/python/test/UserInput_test1.txt'
        ui = userinput.UserInput(userinput_fn, self._num_bins0)
        backtracking = True
        randomSample = True
        gostudy = go_enrichment.GOEnrichmentStudy(
            ui, self._assoc_dict, self._obo_dag, self._alpha, backtracking, randomSample,
            self._abcorr, self._o_or_u_or_both, self._multitest_method)
        results = gostudy.results
        for result in results:
            self.assertAlmostEqual(1, result.__dict__['p_uncorrected'])


#!!! fix tests below. backtracking option is not passed correctly
    # def test_run_study_4(self):
    #     '''
    #     population yeast acteylation observed (slightly modified),
    #     study very small containing only highly abundant proteins from
    #     "ER membrane protein complex"
    #     all YEAST data
    #     therefore p-values should be close to 0
    #     '''
    #     userinput_fn = self._home + r'/modules/cpr/goterm/agotool/static/python/test/UserInput_test_2.txt'
    #     ui = userinput.UserInput(userinput_fn, self._num_bins)
    #     backtracking = False
    #     randomSample = False
    #     gostudy = go_enrichment.GOEnrichmentStudy(
    #         ui, self._assoc_dict, self._obo_dag, self._alpha, backtracking, randomSample,
    #         self._abcorr, self._o_or_u_or_both, self._multitest_method)
    #     results = gostudy.results
    #     for result in results:
    #         self.assertAlmostEqual(0, result.__dict__['p_uncorrected'], msg=(result.__dict__['id'], result.__dict__['p_uncorrected']))

    # def test_assoc_dict_noBacktracking_5(self):
    #     '''
    #     population yeast acteylation observed (slightly modified),
    #     study very small containing only highly abundant proteins from
    #     "ER membrane protein complex"
    #     all YEAST data
    #     therefore p-values should be close to 0
    #     '''
    #     userinput_fn = self._home + r'/modules/cpr/goterm/agotool/static/python/test/UserInput_test_2.txt'
    #     ui = userinput.UserInput(userinput_fn, self._num_bins)
    #     backtracking = False
    #     randomSample = False
    #     gostudy = go_enrichment.GOEnrichmentStudy(
    #         ui, self._assoc_dict, self._obo_dag, self._alpha, backtracking, randomSample,
    #         self._abcorr, self._o_or_u_or_both, self._multitest_method)
    #     results = gostudy.results
    #     for result in results:
    #         self.assertAlmostEqual(0, result.__dict__['p_uncorrected'], msg=result.__dict__['id'])



    # def test_run_study_5(self):
    #     '''
    #     study very small, and population larger
    #     therefore p-values should be close to 0
    #     '''
    #     userinput_fn = self._home + r'/modules/cpr/goterm/agotool/static/python/test/UserInput_test2.txt'
    #     ui = userinput.UserInput(userinput_fn, self._num_bins)
    #     backtracking = False
    #     randomSample = True
    #     gostudy = go_enrichment.GOEnrichmentStudy(
    #         ui, self._assoc_dict, self._obo_dag, self._alpha, backtracking, randomSample,
    #         self._abcorr, self._o_or_u_or_both, self._multitest_method)
    #     results = gostudy.results
    #     for result in results:
    #         self.assertAlmostEqual(0, result.__dict__['p_uncorrected'], msg=result.__dict__['id'])


suite = unittest.TestLoader().loadTestsFromTestCase(TestGOEnrichmentStudy)
unittest.TextTestRunner(verbosity=2).run(suite)







