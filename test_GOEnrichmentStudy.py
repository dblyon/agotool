import unittest, go_enrichment_dbl, os, goretriever, obo_parser

__author__ = 'dblyon'


class TestGOEnrichmentStudy(unittest.TestCase):
    '''
    made to check Fisher-Exact-Test using yeast data with different UserInput
    '''

    @classmethod
    def setUpClass(cls):
        cls._home = os.path.expanduser('~')
        cls._obo_dag = obo_parser.GODag(obo_file = cls._home + r'/CloudStation/CPR/Brian_GO/go_rescources/go_obo/go-basic.obo')
        goa_ref_fn = cls._home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/yeast/gene_association.goa_ref_yeast'
        cls._assoc_dict = goretriever.Parser_UniProt_goa_ref(goa_ref_fn = goa_ref_fn).get_association_dict()
        cls._alpha = 0.05
        cls._methods = ["bonferroni", "sidak", "holm", "benjamini_hochberg"]
        cls._num_bins = 100

    def test_run_study_1(self):
        '''
        study and population are equivalent
        therefore p-values should be 1
        '''
        userinput_fn = self._home + r'/modules/cpr/goterm/test/UserInput_test1.txt'
        ui = goretriever.UserInput(userinput_fn, self._num_bins)
        backtracking = True
        randomSample = False
        gostudy = go_enrichment_dbl.GOEnrichmentStudy(ui, self._assoc_dict, self._obo_dag, self._alpha, self._methods, backtracking, randomSample)
        results = gostudy.run_study()
        for result in results:
            self.assertAlmostEqual(1, result.__dict__['p_uncorrected'])

    def test_run_study_2(self):
        '''
        study and population are equivalent
        therefore p-values should be 1
        '''
        userinput_fn = self._home + r'/modules/cpr/goterm/test/UserInput_test1.txt'
        ui = goretriever.UserInput(userinput_fn, self._num_bins)
        backtracking = False
        randomSample = False
        gostudy = go_enrichment_dbl.GOEnrichmentStudy(ui, self._assoc_dict, self._obo_dag, self._alpha, self._methods, backtracking, randomSample)
        results = gostudy.run_study()
        for result in results:
            self.assertAlmostEqual(1, result.__dict__['p_uncorrected'])

    def test_run_study_3(self):
        '''
        study and population are equivalent
        therefore p-values should be 1
        '''
        userinput_fn = self._home + r'/modules/cpr/goterm/test/UserInput_test1.txt'
        ui = goretriever.UserInput(userinput_fn, self._num_bins)
        backtracking = True
        randomSample = True
        gostudy = go_enrichment_dbl.GOEnrichmentStudy(ui, self._assoc_dict, self._obo_dag, self._alpha, self._methods, backtracking, randomSample)
        results = gostudy.run_study()
        for result in results:
            self.assertAlmostEqual(1, result.__dict__['p_uncorrected'])

    def test_run_study_4(self):
        '''
        study very small, and population larger
        therefore p-values should be close to 0
        '''
        userinput_fn = self._home + r'/modules/cpr/goterm/test/UserInput_test2.txt'
        ui = goretriever.UserInput(userinput_fn, self._num_bins)
        backtracking = False
        randomSample = False
        gostudy = go_enrichment_dbl.GOEnrichmentStudy(ui, self._assoc_dict, self._obo_dag, self._alpha, self._methods, backtracking, randomSample)
        results = gostudy.run_study()
        for result in results:
            self.assertAlmostEqual(0, result.__dict__['p_uncorrected'], msg=result.__dict__['id'])

    def test_run_study_5(self):
        '''
        study very small, and population larger
        therefore p-values should be close to 0
        '''
        userinput_fn = self._home + r'/modules/cpr/goterm/test/UserInput_test2.txt'
        ui = goretriever.UserInput(userinput_fn, self._num_bins)
        backtracking = False
        randomSample = True
        gostudy = go_enrichment_dbl.GOEnrichmentStudy(ui, self._assoc_dict, self._obo_dag, self._alpha, self._methods, backtracking, randomSample)
        results = gostudy.run_study()
        for result in results:
            self.assertAlmostEqual(0, result.__dict__['p_uncorrected'], msg=result.__dict__['id'])




suite = unittest.TestLoader().loadTestsFromTestCase(TestGOEnrichmentStudy)
unittest.TextTestRunner(verbosity=2).run(suite)







