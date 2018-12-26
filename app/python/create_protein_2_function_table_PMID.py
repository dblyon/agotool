import pandas as pd
# import numpy as np
import os, sys #, re
import ast
sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
import variables
DOWNLOADS_DIR = r"/mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads" # variables.DOWNLOADS_DIR
TABLES_DIR = variables.TABLES_DIR
# etype = "-56"
etype = str(variables.functionType_2_entityType_dict["PMID"])


def parse_textmining_entityID_2_proteinID(fn):
    df = pd.read_csv(fn, sep="\t", names=["textmining_id", "species_id", "protein_id"])  # textmining_id = entity_id
    df["ENSP"] = df["species_id"].astype(str) + "." + df["protein_id"].astype(str)
    return df

def parse_textmining_string_matches(fn):
    names = ['PMID', 'sentence', 'paragraph', 'location_start', 'location_end', 'matched_string', 'species', 'entity_id']
    df = pd.read_csv(fn, sep="\t", names=names)
    return df

def sanity_check_1(df_stringmatches, df_txtID):
    # sanity test that df_stringmatches.entity_id are all in df_txtID.textmining_id --> yes. textmining_id is a superset of entity_id --> after filtering df_txtID this is not true
    entity_id = set(df_stringmatches["entity_id"].unique())
    textmining_id = set(df_txtID.textmining_id.unique())
    assert len(entity_id.intersection(textmining_id)) == len(entity_id)

def parse_taxid_2_proteins_get_all_ENSPs(fn_TaxID_2_Proteins_table_STRING):
    ENSP_set = set()
    with open(fn_TaxID_2_Proteins_table_STRING, "r") as fh:
        for line in fh:
            ENSP_set |= ast.literal_eval(line.split("\t")[1])  # reduce DF to ENSPs in DB
    return ENSP_set

def sanity_check_2(df_txtID):
    assert len(df_txtID["textmining_id"].unique()) == len(df_txtID["ENSP"].unique())


if __name__ == "__main__":

    fn_all_entities = os.path.join(DOWNLOADS_DIR, "all_entities.tsv")
    df_txtID = parse_textmining_entityID_2_proteinID(fn_all_entities)

    fn_string_matches = os.path.join(DOWNLOADS_DIR, "string_matches.tsv")
    df_stringmatches = parse_textmining_string_matches(fn_string_matches)

    sanity_check_1(df_stringmatches, df_txtID)

    fn_TaxID_2_Proteins_table_STRING = os.path.join(TABLES_DIR, "TaxID_2_Proteins_table_STRING.txt")
    ENSP_set = parse_taxid_2_proteins_get_all_ENSPs(fn_TaxID_2_Proteins_table_STRING )

    cond = df_txtID["ENSP"].isin(ENSP_set)
    print("reducing df_txtID from {} to {} rows".format(len(cond), sum(cond)))
    df_txtID = df_txtID[cond]
    # sanity check that there is a "one to one mapping" between textmining_id and ENSP --> no --> first remove all ENSPs that are not in DB
    sanity_check_2(df_txtID)

    # filter by ENSPs in DB --> TaxID_2_Protein_table_STRING.txt
    # textminingID_2_ENSP_dict
    entity_id_2_ENSP_dict = pd.Series(df_txtID["ENSP"].values, index=df_txtID["textmining_id"]).to_dict()

    # reduce df_stringmatches to relevant entity_ids
    cond = df_stringmatches["entity_id"].isin(df_txtID["textmining_id"].values)
    print("reducing df_stringmatches from {} to {} rows".format(len(cond), sum(cond)))
    df_stringmatches = df_stringmatches[cond]

    # create an_2_function_set
    # entity_id_2_PMID_dict
    # map entity_id to ENSP
    # df_stringmatches_sub = df_stringmatches[["PMID", "entity_id"]]
    # entity_id_2_PMID_dict = df_stringmatches_sub.groupby("entity_id")["PMID"].apply(set).to_dict()
    df_stringmatches = df_stringmatches[["PMID", "entity_id"]]
    entity_id_2_PMID_dict = df_stringmatches.groupby("entity_id")["PMID"].apply(set).to_dict()

    ENSP_2_PMID_dict = {}
    entity_id_2_ENSP_no_mapping = []
    multi_ENSP = []
    for entity_id, PMID_set in entity_id_2_PMID_dict.items():
        try:
            ENSP = entity_id_2_ENSP_dict[entity_id]
        except KeyError:
            entity_id_2_ENSP_no_mapping.append(entity_id)
            continue
        if ENSP not in ENSP_2_PMID_dict:
            ENSP_2_PMID_dict[ENSP] = PMID_set
        else:
            multi_ENSP.append([entity_id, ENSP])

    assert len(entity_id_2_ENSP_no_mapping) == 0
    assert len(multi_ENSP) == 0

    # | etype | an | func_array |
    fn_Protein_2_Function_table_PMID = os.path.join(TABLES_DIR, "Protein_2_Function_table_PMID.txt")
    with open(fn_Protein_2_Function_table_PMID, "w") as fh_out:
        for ENSP, PMID_set in ENSP_2_PMID_dict.items():
            PMID_with_prefix_list = ["PMID:" + str(PMID) for PMID in sorted(PMID_set)]
            fh_out.write(ENSP + "\t" + "{" + str(PMID_with_prefix_list)[1:-1].replace(" ", "").replace("'", '"') + "}" + "\t" + etype + "\n")

    # #!!! dependency on creating Functions_table_PMID.txt first #!!!
    # reduce Functions_table_PMID.txt to PMIDs that are in Protein_2_Function_table_PMID.txt
    fn_orig = os.path.join(TABLES_DIR, "Functions_table_PMID.txt")
    os.rename(fn_orig, fn_orig + ".orig")
    fn_in = fn_orig + ".orig"
    fn_out = os.path.join(TABLES_DIR, "Functions_table_PMID.txt")

    PMID_set = set(df_stringmatches["PMID"].values)
    PMID_not_relevant = []
    with open(fn_in, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            for line in fh_in:
                PMID_including_prefix = line.split("\t")[1]
                if int(PMID_including_prefix[5:]) in PMID_set:
                    fh_out.write(line)
                else:
                    PMID_not_relevant.append(PMID_including_prefix)
    print("len_PMID_not_relevant", len(PMID_not_relevant))
    print("finished creating Protein_2_Function_table_PMID check it out at \n {}".format(fn_Protein_2_Function_table_PMID))