import os, sys
import ast
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import variables
TABLES_DIR = variables.TABLES_DIR

def test_PMID_reduction_of_tables_consitency():
    # sanity check
    def PMIDs_from_Functions_table_PMID(fn):
        PMID_list = []
        with open(fn, "r") as fh_in:
            for line in fh_in:
                PMID = line.split("\t")[1]
                PMID_list.append(PMID)
        return PMID_list

    # sanity check
    def PMIDs_from_Protein_2_Function_table_PMID(fn):
        PMID_set = set()
        with open(fn, "r") as fh_in:
            for line in fh_in:
                PMID_set |= ast.literal_eval(line.split("\t")[1])
        return PMID_set

    fn = os.path.join(TABLES_DIR, "Functions_table_PMID.txt")
    PMIDs_Functions_table = PMIDs_from_Functions_table_PMID(fn)
    assert len(PMIDs_Functions_table) == len(set(PMIDs_Functions_table))
    PMIDs_Functions_table = set(PMIDs_Functions_table)

    fn = os.path.join(TABLES_DIR, "Protein_2_Function_table_PMID.txt")
    PMIDs_Protein_2_Function_table = PMIDs_from_Protein_2_Function_table_PMID(fn)
    assert len(PMIDs_Protein_2_Function_table.intersection(PMIDs_Functions_table)) == len(PMIDs_Protein_2_Function_table)
    assert len(PMIDs_Protein_2_Function_table) == len(PMIDs_Functions_table)