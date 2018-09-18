import sys, os, fileinput
sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
from collections import defaultdict
import query, variables

def format_list_of_string_2_postgres_array(list_of_string):
    """
    removes internal spaces
    :param list_of_string: List of String
    :return: String
    """
    return "{" + str(list_of_string)[1:-1].replace(" ", "").replace("'", '"') + "}"

def count_terms_v3(ans_set, assoc_dict):
    """
    # ToDo write test for counter functions
    # goterm: 'GO:0007610' has secondary id 'GO:0044708' --> if resolved at table creation not a problem otherwise it is
    count the number of terms in the study group
    association_2_count_dict: key=GOid, val=Num of occurrences
    association_2_ANs_dict: key=GOid, val=SetOfANs
    count_n: Integer(Number of ANs with a GO-term in assoc_dict and obo_dag)
    :return: Tuple(dict, dict, int)
    """
    association_2_ANs_dict = {}
    association_2_count_dict = defaultdict(int)
    for an in (AN for AN in ans_set if AN in assoc_dict):
        for association in assoc_dict[an]:
            association_2_count_dict[association] += 1
            if not association in association_2_ANs_dict:
                association_2_ANs_dict[association] = {an}
            else:
                association_2_ANs_dict[association] |= {an} # update dict
    return association_2_count_dict, association_2_ANs_dict, len(ans_set) #ans_counter

def create_functions_2_ENSP_table():
    for taxid in fileinput.input():
        taxid = taxid.strip()
        ans_list = sorted(query.get_proteins_of_taxid(taxid))
        etype_2_association_dict = query.PersistentQueryObject_STRING.get_association_dict_split_by_category(ans_list)
        for etype in sorted(variables.entity_types_with_data_in_functions_table):
            assoc_dict = etype_2_association_dict[etype]
            association_2_count_dict, association_2_ANs_dict, ans_counter = count_terms_v3(set(ans_list), assoc_dict)
            for association, ans in association_2_ANs_dict.items():
                assert ans_counter >= association_2_count_dict[association]
                print(str(taxid) + "\t" + str(etype) + "\t" + association + "\t" + str(association_2_count_dict[association]) + "\t" + str(ans_counter) + "\t" + "{" + str(ans)[1:-1].replace(" ", "").replace("'", '"') + "}")


if __name__ == "__main__":
    #### set "DB_DOCKER" to False and "DOCKER" to True in variables.py to make this work
    # pqo = query.PersistentQueryObject_STRING()
    # taxid_list = query.get_taxids()
    create_functions_2_ENSP_table()
