import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import create_SQL_tables_snakemake as cst
import variables




def test_get_child_2_direct_parents_and_term_2_level_dict_interpro():
    fn = os.path.join(variables.DOWNLOADS_DIR_SNAKEMAKE, "interpro_parent_2_child_tree.txt")
    child_2_parent_dict, term_2_level_dict = cst.get_child_2_direct_parents_and_term_2_level_dict_interpro(fn)

    expected_parent = {"IPR000276"}
    actual_parent = child_2_parent_dict["IPR000025"]
    assert expected_parent == actual_parent

    expected_parent = {"IPR000025"}
    actual_parent = child_2_parent_dict["IPR002278"]
    assert expected_parent == actual_parent


    expected_parent = {"IPR000174"}
    actual_parent = child_2_parent_dict["IPR000057"]
    assert expected_parent == actual_parent
