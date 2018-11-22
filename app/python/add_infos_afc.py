import fileinput
import pandas as pd
import numpy as np
from collections import defaultdict
import query, variables


def BenjaminiHochberg(pvals, num_total_tests, array=False):
    """
    expects a sorted (ascending) list of uncorrected p-values
    and the total number of tests
    http://stats.stackexchange.com/questions/870/multiple-hypothesis-testing-correction-with-benjamini-hochberg-p-values-or-q-va
    http://projecteuclid.org/DPubS?service=UI&version=1.0&verb=Display&handle=euclid.aos/1074290335
    :param pvals: ListOfFloat
    :param num_total_tests: Integer
    :param array: Bool (flag to indicate if pvals are numpy array or list)
    :return: ListOfFloat
    """
    if array:
        p_values = pvals # already passing np.array
    else:
        p_values = np.array(pvals)
    p_values_corrected = []
    prev_bh_value = 0
    for i, p_value in enumerate(p_values):
        bh_value = p_value * num_total_tests / (i + 1)
        # Sometimes this correction can give values greater than 1,
        # so we set those values at 1
        bh_value = min(bh_value, 1)
        # To preserve monotonicity in the values, we take the
        # maximum of the previous value or this one, so that we
        # don't yield a value less than the previous.
        bh_value = max(bh_value, prev_bh_value)
        prev_bh_value = bh_value
        p_values_corrected.append(bh_value)
    return p_values_corrected


def add_infos_2_afc():
    entityType_2_functionType_dict = variables.entityType_2_functionType_dict
    taxid = 9606
    pqo = query.PersistentQueryObject_STRING(low_memory=False)
    function_an_2_description_dict = pqo.function_an_2_description_dict
    association_2_count_dict_background = pqo.taxid_2_etype_2_association_2_count_dict_background[taxid][-56]

    assoc_list, pval_list, count_in_population_list, average_abundance_ratio_list = [], [], [], []
    for line in fileinput.input():
        # cluster GO:0001665 has size 6 (value average -0.974333) and is larger with p-value 0.009
        # cluster GO:0002053 has size 28 (value average -2.086178) and is smaller with p-value 0.009
        # cluster GO:0004908 has size 7 (value average -1.041286) and is larger with p-value 0.009
        # line_split = line.strip().split()
        # assoc_list.append(line_split[1])
        # count_in_population_list.append(line_split[4])
        # average_abundance_ratio_list.append(line_split[7][:-1])
        # pval_list.append(line_split[-1])

        # KS      KW-0649 14      0.0179843
        # KS      KW-0989 23      0.332197
        line_split = line.strip().split()
        assoc_list.append(line_split[1])
        count_in_population_list.append(line_split[2])
        pval_list.append(line_split[3])


    df = pd.DataFrame()
    df["term"] = assoc_list
    df["p_value"] = pval_list
    df["p_value"] = df["p_value"].astype(float)
    df["FDR"] = ""
    df["foreground_count"] = count_in_population_list

    df["description"] = df["term"].apply(lambda p: function_an_2_description_dict[p])
    df = df.sort_values("p_value", ascending=True)
    df["FDR"] = BenjaminiHochberg(df["p_value"].values, df.shape[0], array=True)
    df = df.sort_values(["FDR", "p_value", "description"]).head(100)

    # term_2_description_dict = defaultdict(lambda: str)
    # term_2_description_dict.update(query.get_description_from_an(assoc_list))
    # df["description"] = df["term"].apply(lambda p: term_2_description_dict[p])



    # association_2_count_dict = defaultdict(lambda: int)
    # association_2_count_dict.update(query.from_taxid_and_association_get_association_2_count_dict(taxid, assoc_list))
    # df["count_in_genome"] = df["term"].apply(lambda p: association_2_count_dict[p])
    df["count_in_genome"] = df["term"].apply(lambda p: association_2_count_dict_background[p])

    df["hierarchical_level"] = df["term"].apply(lambda term: pqo.functerm_2_level_dict[term])

    an_2_etype_dict = defaultdict(lambda: -123)
    an_2_etype_dict.update(query.get_functionAN_2_etype_dict())
    df["etype"] = df["term"].apply(lambda term: an_2_etype_dict[term])
    df["category"] = df["etype"].apply(lambda etype: entityType_2_functionType_dict[int(etype)])

    association_2_ENSPset_dict = defaultdict(lambda: set())
    association_2_ENSPset_dict.update(query.from_taxid_and_association_get_association_2_ENSP(taxid, assoc_list))
    df["foreground_ids"] = df["term"].apply(lambda term: ";".join(association_2_ENSPset_dict[term]))
    cols_sort_order = ['term', 'hierarchical_level', 'p_value', 'FDR', 'category', 'etype', 'description', 'foreground_count', 'foreground_ids']


    cols_sort_order += sorted(set(df.columns.tolist()) - set(cols_sort_order))
    print(df[cols_sort_order].to_csv(sep='\t', header=True, index=False))


if __name__ == "__main__":
    add_infos_2_afc()