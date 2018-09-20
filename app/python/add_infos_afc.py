import fileinput
import pandas as pd
from collections import defaultdict
import query, variables


def add_infos_2_afc():
    entityType_2_functionType_dict = variables.entityType_2_functionType_dict
    taxid = 9606
    pqo = query.PersistentQueryObject_STRING(low_memory=True)

    assoc_list, pval_list, count_in_population_list, average_abundance_ratio_list = [], [], [], []
    for line in fileinput.input():
        line_split = line.strip().split()
        assoc_list.append(line_split[1])
        count_in_population_list.append(line_split[4])
        average_abundance_ratio_list.append(line_split[7][:-1])
        pval_list.append(line_split[-1])

    df = pd.DataFrame()
    df["term"] = assoc_list
    df["p_value"] = pval_list

    term_2_description_dict = defaultdict(lambda: str)
    term_2_description_dict.update(query.get_description_from_an(assoc_list))
    df["description"] = df["term"].apply(lambda p: term_2_description_dict[p])

    association_2_count_dict = defaultdict(lambda: int)
    df["foreground_count"] = count_in_population_list

    association_2_count_dict.update(query.from_taxid_and_association_get_association_2_count_dict(taxid, assoc_list))
    df["count_in_genome"] = df["term"].apply(lambda p: association_2_count_dict[p])

    df["hierarchical_level"] = df["term"].apply(lambda term: pqo.functerm_2_level_dict[term])
    df["FDR"] = ""

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