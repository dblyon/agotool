from __future__ import print_function
import unittest
import sys
sys.path.append("./../")
import db_config, query


def update_list(list_2_update, dict_, key):
    try:
        list_2_update += dict_[key]
    except KeyError:
        pass
    return list_2_update


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = db_config.Connect(echo=False, testing=False, do_logging=False)
        self.an = "P35997"

    test_GO_terms = True
    test_UniProt_keywords = True

    # if test_GO_terms:

    def test_go_terms_1(self):
        ##### GO terms
        ### test 1, manual lookup
        # directly annotated GO terms from Protein_2_Function_table.txt
        go_terms_expected = ['GO:0000028', 'GO:0000462', 'GO:0002181', 'GO:0003735', 'GO:0006412', 'GO:0022627', 'GO:0046872']
        d = query.get_association_dict(connection=self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=None, basic_or_slim="basic", backtracking=False)
        assert sorted(d[self.an]) == sorted(go_terms_expected)

    def test_go_terms_2(self):
        ### test 2, manual lookup
        go_terms_expected = ["GO:0003735", "GO:0006412"]
        d = query.get_association_dict(connection=self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=None, basic_or_slim="slim", backtracking=False)
        assert sorted(d[self.an]) == sorted(go_terms_expected)

    def test_go_terms_3(self):
        ### test 3, sum of parts needs to equal entirety
        results_limit_2_parent = []
        for parent_term in query.humanName_2_functionAN_dict:
            d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=parent_term, basic_or_slim="basic", backtracking=True)
            results_limit_2_parent = update_list(results_limit_2_parent, d, self.an)
        d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=None, basic_or_slim="basic", backtracking=True)
        assert sorted(set(results_limit_2_parent)) == sorted(d[self.an])

    def test_go_terms_4(self):
        ### test 4, sum of parts needs to equal entirety
        results_limit_2_parent = []
        for parent_term in query.humanName_2_functionAN_dict:
            d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=parent_term, basic_or_slim="basic", backtracking=False)
            results_limit_2_parent = update_list(results_limit_2_parent, d, self.an)
        d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=None, basic_or_slim="basic", backtracking=False)
        assert sorted(set(results_limit_2_parent)) == sorted(d[self.an])

    def test_go_terms_5(self):
        ### test 5, sum of parts needs to equal entirety
        results_limit_2_parent = []
        for parent_term in query.humanName_2_functionAN_dict:
            d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=parent_term, basic_or_slim="slim", backtracking=True)
            results_limit_2_parent = update_list(results_limit_2_parent, d, self.an)
        d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=None, basic_or_slim="slim", backtracking=True)
        assert sorted(set(results_limit_2_parent)) == sorted(d[self.an])

    def test_go_terms_6(self):
        ### test 6, sum of parts needs to equal entirety
        results_limit_2_parent = []
        for parent_term in query.humanName_2_functionAN_dict:
            d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=parent_term, basic_or_slim="slim", backtracking=False)
            results_limit_2_parent = update_list(results_limit_2_parent, d, self.an)
        d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=None, basic_or_slim="slim", backtracking=False)
        assert sorted(set(results_limit_2_parent)) == sorted(d[self.an])

    def test_go_terms_7(self):
        ### test 7
        basic_back = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=None, basic_or_slim="basic", backtracking=True)[self.an]
        basic_not_back = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=None, basic_or_slim="basic", backtracking=False)[self.an]
        slim_back = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=None, basic_or_slim="slim", backtracking=True)[self.an]
        slim_not_back = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="GO", limit_2_parent=None, basic_or_slim="slim", backtracking=False)[self.an]
        assert len(basic_back) > len(basic_not_back)
        assert len(slim_back) > len(slim_not_back)
        assert len(basic_back) > len(slim_back)
        assert len(basic_not_back) > len(slim_not_back)


    # if test_UniProt_keywords:

    def test_upk_terms_1(self):
        ##### UPK
        ### test 1, sum of parts needs to equal entirety
        results_limit_2_parent = []
        for parent_term in query.upkTerm_2_functionAN_dict:
            d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="UPK", limit_2_parent=parent_term, basic_or_slim="basic", backtracking=True)
            results_limit_2_parent = update_list(results_limit_2_parent, d, self.an)
        d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="UPK", limit_2_parent=None, basic_or_slim="basic", backtracking=True)
        assert sorted(set(results_limit_2_parent)) == sorted(d[self.an])

    def test_upk_terms_2(self):
        ### test 2, sum of parts needs to equal entirety
        results_limit_2_parent = []
        for parent_term in query.upkTerm_2_functionAN_dict:
            d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="UPK", limit_2_parent=parent_term, basic_or_slim="basic", backtracking=False)
            results_limit_2_parent = update_list(results_limit_2_parent, d, self.an)
        d = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="UPK", limit_2_parent=None, basic_or_slim="basic", backtracking=False)
        assert sorted(set(results_limit_2_parent)) == sorted(d[self.an])

    def test_upk_terms_3(self):
        ### test 3
        no_backtracking = query.get_association_dict(self.connection, protein_ans_list=[self.an], function_type="UPK", limit_2_parent=None, basic_or_slim="basic", backtracking=False)[self.an]
        expected_results = sorted(['UPK:0488', 'UPK:0963', 'UPK:0002', 'UPK:1185', 'UPK:0863', 'UPK:0862', 'UPK:0479', 'UPK:0687', 'UPK:0689', 'UPK:0181'])
        assert sorted(no_backtracking) == expected_results


suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)