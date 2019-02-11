import os
import ast
import pandas as pd


def create_Protein_2_Function_table_PMID__and__reduce_Functions_table_PMID(fn_in_all_entities, fn_in_string_matches, fn_in_TaxID_2_Proteins_table_STRING, fn_in_Functions_table_PMID_temp, fn_out_Functions_table_PMID, fn_out_Protein_2_Function_table_PMID):
    """
    expects 6 strings (file names), 4 input and 2 output
    fn_in_Functions_table_PMID_temp gets reduced and produces fn_out_Functions_table_PMID

    :param fn_in_all_entities: string (file name)
        # all_entities.tsv.gz
        1       1000565 METUNv1_00006
        2       1000565 METUNv1_00011
        3       1000565 METUNv1_00018

    :param fn_in_string_matches: string (file name)
        # string_matches.tsv
        29582004        22      5       7021    7028    my heart        9606    100000998
        29582004        22      5       7021    7028    my heart        2759    100036538
        29309435        13      1       5162    5166    Man-a   9606    23937830

    :param fn_in_TaxID_2_Proteins_table_STRING: string (file name)
        # TaxID_2_Proteins_table_STRING.txt (NCBI_TaxID | ENSP_array | ENSP_count)
        1000565 {"1000565.METUNv1_00006","1000565.METUNv1_00011","1000565.METUNv1_00018","1000565.METUNv1_00019","1000565.METUNv1_00035","1000565.METUNv1_00036","1000565.METUNv1_00037","1000565.METUNv1_00038","1000565.METUNv1_00041","1000565.METUNv1_00042", ... "1000565.METUNv1_04065"}       3926

    :param fn_in_Functions_table_PMID_temp: string (file name)
        # Functions_table_PMID_temp.txt (etype | function_id | description | year | hierarchical_level)
        -56     PMID:10000001   (1991) Quantum-optical properties of polariton waves.   1991    -1
        -56     PMID:1000000    (1976) DNA- and RNA-dependent DNA polymerases: progressive changes in rabbit endometrium during preimplantation stage of pregnancy.     1976    -1
        -56     PMID:10000002   (1991) Optical study of niobium disilicide polycrystalline films.       1991    -1

    :param fn_out_Functions_table_PMID: string (file name)
        # Functions_table_PMID.txt (etype | function_id | description | year | hierarchical_level)
        -56     PMID:10000075   (1991) Binding energy and electronic structure of icosahedral Al-Cu-(Li,Mg) clusters.   1991    -1
        -56     PMID:1000011    (1976) Immunological evidence of uteroglobin (blastokinin) in the male reproductive tract and in nonreproductive ductal tissues and their secretions.   1976    -1
        -56     PMID:10000126   (1991) Linear Tc depression in Mg-doped YBa2Cu3O7- delta.       1991    -1

    :param fn_out_Protein_2_Function_table_PMID: string (file name)
        # Protein_2_Function_table_PMID.txt (ENSP | function_array | etype)
        1000565.METUNv1_00036   {"PMID:27708623"}       -56
        1000565.METUNv1_00081   {"PMID:19514844","PMID:19943898"}       -56
        1000565.METUNv1_00188   {"PMID:25978049"}       -56

    :return: None
    """
    df_txtID = parse_textmining_entityID_2_proteinID(fn_in_all_entities)
    df_stringmatches = parse_textmining_string_matches(fn_in_string_matches)
    # sanity test that df_stringmatches.entity_id are all in df_txtID.textmining_id --> yes. textmining_id is a superset of entity_id --> after filtering df_txtID this is not true
    entity_id = set(df_stringmatches["entity_id"].unique())
    textmining_id = set(df_txtID.textmining_id.unique())
    assert len(entity_id.intersection(textmining_id)) == len(entity_id)

    # sanity check that there is a one to one mapping between textmining_id and ENSP --> no --> first remove all ENSPs that are not in DB
    # --> simpler by filtering based on positive integers in species_id column ?
    # get all ENSPs
    ENSP_set = set()
    with open(fn_in_TaxID_2_Proteins_table_STRING, "r") as fh:
        for line in fh:
            ENSP_set |= ast.literal_eval(line.split("\t")[1])
    # reduce DF to relevant ENSPs
    cond = df_txtID["ENSP"].isin(ENSP_set)
    print("reducing df_txtID from {} to {} rows".format(len(cond), sum(cond)))
    df_txtID = df_txtID[cond]
    # sanity check
    assert len(df_txtID["textmining_id"].unique()) == len(df_txtID["ENSP"].unique())
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
    df_stringmatches_sub = df_stringmatches[["PMID", "entity_id"]]
    entity_id_2_PMID_dict = df_stringmatches_sub.groupby("entity_id")["PMID"].apply(set).to_dict()

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
    etype = "-56"
    with open(fn_out_Protein_2_Function_table_PMID, "w") as fh_out:
        for ENSP, PMID_set in ENSP_2_PMID_dict.items():
            PMID_with_prefix_list = ["PMID:" + str(PMID) for PMID in sorted(PMID_set)]
            fh_out.write(ENSP + "\t" + "{" + str(PMID_with_prefix_list)[1:-1].replace(" ", "").replace("'", '"') + "}" + "\t" + etype + "\n")

    # reduce Functions_table_PMID.txt to PMIDs that are in Protein_2_Function_table_PMID.txt
    PMID_set = set(df_stringmatches["PMID"].values)
    # PMID_not_relevant = []
    with open(fn_in_Functions_table_PMID_temp, "r") as fh_in:
        with open(fn_out_Functions_table_PMID, "w") as fh_out:
            for line in fh_in:
                PMID_including_prefix = line.split("\t")[1]
                if int(PMID_including_prefix[5:]) in PMID_set:
                    fh_out.write(line)
                # else:
                #     PMID_not_relevant.append(PMID_including_prefix)


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
    DOWNLOADS_DIR = r"/home/some/path/downloads"
    TABLES_DIR = r"/home/some/path/output/tables"
    etype = "-56" # PMID

    # input files
    all_entities = os.path.join(DOWNLOADS_DIR, "all_entities.tsv")
    string_matches = os.path.join(DOWNLOADS_DIR, "string_matches.tsv")
    TaxID_2_Proteins_table_STRING = os.path.join(TABLES_DIR, "TaxID_2_Proteins_table_STRING.txt")
    Functions_table_PMID_temp = os.path.join(TABLES_DIR, "Functions_table_PMID_temp.txt")

    # output files
    Functions_table_PMID = os.path.join(TABLES_DIR, "Functions_table_PMID.txt")
    Protein_2_Function_table_PMID = os.path.join(TABLES_DIR, "Protein_2_Function_table_PMID.txt")

    create_Protein_2_Function_table_PMID__and__reduce_Functions_table_PMID(all_entities, string_matches, TaxID_2_Proteins_table_STRING, Functions_table_PMID_temp, Functions_table_PMID, Protein_2_Function_table_PMID)