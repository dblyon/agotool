from __future__ import print_function
import sys
sys.path.append("./../")
import db_config, query


connection = db_config.Connect(echo=False, testing=False, do_logging=False)
# protein_ans_list = ["P35997", "P38711", "P35997", "P38711", "B2RID1", "belk_c_455_5138"]
# protein_ans_list = ["B2RID1"]
# protein_ans_list = ["P35997"]


if __name__ == "__main__":
    an = "P35997"

    ### test 1
    # directly annotated GO terms from Protein_2_Function_table.txt
    go_terms_expected = ['GO:0000028', 'GO:0000462', 'GO:0002181', 'GO:0003735', 'GO:0006412', 'GO:0022627', 'GO:0046872']
    d = query.get_association_dict(connection=connection, protein_ans_list=[an], function_type="GO", limit_2_parent=None, basic_or_slim="basic", backtracking=False)
    assert sorted(d[an]) == sorted(go_terms_expected)

    ### test 2
    go_terms_expected = ["GO:0003735", "GO:0006412"]
    d = query.get_association_dict(connection=connection, protein_ans_list=[an], function_type="GO", limit_2_parent=None, basic_or_slim="slim", backtracking=False)
    assert sorted(d[an]) == sorted(go_terms_expected)

    ### test 3
    results_limit_2_parent = []
    d = query.get_association_dict(connection, protein_ans_list=[an], function_type="GO", limit_2_parent="CP", basic_or_slim="basic", backtracking=True)
    try:
        results_limit_2_parent += d[an]
    except KeyError:
        pass
    d = query.get_association_dict(connection, protein_ans_list=[an], function_type="GO", limit_2_parent="MF", basic_or_slim="basic", backtracking=True)
    try:
        results_limit_2_parent += d[an]
    except KeyError:
        pass
    d = query.get_association_dict(connection, protein_ans_list=[an], function_type="GO", limit_2_parent="BP", basic_or_slim="basic", backtracking=True)
    try:
        results_limit_2_parent += d[an]
    except KeyError:
        pass
    d = query.get_association_dict(connection, protein_ans_list=[an], function_type="GO", limit_2_parent=None, basic_or_slim="basic", backtracking=True)
    assert sorted(results_limit_2_parent) == sorted(d[an])


    ### test 4
    results_limit_2_parent = []
    d = query.get_association_dict(connection, protein_ans_list=[an], function_type="GO", limit_2_parent="CP", basic_or_slim="slim", backtracking=True)
    try:
        results_limit_2_parent += d[an]
    except KeyError:
        pass
    d = query.get_association_dict(connection, protein_ans_list=[an], function_type="GO", limit_2_parent="MF", basic_or_slim="slim", backtracking=True)
    try:
        results_limit_2_parent += d[an]
    except KeyError:
        pass
    d = query.get_association_dict(connection, protein_ans_list=[an], function_type="GO", limit_2_parent="BP", basic_or_slim="slim", backtracking=True)
    try:
        results_limit_2_parent += d[an]
    except KeyError:
        pass

    d = query.get_association_dict(connection, protein_ans_list=[an], function_type="GO", limit_2_parent=None, basic_or_slim="slim", backtracking=True)
    assert sorted(results_limit_2_parent) == sorted(d[an])

