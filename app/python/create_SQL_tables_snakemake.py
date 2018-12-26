import os, json, sys, re, fnmatch, subprocess, time, datetime #, shlex  #, multiprocessing
import gzip
import pandas as pd
import numpy as np
from subprocess import call
# sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import ast, re, obo_parser

import tools, variables, ratio

TYPEDEF_TAG, TERM_TAG = "[Typedef]", "[Term]"
BASH_LOCATION = r"/usr/bin/env bash"
PYTHON_DIR = variables.PYTHON_DIR
LOG_DIRECTORY = variables.LOG_DIRECTORY
POSTGRESQL_DIR = variables.POSTGRESQL_DIR
DOWNLOADS_DIR = variables.DOWNLOADS_DIR
STATIC_DIR = variables.STATIC_POSTGRES_DIR
TABLES_DIR = variables.TABLES_DIR
TEST_DIR = variables.TEST_DIR
FILES_NOT_2_DELETE = variables.FILES_NOT_2_DELETE
NUMBER_OF_PROCESSES = variables.NUMBER_OF_PROCESSES
VERSION_ = variables.VERSION_
PLATFORM = sys.platform


def get_child_2_direct_parent_dict_RCTM_hierarchy(fn_in):
    """
    child_2_parent_dict --> child 2 direct parents
    """
    child_2_parent_dict = {}
    with open(fn_in, "r") as fh_in:
        for line in fh_in:
            parent, child = line.split("\t")
            child = child.strip()
            if child not in child_2_parent_dict:
                child_2_parent_dict[child] = {parent}
            else:
                child_2_parent_dict[child] |= {parent}
    return child_2_parent_dict

def get_parents_iterative(child, child_2_parent_dict):
    """
    par = {"C22":{"C1"}, "C21":{"C1"}, "C1":{"P1"}}
    get_parents_iterative("C22", par)
    """
    if child not in child_2_parent_dict:
        return []
    # important to set() otherwise parent is updated in orig object
    all_parents = set(child_2_parent_dict[child])
    current_parents = set(all_parents)
    while len(current_parents) > 0:
        new_parents = set()
        for parent in current_parents:
            if parent in child_2_parent_dict:
                temp_parents = child_2_parent_dict[parent].difference(all_parents)
                all_parents.update(temp_parents)
                new_parents.update(temp_parents)
        current_parents = new_parents
    return all_parents

def create_protein_2_function_table_Reactome(fn_in, fn_out, child_2_parent_dict, return_all_terms=False):  # term_set_2_use_as_filter
    # entity_type = "-57"
    entity_type = variables.id_2_entityTypeNumber_dict["Reactome"]
    if return_all_terms:
        all_terms = set()
    with open(fn_in, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            line = fh_in.readline()
            taxid, ENSP_without_taxid, term = line.split("\t")
            ENSP = "{}.{}".format(taxid, ENSP_without_taxid)
            term = term.strip()
            term_list = [term] + list(get_parents_iterative(term, child_2_parent_dict))
            if return_all_terms:
                all_terms = all_terms.union(set(term_list))
            ENSP_last = ENSP
            for line in fh_in:
                taxid, ENSP_without_taxid, term = line.split("\t")
                ENSP = "{}.{}".format(taxid, ENSP_without_taxid)
                term = term.strip()
                if ENSP == ENSP_last:
                    term_list += [term] + list(get_parents_iterative(term, child_2_parent_dict))
                    if return_all_terms:
                        all_terms = all_terms.union(set(term_list))
                else:
                    term_string_array = "{" + str(sorted(set(term_list)))[1:-1].replace("'", '"') + "}"
                    fh_out.write(ENSP_last + "\t" + term_string_array + "\t" + entity_type + "\n")
                    term_list = [term] + list(get_parents_iterative(term, child_2_parent_dict))
                    if return_all_terms:
                        all_terms = all_terms.union(set(term_list))
                ENSP_last = ENSP
            term_string_array = "{" + str(sorted(set(term_list)))[1:-1].replace("'", '"') + "}"
            fh_out.write(ENSP_last + "\t" + term_string_array + "\t" + entity_type + "\n")
            term_list = [term] + list(get_parents_iterative(term, child_2_parent_dict))
            if return_all_terms:
                all_terms = all_terms.union(set(term_list))
                return all_terms

def create_Functions_table_Reactome(fn_in, fn_out, term_2_level_dict, all_terms):
    """
    :param fn_in: String (RCTM_associations_sorted.txt)
    :param fn_out: String (Function_table_RCTM.txt)
    :param term_2_level_dict: Dict(key: RCTM-term, val: hierarchical level)
    :param all_terms: Set of String (with all RCTM terms that have any association with the given ENSPs)
    :return: Tuple (List of terms with hierarchy, Set of terms without hierarchy)
    do a sanity check: are terms without a hierarchy used in protein_2_function
    create file Functions_table_Reactome.txt
    etype, term, name, definition, description # old
    | enum | etype | an | description | year | level | # new
    """
    # entity_type = "-57"
    entity_type = variables.id_2_entityTypeNumber_dict["Reactome"]
    year = "-1"
    terms_with_hierarchy, terms_without_hierarchy = [], []
    with open(fn_in, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            for line in fh_in:
                term, url_, description = line.split("\t")
                if term.startswith("R-"):  # R-ATH-109581 --> ATH-109581
                    term = term[2:]
                description = description.strip()
                try:
                    level = term_2_level_dict[term]
                    terms_with_hierarchy.append(term)
                except KeyError:
                    terms_without_hierarchy.append(term)
                    level = "-1"
                if term in all_terms:  # filter relevant terms that occur in protein_2_functions_tables_RCTM.txt
                    fh_out.write(entity_type + "\t" + term + "\t" + description + "\t" + year + "\t" + str(level) + "\n")
    return sorted(set(terms_with_hierarchy)), sorted(set(terms_without_hierarchy))

def get_random_direct_lineage(child, child_2_parent_dict, lineage=[]):
    """
    child = "ATH-111997"
    get_random_direct_lineage(child, child_2_parent_dict)
    """
    try:
        parents = child_2_parent_dict[child]
    except KeyError:
        return lineage  # already at root
    if len(parents) == 0: # already at root as well (for other cases)
        return lineage
    for parent in parents:  # select random parent
        lineage.append(parent)
        return get_random_direct_lineage(parent, child_2_parent_dict, lineage)

def get_all_lineages(child, child_2_parent_dict):
    """
    child included in lineage
    child = "ATH-111997"
    get_all_lineages(child, child_2_parent_dict)
    --> [['ATH-111997', 'ATH-1489509', 'ATH-9006925', 'ATH-162582'],
    ['ATH-111997', 'ATH-111996', 'ATH-112043', 'ATH-112040', 'ATH-111885', 'ATH-418594', 'ATH-388396', 'ATH-372790', 'ATH-162582']]
    """
    all_lineages = []
    parents_2_remove = set()
    try:
        direct_parents = child_2_parent_dict[child]  # {'BTA-927802'}
    except KeyError:
        direct_parents = []
    while True:
        if len(direct_parents - parents_2_remove) == 0:
            return all_lineages
        else:
            parent = list(direct_parents - parents_2_remove)[0]  # 'BTA-927802'
            lineage = [child, parent] + get_random_direct_lineage(parent, child_2_parent_dict, lineage=[])
            all_lineages.append(lineage)
            parents_2_remove.update(set(lineage))

def get_term_2_level_dict(child_2_parent_dict):
    """
    calculate level of hierarchy for data
    if term in hierarchy --> default to level 1
    if term not in hierarchy --> not present in dict
    """
    term_2_level_dict = {}
    for child in child_2_parent_dict.keys():
        lineages = get_all_lineages(child, child_2_parent_dict)

        # set default to 1, lineages include children
        for lineage in lineages:
            for term in lineage:
                term_2_level_dict[term] = 1

        max_lineage = 0
        for lineage in lineages:
            if len(lineage) > max_lineage:
                max_lineage = len(lineage)
        term_2_level_dict[child] = max_lineage
    return term_2_level_dict

def create_table_Protein_2_Function_table_RCTM__and__Function_table_RCTM(fn_associations, fn_descriptions, fn_hierarchy, fn_protein_2_function_table_RCTM, fn_functions_table_RCTM, number_of_processes):
    """
    fn_associations=snakemake.input[0],
    fn_descriptions=snakemake.input[1],
    fn_hierarchy=snakemake.input[2],
    fn_protein_2_function_table_RCTM=snakemake.output[0],
    fn_functions_table_RCTM=snakemake.output[1],
    number_of_processes=snakemake.config["number_of_processes"]
    """
    if variables.VERBOSE:
        print("### creating 2 tables:\n - Protein_2_Function_table_RCTM.txt\n - Function_table_RCTM.txt\n")
    # fn_associations = os.path.join(DOWNLOADS_DIR, fn_associations)
    # fn_associations_sorted = fn_associations + "_sorted.txt"
    # sort on first two columns in order to get all functional associations for a given ENSP in one block
    tools.sort_file(fn_associations, fn_associations, number_of_processes=number_of_processes, verbose=variables.VERBOSE)
    # fn_descriptions = os.path.join(DOWNLOADS_DIR, fn_descriptions)
    # fn_hierarchy = os.path.join(DOWNLOADS_DIR, fn_hierarchy)  # parent-child not child-parent
    # fn_protein_2_function_table_RCTM = os.path.join(TABLES_DIR, "Protein_2_Function_table_RCTM.txt")
    # fn_functions_table_RCTM = os.path.join(TABLES_DIR, "Functions_table_RCTM.txt")
    child_2_parent_dict = get_child_2_direct_parent_dict_RCTM_hierarchy(fn_hierarchy)  # child_2_parent_dict --> child 2 direct parents
    term_2_level_dict = get_term_2_level_dict(child_2_parent_dict)
    all_terms = create_protein_2_function_table_Reactome(fn_in=fn_associations, fn_out=fn_protein_2_function_table_RCTM, child_2_parent_dict=child_2_parent_dict, return_all_terms=True)
    terms_with_hierarchy, terms_without_hierarchy = create_Functions_table_Reactome(fn_in=fn_descriptions, fn_out=fn_functions_table_RCTM, term_2_level_dict=term_2_level_dict, all_terms=all_terms)
    if variables.VERBOSE:
        print("number of terms_without_hierarchy", len(terms_without_hierarchy))
        print("## done with RCTM tables")

def map_string_2_interpro(fn_in_string2uniprot, fn_in_uniprot2interpro, fn_out_string2interpro):
    """
    fn_in_string2uniprot=snakemake.input[0],
    fn_in_uniprot2interpro=snakemake.input[1],
    fn_out_string2interpro=snakemake.output[0]
    read string to uniprot mapping and reverse
    input line e.g. 742765.HMPREF9457_01522 [TAB] G1WQX1
    """
    uniprot2string = {}
    # with gzip.open(input.string2uniprot,'rt') as f:
    with open(fn_in_string2uniprot, 'r') as fh_string2uniprot:
        for line in fh_string2uniprot:
            if line.startswith('#'):
                continue
            # string_id, uniprot_ac = line.rstrip().split('\t')
            split_ = line.strip().split()
            uniprot_ac = split_[1].split("|")[0]
            string_id = split_[2]
            uniprot2string[uniprot_ac] = string_id

    # read uniprot to interpro mapping and map to string (one to many, i.e. string_id:list_interpro_entries)
    # input line e.g.  G1WQX1 [TAB] IPR021778 [TAB] Domain of unknown function DUF3343 [TAB] PF11823 [TAB] 8 [TAB] 68
    string2interpro = {}
    with gzip.open(fn_in_uniprot2interpro, 'rt') as fh_in: # read binary file
        for line in fh_in:
            l = line.split('\t')
            uniprot_ac = l[0]
            if uniprot_ac in uniprot2string:
                string_id = uniprot2string[uniprot_ac]
                if string_id not in string2interpro:
                    string2interpro[string_id] = []
                string2interpro[string_id].append(line)

    # write out string2interpro mapping
    # output line e.g. 742765.HMPREF9457_01522 [TAB] G1WQX1 [TAB] IPR021778 [TAB] Domain of unknown function DUF3343 [TAB] PF11823 [TAB] 8 [TAB] 68
    with gzip.open(fn_out_string2interpro, 'wt') as fh_out:
    # with open(fn_out_string2interpro, 'w') as fh_out:  # gzip.open
        for string_id in string2interpro:
            for line in string2interpro[string_id]:
                # fh_out.write('%s\t%s'%(string_id, line))
                fh_out.write("{}\t{}".format(string_id, line))

def create_Functions_table_InterPro(fn_in, fn_out):
    """
    # | enum | etype | an | description | year | level |
    """
    df = pd.read_csv(fn_in, sep='\t', names=["an", "description"])
    df["etype"] = variables.id_2_entityTypeNumber_dict["INTERPRO"]
    df["year"] = "-1"
    df["level"] = "-1"
    df = df[["etype", "an", "description", "year", "level"]]
    df.to_csv(fn_out, sep="\t", header=False, index=False)

def create_Functions_table_KEGG(fn_in, fn_out, verbose=True):
    """
    # | enum | etype | an | description | year | level |
    """
    etype = variables.id_2_entityTypeNumber_dict["KEGG"]
    level = "-1"
    year = "-1"
    if verbose:
        print("creating {} ".format(fn_out))
    with open(fn_out, "w") as fh_out:
        with open(fn_in, "r") as fh_in:
            for line in fh_in:
                if line.startswith("#"):
                    continue
                an, description = line.strip().split("\t")
                an = "map" + an
                string_2_write = etype + "\t" + an + "\t" + description + "\t" + year +"\t" + level + "\n"
                fh_out.write(string_2_write)

def create_Functions_table_SMART(fn_in, fn_out, max_len_description):
    """
    # | enum | etype | an | description | year | level |
    """
    # http://smart.embl-heidelberg.de/smart/descriptions.pl downloaded 20180808
    columns = ['DOMAIN', 'ACC', 'DEFINITION', 'DESCRIPTION']
    df = pd.read_csv(fn_in, sep="\t", skiprows=2, names=columns)
    # "etype" --> -53
    # "name" --> "DOMAIN"
    # "an" --> "ACC"
    # "definition" --> "DEFINITION; DESCRIPTION"
    entityType_SMART = variables.id_2_entityTypeNumber_dict["SMART"]
    df["etype"] = entityType_SMART
    df = df[["etype", "DOMAIN", "ACC", "DEFINITION", "DESCRIPTION"]]
    df["definition"] = df["DEFINITION"].fillna("") + "; " + df["DESCRIPTION"].fillna("")
    df["definition"] = df["definition"].apply(lambda x: x.replace("\n", "").replace("\t", " "))
    df = df[["etype", "DOMAIN", "ACC", "definition"]]
    df = df.rename(index=str, columns={"DOMAIN": "name", "ACC": "an"})
    df["description"] = df[["name", "definition"]].apply(parse_SMART, axis=1, args=(max_len_description, ))
    df["year"] = "-1"
    df["level"] = "-1"
    df = df[["etype", "an", "description", "year", "level"]]
    df.to_csv(fn_out, sep="\t", header=False, index=False)

def parse_SMART(s, max_len_description=80):
    name = s["name"].strip()
    definition = s["definition"].strip().split(";")
    if definition[0].strip():  # not empty string
        string_ = definition[0].strip()
    elif definition[1].strip():  # not empty string
        string_ = definition[1].strip()
    else:
        string_ = name
    string_ = cut_long_string_at_word(string_, max_len_description=max_len_description)
    return string_

def create_Functions_table_PFAM(fn_in, fn_out):
    # ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.clans.tsv.gz (from 24/02/2017 downloaded 20180808)
    # fn = r"/home/dblyon/agotool/data/PostgreSQL/downloads/Pfam-A.clans.tsv"
    # fn_out = r"/home/dblyon/agotool/data/PostgreSQL/tables/Functions_table_PFAM.txt"
    columns = ['an', 'clan_an', 'HOMSTRAD', 'name', 'description']
    df = pd.read_csv(fn_in, sep="\t", names=columns)
    df["etype"] = variables.id_2_entityTypeNumber_dict["PFAM"]
    df["year"] = "-1"
    df["level"] = "-1"
    df = df[["etype", "an", "description", "year", "level"]]
    df.to_csv(fn_out, sep="\t", header=False, index=False)

def create_Functions_table_GO_or_UPK(fn_in_go_basic, fn_out_functions, is_upk=False):
    """
    # fn_in_go_basic = os.path.join(DOWNLOADS_DIR, "go-basic.obo")
    # fn_out_funcs = os.path.join(TABLES_DIR, "Functions_table_GO.txt")
    # ### functions [Functions_table_STRING.txt]
    # | enum | etype | an | description | year | level |
    id_, name --> Functions_table.txt
    id_, is_a_list --> Child_2_Parent_table_GO.txt
    :return:
    """
    obo = obo_parser.OBOReader_2_text(fn_in_go_basic)
    GO_dag = obo_parser.GODag(obo_file=fn_in_go_basic, upk=is_upk)
    year = "-1"
    child_2_parent_dict = get_child_2_direct_parent_dict_from_dag(GO_dag) # obsolete or top level terms have empty set for parents
    term_2_level_dict = get_term_2_level_dict(child_2_parent_dict)
    with open(fn_out_functions, "w") as fh_funcs:
        for entry in obo:
            id_, name, is_a_list, definition = entry # name --> description
            an = id_
            description = name
            # ('GO:0000001', 'mitochondrion inheritance', ['GO:0048308', 'GO:0048311'], '"The distribution of mitochondria, including the mitochondrial genome, into daughter cells after mitosis or meiosis, mediated by interactions between mitochondria and the cytoskeleton." [GOC:mcc, PMID:10873824, PMID:11389764]')
            # ('KW-0001', '2Fe-2S', ['KW-0411', 'KW-0479'], '"Protein which contains at least one 2Fe-2S iron-sulfur cluster: 2 iron atoms complexed to 2 inorganic sulfides and 4 sulfur atoms of cysteines from the protein." []')
            if not is_upk:
                etype = str(get_entity_type_from_GO_term(id_, GO_dag))
            else:
                etype = "-51"

            if str(etype) == "-24": # don't need obsolete GO terms
                continue

            try:
                level = str(term_2_level_dict[an])
            except KeyError:
                level = "-1"
            line2write_func = etype + "\t" + an + "\t" + description + "\t" + year + "\t" + level + "\n"
            fh_funcs.write(line2write_func)

def get_child_2_direct_parent_dict_from_dag(dag):
    """
    e.g. {'GO:1901681': {'GO:0005488'},
    'GO:0090314': {'GO:0090313', 'GO:0090316', 'GO:1905477'}, ...}
    """
    child_2_direct_parents_dict = {}
    for name, term_object in dag.items():
        child_2_direct_parents_dict[name] = {p.id for p in term_object.parents}
    return child_2_direct_parents_dict

def get_entity_type_from_GO_term(term, GO_dag):
    if term == "GO:0003674" or GO_dag[term].has_parent("GO:0003674"):
        return "-23"
    elif term == "GO:0005575" or GO_dag[term].has_parent("GO:0005575"):
        return "-22"
    elif term == "GO:0008150" or GO_dag[term].has_parent("GO:0008150"):
        return "-21"
    else:
        return "-24"

def cut_long_string_at_word(string_, max_len_description=80):
    try:
        len_string = len(string_)
    except TypeError:
        return ""
    if len_string > max_len_description:
        string_2_use = ""
        for word in string_.split(" "):
            if len(string_2_use + word) > max_len_description:
                string_2_return = string_2_use.strip() + " ..."
                assert len(string_2_return) <= (max_len_description + 4)
                return string_2_return
            else:
                string_2_use += word + " "
    else:
        return string_.strip()

def clean_messy_string(string_):
    try:
        return re.sub('[^A-Za-z0-9\s]+', '', string_).replace("\n", " ").replace("\t", " ")
    except TypeError:
        return string_

def concatenate_Functions_tables(fn_list_str, fn_out_temp, fn_out, number_of_processes):
    # fn_list = [os.path.join(TABLES_DIR, fn) for fn in ["Functions_table_GO.txt", "Functions_table_UPK.txt", "Functions_table_KEGG.txt", "Functions_table_SMART.txt", "Functions_table_PFAM.txt", "Functions_table_InterPro.txt", "Functions_table_RCTM.txt"]]
    fn_list = fn_list_str.split(" ")
    # concatenate files
    tools.concatenate_files(fn_list, fn_out_temp)
    # sort
    tools.sort_file(fn_out_temp, fn_out_temp, number_of_processes=number_of_processes)
    # add functional enumeration column
    with open(fn_out_temp, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            for enum, line in enumerate(fh_in):
                fh_out.write(str(enum) + "\t" + line)

# def create_TaxID_2_Proteins_table(fn_in, fn_out, number_of_processes=1, verbose=True):
#     if verbose:
#         print("Creating TaxID_2_Proteins_table.txt")
#         print("Proteomes_input_table_temp.txt needs sorting, doing it now")
#     tools.sort_file(fn_in, fn_in, columns="1", fn_bash_script="bash_script_sort_Proteomes_input_table_temp.sh", number_of_processes=number_of_processes, verbose=verbose)
#     if verbose:
#         print("parsing Proteomes_input_table_temp.txt")
#     # now parse and transform into wide format
#     with open(fn_in, "r") as fh_in:
#         with open(fn_out, "w") as fh_out:
#             ENSP_list = []
#             did_first = False
#             for line in fh_in:
#                 # 287.DR97_1012   6412
#                 # 287.DR97_1013   6413
#                 ENSP, *rest = line.strip().split()
#                 TaxID = ENSP[:ENSP.index(".")]
#                 if not did_first:
#                     TaxID_previous = TaxID
#                     did_first = True
#                 if TaxID == TaxID_previous:
#                     ENSP_list.append(ENSP)
#                 else:
#                     ENSPs_2_write = sorted(set(ENSP_list))
#                     fh_out.write(TaxID_previous + "\t" + format_list_of_string_2_postgres_array(ENSPs_2_write) + "\t" + str(len(ENSPs_2_write)) + "\n")
#                     ENSP_list = [ENSP]
#                     TaxID_previous = TaxID
#             ENSPs_2_write = sorted(set(ENSP_list))
#             fh_out.write(TaxID_previous + "\t" + format_list_of_string_2_postgres_array(ENSPs_2_write) + "\t" + str(len(ENSPs_2_write)) + "\n")

def format_list_of_string_2_postgres_array(list_of_string):
    """
    removes internal spaces
    :param list_of_string: List of String
    :return: String
    """
    return "{" + str(list_of_string)[1:-1].replace(" ", "").replace("'", '"') + "}"

def get_function_an_2_enum__and__enum_2_function_an_dict_from_flat_file(fn_Functions_table_STRING):
    function_2_enum_dict, enum_2_function_dict = {}, {}
    with open(fn_Functions_table_STRING, "r") as fh_in:
        for line in fh_in:
            line_split = line.split("\t")
            enum = line_split[0]
            function_ = line_split[2]
            function_2_enum_dict[function_] = enum
            enum_2_function_dict[enum] = function_
    return function_2_enum_dict, enum_2_function_dict

def Protein_2_Function_table_map_function_2_function_enumeration(fn_Functions_table_STRING, fn_in_Protein_2_function_table_STRING, fn_out_Protein_2_functionEnum_table_STRING):
    function_2_enum_dict, enum_2_function_dict = get_function_an_2_enum__and__enum_2_function_an_dict_from_flat_file(fn_Functions_table_STRING)
    with open(fn_in_Protein_2_function_table_STRING, "r") as fh_in:
        with open(fn_out_Protein_2_functionEnum_table_STRING, "w") as fh_out:
            ENSP_last, function_arr_str, etype = fh_in.readline().strip().split("\t")
            function_arr = ast.literal_eval(function_arr_str)
            functionEnum_list = _helper(function_arr, function_2_enum_dict)

            for line in fh_in:
                ENSP, function_arr_str, etype = line.strip().split("\t")
                function_arr = ast.literal_eval(function_arr_str)

                if ENSP == ENSP_last:
                    functionEnum_list += _helper(function_arr, function_2_enum_dict)
                else:
                    fh_out.write(ENSP_last + "\t" + "{" + str(sorted(functionEnum_list))[1:-1] + "}" + "\n") # etype is removed
                    functionEnum_list = _helper(function_arr, function_2_enum_dict)

                ENSP_last = ENSP
            fh_out.write(ENSP + "\t" + "{" + str(sorted(functionEnum_list))[1:-1] + "}" + "\n") # etype is removed

def _helper(function_arr, function_2_enum_dict):
    functionEnum_list = []
    for ele in function_arr:
        try:
            functionEnum_list.append(function_2_enum_dict[ele])
        except KeyError:
            print(ele)
            raise StopIteration
    return functionEnum_list

def create_Lineage_table_STRING(fn_in_go_basic, fn_in_keywords, fn_in_rctm_hierarchy, fn_in_functions, fn_out_lineage_table):
    lineage_dict = get_lineage_dict_for_all_entity_types_with_ontologies(fn_in_go_basic, fn_in_keywords, fn_in_rctm_hierarchy)
    year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr = get_lookup_arrays(fn_in_functions, low_memory=True)
    term_2_enum_dict = {key: val for key, val in zip(functionalterm_arr, indices_arr)}
    lineage_dict_enum = {}
    term_no_translation_because_obsolete = []
    for key, val in lineage_dict.items():
        try:
            key_enum = term_2_enum_dict[key]
        except KeyError:
            term_no_translation_because_obsolete.append(key)
            continue
        term_enum_temp = []
        for ele in val:
            try:
                term_enum_temp.append(term_2_enum_dict[ele])
            except KeyError:
                term_no_translation_because_obsolete.append(ele)
        lineage_dict_enum[key_enum] = sorted(term_enum_temp)
    keys_sorted = sorted(lineage_dict_enum.keys())
    with open(fn_out_lineage_table, "w") as fh_out:
        for key in keys_sorted:
            fh_out.write(str(key) + "\t" + "{" + str(sorted(set(lineage_dict_enum[key])))[1:-1].replace("'", '"') + "}\n")

def get_lineage_dict_for_all_entity_types_with_ontologies(fn_go_basic_obo, fn_keywords_obo, fn_rctm_hierarchy):
    lineage_dict = {}
    go_dag = obo_parser.GODag(obo_file=fn_go_basic_obo)
    upk_dag = obo_parser.GODag(obo_file=fn_keywords_obo, upk=True)
    # key=GO-term, val=set of GO-terms (parents)
    for go_term_name in go_dag:
        GOTerm_instance = go_dag[go_term_name]
        lineage_dict[go_term_name] = GOTerm_instance.get_all_parents().union(GOTerm_instance.get_all_children())
    for term_name in upk_dag:
        Term_instance = upk_dag[term_name]
        lineage_dict[term_name] = Term_instance.get_all_parents().union(Term_instance.get_all_children())
    lineage_dict.update(get_lineage_Reactome(fn_rctm_hierarchy))
    return lineage_dict

def get_lineage_Reactome(fn_hierarchy):
    child_2_parent_dict = get_child_2_direct_parent_dict_RCTM_hierarchy(fn_hierarchy)
    parent_2_children_dict = get_parent_2_children_dict(fn_hierarchy)
    lineage_dict = {}
    for parent, children in parent_2_children_dict.items():
        lineage_dict[parent] = children
    for child in child_2_parent_dict:
        parents = get_parents_iterative(child, child_2_parent_dict)
        if child in lineage_dict:
            lineage_dict[child].union(parents)
        else:
            lineage_dict[child] = parents
    return lineage_dict

def get_parent_2_children_dict(fn_hierarchy):
    parent_2_children_dict = {}
    with open(fn_hierarchy, "r") as fh_in:
        for line in fh_in:
            parent, child = line.split("\t")
            child = child.strip()
            if parent not in parent_2_children_dict:
                parent_2_children_dict[parent] = {child}
            else:
                parent_2_children_dict[parent] |= {child}
    return parent_2_children_dict

def get_lookup_arrays(fn_in_functions, low_memory):
    """
    funcEnum_2_hierarchical_level
    simple numpy array of hierarchical levels
    if -1 in DB --> convert to np.nan since these are missing values
    # - funcEnum_2_year
    # - funcEnum_2_hierarchical_level
    # - funcEnum_2_etype
    # - funcEnum_2_description
    # - funcEnum_2_term
    :param fn_in_functions: String (file name for functions_table)
    :param low_memory: Bool flag to return description_array
    :return: immutable numpy array of int
    """
    result = yield_split_line_from_file(fn_in_functions, line_numbers=True)
    shape_ = next(result)
    year_arr = np.full(shape=shape_, fill_value=-1, dtype="int16")  # Integer (-32768 to 32767)
    entitytype_arr = np.full(shape=shape_, fill_value=0, dtype="int8")
    if not low_memory:
        description_arr = np.empty(shape=shape_, dtype=object) # ""U261"))
        # category_arr = np.empty(shape=shape_, dtype=np.dtype("U49"))  # description of functional category (e.g. "Gene Ontology biological process")
        category_arr = np.empty(shape=shape_, dtype=object)  # description of functional category (e.g. "Gene Ontology biological process")
    functionalterm_arr = np.empty(shape=shape_, dtype=object) #np.dtype("U13"))
    hierlevel_arr = np.full(shape=shape_, fill_value=-1, dtype="int8")  # Byte (-128 to 127)
    indices_arr = np.arange(shape_, dtype=np.dtype("uint32"))
    indices_arr.flags.writeable = False

    for res in result:
        func_enum, etype, term, description, year, hierlevel = res
        func_enum = int(func_enum)
        etype = int(etype)
        try:
            year = int(year)
        except ValueError: # e.g. "...."
            year = -1
        hierlevel = int(hierlevel)
        entitytype_arr[func_enum] = etype
        functionalterm_arr[func_enum] = term
        year_arr[func_enum] = year
        hierlevel_arr[func_enum] = hierlevel
        if not low_memory:
            description_arr[func_enum] = description
            category_arr[func_enum] = variables.entityType_2_functionType_dict[etype]

    year_arr.flags.writeable = False # make it immutable
    hierlevel_arr.flags.writeable = False
    entitytype_arr.flags.writeable = False
    functionalterm_arr.flags.writeable = False
    if not low_memory:
        description_arr.flags.writeable = False
        category_arr.flags.writeable = False
        return year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr
    else:
        return year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr

def yield_split_line_from_file(fn_in, line_numbers=False, split_on="\t"):
    if line_numbers:
        num_lines = tools.line_numbers(fn_in)
        yield num_lines

    with open(fn_in, "r") as fh_in:
        for line in fh_in:
            line_split = line.split(split_on)
            line_split[-1] = line_split[-1].strip()
            yield line_split




def create_TaxID_2_Proteins_table(fn_in_protein_shorthands, fn_out_TaxID_2_Proteins_table_STRING, number_of_processes=1, verbose=True):
    if verbose:
        print("Creating TaxID_2_Proteins_table.txt")
        print("protein_shorthands needs sorting, doing it now")
    tools.sort_file(fn_in_protein_shorthands, fn_in_protein_shorthands, columns="1", number_of_processes=number_of_processes, verbose=verbose)
    if verbose:
        print("parsing protein_shorthands")
    # now parse and transform into wide format
    with open(fn_in_protein_shorthands, "r") as fh_in:
        with open(fn_out_TaxID_2_Proteins_table_STRING, "w") as fh_out:
            ENSP_list = []
            did_first = False
            for line in fh_in:
                # 287.DR97_1012   6412
                # 287.DR97_1013   6413
                ENSP, *rest = line.strip().split()
                TaxID = ENSP[:ENSP.index(".")]
                if not did_first:
                    TaxID_previous = TaxID
                    did_first = True
                if TaxID == TaxID_previous:
                    ENSP_list.append(ENSP)
                else:
                    ENSPs_2_write = sorted(set(ENSP_list))
                    fh_out.write(TaxID_previous + "\t" + format_list_of_string_2_postgres_array(ENSPs_2_write) + "\t" + str(len(ENSPs_2_write)) + "\n")
                    ENSP_list = [ENSP]
                    TaxID_previous = TaxID
            ENSPs_2_write = sorted(set(ENSP_list))
            fh_out.write(TaxID_previous + "\t" + format_list_of_string_2_postgres_array(ENSPs_2_write) + "\t" + str(len(ENSPs_2_write)) + "\n")

def create_Taxid_2_FunctionCountArray_table_STRING(Protein_2_FunctionEnum_table_STRING, Functions_table_STRING, fn_out_Taxid_2_FunctionCountArray_table_STRING, number_of_processes=1):
    # - sort Protein_2_FunctionEnum_table_STRING.txt
    # - create array of zeros of function_enumeration_length
    # - for line in Protein_2_FunctionEnum_table_STRING
    #     add counts to array until taxid_new != taxid_previous
    tools.sort_file(Protein_2_FunctionEnum_table_STRING, Protein_2_FunctionEnum_table_STRING, number_of_processes=number_of_processes)
    num_lines = tools.line_numbers(Functions_table_STRING)
    with open(fn_out_Taxid_2_FunctionCountArray_table_STRING, "w") as fh_out:
        with open(Protein_2_FunctionEnum_table_STRING, "r") as fh_in:
            funcEnum_count_background = np.zeros(shape=num_lines, dtype=np.dtype("uint32"))
            line = next(fh_in)
            taxid_previous, ENSP, funcEnum_set = helper_parse_line_Protein_2_FunctionEnum_table_STRING(line)
            funcEnum_count_background = helper_count_funcEnum(funcEnum_count_background, funcEnum_set)

            for line in fh_in:
                taxid, ENSP, funcEnum_set = helper_parse_line_Protein_2_FunctionEnum_table_STRING(line)
                if taxid != taxid_previous:
                    background_n, index_backgroundCount_array_string = helper_format_funcEnum(funcEnum_count_background)
                    fh_out.write(taxid + "\t" + background_n + "\t" + index_backgroundCount_array_string + "\n")
                    funcEnum_count_background = np.zeros(shape=num_lines, dtype=np.dtype("uint32"))

                funcEnum_count_background = helper_count_funcEnum(funcEnum_count_background, funcEnum_set)
                taxid_previous = taxid
            background_n, index_backgroundCount_array_string = helper_format_funcEnum(funcEnum_count_background)
            fh_out.write(taxid + "\t" + background_n + "\t" + index_backgroundCount_array_string + "\n")

    # for taxid, ans_set in
        # get_ANs_of_taxid(fn_in_TaxID_2_Proteins_table_STRING):  #     pass

        # fn_Functions_table_STRING, fn_out_Function_2_ENSP_table_STRING_enum , fn_out_funcount, number_of_processes=1):
    # create_functions_2_ENSP_table(pqo, fn_out, number_of_processes=1, verbose=True)
    # function_2_enum_dict, enum_2_function_dict = get_function_an_2_enum__and__enum_2_function_an_dict_from_flat_file(fn_Functions_table_STRING)
    # fn_in = os.path.join(TABLES_DIR, "Function_2_ENSP_table_STRING.txt")
    # # fn_out_Function_2_ENSP_table_STRING_enum = os.path.join(TABLES_DIR, "Function_2_ENSP_table_STRING_enum.txt")
    # add_enumerations_2_Function_2_ENSP_table(fn_in, fn_out_Function_2_ENSP_table_STRING_enum , function_2_enum_dict, number_of_processes)
    # create_Taxid_2_FunctionCountArray_table_STRING_helper(fn_out_Function_2_ENSP_table_STRING_enum, fn_out_funcount)

# def get_ANs_of_taxid(TaxID_2_Proteins_table_STRING):
#     with open(TaxID_2_Proteins_table_STRING, "r") as fh:
#         for line in fh:
#             taxid, ensp_str, number_of_ENSPs = line.split("\t")
#             number_of_ENSPs = int(number_of_ENSPs.strip())
#             ENSPs_set = ast.literal_eval(ensp_str)
#             assert number_of_ENSPs == len(ENSPs_set)
#             yield taxid, ENSPs_set

def helper_parse_line_Protein_2_FunctionEnum_table_STRING(line):
    ENSP, funcEnum_set = line.split("\t")
    funcEnum_set = ast.literal_eval(funcEnum_set.strip())
    taxid = ENSP.split(".")[0]
    return taxid, ENSP, funcEnum_set

def helper_count_funcEnum(funcEnum_count, funcEnum_set):
    for funcEnum in funcEnum_set:
        funcEnum_count[funcEnum] += 1
    return funcEnum_count

def helper_format_funcEnum(funcEnum_count_background):
    background_n = np.count_nonzero(funcEnum_count_background)
    enumeration_arr = np.arange(0, funcEnum_count_background.shape[0])
    cond = funcEnum_count_background > 0
    funcEnum_count_background = funcEnum_count_background[cond]
    enumeration_arr = enumeration_arr[cond]
    string_2_write = ""
    for ele in zip(funcEnum_count_background, enumeration_arr):
        string_2_write += "{{{0},{1}}},".format(ele[0], ele[1])
    index_backgroundCount_array_string = "{" + string_2_write[:-1] + "}"
    return background_n, index_backgroundCount_array_string

# def create_functions_2_ENSP_table(pqo, fn_out, number_of_processes=1, verbose=True):
#     if verbose:
#         print("creating functions_2_ENSP_table this will take a while")
#     taxid_list = query.get_taxids()
#     with open(fn_out, "w") as fh_out:
#         for taxid in sorted(taxid_list):
#             ans_list = sorted(query.get_proteins_of_taxid(taxid))
#             etype_2_association_dict = pqo.get_association_dict_split_by_category(ans_list)
#             for etype in sorted(variables.entity_types_with_data_in_functions_table):
#                 assoc_dict = etype_2_association_dict[etype]
#                 association_2_count_dict, association_2_ANs_dict, ans_counter = ratio.count_terms_manager(set(ans_list), assoc_dict)
#                 # ans_counter --> number of AccessionNumbers with any association = background_n
#                 # association_2_count_dict --> number of associations per given Association” = background_count
#                 for association, ans in association_2_ANs_dict.items():
#                     assert ans_counter >= association_2_count_dict[association]
#                     fh_out.write(str(taxid) + "\t" + str(etype) + "\t" + association + "\t" + str(association_2_count_dict[association]) + "\t" + str(ans_counter) + "\t" + format_list_of_string_2_postgres_array(ans) + "\n")
#     tools.sort_file(fn_out, fn_out, columns="1,2", number_of_processes=number_of_processes, verbose=verbose)
#     if verbose:
#         print("finished creating functions_2_ENSP_table")


# def add_enumerations_2_Function_2_ENSP_table(fn_in, fn_out, function_2_enum_dict, number_of_processes):
#     print("sorting the input {}".format(fn_in))
#     tools.sort_file(fn_in, fn_in, columns="1,2", number_of_processes=number_of_processes, verbose=True) # #!!! uncomment (should already be sorted, but do to be sure)
#     print("creating new table \n{}\n".format(fn_out))
#     with open(fn_in, "r") as fh_in:
#         with open(fn_out, "w") as fh_out:
#             for line in fh_in:
#                 taxid, etype, term_an, background_count, background_n, an_array = line.split("\t")
#                 term_enum = function_2_enum_dict[term_an]
#                 fh_out.write(taxid + "\t" + etype + "\t" + term_an + "\t" + str(term_enum) + "\t" + background_count + "\t" + background_n + "\t" + an_array) # no newline necessary

# def create_Taxid_2_FunctionCountArray_table_STRING_helper(fn_in, fn_out_funcount, number_of_processes=1):
#     print("sorting the input {}".format(fn_in))
#     tools.sort_file(fn_in, fn_in, columns="1,2", number_of_processes=number_of_processes, verbose=True) # #!!! uncomment (should already be sorted, but do to be sure)
#     print("creating new table \n{}\n".format(fn_out_funcount))
#     ### new table with
#     ### taxid, background_n, background_count_array (corresponds to functionalterm_arr indices, therefore sorted by term_enum, same length as term_enum)
#     max_background_count = 0
#     with open(fn_in, "r") as fh_in:
#         taxid, etype, term_an, term_enum, background_count, background_n, an_array = fh_in.readline().split("\t")
#         taxid_last = taxid
#         background_n_last = background_n
#         if int(background_count) > max_background_count:
#             max_background_count = int(background_count)
#         index_background_count_list = [(term_enum, int(background_count))]
#         with open(fn_out_funcount, "w") as fh_out_funcount:
#             for line in fh_in:
#                 taxid, etype, term_an, term_enum, background_count, background_n, an_array = line.split("\t")
#                 if int(background_count) > max_background_count:
#                     max_background_count = int(background_count)
#                 if taxid == taxid_last:
#                     index_background_count_list.append((term_enum, int(background_count)))
#                 else:
#                     index_backgroundCount_array_string = helper_list_of_tuples_2_Postgres_array(index_background_count_list)
#                     fh_out_funcount.write(taxid_last + "\t" + background_n_last + "\t" + index_backgroundCount_array_string + "\n")
#                     index_background_count_list = [(term_enum, int(background_count))]
#                 taxid_last = taxid
#                 background_n_last = background_n
#             index_backgroundCount_array_string = helper_list_of_tuples_2_Postgres_array(index_background_count_list)
#             fh_out_funcount.write(taxid + "\t" + background_n + "\t" + index_backgroundCount_array_string + "\n")
#     print("max_background_count: {}".format(max_background_count))

# def helper_list_of_tuples_2_Postgres_array(index_background_count_list):
#     """
#     in: [(4, 1), (2, 6), (1, 7)]
#     out: '{{1,7},{2,6},{4,1}}'
#     :param index_background_count_list:
#     :return:
#     """
#     index_background_count_list.sort(key=lambda tup: tup[0])
#     index_backgroundCount_array_string = ""
#     for ele in index_background_count_list:
#         index_backgroundCount_array_string += "{{{0},{1}}},".format(ele[0], ele[1])
#     return "{" + index_backgroundCount_array_string[:-1] + "}"

if __name__ == "__main__":
#     create_table_Protein_2_Function_table_RCTM__and__Function_table_RCTM()

    ### dubugging start
    fn_in_go_basic = os.path.join(DOWNLOADS_DIR, "go-basic.obo")
    fn_out_Functions_table_GO = os.path.join(TABLES_DIR, "Functions_table_GO.txt")
    is_upk = False
    create_Functions_table_GO_or_UPK(fn_in_go_basic, fn_out_Functions_table_GO, is_upk)
    ### dubugging stop