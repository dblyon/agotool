import sys, re, os, subprocess, pickle, json
from scipy import sparse
import gzip
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from collections import defaultdict, deque
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
from ast import literal_eval
import tarfile
from statistics import median
import datetime

import taxonomy
import obo_parser
import tools, query
import variables

TEST_DIR = variables.TEST_DIR
TABLES_DIR = variables.TABLES_DIR

TYPEDEF_TAG, TERM_TAG = "[Typedef]", "[Term]"
BASH_LOCATION = r"/usr/bin/env bash"
PYTHON_DIR = variables.PYTHON_DIR
LOG_DIRECTORY = variables.LOG_DIRECTORY_SNAKEMAKE
DOWNLOADS_DIR = variables.DOWNLOADS_DIR_SNAKEMAKE
TABLES_DIR = variables.TABLES_DIR_SNAKEMAKE
NUMBER_OF_PROCESSES = variables.NUMBER_OF_PROCESSES
if NUMBER_OF_PROCESSES > 10:
    NUMBER_OF_PROCESSES_sorting = 6
else:
    NUMBER_OF_PROCESSES_sorting = NUMBER_OF_PROCESSES
VERSION_ = variables.VERSION_
PLATFORM = sys.platform

def Protein_2_Function_table_InterPro_STS(fn_in_string2interpro, fn_in_Functions_table_InterPro, fn_in_interpro_parent_2_child_tree, fn_out_Protein_2_Function_table_InterPro, number_of_processes=1, verbose=True):
    """
    :param fn_in_string2interpro: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/string2interpro.dat.gz)
    :param fn_out_Protein_2_Function_table_InterPro: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/Protein_2_Function_table_InterPro.txt)
    :param fn_in_interpro_parent_2_child_tree: String (download from interpro downloads page)
    :param fn_in_Functions_table_InterPro: String (/home/dblyon/agotool/data/PostgreSQL/tables/Functions_table_InterPro.txt) with InterPro ANs to verify
    :param number_of_processes: Integer (number of cores, shouldn't be too high since Disks are probably the bottleneck even with SSD, e.g. max 4)
    :param verbose: Bool (flag to print infos)
    :return: None
    """
    ### sort by fn_in first column (data is most probably already sorted, but we need to be certain for the parser that follows)
    ### unzip first, then sort to enable parallel sorting
    ### is the output is NOT zipped, but the
    ### e.g. of line "1298865.H978DRAFT_0001  A0A010P2C8      IPR011990       Tetratricopeptide-like helical domain superfamily       G3DSA:1.25.40.10        182     292"
    if verbose:
        print("\ncreate_Protein_2_Function_table_InterPro")
    fn_in_temp = fn_in_string2interpro + "_temp"
    tools.gunzip_file(fn_in_string2interpro, fn_in_temp)
    tools.sort_file(fn_in_temp, fn_in_temp, columns="1", number_of_processes=number_of_processes, verbose=verbose)
    child_2_parent_dict, _ = get_child_2_direct_parents_and_term_2_level_dict_interpro(fn_in_interpro_parent_2_child_tree)
    lineage_dict = get_lineage_from_child_2_direct_parent_dict(child_2_parent_dict)
    df = pd.read_csv(fn_in_Functions_table_InterPro, sep='\t', names=["etype", "AN", "description", "year", "level"])
    InterPro_AN_superset = set(df["AN"].values.tolist())
    if verbose:
        print("parsing previous result to produce Protein_2_Function_table_InterPro.txt")
    entityType_InterPro = variables.id_2_entityTypeNumber_dict["INTERPRO"]
    with open(fn_out_Protein_2_Function_table_InterPro, "w") as fh_out:
        for ENSP, InterProID_list in parse_string2interpro_yield_entry(fn_in_temp):
            # InterProID_list = sorted({id_ for id_ in InterProID_list if id_ in InterPro_AN_superset})
            # backtrack functions
            InterProID_set = set(InterProID_list)
            for id_ in InterProID_list:
                InterProID_set.update(lineage_dict[id_])
            InterProID_list = sorted(InterProID_set.intersection(InterPro_AN_superset))
            if len(InterProID_list) >= 1:
                fh_out.write(ENSP + "\t" + format_list_of_string_2_postgres_array(InterProID_list) + "\t" + entityType_InterPro + "\n")
    os.remove(fn_in_temp)
    if verbose:
        print("done create_Protein_2_Function_table_InterPro\n")

def parse_string2interpro_yield_entry(fn_in):
    # "1298865.H978DRAFT_0001  A0A010P2C8      IPR011990       Tetratricopeptide-like helical domain superfamily       G3DSA:1.25.40.10        182     292"
    InterProID_list = []
    did_first = False
    for line in tools.yield_line_uncompressed_or_gz_file(fn_in):
        ENSP, UniProtAN, InterProID, *rest = line.split()
        if not did_first:
            ENSP_previous = ENSP
            did_first = True
        if ENSP == ENSP_previous:
            InterProID_list.append(InterProID)
        else:
            yield (ENSP_previous, InterProID_list)
            InterProID_list = [InterProID]
            ENSP_previous = ENSP
    yield (ENSP_previous, InterProID_list)

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
                    # term_string_array = "{" + str(sorted(set(term_list)))[1:-1].replace("'", '"') + "}"
                    term_string_array = format_list_of_string_2_postgres_array(sorted(set(term_list)))
                    fh_out.write(ENSP_last + "\t" + term_string_array + "\t" + entity_type + "\n")
                    term_list = [term] + list(get_parents_iterative(term, child_2_parent_dict))
                    if return_all_terms:
                        all_terms = all_terms.union(set(term_list))
                ENSP_last = ENSP
            # term_string_array = "{" + str(sorted(set(term_list)))[1:-1].replace("'", '"') + "}"
            term_string_array = format_list_of_string_2_postgres_array(sorted(set(term_list)))
            fh_out.write(ENSP_last + "\t" + term_string_array + "\t" + entity_type + "\n")
            term_list = [term] + list(get_parents_iterative(term, child_2_parent_dict))
            if return_all_terms:
                all_terms = all_terms.union(set(term_list))
                return all_terms

def Functions_table_Reactome_combispeed(fn_in_desciptions, fn_out_Functions_table_RCTM, term_2_level_dict, all_terms):
    """
    :param fn_in_desciptions: String (RCTM_descriptions.tsv)
    :param fn_out_Functions_table_RCTM: String (Function_table_RCTM.txt)
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
    with open(fn_in_desciptions, "r") as fh_in:
        with open(fn_out_Functions_table_RCTM, "w") as fh_out:
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

def Functions_table_RCTM(fn_in_descriptions, fn_in_hierarchy, fn_out_Functions_table_RCTM, all_terms=None):
    """
    entity_type = "-57"
    :param fn_in_descriptions: String (RCTM_descriptions.tsv)
    :param fn_in_hierarchy: String
    :param fn_out_Functions_table_RCTM: String (Function_table_RCTM.txt)
    :param all_terms: Set of String (with all RCTM terms that have any association with the given ENSPs)
    :return: Tuple (List of terms with hierarchy, Set of terms without hierarchy)
    do a sanity check: are terms without a hierarchy used in protein_2_function
    create file Functions_table_Reactome.txt
    etype, term, name, definition, description # old
    | enum | etype | an | description | year | level | # new
    """
    child_2_parent_dict = get_child_2_direct_parent_dict_RCTM(fn_in_hierarchy)  # child_2_parent_dict --> child 2 direct parents
    term_2_level_dict = get_term_2_level_dict(child_2_parent_dict)
    entity_type = variables.id_2_entityTypeNumber_dict["Reactome"]
    year = "-1"
    terms_with_hierarchy, terms_without_hierarchy = [], []
    with open(fn_in_descriptions, "r") as fh_in:
        with open(fn_out_Functions_table_RCTM, "w") as fh_out:
            for line in fh_in:
                term, description, taxname = line.split("\t")
                if term.startswith("R-"):  # R-ATH-109581 --> ATH-109581
                    term = term[2:]
                description = description.strip()
                try:
                    level = term_2_level_dict[term]
                    terms_with_hierarchy.append(term)
                except KeyError:
                    terms_without_hierarchy.append(term)
                    level = "-1"
                if all_terms is None:
                    fh_out.write(entity_type + "\t" + term + "\t" + description + "\t" + year + "\t" + str(level) + "\n")
                else:
                    if term in all_terms:  # filter relevant terms that occur in protein_2_functions_tables_RCTM.txt
                        fh_out.write(entity_type + "\t" + term + "\t" + description + "\t" + year + "\t" + str(level) + "\n")
    return sorted(set(terms_with_hierarchy)), sorted(set(terms_without_hierarchy))

def get_direct_parents(child, child_2_parent_dict):
    try:
        # copy is necessary since child_2_parent_dict is otherwise modified by updating direct_parents in get_all_lineages
        # direct_parents = child_2_parent_dict[child].copy() # deprecated
        direct_parents = child_2_parent_dict[child]
    except KeyError:
        direct_parents = []
    return direct_parents

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

def get_term_2_level_dict(child_2_parent_dict):
    """
    calculate level of hierarchy for data
    if term in hierarchy --> default to level 1
    if term not in hierarchy --> not present in dict
    """
    # sys.setrecursionlimit(3500) # hopfully deprecated?
    term_2_level_dict = defaultdict(lambda: 1)
    for child in child_2_parent_dict.keys():
        lineages = get_all_lineages(child, child_2_parent_dict)
        try:
            level = len(max(lineages, key=len)) # if not in dict
        except ValueError: # if lineage [] but not [[]], which can happen for top root terms
            level = 1
        if level == 0: # for root terms
            level = 1
        term_2_level_dict[child] = level
    return term_2_level_dict

def get_child_2_direct_parent_dict_from_dag(dag):
    """
    e.g. {'GO:1901681': {'GO:0005488'},
    'GO:0090314': {'GO:0090313', 'GO:0090316', 'GO:1905477'}, ...}
    """
    child_2_direct_parents_dict = {}
    for name, term_object in dag.items():
        child_2_direct_parents_dict[name] = {p.id for p in term_object.parents}
    return child_2_direct_parents_dict

def get_all_lineages(child, child_2_parent_dict):
    """
    previous recursive version below
    def extend_parents(child_2_parent_dict, lineages=[]):
        for lineage in lineages:
            parents = list(get_direct_parents(lineage[-1], child_2_parent_dict))
            len_parents = len(parents)
            if len_parents == 1: # if single direct parents recursively walk up the tree
                lineage.extend(parents)
                return extend_parents(child_2_parent_dict, lineages)
            elif len_parents > 1: # multiple direct parents
                lineage_temp = lineage[:]
                lineage.extend([parents[0]]) # extend first parent
                for parent in parents[1:]: # copy lineage for the other parents and extend with respective parent
                    lineages.append(lineage_temp + [parent])
                return extend_parents(child_2_parent_dict, lineages)
        return lineages

    def get_all_lineages(child, child_2_parent_dict):
        lineages = []
        for parent in get_direct_parents(child, child_2_parent_dict):
            lineages += extend_parents(child_2_parent_dict, [[child, parent]])
        return lineages
    """
    lineage = [child]
    lineages = [lineage]
    visit_plan = deque()
    visit_plan.append((child, lineage))
    while visit_plan:
        (next_to_visit, lineage) = visit_plan.pop() # # lineage = # for this next_to_visit dude
        parents = list(get_direct_parents(next_to_visit, child_2_parent_dict))
        len_parents = len(parents)
        if len_parents == 1:  # if single direct parents recursively walk up the tree
            lineage.append(parents[0])
            visit_plan.append((parents[0], lineage))
        elif len_parents > 1:  # multiple direct parents
            # remove original/old lineage and replace with the forked
            lineages.remove(lineage)
            for parent in parents:  # copy lineage for the other parents and extend with respective parent
                lineage_fork = lineage[:]
                lineage_fork.append(parent)
                lineages.append(lineage_fork)
                visit_plan.append((parent, lineage_fork))
    return lineages

def Protein_2_Function_table_RCTM__and__Functions_table_RCTM(fn_associations, fn_descriptions, fn_hierarchy, fn_protein_2_function_table_RCTM, fn_functions_table_RCTM, number_of_processes):
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
    # sort on first two columns in order to get all functional associations for a given ENSP in one block
    tools.sort_file(fn_associations, fn_associations, number_of_processes=number_of_processes, verbose=variables.VERBOSE)
    child_2_parent_dict = get_child_2_direct_parent_dict_RCTM(fn_hierarchy)  # child_2_parent_dict --> child 2 direct parents
    term_2_level_dict = get_term_2_level_dict(child_2_parent_dict)
    all_terms = create_protein_2_function_table_Reactome(fn_in=fn_associations, fn_out=fn_protein_2_function_table_RCTM, child_2_parent_dict=child_2_parent_dict, return_all_terms=True)
    terms_with_hierarchy, terms_without_hierarchy = Functions_table_Reactome_combispeed(fn_in=fn_descriptions, fn_out=fn_functions_table_RCTM, term_2_level_dict=term_2_level_dict, all_terms=all_terms)
    if variables.VERBOSE:
        print("number of terms_without_hierarchy", len(terms_without_hierarchy))
        print("## done with RCTM tables")

def string_2_interpro(fn_in_string2uniprot, fn_in_uniprot2interpro, fn_out_string2interpro):
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

def Functions_table_InterPro(fn_in_interprot_AN_2_name, fn_in_interpro_parent_2_child_tree, fn_out_Functions_table_InterPro):
    """
    # | enum | etype | an | description | year | level |
    ### old file called InterPro_name_2_AN.txt
    # ftp://ftp.ebi.ac.uk/pub/databases/interpro/names.dat
    # df = pd.read_csv(fn_in, sep='\t', names=["an", "description"])
    # df["etype"] = variables.id_2_entityTypeNumber_dict["INTERPRO"]
    # df["year"] = "-1"
    # df["level"] = "-1"
    # df = df[["etype", "an", "description", "year", "level"]]
    # df.to_csv(fn_out, sep="\t", header=False, index=False)
    """
    child_2_parent_dict, term_2_level_dict = get_child_2_direct_parents_and_term_2_level_dict_interpro(fn_in_interpro_parent_2_child_tree)
    df = pd.read_csv(fn_in_interprot_AN_2_name, sep='\t')
    df = df.rename(columns={"ENTRY_AC": "an", "ENTRY_NAME": "description"})
    df["year"] = "-1"
    df["etype"] = variables.id_2_entityTypeNumber_dict["INTERPRO"]
    df["level"] = df["an"].apply(lambda term: term_2_level_dict[term])
    df = df[["etype", "an", "description", "year", "level"]]
    df.to_csv(fn_out_Functions_table_InterPro, sep="\t", header=False, index=False)

def get_child_2_direct_parents_and_term_2_level_dict_interpro(fn):
    """
    thus far no term has multiple parents, but code should capture these cases as well if they appear in the future

    IPR041492::Haloacid dehalogenase-like hydrolase:: # term_previous=IPR041492, level_previous=0
    --IPR006439::HAD hydrolase, subfamily IA:: # term=IPR006439, level=1 | term_previous=IPR006439, level_previous=1
    ----IPR006323::Phosphonoacetaldehyde hydrolase:: # term=IPR006323, level=2 | term_previous=IPR006323, level_previous=2
    ----IPR006328::L-2-Haloacid dehalogenase:: # term=IPR006328, level=2
    ----IPR006346::2-phosphoglycolate phosphatase-like, prokaryotic::
    ------IPR037512::Phosphoglycolate phosphatase, prokaryotic::
    ----IPR006351::3-amino-5-hydroxybenzoic acid synthesis-related::
    ----IPR010237::Pyrimidine 5-nucleotidase::
    ----IPR010972::Beta-phosphoglucomutase::
    ----IPR011949::HAD-superfamily hydrolase, subfamily IA, REG-2-like::
    ----IPR011950::HAD-superfamily hydrolase, subfamily IA, CTE7::
    ----IPR011951::HAD-superfamily hydrolase, subfamily IA, YjjG/YfnB::
    ----IPR023733::Pyrophosphatase PpaX::
    ----IPR023943::Enolase-phosphatase E1::
    ------IPR027511::Enolase-phosphatase E1, eukaryotes::
    :param fn: string (interpro_parent_2_child_tree.txt)
    :return dict: key: string val: set of string
    """
    child_2_parent_dict = defaultdict(lambda: set())
    term_2_level_dict = defaultdict(lambda: 1)
    with open(fn, "r") as fh:
        for line in fh:
            if not line.startswith("-"):
                term_previous = line.split(":")[0]
                level_previous = 1
                term_2_level_dict[term_previous] = level_previous
            else:
                term = line.split(":")[0]
                index_ = term.rfind("-")
                level_string = term[:index_ + 1]
                term = term[index_ + 1:]
                level = int(len(level_string) / 2) + 1
                term_2_level_dict[term] = level
                if level > level_previous:
                    if term not in child_2_parent_dict:
                        child_2_parent_dict[term] = {term_previous}
                    else:
                        child_2_parent_dict[term].update({term_previous})
                elif level == level_previous:
                    if term not in child_2_parent_dict:
                        child_2_parent_dict[term] = child_2_parent_dict[term_previous]
                    else:
                        child_2_parent_dict[term].update({child_2_parent_dict[term_previous]})
                elif level < level_previous:
                    term_previous, level_previous = helper_get_previous_term_and_level(child_2_parent_dict, term_2_level_dict, term_previous, level)
                    if term not in child_2_parent_dict:
                        child_2_parent_dict[term] = {term_previous}
                    else:
                        child_2_parent_dict[term].update({term_previous})
                level_previous = level
                term_previous = term
    return child_2_parent_dict, term_2_level_dict

def helper_get_previous_term_and_level(child_2_parent_dict, term_2_level_dict, term_previous, level_current):
    while True:
        term_previous = next(iter(child_2_parent_dict[term_previous]))
        level_previous = term_2_level_dict[term_previous]
        if level_current > level_previous:
            return term_previous, level_previous

def Functions_table_KEGG(fn_in, fn_out, verbose=True):
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

def Functions_table_SMART(fn_in, fn_out_functions_table_SMART, max_len_description, fn_out_map_name_2_an_SMART):
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
    df1 = df[["etype", "an", "description", "year", "level"]]
    df1.to_csv(fn_out_functions_table_SMART, sep="\t", header=False, index=False)
    df2 = df[["name", "an"]]
    df2.to_csv(fn_out_map_name_2_an_SMART, sep="\t", header=False, index=False)

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

def Functions_table_PFAM(fn_in, fn_out_functions_table_PFAM, fn_out_map_name_2_an):
    # ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.clans.tsv.gz (from 24/02/2017 downloaded 20180808)
    # fn = r"/home/dblyon/agotool/data/PostgreSQL/downloads/Pfam-A.clans.tsv"
    # fn_out = r"/home/dblyon/agotool/data/PostgreSQL/tables/Functions_table_PFAM.txt"
    columns = ['an', 'clan_an', 'HOMSTRAD', 'name', 'description']
    df = pd.read_csv(fn_in, sep="\t", names=columns)
    df["etype"] = variables.id_2_entityTypeNumber_dict["PFAM"]
    df["year"] = "-1"
    df["level"] = "-1"
    df1 = df[["etype", "an", "description", "year", "level"]]
    df1.to_csv(fn_out_functions_table_PFAM, sep="\t", header=False, index=False)
    df2 = df[["name", "an"]]
    df2.to_csv(fn_out_map_name_2_an, sep="\t", header=False, index=False)

def Functions_table_GO_or_UPK(fn_in_go_basic, fn_out_functions, is_upk=False, GO_CC_textmining_additional_etype=False):
    """
    # fn_in_go_basic = os.path.join(DOWNLOADS_DIR, "go-basic.obo")
    # fn_out_funcs = os.path.join(TABLES_DIR, "Functions_table_GO.txt")
    # ### functions [Functions_table_STRING.txt]
    # | enum | etype | an | description | year | level |
    id_, name --> Functions_table.txt
    id_, is_a_list --> Child_2_Parent_table_GO.txt
    :param fn_in_go_basic: string
    :param fn_out_functions: string
    :param is_upk: Boolean (flag for UniProtKeywords vs Gene Ontology)
    :param GO_CC_textmining_additional_etype: Boolean (flag to substitute etype -22 with -20 to create a separate category for textmining results)
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

            # only use GO-CC terms and convert etype to -20
            if GO_CC_textmining_additional_etype:
                if etype == "-22":
                    etype = "-20"
                else:
                    continue

            if str(etype) == "-24": # don't need obsolete GO terms
                continue

            try:
                level = str(term_2_level_dict[an])
            except KeyError:
                level = "-1"
            line2write_func = etype + "\t" + an + "\t" + description + "\t" + year + "\t" + level + "\n"
            fh_funcs.write(line2write_func)

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

def clean_messy_string_v2(string_):
    string_ = string_.strip().replace('"', "'")
    tags_2_remove = re.compile("|".join([r"<[^>]+>", r"\[Purpose\]", r"\\", "\/"]))
    string_ = tags_2_remove.sub('', string_)
    if string_.startswith("[") and string_.endswith("]"):
        return clean_messy_string_v2(string_[1:-1])
    elif string_.startswith("[") and string_.endswith("]."):
        return clean_messy_string_v2(string_[1:-2])
    elif string_.isupper():
        return string_[0] + string_[1:].lower()
    else:
        return string_

def concatenate_Functions_tables(fn_list_str, fn_out, number_of_processes): # fn_out_temp
    # fn_list = [os.path.join(TABLES_DIR, fn) for fn in ["Functions_table_GO.txt", "Functions_table_UPK.txt", "Functions_table_KEGG.txt",
    # "Functions_table_SMART.txt", "Functions_table_PFAM.txt", "Functions_table_InterPro.txt", "Functions_table_RCTM.txt"]]
    fn_list = [fn for fn in fn_list_str]
    # concatenate files
    tools.concatenate_files(fn_list, fn_out)
    # sort
    tools.sort_file(fn_out, fn_out, number_of_processes=number_of_processes)
    # don't add functional enumeration column yet, reduce table first
    print("finished creating {}".format(fn_out))

def format_list_of_string_2_postgres_array(list_of_string):
    """
    {{"GO:0005783",0.214286},{"GO:0005794",0.642857},{"GO...
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

def Protein_2_FunctionEnum_table_STS(fn_Functions_table_STRING, fn_in_Protein_2_function_table, fn_out_Protein_2_functionEnum_table_FIN, number_of_processes=1):
    function_2_enum_dict, enum_2_function_dict = get_function_an_2_enum__and__enum_2_function_an_dict_from_flat_file(fn_Functions_table_STRING)
    tools.sort_file(fn_in_Protein_2_function_table, fn_in_Protein_2_function_table, number_of_processes=number_of_processes)
    with open(fn_in_Protein_2_function_table, "r") as fh_in:
        with open(fn_out_Protein_2_functionEnum_table_FIN, "w") as fh_out:
            ENSP_last, function_arr_str, etype = fh_in.readline().split("\t")
            function_list = function_arr_str[1:-1].replace('"', "").split(",")
            functionEnum_list = _helper_format_array(function_list, function_2_enum_dict)
            for line in fh_in:
                ENSP, function_arr_str, etype = line.split("\t")
                function_list = function_arr_str[1:-1].replace('"', "").split(",")
                if ENSP == ENSP_last:
                    functionEnum_list += _helper_format_array(function_list, function_2_enum_dict)
                else:
                    if len(functionEnum_list) > 0:
                        fh_out.write(ENSP_last + "\t" + format_list_of_string_2_postgres_array(sorted(functionEnum_list)) + "\n")  # etype is removed
                    functionEnum_list = _helper_format_array(function_list, function_2_enum_dict)
                ENSP_last = ENSP
                fh_out.write(ENSP_last + "\t" + format_list_of_string_2_postgres_array(sorted(functionEnum_list)) + "\n")  # etype is removed

def Protein_2_FunctionEnum_table_UPS_FIN(fn_Functions_table_STRING, fn_in_Protein_2_Function_table, fn_out_Protein_2_functionEnum_table_FIN, fn_out_Protein_2_FunctionEnum_table_UPS_removed, number_of_processes=1):
    """
    go from multiple lines per protein (one row per etype) to single line of functionEnumeration
    input
    4932    HIS4_YEAST      {"PMID:8375386","PMID:7050665","PMID:25367168","PMID:24998777","PMID:24150815",...}  -56
    4932    HIS4_YEAST      {"WP416","WP514"}       -58
    4932    HIS4_YEAST      {"WP416","WP514"}       -58
    559292  HIS4_YEAST      {"GO:0005575","GO:0005622","GO:0005623","GO:0005634","GO:0005737","GO:0043226","GO:0043227","GO:0043229","GO:0043231","GO:0044424","GO:0044464"}       -22
    559292  HIS4_YEAST      {"IPR006062","IPR011060","IPR011858","IPR013785"}       -54

    output
    4932    HIS4_YEAST      {2662541,2662541,2662753,2662753}
    559292  HIS4_YEAST      {3971,3980,5332,5616,5642,5663,5671,5681,5794,5846,6457,6458,...}
    """
    # # merge multiline
    # ncbi = taxonomy.NCBI_taxonomy(taxdump_directory=DOWNLOADS_DIR, for_SQL=False, update=True)
    # with open(fn_in_Protein_2_Function_table, "r") as fh_in:
    #     with open(fn_out_Protein_2_Function_table_taxids_merged, "w") as fh_out:
    #         taxid_last, UniProtID_last, function_arr_str, etype = fh_in.readline().split("\t")
    function_2_enum_dict, enum_2_function_dict = get_function_an_2_enum__and__enum_2_function_an_dict_from_flat_file(fn_Functions_table_STRING)
    ### tools.sort_file(fn_in_Protein_2_Function_table, fn_in_Protein_2_Function_table, number_of_processes=number_of_processes) # already sorted at creation
    print("creating Protein_2_functionEnum_table_FIN")
    with open(fn_in_Protein_2_Function_table, "r") as fh_in:
        with open(fn_out_Protein_2_functionEnum_table_FIN, "w") as fh_out:
            with open(fn_out_Protein_2_FunctionEnum_table_UPS_removed, "w") as fh_out_removed:
                taxid_last, UniProtID_last, function_arr_str, etype = fh_in.readline().split("\t")
                functionEnum_list = _helper_format_array(function_arr_str[1:-1].replace('"', "").split(","), function_2_enum_dict)
                # for index_, line in enumerate(fh_in):
                for line in fh_in:
                    taxid, UniProtID, function_arr_str, etype = line.split("\t")
                    function_list = function_arr_str[1:-1].replace('"', "").split(",")
                    if UniProtID == UniProtID_last:
                        functionEnum_list += _helper_format_array(function_list, function_2_enum_dict)
                    else:
                        if len(functionEnum_list) > 0:
                            # remove duplicates
                            functionEnum_list = list(set(functionEnum_list))
                            fh_out.write(taxid_last + "\t" + UniProtID_last + "\t" + format_list_of_string_2_postgres_array(sorted(functionEnum_list)) + "\n")
                        else:
                            functionEnum_list = list(set(functionEnum_list))
                            fh_out_removed.write(taxid_last + "\t" + UniProtID_last + "\t" + format_list_of_string_2_postgres_array(sorted(functionEnum_list)) + "\n")
                        functionEnum_list = _helper_format_array(function_list, function_2_enum_dict)
                    UniProtID_last = UniProtID
                    taxid_last = taxid
                # remove duplicates
                # functionEnum_list = list(set(functionEnum_list))
                # fh_out.write(taxid_last + "\t" + UniProtID_last + "\t" + format_list_of_string_2_postgres_array(sorted(functionEnum_list)) + "\n")
                if len(functionEnum_list) > 0:
                    # remove duplicates
                    functionEnum_list = list(set(functionEnum_list))
                    fh_out.write(taxid_last + "\t" + UniProtID_last + "\t" + format_list_of_string_2_postgres_array(sorted(functionEnum_list)) + "\n")
                else:
                    functionEnum_list = list(set(functionEnum_list))
                    fh_out_removed.write(taxid_last + "\t" + UniProtID_last + "\t" + format_list_of_string_2_postgres_array(sorted(functionEnum_list)) + "\n")

def _helper_format_array(function_arr, function_2_enum_dict):
    functionEnum_list = []
    for ele in function_arr:
        try:
            functionEnum_list.append(function_2_enum_dict[ele])
        except KeyError: # e.g. blacklisted terms, terms removed due to single occurrence per genome
            pass
    return [int(ele) for ele in functionEnum_list]

def Lineage_table_FIN(fn_in_GO_obo_Jensenlab, fn_in_GO_obo, fn_in_keywords, fn_in_rctm_hierarchy, fn_in_interpro_parent_2_child_tree, fn_in_functions, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab, fn_out_lineage_table, fn_out_lineage_table_no_translation, fn_out_lineage_table_hr, GO_CC_textmining_additional_etype=False):
    lineage_dict = get_lineage_dict_for_all_entity_types_with_ontologies("allParents", fn_in_GO_obo_Jensenlab, fn_in_keywords, fn_in_rctm_hierarchy, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab, fn_in_interpro_parent_2_child_tree, GO_CC_textmining_additional_etype)
    # Jensenlab obo first, up-to-date GO_obo after to overwrite/update entries
    go_dag = obo_parser.GODag(obo_file=fn_in_GO_obo)
    for go_term_name in go_dag:
        GOTerm_instance = go_dag[go_term_name]
        lineage_dict[go_term_name] = GOTerm_instance.get_all_parents()

    # year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr = get_lookup_arrays(fn_in_functions, low_memory=True)
    year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr = query.get_lookup_arrays(read_from_flat_files=True)
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

    with open(fn_out_lineage_table_no_translation, "w") as fh_out_no_trans:
        for term in term_no_translation_because_obsolete:
            fh_out_no_trans.write(term + "\n")

    with open(fn_out_lineage_table_hr, "w") as fh_out_hr:
        for key, value in lineage_dict.items():
            fh_out_hr.write(str(key) + "\t" + "{" + str(sorted(set(value)))[1:-1].replace("'", '"') + "}\n")

def get_lineage_dict_for_all_entity_types_with_ontologies(direct_or_allParents, *args, **kwags):
    """

    """
    if direct_or_allParents == "allParents":
        return get_lineage_dict_for_all_entity_types_with_ontologies_allParents(*args, **kwags)
    else:
        return get_lineage_dict_for_all_entity_types_with_ontologies_directParents(*args, **kwags)

def yield_direct_parents(terms, lineage_dict):
    """
    generator: to return all direct parents of given terms
    lineage_dict = cst.get_lineage_dict_for_all_entity_types_with_ontologies(direct_or_allParents="direct")
    terms = ["GO:0016572"]
    for parents in yield_direct_parents(terms, lineage_dict):
        print(parents)
    :param terms: list of string
    :param lineage_dict: child 2 direct parents dict
    :return: list of string
    """
    def get_direct_parents(terms, lineage_dict):
        parents = []
        for term in terms:
            try:
                parents += lineage_dict[term]
            except KeyError:
                pass
        parents = sorted(set(parents))
        return parents
    parents = get_direct_parents(terms, lineage_dict)
    while parents:
        yield parents
        parents = get_direct_parents(parents, lineage_dict)
    return None

def get_lineage_dict_for_all_entity_types_with_ontologies_directParents(GO_obo_Jensenlab=None, go_basic_obo=None, keywords_obo=None, RCTM_hierarchy=None, DOID_obo_Jensenlab=None, BTO_obo_Jensenlab=None, GO_CC_textmining_additional_etype=True):
    """
    """
    if GO_obo_Jensenlab is None:
        GO_obo_Jensenlab = os.path.join(DOWNLOADS_DIR, "go_Jensenlab.obo")
    if go_basic_obo is None:
        go_basic_obo = os.path.join(DOWNLOADS_DIR, "go-basic.obo")
    if DOID_obo_Jensenlab is None:
        DOID_obo_Jensenlab = os.path.join(DOWNLOADS_DIR, "doid_Jensenlab.obo")
    if BTO_obo_Jensenlab is None:
        BTO_obo_Jensenlab = os.path.join(DOWNLOADS_DIR, "bto_Jensenlab.obo")
    if keywords_obo is None:
        keywords_obo = os.path.join(DOWNLOADS_DIR, "keywords-all.obo")
    if RCTM_hierarchy is None:
        RCTM_hierarchy = os.path.join(DOWNLOADS_DIR, "RCTM_hierarchy.tsv")

    lineage_dict = {}
    go_dag_Jensenlab = obo_parser.GODag(obo_file=GO_obo_Jensenlab)
    # key=GO-term, val=set of GO-terms (parents)
    for go_term_name in go_dag_Jensenlab:
        GOTerm_instance = go_dag_Jensenlab[go_term_name]
        lineage_dict[go_term_name] = GOTerm_instance.get_direct_parents()
    if GO_CC_textmining_additional_etype:
        for go_term_name in go_dag_Jensenlab:
            etype = str(get_entity_type_from_GO_term(go_term_name, go_dag_Jensenlab))
            if etype == "-22": # GO-CC need be changed since unique names needed
                GOTerm_instance = go_dag_Jensenlab[go_term_name]
                lineage_dict[go_term_name.replace("GO:", "GOCC:")] = {ele.replace("GO:", "GOCC:") for ele in GOTerm_instance.get_all_parents()}

    go_dag_basic = obo_parser.GODag(obo_file=go_basic_obo)
    for term_name in go_dag_basic:
        Term_instance = go_dag_basic[term_name]
        lineage_dict[term_name] = Term_instance.get_direct_parents()
    upk_dag = obo_parser.GODag(obo_file=keywords_obo, upk=True)
    for term_name in upk_dag:
        Term_instance = upk_dag[term_name]
        lineage_dict[term_name] = Term_instance.get_direct_parents()
    bto_dag = obo_parser.GODag(obo_file=BTO_obo_Jensenlab)
    for term_name in bto_dag:
        Term_instance = bto_dag[term_name]
        lineage_dict[term_name ] = Term_instance.get_direct_parents()
    doid_dag = obo_parser.GODag(obo_file=DOID_obo_Jensenlab)
    for term_name in doid_dag:
        Term_instance = doid_dag[term_name]
        lineage_dict[term_name ] = Term_instance.get_direct_parents()

    child_2_parent_dict = get_child_2_direct_parent_dict_RCTM(RCTM_hierarchy)
    lineage_dict.update(child_2_parent_dict)

    return lineage_dict

def get_lineage_dict_for_all_entity_types_with_ontologies_allParents(fn_go_basic_obo, fn_keywords_obo, fn_rctm_hierarchy, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab, fn_in_interpro_parent_2_child_tree, GO_CC_textmining_additional_etype=False):
    lineage_dict = {}
    go_dag = obo_parser.GODag(obo_file=fn_go_basic_obo)
    upk_dag = obo_parser.GODag(obo_file=fn_keywords_obo, upk=True)
    # key=GO-term, val=set of GO-terms (parents)
    for go_term_name in go_dag:
        GOTerm_instance = go_dag[go_term_name]
        # lineage_dict[go_term_name] = GOTerm_instance.get_all_parents().union(GOTerm_instance.get_all_children()) # wrong for this use case
        lineage_dict[go_term_name] = GOTerm_instance.get_all_parents()
    if GO_CC_textmining_additional_etype:
        for go_term_name in go_dag:
            etype = str(get_entity_type_from_GO_term(go_term_name, go_dag))
            if etype == "-22": # GO-CC need be changed since unique names needed
                GOTerm_instance = go_dag[go_term_name]
                lineage_dict[go_term_name.replace("GO:", "GOCC:")] = {ele.replace("GO:", "GOCC:") for ele in GOTerm_instance.get_all_parents()}

    for term_name in upk_dag:
        Term_instance = upk_dag[term_name]
        lineage_dict[term_name] = Term_instance.get_all_parents()

    bto_dag = obo_parser.GODag(obo_file=fn_in_BTO_obo_Jensenlab)
    for term_name in bto_dag:
        Term_instance = bto_dag[term_name]
        lineage_dict[term_name ] = Term_instance.get_all_parents()
    doid_dag = obo_parser.GODag(obo_file=fn_in_DOID_obo_Jensenlab)
    for term_name in doid_dag:
        Term_instance = doid_dag[term_name]
        lineage_dict[term_name ] = Term_instance.get_all_parents()

    # lineage_dict.update(get_lineage_Reactome(fn_rctm_hierarchy))
    child_2_parent_dict = get_child_2_direct_parent_dict_RCTM(fn_rctm_hierarchy)
    lineage_dict.update(get_lineage_from_child_2_direct_parent_dict(child_2_parent_dict))

    child_2_parent_dict, term_2_level_dict = get_child_2_direct_parents_and_term_2_level_dict_interpro(fn_in_interpro_parent_2_child_tree)
    lineage_dict.update(get_lineage_from_child_2_direct_parent_dict(child_2_parent_dict))
    return lineage_dict

def get_lineage_dict_for_DOID_BTO_GO(fn_go_basic_obo, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab, GO_CC_textmining_additional_etype=False, direct_parents_only=False):
    lineage_dict = {}
    go_dag = obo_parser.GODag(obo_file=fn_go_basic_obo)
    ### key=GO-term, val=set of GO-terms (parents)
    for go_term_name in go_dag:
        GOTerm_instance = go_dag[go_term_name]
        if direct_parents_only:
            lineage_dict[go_term_name] = GOTerm_instance.get_direct_parents()
        else:
            lineage_dict[go_term_name] = GOTerm_instance.get_all_parents()
    if GO_CC_textmining_additional_etype:
        for go_term_name in go_dag:
            etype = str(get_entity_type_from_GO_term(go_term_name, go_dag))
            if etype == "-22": # GO-CC need be changed since unique names needed
                GOTerm_instance = go_dag[go_term_name]
                if direct_parents_only:
                    lineage_dict[go_term_name.replace("GO:", "GOCC:")] = {ele.replace("GO:", "GOCC:") for ele in GOTerm_instance.get_direct_parents()}
                else:
                    lineage_dict[go_term_name.replace("GO:", "GOCC:")] = {ele.replace("GO:", "GOCC:") for ele in GOTerm_instance.get_all_parents()}
    bto_dag = obo_parser.GODag(obo_file=fn_in_BTO_obo_Jensenlab)
    for term_name in bto_dag:
        Term_instance = bto_dag[term_name]
        if direct_parents_only:
            lineage_dict[term_name ] = Term_instance.get_direct_parents()
        else:
            lineage_dict[term_name ] = Term_instance.get_all_parents()
    doid_dag = obo_parser.GODag(obo_file=fn_in_DOID_obo_Jensenlab)
    for term_name in doid_dag:
        Term_instance = doid_dag[term_name]
        if direct_parents_only:
            lineage_dict[term_name ] = Term_instance.get_direct_parents()
        else:
            lineage_dict[term_name ] = Term_instance.get_all_parents()
    return lineage_dict

def get_alternative_2_current_ID_dict(fn_obo, upk=False):
    alternative_2_current_ID_dict = {}
    for rec in obo_parser.OBOReader(fn_obo, upk=upk):
        rec_id = rec.id
        for alternative in rec.alt_ids:
            alternative_2_current_ID_dict[alternative] = rec_id
    return alternative_2_current_ID_dict

def get_lineage_from_child_2_direct_parent_dict(child_2_direct_parent_dict):
    lineage_dict = defaultdict(lambda: set())
    for child in child_2_direct_parent_dict:
        parents = get_parents_iterative(child, child_2_direct_parent_dict)
        if child in lineage_dict:
            lineage_dict[child].union(parents)
        else:
            lineage_dict[child] = parents
    return lineage_dict

def get_child_2_direct_parent_dict_RCTM(fn_in):
    """
    child_2_parent_dict --> child 2 direct parents
    """
    child_2_parent_dict = {}
    with open(fn_in, "r") as fh_in:
        for line in fh_in:
            parent, child = line.split("\t")
            child = child.strip()
            if child.startswith("R-"):
                child = child[2:]
            if parent.startswith("R-"):
                parent = parent[2:]
            if child not in child_2_parent_dict:
                child_2_parent_dict[child] = {parent}
            else:
                child_2_parent_dict[child] |= {parent}
    return child_2_parent_dict

# def get_lookup_arrays(fn_in_functions, low_memory):
#     """
#     funcEnum_2_hierarchical_level
#     simple numpy array of hierarchical levels
#     if -1 in DB --> convert to np.nan since these are missing values
#     # - funcEnum_2_year
#     # - funcEnum_2_hierarchical_level
#     # - funcEnum_2_etype
#     # - funcEnum_2_description
#     # - funcEnum_2_term
#     :param fn_in_functions: String (file name for functions_table)
#     :param low_memory: Bool flag to return description_array
#     :return: immutable numpy array of int
#     """
#     result = yield_split_line_from_file(fn_in_functions, line_numbers=True)
#     shape_ = next(result)
#     year_arr = np.full(shape=shape_, fill_value=-1, dtype="int16")  # Integer (-32768 to 32767)
#     entitytype_arr = np.full(shape=shape_, fill_value=0, dtype="int8")
#     if not low_memory:
#         description_arr = np.empty(shape=shape_, dtype=object) # ""U261"))
#         # category_arr = np.empty(shape=shape_, dtype=np.dtype("U49"))  # description of functional category (e.g. "Gene Ontology biological process")
#         category_arr = np.empty(shape=shape_, dtype=object)  # description of functional category (e.g. "Gene Ontology biological process")
#     functionalterm_arr = np.empty(shape=shape_, dtype=object) #np.dtype("U13"))
#     hierlevel_arr = np.full(shape=shape_, fill_value=-1, dtype="int8")  # Byte (-128 to 127)
#     indices_arr = np.arange(shape_, dtype=np.dtype("uint32"))
#     indices_arr.flags.writeable = False
#
#     for res in result:
#         func_enum, etype, term, description, year, hierlevel = res
#         func_enum = int(func_enum)
#         etype = int(etype)
#         try:
#             year = int(year)
#         except ValueError: # e.g. "...."
#             year = -1
#         hierlevel = int(hierlevel)
#         entitytype_arr[func_enum] = etype
#         functionalterm_arr[func_enum] = term
#         year_arr[func_enum] = year
#         hierlevel_arr[func_enum] = hierlevel
#         if not low_memory:
#             description_arr[func_enum] = description
#             category_arr[func_enum] = variables.entityType_2_functionType_dict[etype]
#
#     year_arr.flags.writeable = False # make it immutable
#     hierlevel_arr.flags.writeable = False
#     entitytype_arr.flags.writeable = False
#     functionalterm_arr.flags.writeable = False
#     if not low_memory:
#         description_arr.flags.writeable = False
#         category_arr.flags.writeable = False
#         return year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr
#     else:
#         return year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr

def yield_split_line_from_file(fn_in, line_numbers=False, split_on="\t"):
    if line_numbers:
        num_lines = tools.line_numbers(fn_in)
        yield num_lines

    with open(fn_in, "r") as fh_in:
        for line in fh_in:
            line_split = line.split(split_on)
            line_split[-1] = line_split[-1].strip()
            yield line_split

def Taxid_2_Proteins_table_STS(fn_in_protein_shorthands, fn_out_Taxid_2_Proteins_table_STRING, number_of_processes=1, verbose=True):
    if verbose:
        print("Creating Taxid_2_Proteins_table_STRING.txt")
        print("protein_shorthands needs sorting, doing it now")
    tools.sort_file(fn_in_protein_shorthands, fn_in_protein_shorthands, columns="1", number_of_processes=number_of_processes, verbose=verbose)
    if verbose:
        print("parsing protein_shorthands")
    # now parse and transform into wide format
    with open(fn_in_protein_shorthands, "r") as fh_in:
        with open(fn_out_Taxid_2_Proteins_table_STRING, "w") as fh_out:
            ENSP_list = []
            did_first = False
            for line in fh_in:
                # 287.DR97_1012   6412
                # 287.DR97_1013   6413
                ENSP, *rest = line.strip().split()
                Taxid = ENSP[:ENSP.index(".")]
                if not did_first:
                    Taxid_previous = Taxid
                    did_first = True
                if Taxid == Taxid_previous:
                    ENSP_list.append(ENSP)
                else:
                    ENSPs_2_write = sorted(set(ENSP_list))
                    fh_out.write(Taxid_previous + "\t" + format_list_of_string_2_postgres_array(ENSPs_2_write) + "\t" + str(len(ENSPs_2_write)) + "\n")
                    ENSP_list = [ENSP]
                    Taxid_previous = Taxid
            ENSPs_2_write = sorted(set(ENSP_list))
            fh_out.write(Taxid_previous + "\t" + format_list_of_string_2_postgres_array(ENSPs_2_write) + "\t" + str(len(ENSPs_2_write)) + "\n")

def Taxid_2_Proteins_table_UPS(UniProt_reference_proteomes_dir, Taxid_2_Proteins_table_UniProt): #, Taxid_without_mapping_2_species_rank):
    """
    Taxid_2_Proteins_table_UniProt --> UniProt entry name (ID) not accession
    """
    # ncbi = taxonomy.NCBI_taxonomy(taxdump_directory=DOWNLOADS_DIR, for_SQL=False, update=True)
    # taxid_no_proper_translation = []
    with open(Taxid_2_Proteins_table_UniProt, "w") as fh_out:
        for fn in [fn for fn in os.listdir(UniProt_reference_proteomes_dir) if fn.endswith(".fasta.gz")]:
            taxid, fasta, gz = os.path.basename(fn).split("_")[-1].split(".")
            uniprot_ans = []
            for line in tools.yield_line_uncompressed_or_gz_file(os.path.join(UniProt_reference_proteomes_dir, fn)):
                if line.startswith(">"): # >tr|M0AEL4|M0AEL4_NATA1 Uncharacterized protein OS=Natrialba asiatica (strain ATCC 700177 / DSM 12278 / JCM 9576 / FERM P-10747 / NBRC 102637 / 172P1) OX=29540 GN=C481_20731 PE
                    uniprot_ans.append(line.split("|")[2].split()[0])
            num_ans = len(uniprot_ans)
            assert num_ans == len(set(uniprot_ans))
            # | 9606 | {"9606.ENSP00000000233","9606.ENSP00000000412","9606.ENSP00000001008","9606.ENSP00000001146", ...} | 19566 | -60 | --> add etype when merging with STRING ENSP space
            an_arr = format_list_of_string_2_postgres_array(sorted(set(uniprot_ans)))
            # try:
            #     taxid = int(taxid)
            # except ValueError:
            #     taxid_no_proper_translation.apend(taxid)
            # taxid_corrected = ncbi.get_genus_or_higher(taxid, "species")
            # if ncbi.get_rank(taxid_corrected) != "species":
            #     taxid_no_proper_translation.append(taxid_corrected)
            # if taxid == "559292":  # replace entry for Yeast reference proteome on taxonomic rank species (instead of strain level)
            #     fh_out.write("{}\t{}\t{}\n".format("4932", num_ans, an_arr))
            # elif taxid == "284812":
            #     fh_out.write("{}\t{}\t{}\n".format("4896", num_ans, an_arr))
            # else:
            fh_out.write("{}\t{}\t{}\n".format(taxid, num_ans, an_arr))

def Taxid_2_Proteins_table_FIN(fn_in_Taxid_2_Proteins_table_STRING, fn_in_Taxid_2_Proteins_table_UniProt, fn_out_Taxid_2_Proteins_table_FIN, number_of_processes, verbose=True):
    # concatenate STRING ENSPs and UniProt AC
    # add etype
    with open(fn_out_Taxid_2_Proteins_table_FIN, "w") as fh_out:
        with open(fn_in_Taxid_2_Proteins_table_STRING, "r") as fh_in1:
            etype = variables.searchspace_2_entityType_dict["STRING"]
            for line in fh_in1:
                fh_out.write(line.strip() + "\t{}\n".format(etype))
        with open(fn_in_Taxid_2_Proteins_table_UniProt, "r") as fh_in2:
            etype = variables.searchspace_2_entityType_dict["UniProt"]
            for line in fh_in2:
                fh_out.write(line.strip() + "\t{}\n".format(etype))
    tools.sort_file(fn_out_Taxid_2_Proteins_table_FIN, fn_out_Taxid_2_Proteins_table_FIN, number_of_processes=number_of_processes, verbose=verbose)

def Taxid_2_FunctionCountArray_table_FIN(Protein_2_FunctionEnum_table_STRING, Functions_table_STRING, Taxid_2_Proteins_table, fn_out_Taxid_2_FunctionCountArray_table_FIN, number_of_processes=1, verbose=True):
    # - sort Protein_2_FunctionEnum_table_STRING.txt
    # - create array of zeros of function_enumeration_length
    # - for line in Protein_2_FunctionEnum_table_STRING
    #     add counts to array until taxid_new != taxid_previous
    print("creating Taxid_2_FunctionCountArray_table_FIN")
    tools.sort_file(Protein_2_FunctionEnum_table_STRING, Protein_2_FunctionEnum_table_STRING, number_of_processes=number_of_processes, verbose=verbose)
    taxid_2_total_protein_count_dict = _helper_get_taxid_2_total_protein_count_dict(Taxid_2_Proteins_table)
    num_lines = tools.line_numbers(Functions_table_STRING)
    print("writing {}".format(fn_out_Taxid_2_FunctionCountArray_table_FIN))
    with open(fn_out_Taxid_2_FunctionCountArray_table_FIN, "w") as fh_out:
        with open(Protein_2_FunctionEnum_table_STRING, "r") as fh_in:
            funcEnum_count_background = np.zeros(shape=num_lines, dtype=np.dtype("uint32"))
            line = next(fh_in)
            fh_in.seek(0)
            taxid_previous, ENSP, funcEnum_set = helper_parse_line_Protein_2_FunctionEnum_table_STRING(line)

            for line in fh_in:
                taxid, ENSP, funcEnum_set = helper_parse_line_Protein_2_FunctionEnum_table_STRING(line)
                if taxid != taxid_previous:
                    index_backgroundCount_array_string = helper_format_funcEnum(funcEnum_count_background)
                    background_n = taxid_2_total_protein_count_dict[taxid_previous]
                    fh_out.write(taxid_previous + "\t" + background_n + "\t" + index_backgroundCount_array_string + "\n")
                    funcEnum_count_background = np.zeros(shape=num_lines, dtype=np.dtype(variables.dtype_functionEnumeration))

                funcEnum_count_background = helper_count_funcEnum(funcEnum_count_background, funcEnum_set)
                taxid_previous = taxid
            index_backgroundCount_array_string = helper_format_funcEnum(funcEnum_count_background)
            background_n = taxid_2_total_protein_count_dict[taxid]
            fh_out.write(taxid + "\t" + background_n + "\t" + index_backgroundCount_array_string + "\n")

# def Protein_2_FunctionEnum_table_for_Taxid_2_FunctionCountArray_table_UPS_FIN(Protein_2_FunctionEnum_table_UPS_FIN, Taxid_2_Proteins_table_UPS_FIN)
def Taxid_2_FunctionCountArray_table_UPS_old(Protein_2_FunctionEnum_table_UPS_FIN, Functions_table_UPS_FIN, Taxid_2_Proteins_table, fn_out_Taxid_2_FunctionCountArray_table_FIN, number_of_processes=1, verbose=True):
    """
    # - sort Protein_2_FunctionEnum_table_UPS_FIN.txt on Taxid and UniProtID
    # - create array of zeros of function_enumeration_length
    # - for line in Protein_2_FunctionEnum_table_UPS_FIN
    #     add counts to array until taxid_new != taxid_previous
    # only use Taxids that exist in Taxid_2_Proteins_table_UPS_FIN, since these are UniProt Reference Proteome proteins (no ref prot for other taxids)
    output format changed from
    1000565 3919    {{3936,9},{3945,1},{3949,7}, ... }
    to
    1000565 3919 {3936,3945,3949, ... } {9,1,7, ... }

    # version 2:
    grep UniProtIDs from Taxid_2_Proteins_table_UPS_FIN:

    what I need is:
    for every reference proteome
        grep UniProtIDs
            for UniProtID
                count function enumeration

    how to get that sort order?
    filter Protein_2_FunctionEnum_table_UPS_FIN and modify taxid
        UniProtID 2 Taxid dict from Taxid_2_Proteins_table_UPS_FIN

    """
    print("creating Taxid_2_FunctionCountArray_table_FIN")
    tools.sort_file(Protein_2_FunctionEnum_table_UPS_FIN, Protein_2_FunctionEnum_table_UPS_FIN, number_of_processes=number_of_processes, verbose=verbose)  # sort on Taxid and UniProtID
    taxid_2_total_protein_count_dict = _helper_get_taxid_2_total_protein_count_dict(Taxid_2_Proteins_table)
    taxid_whiteset = set(taxid_2_total_protein_count_dict.keys())
    num_lines = tools.line_numbers(Functions_table_UPS_FIN)
    print("writing {}".format(fn_out_Taxid_2_FunctionCountArray_table_FIN))
    with open(fn_out_Taxid_2_FunctionCountArray_table_FIN, "w") as fh_out:
        for entry in yield_funcEnumList_per_taxid(Protein_2_FunctionEnum_table_UPS_FIN, taxid_whiteset):
            taxid, UniProtID_list, funcEnumList_list = entry
            if taxid_2_total_protein_count_dict[taxid] != "-1":  # restrict to Reference Proteomes # with new file this breaks #!!! since
                # UniProt ref prots are partially strain level, and Protein_2_FunctionEnum_table_UPS_FIN are species level
                UniProtID_set = set(query.get_proteins_of_taxid(taxid, read_from_flat_files=variables.READ_FROM_FLAT_FILES))
                funcEnum_count_background = np.zeros(shape=num_lines, dtype=np.dtype("uint32"))
                for index_, UniProtID in enumerate(UniProtID_list):
                    if UniProtID in UniProtID_set:
                        funcEnum_list = funcEnumList_list[index_]
                        funcEnum_count_background = helper_count_funcEnum(funcEnum_count_background, funcEnum_list)
                background_n = taxid_2_total_protein_count_dict[taxid]
                # funcEnum_count_background: array of zeros, if non-zero then count of gene associations
                # --> create 2 array:
                # first funcEnum positions --> index_positions_arr
                # second funcCounts --> counts_arr
                index_positions_arr_counts_arr_str = helper_format_funcEnum_reformatted(funcEnum_count_background)
                fh_out.write(taxid + "\t" + background_n + "\t" + index_positions_arr_counts_arr_str + "\n")

def Taxid_2_FunctionCountArray_table_UPS(Protein_2_FunctionEnum_table_UPS_FIN, Functions_table_UPS_FIN, Taxid_2_Proteins_table_UPS_FIN, fn_out_Taxid_2_FunctionCountArray_table_UPS_FIN, Protein_2_FunctionEnum_table_UPS_FIN_for_Taxid_count, number_of_processes=1, verbose=True):
    """
    # - sort Protein_2_FunctionEnum_table_UPS_FIN.txt on Taxid and UniProtID
    # - create array of zeros of function_enumeration_length
    # - for line in Protein_2_FunctionEnum_table_UPS_FIN
    #     add counts to array until taxid_new != taxid_previous
    # only use Taxids that exist in Taxid_2_Proteins_table_UPS_FIN, since these are UniProt Reference Proteome proteins (no ref prot for other taxids)
    BUT try to map taxid to UniProtRefProtTaxid
    output format changed from
    1000565 3919    {{3936,9},{3945,1},{3949,7}, ... }
    to
    1000565 3919 {3936,3945,3949, ... } {9,1,7, ... }

    # version 2:
    grep UniProtIDs from Taxid_2_Proteins_table_UPS_FIN:

    what I need is:
    for every reference proteome
        grep UniProtIDs
            for UniProtID
                count function enumeration

    how to get that sort order?
    filter Protein_2_FunctionEnum_table_UPS_FIN and modify taxid (change it from species level to strain level, since mapping exists from Taxid_2_Proteins_table_UPS_FIN )
        UniProtID 2 Taxid dict from Taxid_2_Proteins_table_UPS_FIN

    """
    print("creating Taxid_2_FunctionCountArray_table_FIN")
    tools.sort_file(Protein_2_FunctionEnum_table_UPS_FIN, Protein_2_FunctionEnum_table_UPS_FIN, number_of_processes=number_of_processes, verbose=verbose)  # sort on Taxid and UniProtID
    taxid_2_total_protein_count_dict = _helper_get_taxid_2_total_protein_count_dict(Taxid_2_Proteins_table_UPS_FIN)
    taxid_whiteset = set(taxid_2_total_protein_count_dict.keys())
    num_lines = tools.line_numbers(Functions_table_UPS_FIN)

    # get the mapping from UniProtID 2 TaxID from UniProt reference proteomes, and the subset of UniProtIDs needed
    uniprotid_2_taxid_dict = {}
    with open(Taxid_2_Proteins_table_UPS_FIN, "r") as fh:
        for line in fh:
            taxid, background_count, prot_arr = line.split("\t")  # UniProt
            prot_arr = prot_arr.strip()[1:-1].replace("'", "").replace('"', "").split(",")
            for prot in prot_arr:
                uniprotid_2_taxid_dict[prot] = taxid # taxid that it should be in the end

    with open(Protein_2_FunctionEnum_table_UPS_FIN, "r") as fh_in:
        with open(Protein_2_FunctionEnum_table_UPS_FIN_for_Taxid_count, "w") as fh_out_for_taxid_count:
            for line in fh_in:
                taxid_not_2_use, UniProtID, funcEnum_set = line.split("\t")  # taxid on
                if UniProtID in uniprotid_2_taxid_dict:  # filter for UniProtIDs that are in Reference Proteomes
                    taxid = uniprotid_2_taxid_dict[UniProtID]
                    fh_out_for_taxid_count.write(taxid + "\t" + UniProtID + "\t" + funcEnum_set)

    # below is the previous code, above is filtering things and mapping to taxid of reference proteomes
    tools.sort_file(Protein_2_FunctionEnum_table_UPS_FIN_for_Taxid_count, Protein_2_FunctionEnum_table_UPS_FIN_for_Taxid_count, number_of_processes=number_of_processes, verbose=verbose)
    print("writing {}".format(fn_out_Taxid_2_FunctionCountArray_table_UPS_FIN))
    with open(fn_out_Taxid_2_FunctionCountArray_table_UPS_FIN, "w") as fh_out:
        for entry in yield_funcEnumList_per_taxid(Protein_2_FunctionEnum_table_UPS_FIN_for_Taxid_count, taxid_whiteset):
            taxid, UniProtID_list, funcEnumList_list = entry
            if taxid_2_total_protein_count_dict[taxid] != "-1":  # restrict to Reference Proteomes # with new file this breaks #!!! since
                # UniProt ref prots are partially strain level, and Protein_2_FunctionEnum_table_UPS_FIN are species level
                UniProtID_set = set(query.get_proteins_of_taxid(taxid, read_from_flat_files=variables.READ_FROM_FLAT_FILES))
                funcEnum_count_background = np.zeros(shape=num_lines, dtype=np.dtype("uint32"))
                for index_, UniProtID in enumerate(UniProtID_list):
                    if UniProtID in UniProtID_set:
                        funcEnum_list = funcEnumList_list[index_]
                        funcEnum_count_background = helper_count_funcEnum(funcEnum_count_background, funcEnum_list)
                background_n = taxid_2_total_protein_count_dict[taxid]
                # funcEnum_count_background: array of zeros, if non-zero then count of gene associations
                # --> create 2 array:
                # first funcEnum positions --> index_positions_arr
                # second funcCounts --> counts_arr
                index_positions_arr_counts_arr_str = helper_format_funcEnum_reformatted(funcEnum_count_background)
                fh_out.write(taxid + "\t" + background_n + "\t" + index_positions_arr_counts_arr_str + "\n")

def yield_funcEnumList_per_taxid(Protein_2_FunctionEnum_table_UPS_FIN, taxid_whiteset):
    with open(Protein_2_FunctionEnum_table_UPS_FIN, "r") as fh_in:
        UniProtID_list, funcEnum_list = [], []
        taxid_previous, UniProtID, funcEnum = helper_parse_line_Protein_2_FunctionEnum_table_UPS(fh_in.readline(), taxid_whiteset)
        UniProtID_list.append(UniProtID)
        funcEnum_list.append(funcEnum)
        for line in fh_in:
            taxid, UniProtID, funcEnum = helper_parse_line_Protein_2_FunctionEnum_table_UPS(line, taxid_whiteset)
            if taxid_previous != taxid:
                yield (taxid_previous, UniProtID_list, funcEnum_list)
                taxid_previous = taxid
                UniProtID_list, funcEnum_list = [], []
            UniProtID_list.append(UniProtID)
            funcEnum_list.append(funcEnum)
        yield (taxid, UniProtID_list, funcEnum_list)

def helper_parse_line_Protein_2_FunctionEnum_table_UPS(line, taxid_whiteset):
    taxid, UniProtID, funcEnum_set = line.split("\t")
    if taxid in taxid_whiteset:
        funcEnum_list = [int(num) for num in funcEnum_set.strip()[1:-1].split(",")]
        return taxid, UniProtID, funcEnum_list
    else:
        return taxid, "-1", []

def helper_merge_funcEnum_count_arrays(funcEnum_count_arr_last, funcEnum_count_arr):
    funcEnum_count_arr_last += funcEnum_count_arr
    funcEnum_count_arr_last = sorted(funcEnum_count_arr_last)
    # funcEnum_list = [ele[0] for ele in funcEnum_count_arr_last]
    # no duplicate function enumerations since the etypes being merged are different
    #assert len(set(funcEnum_list)) == len(funcEnum_list)
    return funcEnum_count_arr_last

def helper_parse_line_Protein_2_FunctionEnum_table_STRING(line):
    ENSP, funcEnum_set = line.split("\t")
    funcEnum_set = {int(num) for num in literal_eval(funcEnum_set.strip())} # replace literal_eval with your own parser
    taxid = ENSP.split(".")[0]
    return taxid, ENSP, funcEnum_set

def helper_count_funcEnum(funcEnum_count, funcEnum_set):
    for funcEnum in funcEnum_set:
        funcEnum_count[funcEnum] += 1
    return funcEnum_count

def helper_format_funcEnum(funcEnum_count_background):
    # background_n = str(np.count_nonzero(funcEnum_count_background)) # wrong count
    enumeration_arr = np.arange(0, funcEnum_count_background.shape[0])
    cond = funcEnum_count_background > 0
    funcEnum_count_background = funcEnum_count_background[cond]
    enumeration_arr = enumeration_arr[cond]
    string_2_write = ""
    for ele in zip(enumeration_arr, funcEnum_count_background):
        string_2_write += "{{{0},{1}}},".format(ele[0], int(round(ele[1])))
    return "{" + string_2_write[:-1] + "}" # index_backgroundCount_array_string

def helper_format_funcEnum_reformatted(funcEnum_count_background):
    """
    funcEnum_count_background: array of zeros, if non-zero then count of gene associations
    --> create 2 array:
    first funcEnum positions --> index_positions_arr
    second funcCounts --> counts_arr
    """
    enumeration_arr = np.arange(0, funcEnum_count_background.shape[0])
    cond = funcEnum_count_background > 0
    funcEnum_count_background = funcEnum_count_background[cond]
    enumeration_arr = enumeration_arr[cond]
    index_positions_list, counts_list = [], []
    for ele in zip(enumeration_arr, funcEnum_count_background):
        index_positions_list.append(ele[0])
        counts_list.append(int(round(ele[1])))
    return "{" + ",".join([str(ele) for ele in index_positions_list]) + "}\t" + "{" + ",".join([str(ele) for ele in counts_list]) + "}"

def Protein_2_Function_table_KEGG_STS(fn_in_kegg_benchmarking, fn_out_Protein_2_Function_table_KEGG, fn_out_KEGG_Taxid_2_acronym_table, number_of_processes=1):
    fn_out_temp = fn_out_Protein_2_Function_table_KEGG + "_temp"
    # create long format of ENSP 2 KEGG table
    taxid_2_acronym_dict = {}
    with open(fn_in_kegg_benchmarking, "r") as fh_in:
        with open(fn_out_temp, "w") as fh_out:
            for line in fh_in:
                # 292     bced03020       4       DM42_1447 DM42_1480 DM42_1481 DM42_836
                Taxid, KEGG, num_ENSPs, *ENSPs = line.split()
                if KEGG.startswith("CONN_"):
                    continue
                else: # e.g. bced00190 or rhi00290
                    match = re.search("\d", KEGG)
                    if match:
                        index_ = match.start()
                        acro = KEGG[:index_]
                        taxid_2_acronym_dict[Taxid] = acro
                    KEGG = KEGG[-5:]
                # add Taxid to complete the ENSP
                ENSPs = [Taxid + "." + ENSP for ENSP in ENSPs]
                for ENSP in ENSPs:
                    fh_out.write(ENSP + "\t" + "map" + KEGG + "\n")
    with open(fn_out_KEGG_Taxid_2_acronym_table, "w") as fh_acro:
        for taxid, acronym in taxid_2_acronym_dict.items():
            fh_acro.write(taxid + "\t" + acronym + "\n")

    # sort by first column and transform to wide format
    tools.sort_file(fn_out_temp, fn_out_temp, columns="1", number_of_processes=number_of_processes)

    # convert long to wide format and add entity type
    entityType_UniProtKeywords = variables.id_2_entityTypeNumber_dict["KEGG"]
    long_2_wide_format(fn_out_temp, fn_out_Protein_2_Function_table_KEGG, entityType_UniProtKeywords)

def long_2_wide_format(fn_in, fn_out, etype=None):
    function_list = []
    with open(fn_in, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            an_last, function_ = fh_in.readline().strip().split("\t")
            function_list.append(function_)
            for line in fh_in:
                an, function_ = line.strip().split("\t")
                if an == an_last:
                    function_list.append(function_)
                else:
                    if etype is None:
                        fh_out.write(an_last + "\t{" + ','.join('"' + item + '"' for item in sorted(set(function_list))) + "}\n")
                    else:
                        fh_out.write(an_last + "\t{" + ','.join('"' + item + '"' for item in sorted(set(function_list))) + "}\t" + etype + "\n")

                    function_list = []
                    an_last = an
                    function_list.append(function_)
            if etype is None:
                fh_out.write(an + "\t{" + ','.join('"' + item + '"' for item in sorted(set(function_list))) + "}\n")
            else:
                fh_out.write(an + "\t{" + ','.join('"' + item + '"' for item in sorted(set(function_list))) + "}\t" + etype + "\n")

def Protein_2_Function_table_SMART_and_PFAM_temp(fn_in_dom_prot_full, fn_out_SMART_temp, fn_out_PFAM_temp, number_of_processes=1, verbose=True):
    """
    :param fn_in_dom_prot_full: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/string11_dom_prot_full.sql)
    :param fn_out_SMART_temp: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/Protein_2_Function_table_SMART.txt)
    :param fn_out_PFAM_temp: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/Protein_2_Function_table_PFAM.txt)
    :param number_of_processes: Integer (number of cores, shouldn't be too high since Disks are probably the bottleneck even with SSD, e.g. max 8 !?)
    :param verbose: Bool (flag to print infos)
    :return: None
    """
    if verbose:
        print("\ncreate_Protein_2_Functions_table_SMART and PFAM")
    tools.sort_file(fn_in_dom_prot_full, fn_in_dom_prot_full, columns="2", number_of_processes=number_of_processes)
    if verbose:
        print("parsing previous result to produce create_Protein_2_Function_table_SMART.txt and Protein_2_Function_table_PFAM.txt")
    entityType_SMART = variables.id_2_entityTypeNumber_dict["SMART"]
    entityType_PFAM = variables.id_2_entityTypeNumber_dict["PFAM"]
    with open(fn_out_PFAM_temp, "w") as fh_out_PFAM:
        with open(fn_out_SMART_temp, "w") as fh_out_SMART:
            for ENSP, PFAM_list_SMART_list in parse_string11_dom_prot_full_yield_entry(fn_in_dom_prot_full):
                PFAM_list, SMART_list = PFAM_list_SMART_list
                if len(PFAM_list) >= 1:
                    fh_out_PFAM.write(ENSP + "\t" + "{" + str(PFAM_list)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_PFAM + "\n")
                if len(SMART_list) >= 1:
                    fh_out_SMART.write(ENSP + "\t" + "{" + str(SMART_list)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_SMART + "\n")
    if verbose:
        print("done create_Protein_2_Function_table_SMART\n")

def parse_string11_dom_prot_full_yield_entry(fn_in):
    domain_list = []
    did_first = False
    ENSP_previous = ""
    counter = 0
    with open(fn_in, "r") as fh_in:
        for line in fh_in:
            counter += 1
            domain, ENSP, *rest = line.split()
            if not did_first:
                ENSP_previous = ENSP
                did_first = True
            if ENSP == ENSP_previous:
                domain_list.append(domain)
            else:
                yield (ENSP_previous, sort_PFAM_and_SMART(domain_list))
                domain_list = [domain]
                ENSP_previous = ENSP
        yield (ENSP_previous, sort_PFAM_and_SMART(domain_list))

def sort_PFAM_and_SMART(list_of_domain_names):
    PFAM_list, SMART_list = [], []
    for domain in set(list_of_domain_names):
        if domain.startswith("Pfam:"):
            PFAM_list.append(domain.replace("Pfam:", ""))
        elif domain in {"TRANS", "COIL", "SIGNAL"}:
            continue
        else:
            SMART_list.append(domain)
    return sorted(PFAM_list), sorted(SMART_list)

# def map_Name_2_AN(fn_in, fn_out, fn_dict, fn_no_mapping):
#     """
#     SMART and PFAM Protein_2_Function_table(s) contain names from parsing the
#     orig source, convert names to accessions
#     :param fn_in: String (Protein_2_Function_table_temp_SMART.txt)
#     :param fn_out: String (Protein_2_Function_table_SMART.txt)
#     :param fn_dict: String (Functions_table_SMART.txt
#     :param fn_no_mapping: String (missing mapping)
#     :return: NONE
#     """
#     print("map_Name_2_AN for {}".format(fn_in))
#     df = pd.read_csv(fn_dict, sep="\t", names=["name", "an"]) # names=["etype", "name", "an", "definition"])
#     name_2_an_dict = pd.Series(df["an"].values, index=df["name"]).to_dict()
#     df["name_v2"] = df["name"].apply(lambda x: x.replace("-", "_").lower())
#     name_2_an_dict_v2 = pd.Series(df["an"].values, index=df["name_v2"]).to_dict()
#     name_2_an_dict.update(name_2_an_dict_v2)
#     name_no_mapping_list = []
#     with open(fn_in, "r") as fh_in:
#         with open(fn_out, "w") as fh_out:
#             for line in fh_in:
#                 ENSP, name_array, etype_newline = line.split("\t")
#                 name_set = literal_eval(name_array) # replace literal_eval with your own parser
#                 an_list = []
#                 for name in name_set:
#                     try:
#                         an_list.append(name_2_an_dict[name])
#                     except KeyError:
#                         # not in the lookup, therefore should be skipped since most likely obsolete in current version
#                         name_no_mapping_list.append(name)
#                 if an_list: # not empty
#                     fh_out.write(ENSP + "\t{" + str(sorted(an_list))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + etype_newline)
#     with open(fn_no_mapping, "w") as fh_no_mapping:
#         fh_no_mapping.write("\n".join(sorted(set(name_no_mapping_list))))

def Protein_2_Function_table_GO_STS(fn_in_obo_file, fn_in_knowledge, fn_out_Protein_2_Function_table_GO, number_of_processes=1, verbose=True):
    """
    secondary GOids are converted to primary GOids
    e.g. goterm: 'GO:0007610' has secondary id 'GO:0044708', thus if 'GO:0044708' is associated it will be mapped to 'GO:0007610'
    :param fn_in_obo_file: String (file name for obo file)
    :param fn_in_knowledge: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/knowledge.tsv.gz)
    :param fn_out_Protein_2_Function_table_GO: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/Protein_2_Function_table_GO.txt)
    :param number_of_processes: Integer (number of cores, shouldn't be too high since Disks are probably the bottleneck even with SSD, e.g. max 4)
    :param verbose: Bool (flag to print infos)
    :return: None
    """
    ### e.g. of lines
    # 1001530 PMSV_1450       -21     GO:0000302      UniProtKB-EC    IEA     2       FALSE   http://www.uniprot.org/uniprot/SODF_PHOLE
    # 1000565 METUNv1_03599   -23     GO:0003824      UniProtKB-EC    IEA     2       FALSE   http://www.uniprot.org/uniprot/GMAS_METUF
    if verbose:
        print("\ncreate_Protein_2_Function_table_GO")
    GO_dag = obo_parser.GODag(obo_file=fn_in_obo_file, upk=False)
    fn_in_temp = fn_in_knowledge + "_temp"
    tools.gunzip_file(fn_in_knowledge, fn_in_temp)
    tools.sort_file(fn_in_temp, fn_in_temp, columns="1,2", number_of_processes=number_of_processes)
    if verbose:
        print("gunzip and sorting {}".format(fn_in_knowledge))
    GOterms_not_in_obo = []
    if verbose:
        print("parsing previous result to produce Protein_2_Function_table_GO.txt")
    with open(fn_out_Protein_2_Function_table_GO, "w") as fh_out:
        for ENSP, GOterm_list, _ in parse_string_go_yield_entry(fn_in_temp):
            GOterm_list, GOterms_not_in_obo_temp = get_all_parent_terms(GOterm_list, GO_dag)
            GOterms_not_in_obo += GOterms_not_in_obo_temp
            if len(GOterm_list) >= 1:
                # fh_out.write(ENSP + "\t" + "{" + str(GOterm_list)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType + "\n")
                MFs, CPs, BPs, not_in_OBO = divide_into_categories(GOterm_list, GO_dag, [], [], [], [])
                GOterms_not_in_obo_temp += not_in_OBO
                if MFs:
                    fh_out.write(ENSP + "\t" + "{" + str(MFs)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + variables.id_2_entityTypeNumber_dict['GO:0003674'] + "\n") # 'Molecular Function', -23
                if CPs:
                    fh_out.write(ENSP + "\t" + "{" + str(CPs)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + variables.id_2_entityTypeNumber_dict['GO:0005575'] + "\n") # 'Cellular Component', -22
                if BPs:
                    fh_out.write(ENSP + "\t" + "{" + str(BPs)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + variables.id_2_entityTypeNumber_dict['GO:0008150'] + "\n") # 'Biological Process', -21
    GOterms_not_in_obo = sorted(set(GOterms_not_in_obo))
    fn_log = os.path.join(LOG_DIRECTORY, "create_SQL_tables_GOterms_not_in_OBO.log")
    os.remove(fn_in_temp)
    with open(fn_log, "w") as fh_out:
        fh_out.write(";".join(GOterms_not_in_obo))
    if verbose:
        print("Number of GO terms not in OBO: ", len(GOterms_not_in_obo))
        print("done create_Protein_2_Function_table_GO\n")

def parse_string_go_yield_entry(fn_in):
    """
    careful the entity type will NOT (necessarily) be consistent as multiple annotations are given
    :param fn_in:
    :return:
    """
    # "9606    ENSP00000281154 -24     GO:0019861      UniProtKB       CURATED 5       TRUE    http://www.uniprot.org/uniprot/ADT4_HUMAN"
    GOterm_list = []
    did_first = False
    for line in tools.yield_line_uncompressed_or_gz_file(fn_in):
        Taxid, ENSP_without_Taxid, EntityType, GOterm, *rest = line.split()
        if not GOterm.startswith("GO:"):
            continue
        ENSP = Taxid + "." + ENSP_without_Taxid
        if not did_first:
            ENSP_previous = ENSP
            did_first = True
        if ENSP == ENSP_previous:
            GOterm_list.append(GOterm)
        else:
            yield (ENSP_previous, GOterm_list, EntityType)
            GOterm_list = [GOterm]
            ENSP_previous = ENSP
    yield (ENSP_previous, GOterm_list, EntityType)

def get_all_parent_terms(GOterm_list, GO_dag):
    """
    backtracking to root INCLUDING given children
    :param GOterm_list: List of String
    :param GO_dag: Dict like object
    :return: List of String
    """
    parents = []
    not_in_obo = []
    for GOterm in GOterm_list:
        try:
            parents += GO_dag[GOterm].get_all_parents()
        except KeyError: # remove GOterm from DB since not in OBO
            not_in_obo.append(GOterm)
    return sorted(set(parents).union(set(GOterm_list))), sorted(set(not_in_obo))

def divide_into_categories(GOterm_list, GO_dag, MFs=[], CPs=[], BPs=[], not_in_OBO=[]):
    """
    split a list of GO-terms into the 3 parent categories in the following order MFs, CPs, BPs
    'GO:0003674': "-23",  # 'Molecular Function',
    'GO:0005575': "-22",  # 'Cellular Component',
    'GO:0008150': "-21",  # 'Biological Process',
    29,687 Biological process
    11,110 Molecular Function
    4,206 Celular component
    :param GOterm_list: List of String
    :param GO_dag: Dict like object
    :return: Tuple (List of String x 3)
    """
    for term in GOterm_list:
        namespace = GO_dag[term].namespace
        if namespace == "biological_process":
            BPs.append(GO_dag[term].id)
        elif namespace == "molecular_function":
            MFs.append(GO_dag[term].id)
        elif namespace == "cellular_component":
            CPs.append(GO_dag[term].id)
        else:
            try:
                GO_id = GO_dag[term].id
            except KeyError:
                not_in_OBO.append(term)
                continue
            if GO_dag[GO_id].is_obsolete:
                not_in_OBO.append(term)
            else:
                MFs, CPs, BPs, not_in_OBO = divide_into_categories([GO_id], GO_dag, MFs, CPs, BPs, not_in_OBO)
    return sorted(MFs), sorted(CPs), sorted(BPs), sorted(not_in_OBO)

def Protein_2_Function_table_UPK_STS(fn_in_Functions_table_UPK, fn_in_obo, fn_in_uniprot_SwissProt_dat, fn_in_uniprot_TrEMBL_dat, fn_in_uniprot_2_string, fn_out_Protein_2_Function_table_UPK, number_of_processes=1,  verbose=True):
    if verbose:
        print("\ncreate_Protein_2_Function_table_UniProtKeywords")
    UPK_dag = obo_parser.GODag(obo_file=fn_in_obo, upk=True)
    UPK_Name_2_AN_dict = get_keyword_2_upkan_dict(fn_in_Functions_table_UPK)  # depends on create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK
    uniprot_2_string_missing_mapping = []
    uniprot_2_ENSPs_dict = parse_full_uniprot_2_string(fn_in_uniprot_2_string)
    entityType_UniProtKeywords = variables.id_2_entityTypeNumber_dict["UniProtKeywords"]
    UPKs_not_in_obo_list = []
    with open(fn_out_Protein_2_Function_table_UPK, "w") as fh_out:
        if verbose:
            print("parsing {}".format(fn_in_uniprot_SwissProt_dat))
        for UniProtAN_list, KeyWords_list in parse_uniprot_dat_dump_yield_entry(fn_in_uniprot_SwissProt_dat):
            for UniProtAN in UniProtAN_list:
                try:
                    ENSP_list = uniprot_2_ENSPs_dict[UniProtAN]
                except KeyError:
                    uniprot_2_string_missing_mapping.append(UniProtAN)
                    continue
                for ENSP in ENSP_list:
                    if len(KeyWords_list) >= 1:
                        UPK_ANs, UPKs_not_in_obo_temp = map_keyword_name_2_AN(UPK_Name_2_AN_dict, KeyWords_list)
                        UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                        UPK_ANs, UPKs_not_in_obo_temp = get_all_parent_terms(UPK_ANs, UPK_dag)
                        UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                    else:
                        continue
                    if len(UPK_ANs) >= 1:
                        fh_out.write(ENSP + "\t" + "{" + str(sorted(UPK_ANs))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_UniProtKeywords + "\n")

        if verbose:
            print("parsing {}".format(fn_in_uniprot_TrEMBL_dat))
        for UniProtAN_list, KeyWords_list in parse_uniprot_dat_dump_yield_entry(fn_in_uniprot_TrEMBL_dat):
            for UniProtAN in UniProtAN_list:
                try:
                    ENSP_list = uniprot_2_ENSPs_dict[UniProtAN]
                except KeyError:
                    uniprot_2_string_missing_mapping.append(UniProtAN)
                    continue
                for ENSP in ENSP_list:
                    if len(KeyWords_list) >= 1:
                        UPK_ANs, UPKs_not_in_obo_temp = map_keyword_name_2_AN(UPK_Name_2_AN_dict, KeyWords_list)
                        UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                        UPK_ANs, UPKs_not_in_obo_temp = get_all_parent_terms(UPK_ANs, UPK_dag)
                        UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                    else:
                        continue
                    if len(UPK_ANs) >= 1:
                        fh_out.write(ENSP + "\t" + "{" + str(sorted(UPK_ANs))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_UniProtKeywords + "\n")

    ### table Protein_2_Function_table_UniProtKeywords.txt needs sorting
    tools.sort_file(fn_out_Protein_2_Function_table_UPK, fn_out_Protein_2_Function_table_UPK, columns="1", number_of_processes=number_of_processes, verbose=verbose)

    UPKs_not_in_obo_list = sorted(set(UPKs_not_in_obo_list))
    fn_log = os.path.join(LOG_DIRECTORY, "create_SQL_tables_UniProtKeywords_not_in_OBO.log")
    with open(fn_log, "w") as fh_out:
        fh_out.write(";".join(UPKs_not_in_obo_list))

    if len(uniprot_2_string_missing_mapping) > 0:
        print("#!$%^@"*80)
        print("writing uniprot_2_string_missing_mapping to log file\n", os.path.join(LOG_DIRECTORY, "create_SQL_tables_STRING.log"))
        print("number of uniprot_2_string_missing_mapping", len(uniprot_2_string_missing_mapping))
        print("number of uniprot_2_ENSPs_dict keys", len(uniprot_2_ENSPs_dict.keys()))
        print("#!$%^@" * 80)
        with open(os.path.join(LOG_DIRECTORY, "create_SQL_tables_STRING.log"), "a+") as fh:
            fh.write(";".join(uniprot_2_string_missing_mapping))

    if verbose:
        print("Number of UniProt Keywords not in OBO: ", len(UPKs_not_in_obo_list))
        print("done create_Protein_2_Function_table_UniProtKeywords\n")

def Protein_2_Function_table_UniProtKeyword_UniProtSpace(fn_in_Functions_table_UPK, fn_in_obo, fn_in_uniprot_SwissProt_dat, fn_in_uniprot_TrEMBL_dat, fn_out_Protein_2_Function_table_UPK, number_of_processes=1,  verbose=True):
    if verbose:
        print("\ncreate_Protein_2_Function_table_UniProtKeywords")
    UPK_dag = obo_parser.GODag(obo_file=fn_in_obo, upk=True)
    UPK_Name_2_AN_dict = get_keyword_2_upkan_dict(fn_in_Functions_table_UPK)  # depends on create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK
    entityType_UniProtKeywords = variables.id_2_entityTypeNumber_dict["UniProtKeywords"]
    UPKs_not_in_obo_list = []
    with open(fn_out_Protein_2_Function_table_UPK, "w") as fh_out:
        if verbose:
            print("parsing {}".format(fn_in_uniprot_SwissProt_dat))
        for UniProtAN_list, KeyWords_list in parse_uniprot_dat_dump_yield_entry(fn_in_uniprot_SwissProt_dat):
            for UniProtAN in UniProtAN_list:
                if len(KeyWords_list) >= 1:
                    UPK_ANs, UPKs_not_in_obo_temp = map_keyword_name_2_AN(UPK_Name_2_AN_dict, KeyWords_list)
                    UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                    UPK_ANs, UPKs_not_in_obo_temp = get_all_parent_terms(UPK_ANs, UPK_dag)
                    UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                else:
                    continue
                if len(UPK_ANs) >= 1:
                    fh_out.write(UniProtAN + "\t" + "{" + str(sorted(UPK_ANs))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_UniProtKeywords + "\n")

        if verbose:
            print("parsing {}".format(fn_in_uniprot_TrEMBL_dat))
        for UniProtAN_list, KeyWords_list in parse_uniprot_dat_dump_yield_entry(fn_in_uniprot_TrEMBL_dat):
            for UniProtAN in UniProtAN_list:
                if len(KeyWords_list) >= 1:
                    UPK_ANs, UPKs_not_in_obo_temp = map_keyword_name_2_AN(UPK_Name_2_AN_dict, KeyWords_list)
                    UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                    UPK_ANs, UPKs_not_in_obo_temp = get_all_parent_terms(UPK_ANs, UPK_dag)
                    UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                else:
                    continue
                if len(UPK_ANs) >= 1:
                    fh_out.write(UniProtAN + "\t" + "{" + str(sorted(UPK_ANs))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_UniProtKeywords + "\n")

    ### table Protein_2_Function_table_UniProtKeywords.txt needs sorting
    tools.sort_file(fn_out_Protein_2_Function_table_UPK, fn_out_Protein_2_Function_table_UPK, columns="1", number_of_processes=number_of_processes, verbose=verbose)

    UPKs_not_in_obo_list = sorted(set(UPKs_not_in_obo_list))
    fn_log = os.path.join(LOG_DIRECTORY, "create_SQL_tables_UniProtKeywords_not_in_OBO.log")
    with open(fn_log, "w") as fh_out:
        fh_out.write(";".join(UPKs_not_in_obo_list))

        print("#!$%^@"*80)
        print("writing uniprot_2_string_missing_mapping to log file\n", os.path.join(LOG_DIRECTORY, "create_SQL_tables_STRING.log"))
        print("#!$%^@" * 80)

    if verbose:
        print("Number of UniProt Keywords not in OBO: ", len(UPKs_not_in_obo_list))
        print("done create_Protein_2_Function_table_UniProtKeywords\n")

def parse_full_uniprot_2_string(fn_in):
    """
    #species   uniprot_ac|uniprot_id   string_id   identity   bit_score
    742765  G1WQX1|G1WQX1_9FIRM     742765.HMPREF9457_01522 100.0   211.0
    742765  G1WQX2|G1WQX2_9FIRM     742765.HMPREF9457_01523 100.0   70.5
    """
    uniprot_2_ENSPs_dict = {}
    with open(fn_in, "r") as fh:
        next(fh) # skip header line
        for line in fh:
            taxid, uniprot_ac_and_uniprot_id, ENSP, *rest= line.strip().split()
            uniprot = uniprot_ac_and_uniprot_id.split("|")[0]
            if not uniprot in uniprot_2_ENSPs_dict :
                uniprot_2_ENSPs_dict[uniprot] = [ENSP]
            else: # it can be a one to many mapping (1 UniProtAN to multiple ENSPs)
                uniprot_2_ENSPs_dict[uniprot].append(ENSP)
    return uniprot_2_ENSPs_dict

def get_keyword_2_upkan_dict(Functions_table_UPK):
    """
    UniProt-keyword 2 UPK-AccessionNumber
    :return: Dict(String2String)
    """
    keyword_2_upkan_dict = {}
    with open(Functions_table_UPK, "r") as fh:
        for line in fh:
            line_split = line.strip().split("\t")
            keyword = line_split[2]
            upkan = line_split[1]
            keyword_2_upkan_dict[keyword] = upkan
    return keyword_2_upkan_dict

def parse_uniprot_dat_dump_yield_entry(fn_in):
    """
    yield parsed entry from UniProt DB dump file
    :param fn_in:
    :return:
    """
    for entry in yield_entry_UniProt_dat_dump(fn_in):
        UniProtAN_list, UniProtAN, Keywords_string = [], "", ""
        for line in entry:
            line_code = line[:2]
            rest = line[2:].strip()
            if line_code == "AC":
                UniProtAN_list += [UniProtAN.strip() for UniProtAN in rest.split(";") if len(UniProtAN) > 0]
            elif line_code == "KW":
                Keywords_string += rest
        UniProtAN_list = sorted(set(UniProtAN_list))
        Keywords_list = sorted(set(Keywords_string.split(";")))
        # remove empty strings from keywords_list
        Keywords_list = [cleanup_Keyword(keyword) for keyword in Keywords_list if len(keyword) > 0]
        yield (UniProtAN_list, Keywords_list)

def Protein_2_Function_table_UniProtDump_UPS(fn_in_Functions_table_UPK, fn_in_obo_GO, fn_in_obo_UPK, fn_in_list_uniprot_dumps, fn_in_interpro_parent_2_child_tree, fn_in_hierarchy_reactome, fn_out_Protein_2_Function_table_UniProt_dump, verbose=True): # fn_out_UniProt_AC_2_ID_2_Taxid,fn_out_UniProtID_2_ENSPs_2_KEGGs_mapping fn_out_UniProtID_2_ENSPs_2_KEGGs_mapping
    if verbose:
        print("\nparsing UniProt dumps: creating output file \n{}".format(fn_out_Protein_2_Function_table_UniProt_dump))
    etype_UniProtKeywords = variables.id_2_entityTypeNumber_dict["UniProtKeywords"]
    etype_GOMF = variables.id_2_entityTypeNumber_dict['GO:0003674']
    etype_GOCC = variables.id_2_entityTypeNumber_dict['GO:0005575']
    etype_GOBP = variables.id_2_entityTypeNumber_dict['GO:0008150']
    etype_interpro = variables.id_2_entityTypeNumber_dict['INTERPRO']
    etype_pfam = variables.id_2_entityTypeNumber_dict['PFAM']
    etype_reactome = variables.id_2_entityTypeNumber_dict['Reactome']
    GO_dag = obo_parser.GODag(obo_file=fn_in_obo_GO, upk=False)
    UPK_dag = obo_parser.GODag(obo_file=fn_in_obo_UPK, upk=True)
    UPK_Name_2_AN_dict = get_keyword_2_upkan_dict(fn_in_Functions_table_UPK)
    UPKs_not_in_obo_list, GOterms_not_in_obo_temp = [], []
    child_2_parent_dict_interpro, _ = get_child_2_direct_parents_and_term_2_level_dict_interpro(fn_in_interpro_parent_2_child_tree)
    lineage_dict_interpro = get_lineage_from_child_2_direct_parent_dict(child_2_parent_dict_interpro)
    child_2_parent_dict_reactome = get_child_2_direct_parent_dict_RCTM(fn_in_hierarchy_reactome)

    with open(fn_out_Protein_2_Function_table_UniProt_dump, "w") as fh_out:
        # with open(fn_out_UniProtID_2_ENSPs_2_KEGGs_mapping, "w") as fh_out_KEGG:
        #     with open(fn_out_UniProt_AC_2_ID_2_Taxid, "w") as fh_out_UniProt_AC_2_ID:
                for uniprot_dump_fn in fn_in_list_uniprot_dumps:
                    if verbose:
                        print("parsing {}".format(uniprot_dump_fn))
                    for UniProtID, UniProtAC_list, NCBI_Taxid, Keywords_list, GOterm_list, InterPro, Pfam, Reactome in parse_uniprot_dat_dump_yield_entry_v2(uniprot_dump_fn):
                        # ['Complete proteome', 'Reference proteome', 'Transcription', 'Activator', 'Transcription regulation', ['GO:0046782'], ['IPR007031'], ['PF04947'], ['vg:2947773'], [], [], ['UP000008770']]
                        # for UniProtAN in UniProtAC_and_ID_list:
                        if NCBI_Taxid in {"559292", "284812"}:
                            if NCBI_Taxid == "559292":
                                NCBI_Taxid = "4932"
                            elif NCBI_Taxid == "284812":
                                NCBI_Taxid = "4896"
                        if len(Keywords_list) > 0:
                            UPK_ANs, UPKs_not_in_obo_temp = map_keyword_name_2_AN(UPK_Name_2_AN_dict, Keywords_list)
                            UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                            UPK_ANs, UPKs_not_in_obo_temp = get_all_parent_terms(UPK_ANs, UPK_dag)
                            UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                            if len(UPK_ANs) > 0:
                                fh_out.write(NCBI_Taxid + "\t" + UniProtID + "\t" + format_list_of_string_2_postgres_array(sorted(UPK_ANs)) + "\t" + etype_UniProtKeywords + "\n")
                        if len(GOterm_list) > 0: # do backtracking, split GO into 3 categories and add etype
                            GOterm_list, not_in_obo_GO = get_all_parent_terms(GOterm_list, GO_dag)
                            GOterms_not_in_obo_temp += not_in_obo_GO
                            MFs, CPs, BPs, not_in_obo_GO = divide_into_categories(GOterm_list, GO_dag, [], [], [], [])
                            GOterms_not_in_obo_temp += not_in_obo_GO
                            if MFs:
                                fh_out.write(NCBI_Taxid + "\t" + UniProtID + "\t" + format_list_of_string_2_postgres_array(sorted(MFs)) + "\t" + etype_GOMF + "\n")  # 'Molecular Function', -23
                            if CPs:
                                fh_out.write(NCBI_Taxid + "\t" + UniProtID + "\t" + format_list_of_string_2_postgres_array(sorted(CPs)) + "\t" + etype_GOCC + "\n")  # 'Cellular Component', -22
                            if BPs:
                                fh_out.write(NCBI_Taxid + "\t" + UniProtID + "\t" + format_list_of_string_2_postgres_array(sorted(BPs)) + "\t" + etype_GOBP + "\n")  # 'Biological Process', -21
                        if len(InterPro) > 0:
                            InterPro_set = set(InterPro)
                            for id_ in InterPro:
                                InterPro_set.update(lineage_dict_interpro[id_])
                            fh_out.write(NCBI_Taxid + "\t" + UniProtID + "\t" + format_list_of_string_2_postgres_array(sorted(InterPro_set)) + "\t" + etype_interpro + "\n")
                        if len(Pfam) > 0:
                            fh_out.write(NCBI_Taxid + "\t" + UniProtID + "\t" + format_list_of_string_2_postgres_array(sorted(Pfam)) + "\t" + etype_pfam + "\n")
                        if len(Reactome) > 0:
                            reactome_list = Reactome.copy()
                            for term in reactome_list:
                                reactome_list += list(get_parents_iterative(term, child_2_parent_dict_reactome))
                            fh_out.write(NCBI_Taxid + "\t" + UniProtID + "\t" + format_list_of_string_2_postgres_array(sorted(set(reactome_list))) + "\t" + etype_reactome + "\n")

                        # translation needed from KEGG identifier to pathway, ID vs AC can be easily distinguished via "_"
                        # if len(KEGG) > 0:
                        #     fh_out_KEGG.write(NCBI_Taxid + "\t" + UniProtID + "\t" + ";".join(STRING) + "\t" + ";".join(sorted(set(KEGG))) + "\n")

                        # for AC in UniProtAC_list:
                        #     fh_out_UniProt_AC_2_ID.write("{}\t{}\t{}\n".format(NCBI_Taxid, AC, UniProtID))

def parse_uniprot_dat_dump_yield_entry_v2(fn_in):
    """
    UniProtKeywords
    GO
    InterPro
    Pfam
    KEGG
    Reactome
    @KEGG : I have a mapping from UniProt accession (e.g. "P31946") to KEGG entry (e.g. "hsa:7529")
        what I'm missing is from KEGG entry to KEGG pathway (e.g.
        hsa:7529    path:hsa04110
        hsa:7529    path:hsa04114
        hsa:7529    path:hsa04722)
    """
    for entry in yield_entry_UniProt_dat_dump(fn_in):
        UniProtAC_list, Keywords_string, functions_2_return = [], "", []
        Functions_other_list = []
        UniProtID, NCBI_Taxid = "-1", "-1"
        for line in entry:
            try:
                line_code, rest = line.split(maxsplit=1)
            except ValueError:
                continue

            if line_code == "ID":
                UniProtID = rest.split()[0]
            elif line_code == "AC":
                UniProtAC_list += [UniProtAN.strip() for UniProtAN in rest.split(";") if len(UniProtAN) > 0]
            elif line_code == "KW":
                Keywords_string += rest
            elif line_code == "DR":
                Functions_other_list.append(rest)
            elif line_code == "OX":
                # OX   NCBI_Taxid=654924;
                # OX   NCBI_Taxid=418404 {ECO:0000313|EMBL:QAB05112.1};
                if rest.startswith("NCBI_TaxID="):
                    NCBI_Taxid = rest.replace("NCBI_TaxID=", "").split(";")[0].split()[0]

        # UniProtAC_list = sorted(set(UniProtAC_list))Taxid_2_funcEnum_2_scores_table_FIN
        Keywords_list = [cleanup_Keyword(keyword) for keyword in sorted(set(Keywords_string.split(";"))) if len(keyword) > 0]  # remove empty strings from keywords_list
        # other_functions = helper_parse_UniProt_dump_other_functions(Functions_other_list)
        GOterm_list, InterPro, Pfam, Reactome = helper_parse_UniProt_dump_other_functions(Functions_other_list)
        # GO, InterPro, Pfam, KEGG, Reactome, STRING, Proteomes
        # functions_2_return.append(Keywords_list)
        # functions_2_return += other_functions # GO, InterPro, Pfam, Reactome
        # yield UniProtID, UniProtAC_list, NCBI_Taxid, functions_2_return
        yield UniProtID, UniProtAC_list, NCBI_Taxid, Keywords_list, GOterm_list, InterPro, Pfam, Reactome

def helper_parse_UniProt_dump_other_functions(list_of_string):
    """
    e.g. input
    [['EMBL; AY548484; AAT09660.1; -; Genomic_DNA.'],
     ['RefSeq; YP_031579.1; NC_005946.1.'],
     ['ProteinModelPortal; Q6GZX4; -.'],
     ['SwissPalm; Q6GZX4; -.'],
     ['GeneID; 2947773; -.'],
     ['KEGG; vg:2947773; -.'],
     ['Proteomes; UP000008770; Genome.'],
     ['GO; GO:0046782; P:regulation of viral transcription; IEA:InterPro.'],
     ['InterPro; IPR007031; Poxvirus_VLTF3.'],
     ['Pfam; PF04947; Pox_VLTF3; 1.']]
     EnsemblPlants; AT3G09880.1; AT3G09880.1; AT3G09880.
    """
    # GO, InterPro, Pfam, KEGG, Reactome, STRING, Proteomes = [], [], [], [], [], [], []
    GO, InterPro, Pfam, Reactome = [], [], [], []
    for row in list_of_string:
        row_split = row.split(";")
        func_type = row_split[0]
        try:
            annotation = row_split[1].strip()
        except IndexError:
            continue
        # if func_type == "KEGG":
        #     KEGG.append(annotation)
        if func_type == "GO":
            GO.append(annotation)
        elif func_type == "InterPro":
            InterPro.append(annotation)
        elif func_type == "Pfam":
            Pfam.append(annotation)
        elif func_type == "Reactome":        # DR   Reactome; R-DME-6799198; Complex I biogenesis.
            if annotation.startswith("R-"):  # R-DME-6799198 --> DME-6799198
                annotation = annotation[2:]
            Reactome.append(annotation)
        # elif func_type == "STRING":
        #     funcs_2_return = []
        #     try:
        #         for func in [func.strip() for func in row_split[1:]]:
        #             if func.endswith("."):
        #                 func = func[:-1]
        #             if func == "-":
        #                 continue
        #             funcs_2_return.append(func)
        #     except IndexError:
        #         continue
        #     STRING += funcs_2_return
        # elif func_type == "Proteomes":
        #     Proteomes.append(annotation)
    # return [GO, InterPro, Pfam, KEGG, Reactome, STRING, Proteomes]
    return GO, InterPro, Pfam, Reactome

def KEGG_Taxid_2_acronym_table_UPS(fn_in_KEGG_taxonomic_rank_file, fn_out_KEGG_Taxid_2_acronym_table_UP):
    """
    # Eukaryotes
    ## Animals
    ### Homo
    hsa	9606	9606	9605	9604	Homo sapiens (human)	Homo sapiens	Homo
    ### Pan
    ptr	9598	9598	9596	9604	Pan troglodytes (chimpanzee)	Pan troglodytes	Pan
    pps	9597	9597	9596	9604	Pan paniscus (bonobo)	Pan paniscus	Pan
    ### Gorilla
    """
    with open(fn_in_KEGG_taxonomic_rank_file, "r") as fh_in:
        with open(fn_out_KEGG_Taxid_2_acronym_table_UP, "w") as fh_out:
            for line in fh_in:
                if line.startswith("#"):
                    continue
                ls = line.split("\t")
                acronym = ls[0]
                taxid = ls[1]
                # taxname = ls[5]
                if acronym != taxid:
                    fh_out.write(taxid + "\t" + acronym + '\n')

def KEGG_Taxid_2_acronym_table_FIN(KEGG_Taxid_2_acronym_table_STRING, KEGG_Taxid_2_acronym_table_UP, KEGG_Taxid_2_acronym_table_FIN, KEGG_Taxid_2_acronym_ambiguous_table):
    taxid_2_acronym_dict = {}
    taxid_2_acronym_ambiguous_dict = {}
    for fn in [KEGG_Taxid_2_acronym_table_UP, KEGG_Taxid_2_acronym_table_STRING]:
        with open(fn, "r") as fh_in:
            for line in fh_in:
                acronym, taxid = line.split("\t")
                taxid = taxid.strip()
                if taxid not in taxid_2_acronym_dict:
                    taxid_2_acronym_dict[taxid] = acronym
                else:
                    acronym_first = taxid_2_acronym_dict[taxid]
                    if acronym != acronym_first:
                        # print("ambiguity in KEGG Taxid to acronym translation. {} {} {}".format(taxid, acronym_first, acronym))
                        if taxid not in taxid_2_acronym_ambiguous_dict:
                            taxid_2_acronym_ambiguous_dict[taxid] = [acronym_first, acronym]
                        else:
                            taxid_2_acronym_ambiguous_dict[taxid].append(acronym)
                    else:
                        continue
    with open(KEGG_Taxid_2_acronym_table_FIN, "w") as fh_out:
        for taxid, acronym in taxid_2_acronym_dict.items():
            fh_out.write(taxid + "\t" + acronym + "\n")

    with open(KEGG_Taxid_2_acronym_ambiguous_table, "w") as fh_out:
        for taxid, acronym_list in taxid_2_acronym_ambiguous_dict.items():
            fh_out.write(taxid + "\t" + ";".join(acronym_list) + "\n")

def get_KEGG_Protein_2_pathwayName_dict(fn_list):
    """
    from KEGG dump --> e.g. hsa.list
    parse KEGG pathway name 2 KEGG protein information
    rename path: to map
    combine this data with UniProt dump information (UniProtAC 2 KeggProtein)
    --> UniProtAC 2 KeggPathwayName
    """
    Protein_2_pathwayName_dict = {}
    for fn in fn_list:
        basename = os.path.basename(fn)
        acronym = basename.replace(".tar.gz", "")
        tar = tarfile.open(fn, "r:gz")
        fhan = tar.extractfile("{}/{}.list".format(acronym, acronym))
        for line in fhan.readlines():
            ls = line.decode("utf-8").strip().split("\t")
            pathwayName = "map" + ls[0][-5:]
            KeggProtein = ls[1]
            if KeggProtein not in Protein_2_pathwayName_dict:
                Protein_2_pathwayName_dict[KeggProtein] = [pathwayName]
            else:
                Protein_2_pathwayName_dict[KeggProtein].append(pathwayName)
    return Protein_2_pathwayName_dict

def Protein_2_Function_table_KEGG_UPS_and_ENSP_2_KEGG_benchmark(KEGG_dir, fn_in_Taxid_2_UniProtID_2_ENSPs_2_KEGGs, fn_out_Protein_2_Function_table_KEGG_UP, fn_out_Protein_2_Function_table_KEGG_UP_ENSP_benchmark, fn_out_KEGG_entry_no_pathway_annotation, verbose=True):
    """
    fn_out_Protein_2_Function_table_KEGG_UP_ENSP_benchmark: ENSP 2 KEGG benchmark coming from UniProt 2 KEGG and mapping STRING 2 UniProt
    """
    fn_list_KEGG_tar_gz = sorted([os.path.join(KEGG_dir, fn) for fn in os.listdir(KEGG_dir) if fn.endswith(".tar.gz")])
    if verbose:
        print("number of KEGG files to parse {}".format(len(fn_list_KEGG_tar_gz)))
    KEGG_Protein_2_pathwayNames_list_dict = get_KEGG_Protein_2_pathwayName_dict(fn_list_KEGG_tar_gz)
    etype = variables.id_2_entityTypeNumber_dict["KEGG"]
    no_pathway_annotation_KEGG_proteins = []
    with open(fn_out_Protein_2_Function_table_KEGG_UP, "w") as fh_out:
        with open(fn_out_Protein_2_Function_table_KEGG_UP_ENSP_benchmark, "w") as fh_out_ENSP:
            with open(fn_in_Taxid_2_UniProtID_2_ENSPs_2_KEGGs, "r") as fh_in:  # always a one to many mapping
                for line in fh_in:
                    # uniprot_an_or_id, STRING_ENSP, kegg_an = line.split("\t")  # single STRING ENSP
                    taxid, UniProtID, STRING_ENSP, kegg_an = line.split("\t")  # single STRING ENSP
                    kegg_protein_list = kegg_an.strip().split(";")
                    ENSP_list = STRING_ENSP.split(";")
                    pathwayNames_list = []
                    for kegg_protein_entry in kegg_protein_list:
                        try:
                            pathwayNames_list += KEGG_Protein_2_pathwayNames_list_dict[kegg_protein_entry]
                        except KeyError:
                            no_pathway_annotation_KEGG_proteins.append(kegg_protein_entry)
                    pathwayNames_set = set(pathwayNames_list)
                    if len(pathwayNames_set) > 0:
                        fh_out.write(taxid + "\t" + UniProtID + "\t" + format_list_of_string_2_postgres_array(sorted(pathwayNames_set)) + "\t" + etype + "\n")
                        for ENSP in ENSP_list:
                            fh_out_ENSP.write(ENSP + "\t" + format_list_of_string_2_postgres_array(sorted(pathwayNames_set)) + "\n")
    with open(fn_out_KEGG_entry_no_pathway_annotation, "w") as fh_out_KEGG_entry_no_pathway_annotation:
        for kegg_entry in no_pathway_annotation_KEGG_proteins:
            fh_out_KEGG_entry_no_pathway_annotation.write(kegg_entry + "\n")

def map_keyword_name_2_AN(UPK_Name_2_AN_dict, KeyWords_list):
    UPK_ANs, UPKs_not_in_obo_temp = [], []
    for keyword in KeyWords_list:
        try:
            AN = UPK_Name_2_AN_dict[keyword]
        except KeyError:
            UPKs_not_in_obo_temp.append(keyword)
            continue
        UPK_ANs.append(AN)
    return UPK_ANs, UPKs_not_in_obo_temp

def cleanup_Keyword(keyword):
    """
    remove stuff after '{'
    remove '.' at last keyword
    remove last ',' in string
    "ATP-binding{ECO:0000256|HAMAP-Rule:MF_00175,","Chaperone{ECO:0000256|HAMAP-Rule:MF_00175,","Completeproteome{ECO:0000313|Proteomes:UP000005019}","ECO:0000256|SAAS:SAAS00645729}","ECO:0000256|SAAS:SAAS00645733}","ECO:0000256|SAAS:SAAS00645738}.","ECO:0000256|SAAS:SAAS00701776}","ECO:0000256|SAAS:SAAS00701780,ECO:0000313|EMBL:EGK73413.1}","Hydrolase{ECO:0000313|EMBL:EGK73413.1}","Metal-binding{ECO:0000256|HAMAP-Rule:MF_00175,","Nucleotide-binding{ECO:0000256|HAMAP-Rule:MF_00175,","Protease{ECO:0000313|EMBL:EGK73413.1}","Referenceproteome{ECO:0000313|Proteomes:UP000005019}","Zinc{ECO:0000256|HAMAP-Rule:MF_00175,ECO:0000256|SAAS:SAAS00645735}","Zinc-finger{ECO:0000256|HAMAP-Rule:MF_00175,"
    :param keyword:
    :return:
    """
    try:
        index_ = keyword.index("{")
    except ValueError:
        index_ = False
    if index_:
        keyword = keyword[:index_]
    return keyword.replace(".", "").strip()

def yield_entry_UniProt_dat_dump(fn_in):
    """
    yield a single entry, delimited by '//' at the end
    of UniProt DB dump files
    fn_in = "uniprot_sprot.dat.gz"
    '//         Terminator                        Once; ends an entry'
    # ID   D5EJT0_CORAD            Unreviewed;       296 AA.
    # AC   D5EJT0;
    # DT   15-JUN-2010, integrated into UniProtKB/TrEMBL.
    # DT   15-JUN-2010, sequence version 1.
    # DT   25-OCT-2017, entry version 53.
    # DE   SubName: Full=Binding-protein-dependent transport systems inner membrane component {ECO:0000313|EMBL:ADE54679.1};
    # GN   OrderedLocusNames=Caka_1660 {ECO:0000313|EMBL:ADE54679.1};
    # OS   Coraliomargarita akajimensis (strain DSM 45221 / IAM 15411 / JCM 23193
    # OS   / KCTC 12865 / 04OKA010-24).
    # OC   Bacteria; Verrucomicrobia; Opitutae; Puniceicoccales;
    # OC   Puniceicoccaceae; Coraliomargarita.
    # OX   NCBI_Taxid=583355 {ECO:0000313|EMBL:ADE54679.1, ECO:0000313|Proteomes:UP000000925};
    # RN   [1] {ECO:0000313|EMBL:ADE54679.1, ECO:0000313|Proteomes:UP000000925}
    # RP   NUCLEOTIDE SEQUENCE [LARGE SCALE GENOMIC DNA].
    # RC   STRAIN=DSM 45221 / IAM 15411 / JCM 23193 / KCTC 12865
    # RC   {ECO:0000313|Proteomes:UP000000925};
    # RX   PubMed=21304713; DOI=10.4056/sigs.952166;
    # RA   Mavromatis K., Abt B., Brambilla E., Lapidus A., Copeland A.,
    # RA   Deshpande S., Nolan M., Lucas S., Tice H., Cheng J.F., Han C.,
    # RA   Detter J.C., Woyke T., Goodwin L., Pitluck S., Held B., Brettin T.,
    # RA   Tapia R., Ivanova N., Mikhailova N., Pati A., Liolios K., Chen A.,
    # RA   Palaniappan K., Land M., Hauser L., Chang Y.J., Jeffries C.D.,
    # RA   Rohde M., Goker M., Bristow J., Eisen J.A., Markowitz V.,
    # RA   Hugenholtz P., Klenk H.P., Kyrpides N.C.;
    # RT   "Complete genome sequence of Coraliomargarita akajimensis type strain
    # RT   (04OKA010-24).";
    # RL   Stand. Genomic Sci. 2:290-299(2010).
    # CC   -!- SUBCELLULAR LOCATION: Cell membrane
    # CC       {ECO:0000256|RuleBase:RU363032}; Multi-pass membrane protein
    # CC       {ECO:0000256|RuleBase:RU363032}.
    # CC   -!- SIMILARITY: Belongs to the binding-protein-dependent transport
    # CC       system permease family. {ECO:0000256|RuleBase:RU363032,
    # CC       ECO:0000256|SAAS:SAAS00723689}.
    # CC   -----------------------------------------------------------------------
    # CC   Copyrighted by the UniProt Consortium, see http://www.uniprot.org/terms
    # CC   Distributed under the Creative Commons Attribution-NoDerivs License
    # CC   -----------------------------------------------------------------------
    # DR   EMBL; CP001998; ADE54679.1; -; Genomic_DNA.
    # DR   RefSeq; WP_013043401.1; NC_014008.1.
    # DR   STRING; 583355.Caka_1660; -.
    # DR   EnsemblBacteria; ADE54679; ADE54679; Caka_1660.
    # DR   KEGG; caa:Caka_1660; -.
    # DR   eggNOG; ENOG4105C2T; Bacteria.
    # DR   eggNOG; COG1173; LUCA.
    # DR   HOGENOM; HOG000171367; -.
    # DR   KO; K15582; -.
    # DR   OMA; PTGIWWT; -.
    # DR   OrthoDB; POG091H0048; -.
    # DR   Proteomes; UP000000925; Chromosome.
    # DR   GO; GO:0016021; C:integral component of membrane; IEA:UniProtKB-KW.
    # DR   GO; GO:0005886; C:plasma membrane; IEA:UniProtKB-SubCell.
    # DR   GO; GO:0006810; P:transport; IEA:UniProtKB-KW.
    # DR   CDD; cd06261; TM_PBP2; 1.
    # DR   Gene3D; 1.10.3720.10; -; 1.
    # DR   InterPro; IPR000515; MetI-like.
    # DR   InterPro; IPR035906; MetI-like_sf.
    # DR   InterPro; IPR025966; OppC_N.
    # DR   Pfam; PF00528; BPD_transp_1; 1.
    # DR   Pfam; PF12911; OppC_N; 1.
    # DR   SUPFAM; SSF161098; SSF161098; 1.
    # DR   PROSITE; PS50928; ABC_TM1; 1.
    # PE   3: Inferred from homology;
    # KW   Cell membrane {ECO:0000256|SAAS:SAAS00894688};
    # KW   Complete proteome {ECO:0000313|Proteomes:UP000000925};
    # KW   Membrane {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00893669};
    # KW   Reference proteome {ECO:0000313|Proteomes:UP000000925};
    # KW   Transmembrane {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00894237};
    # KW   Transmembrane helix {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00894527};
    # KW   Transport {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00723738}.
    # FT   TRANSMEM     34     53       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM     94    119       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    131    150       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    156    175       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    214    239       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    259    282       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   DOMAIN       92    282       ABC transmembrane type-1.
    # FT                                {ECO:0000259|PROSITE:PS50928}.
    # SQ   SEQUENCE   296 AA;  32279 MW;  3DB3B060376AFDB5 CRC64;
    #      MIKQQREAKA VSVAATSLGQ DAWERLKRNN MARIGGTLFA IITALCIVGP WLLPHSYDAQ
    #      NLAYGAQGPS WQHLLGTDDL GRDLLVRILV GGRISIGVGF AASLVALIIG VSYGALAGYI
    #      GGRTESVMMR FVDAVYALPF TMIVIILTVT FDEKSIFLIF MAIGLVEWLT MARIVRGQTK
    #      ALRQLNYIDA ARTMGASHLS ILTRHILPNL LGPVIVFTTL TIPAVILLES ILSFLGLGVQ
    #      PPMSSWGILI NEGADKIDIY PWLLIFPALF FSLTIFALNF IGDGLRDALD PKESQH
    # //
    """
    lines_list = []
    for line in tools.yield_line_uncompressed_or_gz_file(fn_in):
        line = line.strip()
        if not line.startswith("//"):
            lines_list.append(line)
        else:
            yield lines_list
            lines_list = []
    if lines_list:
        if len(lines_list[0]) == 0:
            # return None #
            yield StopIteration
    else:
        yield lines_list

def parse_textmining_entityID_2_proteinID(fn):
    df = pd.read_csv(fn, sep="\t", names=["textmining_id", "species_id", "protein_id"])# textmining_id = entity_id
    df["ENSP"] = df["species_id"].astype(str) + "." + df["protein_id"].astype(str)
    return df

def parse_textmining_string_matches(fn):
    """
    # textmining_id = entity_id
    """
    names=['PMID', 'sentence', 'paragraph', 'location_start', 'location_end', 'matched_string', 'species', 'entity_id']
    df = pd.read_csv(fn, sep="\t", names=names)
    return df

def get_all_ENSPs(Taxid_2_Proteins_table_STRING):
    ENSP_set = set()
    with open(Taxid_2_Proteins_table_STRING, "r") as fh:
        for line in fh:
            ENSP_set |= literal_eval(line.split("\t")[1]) # ToDo replace with own version
    return ENSP_set

def get_all_UniProtIDs_with_annotations(Protein_2_FunctionEnum_table_UPS_FIN):
    UniProtIDs_list = []
    with open(Protein_2_FunctionEnum_table_UPS_FIN, "r") as fh:
        for line in fh:
            UniProtIDs_list.append(line.split("\t")[1])
    return set(UniProtIDs_list)

def Protein_2_Function_table_PMID_fulltexts(fn_in_all_entities, fn_in_string_matches, fn_in_Taxid_2_Proteins_table_STRING, fn_out_Protein_2_Function_table_PMID): # fn_in_Functions_table_PMID_temp, fn_out_Functions_table_PMID
    """
    textmining_id = entity_id
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
    ENSP_set = get_all_ENSPs(fn_in_Taxid_2_Proteins_table_STRING)
    # reduce DF to ENSPs in DB
    cond = df_txtID["ENSP"].isin(ENSP_set)
    print("reducing df_txtID from {} to {} rows".format(len(cond), sum(cond)))
    df_txtID = df_txtID[cond]
    # sanity check
    assert len(df_txtID["textmining_id"].unique()) == len(df_txtID["ENSP"].unique())
    # filter by ENSPs in DB --> Taxid_2_Protein_table_STRING.txt
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
    # #!!! dependency on Lars initial text mining file (without automatic updates)
    # PMID_set = set(df_stringmatches["PMID"].values) # how to fix this ??? --> disable since Function_2_ENSP retains only those functions which are associated with relevant ENSPs

    # PMID_not_relevant = []
    # with open(fn_in_Functions_table_PMID_temp, "r") as fh_in:
    #     with open(fn_out_Functions_table_PMID, "w") as fh_out:
    #         for line in fh_in:
    #             PMID_including_prefix = line.split("\t")[1]
    #             if int(PMID_including_prefix[5:]) in PMID_set:
    #                 fh_out.write(line)
                # else:
                #     PMID_not_relevant.append(PMID_including_prefix)

def Protein_2_Function_table(fn_list, fn_in_Taxid_2_Proteins_table_STRING, fn_out_Protein_2_Function_table_STRING, number_of_processes=1):
    # fn_list = fn_list_str.split(" ")
    ### concatenate files
    fn_out_Protein_2_Function_table_STRING_temp = fn_out_Protein_2_Function_table_STRING + "_temp"
    fn_out_Protein_2_Function_table_STRING_rest = fn_out_Protein_2_Function_table_STRING + "_rest"
    tools.concatenate_files(fn_list, fn_out_Protein_2_Function_table_STRING_temp)
    ### sort
    tools.sort_file(fn_out_Protein_2_Function_table_STRING_temp, fn_out_Protein_2_Function_table_STRING_temp, number_of_processes=number_of_processes)
    reduce_Protein_2_Function_table_2_STRING_proteins(
        fn_in_protein_2_function_temp=fn_out_Protein_2_Function_table_STRING_temp,
        fn_in_Taxid_2_Proteins_table_STRING=fn_in_Taxid_2_Proteins_table_STRING,
        fn_out_protein_2_function_reduced=fn_out_Protein_2_Function_table_STRING,
        fn_out_protein_2_function_rest=fn_out_Protein_2_Function_table_STRING_rest,
        number_of_processes=number_of_processes)

def Protein_2_Function_table_UPS(fn_list, fn_out_Protein_2_Function_table_orig, fn_out_Protein_2_Function_table_taxids_merged, number_of_processes=1):
    print("creating {} and {}".format(fn_out_Protein_2_Function_table_orig, fn_out_Protein_2_Function_table_taxids_merged))
    # fn_list = fn_list_str.split(" ")
    ### concatenate files
    tools.concatenate_files(fn_list, fn_out_Protein_2_Function_table_orig)

    ncbi = taxonomy.NCBI_taxonomy(taxdump_directory=DOWNLOADS_DIR, for_SQL=False, update=True)
    taxids_accepted = set()
    with open(fn_out_Protein_2_Function_table_orig, "r") as fh_in:
        with open(fn_out_Protein_2_Function_table_taxids_merged, "w") as fh_out:
            for line in fh_in:
                taxid, UniProtID, function_arr_str, etype = line.split("\t")
                if taxid in taxids_accepted:
                    fh_out.write(line)
                else:
                    try:
                        taxid = int(taxid)
                    except:
                        pass
                    taxid = ncbi.get_genus_or_higher(taxid, "species")
                    fh_out.write(str(taxid) + "\t" + UniProtID + "\t" + function_arr_str + "\t" + etype)
                    taxids_accepted |= {str(taxid)}

    ### sort
    tools.sort_file(fn_out_Protein_2_Function_table_orig, fn_out_Protein_2_Function_table_orig, number_of_processes=number_of_processes, verbose=True)
    tools.sort_file(fn_out_Protein_2_Function_table_taxids_merged, fn_out_Protein_2_Function_table_taxids_merged, number_of_processes=number_of_processes, verbose=True)

def reduce_Protein_2_Function_table_2_STRING_proteins(fn_in_protein_2_function_temp, fn_in_Taxid_2_Proteins_table_STRING, fn_out_protein_2_function_reduced, fn_out_protein_2_function_rest, number_of_processes=1):#, minimum_number_of_annotations=1):
    """
    - reduce Protein_2_Function_table_2_STRING to relevant ENSPs (those that are in fn_in_Taxid_2_Proteins_table_STRING)
    - and remove duplicates
    second reduction step is done elsewhere (minimum number of functional associations per taxon)
    """
    ENSP_set = parse_taxid_2_proteins_get_all_ENSPs(fn_in_Taxid_2_Proteins_table_STRING)
    print('producing new file {}'.format(fn_out_protein_2_function_reduced))
    print('producing new file {}'.format(fn_out_protein_2_function_rest))
    with open(fn_in_protein_2_function_temp, "r") as fh_in:
        line_last = fh_in.readline()
        fh_in.seek(0)
        with open(fn_out_protein_2_function_reduced, "w") as fh_out_reduced:
            with open(fn_out_protein_2_function_rest, "w") as fh_out_rest:
                for line in fh_in:
                    if line_last == line:
                        continue
                    ls = line.split("\t")
                    ENSP = ls[0]
                    if ENSP in ENSP_set:
                        fh_out_reduced.write(line)
                    else:
                        fh_out_rest.write(line)
    tools.sort_file(fn_out_protein_2_function_reduced, fn_out_protein_2_function_reduced, number_of_processes=number_of_processes)
    print("finished with reduce_Protein_2_Function_table_2_STRING_proteins")

def parse_taxid_2_proteins_get_all_ENSPs(fn_Taxid_2_Proteins_table_STRING):
    ENSP_set = set()
    with open(fn_Taxid_2_Proteins_table_STRING, "r") as fh:
        for line in fh:
            ENSP_set |= literal_eval(line.split("\t")[1])  # reduce DF to ENSPs in DB
    return ENSP_set

def Function_2_ENSP_table(fn_in_Protein_2_Function_table, fn_in_Taxid_2_Proteins_table, fn_in_Functions_table, fn_out_Function_2_ENSP_table, fn_out_Function_2_ENSP_table_reduced, fn_out_Function_2_ENSP_table_removed, min_count=1, verbose=True):
    """
    min_count: for each function minimum number of ENSPs per Taxid, e.g. 1 otherwise removed, also from Protein_2_Function_table_STRING
    """
    if verbose:
        print("creating Function_2_ENSP_table this will take a while")
    function_2_ENSPs_dict = defaultdict(list)
    taxid_2_total_protein_count_dict = _helper_get_taxid_2_total_protein_count_dict(fn_in_Taxid_2_Proteins_table)
    _, function_2_etype_dict = _helper_get_function_2_funcEnum_dict__and__function_2_etype_dict(fn_in_Functions_table) # funcenum not correct at this stage since some functions will be removed
    with open(fn_in_Protein_2_Function_table, "r") as fh_in:
        taxid_ENSP, taxid_last, etype_dont_use, function_an_set = _helper_parse_line_prot_2_func(fh_in.readline())
        fh_in.seek(0)
        with open(fn_out_Function_2_ENSP_table, "w") as fh_out:
            with open(fn_out_Function_2_ENSP_table_reduced, "w") as fh_out_reduced:
                with open(fn_out_Function_2_ENSP_table_removed, "w") as fh_out_removed:
                    for line in fh_in:
                        taxid_ENSP, taxid, etype_dont_use, function_an_set = _helper_parse_line_prot_2_func(line)
                        if taxid != taxid_last:
                            num_ENSPs_total_for_taxid = taxid_2_total_protein_count_dict[taxid_last]
                            for function_an, ENSPs in function_2_ENSPs_dict.items():
                                num_ENSPs = len(ENSPs)
                                arr_of_ENSPs = format_list_of_string_2_postgres_array(ENSPs)
                                etype = function_2_etype_dict[function_an] # "-1" default values for blacklisted terms in variables.py
                                fh_out.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_ENSPs) + "\t" + str(num_ENSPs_total_for_taxid) + "\t" + arr_of_ENSPs + "\n")
                                if num_ENSPs > min_count:
                                    fh_out_reduced.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_ENSPs) + "\t" + str(num_ENSPs_total_for_taxid) + "\t" + arr_of_ENSPs + "\n")
                                else:
                                    fh_out_removed.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_ENSPs) + "\t" + str(num_ENSPs_total_for_taxid) + "\t" + arr_of_ENSPs + "\n")
                            function_2_ENSPs_dict = defaultdict(list)
                        else:
                            for function in function_an_set:
                                function_2_ENSPs_dict[function].append(taxid_ENSP)
                        taxid_last = taxid
                    num_ENSPs_total_for_taxid = taxid_2_total_protein_count_dict[taxid]
                    for function_an, ENSPs in function_2_ENSPs_dict.items():
                        num_ENSPs = len(ENSPs)
                        arr_of_ENSPs = format_list_of_string_2_postgres_array(ENSPs)
                        etype = function_2_etype_dict[function_an]  # "-1" default values for blacklisted terms in variables.py
                        fh_out.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_ENSPs) + "\t" + str(num_ENSPs_total_for_taxid) + "\t" + arr_of_ENSPs + "\n")
                        if num_ENSPs > min_count:
                            fh_out_reduced.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_ENSPs) + "\t" + str(num_ENSPs_total_for_taxid) + "\t" + arr_of_ENSPs + "\n")
                        else:
                            fh_out_removed.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_ENSPs) + "\t" + str(num_ENSPs_total_for_taxid) + "\t" + arr_of_ENSPs + "\n")
    tools.sort_file(fn_out_Function_2_ENSP_table_reduced, fn_out_Function_2_ENSP_table_reduced)
    if verbose:
        print("finished creating \n{}\nand\n{}".format(fn_out_Function_2_ENSP_table, fn_out_Function_2_ENSP_table_reduced))

def Function_2_Protein_table_UPS(fn_in_Protein_2_Function_table_UPS, fn_in_Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS, fn_in_Taxid_2_Proteins_table_UPS_FIN, fn_in_Functions_table_all, fn_out_Function_2_Protein_table_UPS, fn_out_Function_2_Protein_table_UPS_reduced, fn_out_Function_2_Protein_table_UPS_removed, number_of_threads, min_count=1):
    """
    merge fn_in_Protein_2_Function_table_UPS and fn_in_Protein_2_Function_and_Score_DOID_BTO_GOCC_UPS
    then sort based on Taxid and UniProtID
    then iterate over merged table

    sort fn_in_Protein_2_Function_table_UPS by Taxid and UnFunctions_table_RCTMProtID
    sort fn_in_Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPSby Taxid and UniProtID
    """
    Protein_2_Function_table_merged = fn_in_Protein_2_Function_table_UPS + ".concat_temp"
    tools.concatenate_files([fn_in_Protein_2_Function_table_UPS, fn_in_Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS], Protein_2_Function_table_merged)
    tools.sort_file(Protein_2_Function_table_merged, Protein_2_Function_table_merged, number_of_processes=number_of_threads)
    print("done sorting, creating Function_2_Protein_table_UPS and removed, reduced files")
    function_2_UniProtID_dict = defaultdict(list)
    taxid_2_total_protein_count_dict = _helper_get_taxid_2_total_protein_count_dict(fn_in_Taxid_2_Proteins_table_UPS_FIN)
    # taxid_2_total_protein_count_dict defaults to -1 for taxids without reference proteomes --> use number of all proteins for given taxid instead?
    function_2_etype_dict = _helper_get_function_2_etype_dict(fn_in_Functions_table_all) # funcenum not correct at this stage therefore not present
    with open(Protein_2_Function_table_merged, "r") as fh_in:
        taxid_last, UniProtID, etype_dont_use, function_an_set = _helper_parse_line_prot_2_func_UPS(fh_in.readline())
        fh_in.seek(0)
        with open(fn_out_Function_2_Protein_table_UPS, "w") as fh_out:
            with open(fn_out_Function_2_Protein_table_UPS_reduced, "w") as fh_out_reduced:
                with open(fn_out_Function_2_Protein_table_UPS_removed, "w") as fh_out_removed:
                    for line in fh_in:
                        taxid, UniProtID, etype_dont_use, function_an_set = _helper_parse_line_prot_2_func_UPS(line)
                        if taxid != taxid_last:
                            num_UniProtIDs_total_for_taxid = taxid_2_total_protein_count_dict[taxid_last]
                            for function_an, UniProtIDs in function_2_UniProtID_dict.items():
                                num_UniProtIDs = len(UniProtIDs)
                                arr_of_UniProtIDs = ";".join(sorted(set(UniProtIDs)))
                                etype = function_2_etype_dict[function_an]  # "-1" default values for blacklisted terms in variables.py
                                fh_out.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_UniProtIDs) + "\t" + str(num_UniProtIDs_total_for_taxid) + "\t" + arr_of_UniProtIDs + "\n")
                                if num_UniProtIDs > min_count: # #!!! could also be reduced by blacklisted terms
                                    fh_out_reduced.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_UniProtIDs) + "\t" + str(num_UniProtIDs_total_for_taxid) + "\t" + arr_of_UniProtIDs + "\n")
                                else:
                                    fh_out_removed.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_UniProtIDs) + "\t" + str(num_UniProtIDs_total_for_taxid) + "\t" + arr_of_UniProtIDs + "\n")
                            function_2_UniProtID_dict = defaultdict(list)
                        else:
                            for function in function_an_set:
                                function_2_UniProtID_dict[function].append(UniProtID)
                        taxid_last = taxid
                    num_UniProtIDs_total_for_taxid = taxid_2_total_protein_count_dict[taxid]
                    for function_an, UniProtIDs in function_2_UniProtID_dict.items():
                        num_UniProtIDs = len(UniProtIDs)
                        arr_of_UniProtIDs = ";".join(sorted(set(UniProtIDs)))
                        etype = function_2_etype_dict[function_an]  # "-1" default values for blacklisted terms in variables.py
                        fh_out.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_UniProtIDs) + "\t" + str(num_UniProtIDs_total_for_taxid) + "\t" + arr_of_UniProtIDs + "\n")
                        if num_UniProtIDs > min_count:
                            fh_out_reduced.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_UniProtIDs) + "\t" + str(num_UniProtIDs_total_for_taxid) + "\t" + arr_of_UniProtIDs + "\n")
                        else:
                            fh_out_removed.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_UniProtIDs) + "\t" + str(num_UniProtIDs_total_for_taxid) + "\t" + arr_of_UniProtIDs + "\n")
    tools.sort_file(fn_out_Function_2_Protein_table_UPS_reduced, fn_out_Function_2_Protein_table_UPS_reduced, number_of_processes=number_of_threads)

def Functions_table_STRING(fn_in_Functions_table, fn_in_Function_2_ENSP_table_reduced, fn_out_Functions_table_STRING_removed, fn_out_Functions_table_STRING_reduced):
    """
    create Functions_table_STRING_reduced
    """
    # get relevant set of functions
    all_relevant_functions = set()
    with open(fn_in_Function_2_ENSP_table_reduced, "r") as fh_in:
        for line in fh_in:
            function_an = line.split("\t")[2]
            all_relevant_functions.update([function_an])

    # discard all blacklisted terms from Protein_2_Function_table and Functions
    all_relevant_functions = all_relevant_functions - set(variables.blacklisted_terms)

    counter = 0
    with open(fn_out_Functions_table_STRING_reduced, "w") as fh_out_reduced:
        with open(fn_out_Functions_table_STRING_removed, "w") as fh_out_removed:
            with open(fn_in_Functions_table, "r") as fh_in:
                for line in fh_in:
                    ls = line.split("\t")
                    wrong_enum, etype, function, description, year, hier_newline = ls
                    if function in all_relevant_functions:
                        fh_out_reduced.write(str(counter) + "\t" + etype + "\t" + function + "\t" + description + "\t" + year + "\t" + hier_newline)
                        counter += 1
                    elif etype == "-25" or etype == "-26" or etype == "-20": # include all DOID and BTO terms and GOCC (additional etype)
                        fh_out_reduced.write(str(counter) + "\t" + etype + "\t" + function + "\t" + description + "\t" + year + "\t" + hier_newline)
                        counter += 1
                    else:
                        fh_out_removed.write("-1" + "\t" + etype + "\t" + function + "\t" + description + "\t" + year + "\t" + hier_newline)

def _helper_parse_line_prot_2_func(line):
    taxid_ENSP, function_an_set_str, etype = line.split("\t")
    taxid = taxid_ENSP.split(".")[0]
    etype = etype.strip()
    function_an_set = literal_eval(function_an_set_str)
    return taxid_ENSP, taxid, etype, function_an_set

def _helper_parse_line_prot_2_func_UPS(line):
    # 3702    NAC1_ARATH      {"GO:0005777","GO:0044425", ...}     -22
    taxid, uniprotid, func_array, etype = line.split("\t")
    function_name_set = set(func_array[1:-1].replace('"', "").split(","))
    return taxid, uniprotid, etype.strip(), function_name_set

def _helper_get_taxid_2_total_protein_count_dict(fn_in_Taxid_2_Proteins_table_STRING):
    taxid_2_total_protein_count_dict = defaultdict(lambda: "-1")
    with open(fn_in_Taxid_2_Proteins_table_STRING, "r") as fh_in:
        for line in fh_in:
            taxid, count, __ENSP_arr_str= line.split("\t")
            taxid_2_total_protein_count_dict[taxid] = count
    return taxid_2_total_protein_count_dict

def _helper_get_function_2_funcEnum_dict__and__function_2_etype_dict(fn_in_Functions_table):
    function_2_funcEnum_dict, function_2_etype_dict = {}, defaultdict(lambda: "-1")
    with open(fn_in_Functions_table, "r") as fh_in:
        for line in fh_in:
            enum, etype, an, description, year, hier_nr = line.split("\t")
            function_2_funcEnum_dict[an] = enum
            function_2_etype_dict[an] = etype
    return function_2_funcEnum_dict, function_2_etype_dict

def _helper_get_function_2_etype_dict(fn_in_Functions_table):
    function_2_etype_dict = defaultdict(lambda: "-1")
    with open(fn_in_Functions_table, "r") as fh_in:
        for line in fh_in:
            etype, an, description, year, hier_nr = line.split("\t")
            function_2_etype_dict[an] = etype
    return function_2_etype_dict

def Protein_2_Function_table_reduced(fn_in_protein_2_function, fn_in_function_2_ensp_rest, fn_in_Functions_table_STRING_reduced, fn_out_protein_2_function_reduced, fn_out_protein_2_function_rest):
    """
    _by_subtracting_Function_2_ENSP_rest_and_Functions_table_STRING_reduced
    """
    # use Function_2_ENSP_table_STRING_rest to reduce Protein 2 function
    ENSP_2_assocSet_dict = {} # terms to be removed from protein_2_function
    with open(fn_in_function_2_ensp_rest, "r") as fh_in:
        for line in fh_in:
            line_split = line.strip().split("\t")
            assoc = line_split[2]
            ENSP = line_split[-1][2:-2]
            assert len(assoc.split(";")) == 1
            if ENSP not in ENSP_2_assocSet_dict:
                ENSP_2_assocSet_dict[ENSP] = {assoc}
            else:
                ENSP_2_assocSet_dict[ENSP] |= {assoc}

    # if functional terms not in fn_in_Functions_table_STRING_reduced then don't include in fn_out_protein_2_function_reduced
    funcs_2_include = []
    with open(fn_in_Functions_table_STRING_reduced, "r") as fh_in:
        for line in fh_in:
            funcs_2_include.append(line.split("\t")[2])
    funcs_2_include = set(funcs_2_include)

    print("producing new file {}".format(fn_out_protein_2_function_reduced))
    print("producing new file {}".format(fn_out_protein_2_function_rest))
    with open(fn_in_protein_2_function, "r") as fh_in:
        with open(fn_out_protein_2_function_reduced, "w") as fh_out_reduced:
            with open(fn_out_protein_2_function_rest, "w") as fh_out_rest:
                for line in fh_in:
                    line_split = line.strip().split("\t")
                    ENSP = line_split[0]
                    assoc_set = literal_eval(line_split[1])
                    etype = line_split[2]
                    try:
                        assoc_set_2_remove = ENSP_2_assocSet_dict[ENSP]
                        try:
                            assoc_reduced = assoc_set - assoc_set_2_remove
                            assoc_rest = assoc_set - assoc_reduced
                            assoc_reduced = [an for an in assoc_reduced if an in funcs_2_include]
                        except TypeError: # empty set, which should not happen
                            continue
                        if assoc_reduced:
                            fh_out_reduced.write(ENSP + "\t" + "{" + str(sorted(assoc_reduced))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + etype + "\n")
                        if assoc_rest:
                            fh_out_rest.write(ENSP + "\t" + "{" + str(sorted(assoc_rest))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + etype + "\n")
                    except KeyError:
                        assoc_reduced, assoc_rest = [], []
                        for an in assoc_set:
                            if an in funcs_2_include:
                                assoc_reduced.append(an)
                            else:
                                assoc_rest.append(an)
                        if assoc_reduced:
                            fh_out_reduced.write(ENSP + "\t" + "{" + str(sorted(assoc_reduced))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + etype + "\n")
                        if assoc_rest:
                            fh_out_rest.write(ENSP + "\t" + "{" + str(sorted(assoc_rest))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + etype + "\n")
    print("finished with reduce_Protein_2_Function_by_subtracting_Function_2_ENSP_rest")

def AFC_KS_enrichment_terms_flat_files(fn_in_Protein_shorthands, fn_in_Functions_table_STRING_reduced, fn_in_Function_2_ENSP_table_STRING_reduced, KEGG_Taxid_2_acronym_table, fn_out_AFC_KS_DIR, verbose=True):
    print("AFC_KS_enrichment_terms_flat_files start")
    ENSP_2_internalID_dict = {}
    with open(fn_in_Protein_shorthands, "r") as fh:
        for line in fh:
            ENSP, internalID = line.split()
            internalID = internalID.strip()
            ENSP_2_internalID_dict[ENSP] = internalID

    association_2_description_dict = {}
    with open(fn_in_Functions_table_STRING_reduced, "r") as fh:
        for line in fh:
            enum, etype, an, description, year, level = line.split("\t")
            association_2_description_dict[an] = description

    taxid_2_acronym_dict = {}
    with open(KEGG_Taxid_2_acronym_table, "r") as fh:
        for line in fh:
            taxid, acronym = line.split("\t")
            acronym = acronym.strip()
            taxid_2_acronym_dict[taxid] = acronym

    counter = 0
    fn_out_prefix = os.path.join(fn_out_AFC_KS_DIR + "{}_AFC_KS_all_terms.tsv")
    with open(fn_in_Function_2_ENSP_table_STRING_reduced, "r") as fh_in:
        taxid_last, etype, association, background_count, background_n, an_array = fh_in.readline().split()
        fn_out = fn_out_prefix.format(taxid_last)
        fh_out = open(fn_out, "w")
        fh_in.seek(0)
        for line in fh_in:
            taxid, etype, association, background_count, background_n, an_array = line.split()
            an_array = literal_eval(an_array.strip())
            try:
                description = association_2_description_dict[association]
            except KeyError: # since removed due to e.g. blacklisting
                continue
            number_of_ENSPs = str(len(an_array))
            array_of_ENSPs_with_internal_IDS = " ".join(sorted(map_ENSPs_2_internalIDs(an_array, ENSP_2_internalID_dict)))
            if taxid != taxid_last:
                fh_out.close()
                fn_out = fn_out_prefix.format(taxid)
                fh_out = open(fn_out, "w")
            if etype == "-52": # KEGG
                try:
                    acronym = taxid_2_acronym_dict[taxid]
                except KeyError:
                    print("no KEGG acronym translation for Taxid: {}".format(taxid))
                    acronym = "map"
                association = association.replace("map", acronym)
            fh_out.write(association + "\t" + etype + "\t" + description + "\t" + number_of_ENSPs + "\t" + array_of_ENSPs_with_internal_IDS + "\n")
            taxid_last = taxid
        if verbose:
            if counter % 500 == 0:
                print(".", end="")
        counter += 1
        fh_out.close()
    print("AFC_KS_enrichment_terms_flat_files done :)")

def map_ENSPs_2_internalIDs(ENSPs, ENSP_2_internalID_dict):
    list_2_return = []
    for ENSP in ENSPs:
        try:
            internalID = ENSP_2_internalID_dict[ENSP]
            list_2_return.append(internalID)
        except KeyError:
            print("{} # no internal ID found".format(ENSP))
    return list_2_return

### Jensenlab
def Functions_table_PMID(Function_2_Description_PMID, Functions_table_PMID_temp, max_len_description=250): # string_matches
    # df_stringmatches = parse_textmining_string_matches(string_matches)
    # PMID_set = set(df_stringmatches["PMID"].values)
    hierarchical_level = "-1"
    # with open(Function_2_Description_PMID, "r") as fh_in:
    #         for line in fh_in:
    counter = -1
    with open(Functions_table_PMID_temp, "w") as fh_out:
        for line in tools.yield_line_uncompressed_or_gz_file(Function_2_Description_PMID):
            ls = line.split("\t")
            counter += 1
            try:
                etype, PMID, description, year = ls
            except ValueError: # not enough values to unpack
                print("def Functions_table_PMID", counter, ls, "###", line)
                continue
            # if PMID not in PMID_set:
            #     continue
            year = year.strip()
            if not year:
                year = "...."
            year_prefix = description[:7]
            description_2_clean = description[7:]
            description_2_clean = clean_messy_string_v2(description_2_clean)  # in order to capture foreign language titles' open and closing brackets e.g. "[bla bla bla]"
            description_2_clean = cut_long_string_at_word(description_2_clean, max_len_description)
            description = year_prefix + " ".join(description_2_clean.split())  # replace multiple spaces with single space
            fh_out.write(etype + "\t" + PMID + "\t" + description + "\t" + year + "\t" + hierarchical_level + "\n")


def Protein_2_Function_table_PMID_STS(Taxid_2_Proteins_table_STRING, Protein_2_Function_table_PMID_abstracts, Protein_2_Function_table_PMID_fulltexts, Protein_2_Function_table_PMID_combi, Protein_2_Function_table_PMID, number_of_processes=1, verbose=True):
    """
    concatenate files, sort and create set of union of functional associations
    filter PMID associations that are not STRING ENSPs. use Taxid_2_Proteins_table_STRING
    :param Taxid_2_Proteins_table_STRING: string
    :param Protein_2_Function_table_PMID_abstracts: string
        1000565.METUNv1_03313   {"PMID:29179769"}       -56
        1000565.METUNv1_03481   {"PMID:27682085"}       -56
        1001530.BACE01000001_gene3552   {"PMID:9183020"}        -56
    :param Protein_2_Function_table_PMID_fulltexts: string
        1000565.METUNv1_03313   {"PMID:24905407","PMID:29179769"}       -56
        1000565.METUNv1_00036   {"PMID:27708623"}       -56
        1000565.METUNv1_00081   {"PMID:19514844","PMID:19943898"}       -56
    :param Protein_2_Function_table_PMID_combi: string
    :param Protein_2_Function_table_PMID: string
    :param number_of_processes: Integer
    :param verbose: Bool
    :return: None
    """
    # concatenate files
    tools.concatenate_files([Protein_2_Function_table_PMID_abstracts, Protein_2_Function_table_PMID_fulltexts], Protein_2_Function_table_PMID_combi)
    # sort files
    tools.sort_file(Protein_2_Function_table_PMID_combi, Protein_2_Function_table_PMID_combi, number_of_processes=number_of_processes, verbose=verbose)
    # merge lines with duplicate ENSPs

    ENSP_set = get_all_ENSPs(Taxid_2_Proteins_table_STRING)

    with open(Protein_2_Function_table_PMID_combi, "r") as fh_in:
        ls = fh_in.readline().split("\t")
        fh_in.seek(0)
        ENSP_last, PMID_arr_last, etype = ls
        PMID_list = helper_string_array_to_list(PMID_arr_last)
        with open(Protein_2_Function_table_PMID, "w") as fh_out:
            for line in fh_in:
                ls = line.split("\t")
                ENSP, PMID_arr, etype = ls
                if ENSP == ENSP_last: # add
                    PMID_list += helper_string_array_to_list(PMID_arr)
                else: # write
                    if ENSP_last in ENSP_set:
                        fh_out.write(ENSP_last + "\t" + format_list_of_string_2_postgres_array(sorted(set(PMID_list))) + "\t" + etype)
                    PMID_list = helper_string_array_to_list(PMID_arr) # create new list
                    ENSP_last = ENSP
            if ENSP in ENSP_set:
                fh_out.write(ENSP + "\t" + format_list_of_string_2_postgres_array(sorted(set(PMID_list))) + "\t" + etype)

def helper_string_array_to_list(string_):
    """
    string_ = '{"PMID:19514844","PMID:19943898"}'
    ['PMID:19514844', 'PMID:19943898']
    """
    return [an[1:-1] for an in string_[1:-1].split(",")]

def Functions_table_DOID_BTO_GOCC(Function_2_Description_DOID_BTO_GO_down, BTO_obo_Jensenlab, DOID_obo_Jensenlab, GO_obo_Jensenlab, Blacklisted_terms_Jensenlab, Functions_table_DOID_BTO_GOCC, GO_CC_textmining_additional_etype=True, number_of_processes=4, verbose=True):
    """
    - add hierarchical level, year placeholder
    - merge with Functions_table
    | enum | etype | an | description | year | level |
    """
    # get term 2 hierarchical level
    bto_dag = obo_parser.GODag(obo_file=BTO_obo_Jensenlab)
    child_2_parent_dict = get_child_2_direct_parent_dict_from_dag(bto_dag)  # obsolete or top level terms have empty set for parents
    term_2_level_dict_bto = get_term_2_level_dict(child_2_parent_dict)
    doid_dag = obo_parser.GODag(obo_file=DOID_obo_Jensenlab)
    child_2_parent_dict = get_child_2_direct_parent_dict_from_dag(doid_dag)  # obsolete or top level terms have empty set for parents
    term_2_level_dict_doid = get_term_2_level_dict(child_2_parent_dict)

    gocc_dag = obo_parser.GODag(obo_file=GO_obo_Jensenlab)
    child_2_parent_dict = get_child_2_direct_parent_dict_from_dag(gocc_dag)  # obsolete or top level terms have empty set for parents
    term_2_level_dict_gocc_temp = get_term_2_level_dict(child_2_parent_dict)
    term_2_level_dict_gocc = {}
    # convert "GO:" to "GOCC:"
    for term, level in term_2_level_dict_gocc_temp.items():
        term = term.replace("GO:", "GOCC:")
        term_2_level_dict_gocc[term] = level

    term_2_level_dict = {}
    term_2_level_dict.update(term_2_level_dict_doid)
    term_2_level_dict.update(term_2_level_dict_bto)
    term_2_level_dict.update(term_2_level_dict_gocc)
    # get blacklisted terms to exclude them
    blacklisted_ans = []
    with open(Blacklisted_terms_Jensenlab, "r") as fh:
        for line in fh:
            etype, an = line.split("\t")
            # don't include Lars' blacklisted GO terms
            # Lars' blacklist is for a subcellular localization resource, so telling that the protein is part of complex X is not
            # really the information that you are after. But for the enrichment, the situation is different.
            if etype != "-22":
                blacklisted_ans.append(an.strip())
    blacklisted_ans = set(blacklisted_ans)
    blacklisted_ans.update(variables.blacklisted_terms) # exclude top level terms, and manually curated

    year = "-1" # placeholder
    with open(Functions_table_DOID_BTO_GOCC, "w") as fh_out:
        for line in tools.yield_line_uncompressed_or_gz_file(Function_2_Description_DOID_BTO_GO_down):
            etype, function_an, description = line.split("\t")
            if GO_CC_textmining_additional_etype:
                if etype == "-22":
                    etype = "-20"
                    function_an = function_an.replace("GO:", "GOCC:")
            description = description.strip()
            if function_an in blacklisted_ans:
                continue
            try:
                level = term_2_level_dict[function_an] # level is an integer
            except KeyError:
                level = -1
            fh_out.write(etype + "\t" + function_an + "\t" + description + "\t" + year + "\t" + str(level) + "\n")

    # remove redundant terms, keep those with "better" descriptions (not simply GO-ID as description e.g.
    # -22     GO:0000793      Condensed chromosome
    # -22     GO:0000793      GO:0000793
    # sort it
    # remove redundant terms
    # overwrite redundant file with cleaned up version
    tools.sort_file(Functions_table_DOID_BTO_GOCC, Functions_table_DOID_BTO_GOCC, number_of_processes=number_of_processes, verbose=verbose)
    func_redundancy_dict = {}
    Functions_table_DOID_BTO_GOCC_temp = Functions_table_DOID_BTO_GOCC + "_temp"
    with open(Functions_table_DOID_BTO_GOCC_temp, "w") as fh_out:
        with open(Functions_table_DOID_BTO_GOCC, "r") as fh_in:
            line = next(fh_in)
            etype_last, function_last, description_last, year_last, hier_last = line.split("\t")
            func_redundancy_dict[function_last] = line
            for line in fh_in:
                etype, function, description, year, hier = line.split("\t")
                if function in func_redundancy_dict:
                    # take every description, but overwrite existing only if function_id is not equal to description
                    if function.replace("GOCC:", "GO:").strip().lower() != description.strip().lower():
                        func_redundancy_dict[function] = line
                else:
                    func_redundancy_dict[function] = line
        for line in sorted(func_redundancy_dict.values()):
            fh_out.write(line)
    os.rename(Functions_table_DOID_BTO_GOCC_temp, Functions_table_DOID_BTO_GOCC)

def Protein_2_FunctionEnum_and_Score_table_STS(Protein_2_Function_and_Score_DOID_GO_BTO, Functions_table_STRING_reduced, Taxid_2_Proteins_table_STRING, Protein_2_FunctionEnum_and_Score_table, fn_an_without_translation, GO_CC_textmining_additional_etype=False):
    """
    temp
    3702.AT1G01010.1        {{"GO:0005777",0.535714},{"GO:0005783",0.214286},{"GO:0044444",1.234689},{"GO:0043226",3.257143},{"GO:0005575",4.2},{"GO:0044425",3},{"GO:0042579",0.535714},{"GO:0016020",3},{"GO:0031224",3},{"GO:0005794",0.642857},{"GO:0005854",0.741623},{"GO:0044214",0.639807},{"GO:0043227",3.257143},{"GO:0005622",4.166357},{"GO:0005737",1.234689},{"GO:0009507",0.214286},{"GO:0005773",0.428571},{"GO:0043229",3.257143},{"GO:0005829",1.189679},{"GO:0005623",4.195121},{"GO:0009536",0.214286},{"GO:0005634",3.257143},{"GO:0044464",4.195121},{"GO:0016021",3},{"GO:0043231",3.257143},{"GO:0044424",4.166357}}        -22
3702.AT1G01020.1        {{"GO:0005783",0.614858}}       -22
3702.AT1G01030.1        {{"GO:0043231",4.144794},{"GO:0005575",4.2},{"GO:0009536",0.214286},{"GO:0044464",4.2},{"GO:0009507",0.214286},{"GO:1902911",1.009029},{"GO:0020007",1.593395},{"GO:0005737",0.214286},{"GO:0044444",0.214286},{"GO:0043229",4.144794},{"GO:0005623",4.2},{"GO:0043226",4.144794},{"GO:0061695",0.68545},{"GO:0044424",4.2},{"GO:0043227",4.144794},{"GO:0005576",0.214286},{"GO:0005622",4.2},{"GO:0045177",1.589376},{"GO:0005634",4.143193}} -22


    Protein_2_Function_and_Score_DOID_GO_BTO.txt
    6239.C30G4.7    {{"GO:0043226",0.875},{"GO:0043227",0.875},{"GO:0043231",0.875},{"GO:0044424",2.96924}, ... , {"GO:0005737",2.742276},{"GO:0005777",0.703125}}      -22
    10116.ENSRNOP00000049139        {{"GO:0005623",2.927737},{"GO:0044424",2.403304},{"GO:0044425",3},{"GO:0031224",3}, ... ,{"GO:0043232",0.375}}       -22

    Protein_2_FuncEnum_and_Score_DOID_BTO_GOCC.txt
    10116.ENSRNOP00000049139  {{{0,2.927737},{3,2.403304},{4,3},{666,3}, ... ,{3000000,0.375}}

    9606.ENSP00000000233    {{33885,1.00616},{34752,0.709055},{35541,1.297117},{35543,1.296111},{35907,0.600582},{36031,0.670014},{36271,0.527888},{36276,0.552587},{36417,0.51056},{36650,0.534848},{38517,0.513162},{38635,0.704968}}
    9606.ENSP00000000233    {{24755,0.711807},{24758,0.39794},{24760,1.60995},{24783,1.684247},{24785,1.283301},{24797,0.161368},{24803,0.09691},{24814,0.733333},{24815,0.733333},{24819,0.954243},{24821,0.883661},{24823,1.767898},{24824,4.692989},{24828,0.939644},{24838,1.684247},{24841,0.748188},{24861,1.717671},{24867,0.60206},{24878,4.69092},{24881,1.78864},{24882,0.939644},{24883,1.78864}, ... }

    - remove anything on blacklist (all_hidden.tsv) already happend while creating Functions_table_DOID_BTO (and all terms not present therein will be filtered out)
    - omit GO-CC (etype -22)
    """
    ENSP_last, ENSP = "bubu", "bubu"
    funcEnum_2_score = []
    # year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr = get_lookup_arrays(Functions_table_STRING_reduced, low_memory=True)
    year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr = query.get_lookup_arrays(read_from_flat_files=True)
    term_2_enum_dict = {key: val for key, val in zip(functionalterm_arr, indices_arr)}
    ENSP_set = get_all_ENSPs(Taxid_2_Proteins_table_STRING)
    an_without_translation = []
    with open(Protein_2_FunctionEnum_and_Score_table, "w") as fh_out:
        for line in tools.yield_line_uncompressed_or_gz_file(Protein_2_Function_and_Score_DOID_GO_BTO):
            ENSP_last, funcName_2_score_arr_str_last, etype_last = line.split("\t")
            break

        for line in tools.yield_line_uncompressed_or_gz_file(Protein_2_Function_and_Score_DOID_GO_BTO):
            ENSP, funcName_2_score_arr_str, etype = line.split("\t")
            etype = etype.strip()
            if ENSP != ENSP_last: # write old results and parse new
                if len(funcEnum_2_score) > 0 and ENSP in ENSP_set: # don't add empty results due to blacklisting or GO-CC terms
                    funcEnum_2_score.sort(key=lambda sublist: sublist[0]) # sort anEnum in ascending order
                    funcEnum_2_score = format_list_of_string_2_postgres_array(funcEnum_2_score)
                    funcEnum_2_score = funcEnum_2_score.replace("[", "{").replace("]", "}")
                    fh_out.write(ENSP_last + "\t" + funcEnum_2_score + "\n")
                funcEnum_2_score = []
                ENSP_last = ENSP
            # parse current and add to funcEnum_2_score
            funcName_2_score_list = helper_convert_str_arr_2_nested_list(funcName_2_score_arr_str)
            for an_score in funcName_2_score_list:
                an, score = an_score
                if GO_CC_textmining_additional_etype: # works only if GOCC textmining etype 20 is included in Functions_table_all and then not excluded in Functions_table_FIN
                    if etype == "-22": # change etype to separate etype GO-CC (etype -22 --> -20)
                        an = an.replace("GO:", "GOCC:")
                try:
                    anEnum = term_2_enum_dict[an]
                    funcEnum_2_score.append([anEnum, score])
                except KeyError: # because e.g. blacklisted
                    an_without_translation.append(an)

        if len(funcEnum_2_score) > 0 and ENSP in ENSP_set:  # don't add empty results due to blacklisting or GO-CC terms
            funcEnum_2_score.sort(key=lambda sublist: sublist[0])  # sort anEnum in ascending order
            funcEnum_2_score = format_list_of_string_2_postgres_array(funcEnum_2_score)
            funcEnum_2_score = funcEnum_2_score.replace("[", "{").replace("]", "}")
            fh_out.write(ENSP + "\t" + funcEnum_2_score + "\n")

    with open(fn_an_without_translation, "w") as fh_an_without_translation:
        fh_an_without_translation.write("\n".join(sorted(set(an_without_translation))))

def Protein_2_FunctionEnum_and_Score_table_UPS(fn_go_basic_obo, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab, fn_in_Taxid_2_UniProtID_2_ENSPs_2_KEGGs, Protein_2_Function_and_Score_DOID_BTO_GOCC_STS, Functions_table_UPS, fn_out_Protein_2_FunctionEnum_and_Score_table_UPS, fn_out_DOID_GO_BTO_an_without_translation, fn_out_ENSP_2_UniProtID_without_translation, fn_out_DOID_GO_BTO_an_without_lineage, GO_CC_textmining_additional_etype=True):
    """
    ToDo: restrict functions by associations in Functions_table_UPS
    bug in previous version of this functions inner loop, not sure why? fixed now
    differences to STS version:
     - no need to filter to analog of ENSPs in proteome (we want all annotations even for UniProtAC/IDs that are not in reference proteome/background proteome), filter later on
     - translate to UniProtID on the fly using ENSP_2_UniProtID
    see other comments above

    e.g. of 2 ENSPs with too many scores for single function
        9606.ENSP00000396163;9606.ENSP00000265849
        DOID:0050654 	9 	Baller-Gerold syndrome
    """
    alternative_2_current_ID_dict = {}
    alternative_2_current_ID_dict.update(get_alternative_2_current_ID_dict(fn_go_basic_obo, upk=False))  # GOCC not needed yet, lineage_dict has GOCC terms but output file has normal GO terms, conversion happens later
    alternative_2_current_ID_dict.update(get_alternative_2_current_ID_dict(fn_in_DOID_obo_Jensenlab, upk=True))
    alternative_2_current_ID_dict.update(get_alternative_2_current_ID_dict(fn_in_BTO_obo_Jensenlab, upk=True))

    ENSP_2_UniProtID_dict = get_ENSP_2_UniProtID_dict(fn_in_Taxid_2_UniProtID_2_ENSPs_2_KEGGs) # defaultdict

    ENSP_last, ENSP = "-1", "-1"
    funcEnum_2_score_per_ENSP = []
    year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr = query.get_lookup_arrays(read_from_flat_files=True)
    term_2_enum_dict = {key: val for key, val in zip(functionalterm_arr, indices_arr)}
    an_without_translation, ENSP_without_translation, without_lineage = [], [], set()
    lineage_dict_direct_parents = get_lineage_dict_for_DOID_BTO_GO(fn_go_basic_obo, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab, GO_CC_textmining_additional_etype=False, direct_parents_only=True)
    blacklisted_funcNames_set = variables.blacklisted_terms # DBL blacklisted, manually curated GOCC terms to exclude

    with open(fn_out_Protein_2_FunctionEnum_and_Score_table_UPS, "w") as fh_out:
        for line in tools.yield_line_uncompressed_or_gz_file(Protein_2_Function_and_Score_DOID_BTO_GOCC_STS):
            ENSP_last, _, _ = line.split("\t")
            break

        for line in tools.yield_line_uncompressed_or_gz_file(Protein_2_Function_and_Score_DOID_BTO_GOCC_STS):
            funcEnum_2_score = []
            ENSP, funcName_2_score_arr_str, etype = line.split("\t")
            etype = etype.strip()
            taxid = ENSP.split(".")[0]
            if ENSP != ENSP_last: # write old results and parse new
                if len(funcEnum_2_score_per_ENSP) > 0: # don't add empty results due to blacklisting or GO-CC terms
                    funcEnum_2_score_per_ENSP.sort(key=lambda sublist: sublist[0]) # sort anEnum in ascending order
                    funcEnum_arr_and_score_arr_str = helper_reformat_funcEnum_2_score(funcEnum_2_score_per_ENSP)
                    UniProtID_list = ENSP_2_UniProtID_dict[ENSP_last]
                    if len(UniProtID_list) >= 1:
                        for UniProtID in UniProtID_list:
                            fh_out.write(taxid + "\t" + UniProtID + "\t" + funcEnum_arr_and_score_arr_str + "\n")
                    else:
                        ENSP_without_translation.append(ENSP_last)
                funcEnum_2_score_per_ENSP = []
            # parse current and add to funcEnum_2_score
            funcName_2_score_list_temp = helper_convert_str_arr_2_nested_list(funcName_2_score_arr_str)
            funcName_2_score_list = []
            for funcName, score in funcName_2_score_list_temp:
                if funcName not in blacklisted_funcNames_set:
                    funcName_2_score_list.append([funcName, score])
            # backtracking. funcName_2_score_list --> scores are now integer NOT floats
            funcName_2_score_list, without_lineage_temp = helper_backtrack_funcName_2_score_list(funcName_2_score_list, lineage_dict_direct_parents)
            without_lineage |= without_lineage_temp
            for an_score in funcName_2_score_list:
                an, score = an_score
                try: # translate from alternative/alias to main name (synonym or obsolete funcName to current name)
                    an = alternative_2_current_ID_dict[an]
                except KeyError:
                    an = an

                if GO_CC_textmining_additional_etype: # works only if GOCC textmining etype 20 is included in Functions_table_all and then not excluded in Functions_table_FIN
                    if etype == "-22": # change etype to separate etype GO-CC (etype -22 --> -20)
                        an = an.replace("GO:", "GOCC:")
                try:
                    anEnum = term_2_enum_dict[an]
                    funcEnum_2_score.append([anEnum, score])
                except KeyError: # because e.g. blacklisted via Jensenlab blacklist download file
                    an_without_translation.append(an)
            funcEnum_2_score = helper_select_higher_score_if_redundant(funcEnum_2_score) # can happen due to mapping of alternate IDs
            funcEnum_2_score_per_ENSP += funcEnum_2_score
            ENSP_last = ENSP

        if len(funcEnum_2_score_per_ENSP) > 0:  # don't add empty results due to blacklisting or GO-CC terms
            funcEnum_2_score_per_ENSP.sort(key=lambda sublist: sublist[0])  # sort anEnum in ascending order
            funcEnum_arr_and_score_arr_str = helper_reformat_funcEnum_2_score(funcEnum_2_score_per_ENSP)
            UniProtID_list = ENSP_2_UniProtID_dict[ENSP_last]
            if len(UniProtID_list) >= 1:
                for UniProtID in UniProtID_list:
                    fh_out.write(taxid + "\t" + UniProtID + "\t" + funcEnum_arr_and_score_arr_str + "\n")
            else:
                ENSP_without_translation.append(ENSP_last)

    with open(fn_out_DOID_GO_BTO_an_without_translation, "w") as fh_an_without_translation:
        fh_an_without_translation.write("\n".join(sorted(set(an_without_translation))))
    with open(fn_out_ENSP_2_UniProtID_without_translation, "w") as fh_ENSP_2_UniProtID_without_translation:
        fh_ENSP_2_UniProtID_without_translation.write("\n".join(sorted(set(ENSP_without_translation))))
    with open(fn_out_DOID_GO_BTO_an_without_lineage, "w") as fh_without_lineage:
        for funcName in sorted(without_lineage):
            fh_without_lineage.write(funcName + "\n")

def helper_reformat_funcEnum_2_score(funcEnum_2_score):
    funcEnum_list, score_list = [], []
    for funcEnum, score in funcEnum_2_score:
        funcEnum_list.append(str(funcEnum))
        score_list.append(str(score))
    return "{" + ",".join(funcEnum_list) + "}\t{" + ",".join(score_list) + "}"

def helper_select_higher_score_if_redundant(funcEnum_2_score_per_ENSP):
    funcEnum_2_score_dict = {}
    for funcEnum, score in funcEnum_2_score_per_ENSP:
        if funcEnum not in funcEnum_2_score_dict:
            funcEnum_2_score_dict[funcEnum] = score
        else:
            previous_score = funcEnum_2_score_dict[funcEnum]
            if score > previous_score:
                funcEnum_2_score_dict[funcEnum] = score
            else:
                pass # keep current score, since higher
    return [[funcEnum, funcEnum_2_score_dict[funcEnum]] for funcEnum in funcEnum_2_score_dict.keys()]

# def helper_backtrack_funcName_2_score_list_orig(funcName_2_score_list, lineage_dict):
#     """
#     backtrack and propage text mining scores from Jensenlab without creating redundancy
#     backtrack functions to root and propagate scores
#         - only if there is no score for that term
#         - if different scores exist for various children then
#     convert scores from float to int (by scaling 1e6 and cutting)
#     funcName_2_score_list = [['DOID:11613', 0.686827], ['DOID:1923', 0.817843], ['DOID:4', 1.982001], ['DOID:7', 1.815976]]
#
#     lineage_dict["DOID:11613"] = {'DOID:11613', 'DOID:1923', 'DOID:2277', 'DOID:28', 'DOID:4', 'DOID:7'}
#     funcName_2_score_list_backtracked = [['DOID:11613', 686827], ['DOID:1923', 817843], ['DOID:4', 1982001], ['DOID:7', 1815976], # previously set
#     ['DOID:28', 686827], ['DOID:2277', 686827]} # backtracked new
#     ['DOID:28', 817843], ['DOID:2277', 817843]} # backtracked new corrected
#
#     """
#     funcName_2_score_dict_backtracked, without_lineage = {}, []
#     # funcName_2_score_dict_backtracked: key=String, val=Float(if unique), List of Float(if averaged)
#     # fill dict with all given values, these should be unique (funcName has only single value)
#     for funcName_2_score in funcName_2_score_list:
#         funcName, score = funcName_2_score
#         if funcName not in funcName_2_score_dict_backtracked:
#             funcName_2_score_dict_backtracked[funcName] = score
#         else:
#             print("helper_backtrack_funcName_2_score_list", funcName, funcName_2_score_dict_backtracked[funcName], score, " duplicates")
#
#     # backtrack from child to direct parent terms and fill value
#     # if entry exists, don't change it (set as a float)
#     # if it doesn't exist, then collect all scores (append to list) and average/median in the end
#     for funcName in list(funcName_2_score_dict_backtracked.keys()):
#         try:
#             all_parents = lineage_dict[funcName]
#         except KeyError:
#             without_lineage.append(funcName)
#             all_parents = []
#         score = funcName_2_score_dict_backtracked[funcName]
#         for parent in all_parents:
#             # check if parent exists
#             # if it does not, add the entry
#             if parent not in funcName_2_score_dict_backtracked:
#                 funcName_2_score_dict_backtracked[parent] = [score]
#             # if it does, check if it is a Float or a list of Float (which means append to it) or string
#             else:
#                 if isinstance(funcName_2_score_dict_backtracked[parent], float):
#                     continue  # don't change the value, since it is the original value
#                 elif isinstance(funcName_2_score_dict_backtracked[parent], list): # add to it
#                     funcName_2_score_dict_backtracked[parent].append(score)
#                 else:
#                     print("helper_backtrack_funcName_2_score_list", parent, funcName_2_score_dict_backtracked[parent], " type not known")
#                     raise StopIteration
#
#     # now calc median if multiple values exist
#     funcName_2_score_list_backtracked = []
#     for funcName in funcName_2_score_dict_backtracked:
#         val = funcName_2_score_dict_backtracked[funcName]
#         if isinstance(val, float):
#             funcName_2_score_list_backtracked.append([funcName, int(val * 1e6)])
#         else:
#             funcName_2_score_list_backtracked.append([funcName, int(median(val) * 1e6)])
#
#     return funcName_2_score_list_backtracked, set(without_lineage)

def helper_backtrack_funcName_2_score_list(funcName_2_score_list, lineage_dict_direct_parents):
    """
    backtrack and propage text mining scores from Jensenlab without creating redundancy
    backtrack functions to root and propagate scores
        - only if there is no score for that term
        - if different scores exist for various children then
    convert scores from float to int (by scaling 1e6 and cutting)
    funcName_2_score_list = [['DOID:11613', 0.686827], ['DOID:1923', 0.817843], ['DOID:4', 1.982001], ['DOID:7', 1.815976]]
    lineage_dict["DOID:11613"] = {'DOID:11613', 'DOID:1923', 'DOID:2277', 'DOID:28', 'DOID:4', 'DOID:7'}
    funcName_2_score_list_backtracked = [['DOID:11613', 686827], ['DOID:1923', 817843], ['DOID:4', 1982001], ['DOID:7', 1815976], # previously set
    ['DOID:28', 686827], ['DOID:2277', 686827]} # backtracked new
    ['DOID:28', 817843], ['DOID:2277', 817843]} # backtracked new corrected
    set score directly that stem from textmining, propagate from child to parent term(s), if term has multiple children then the average of the scores is used
    visit all
    """
    funcName_2_score_dict_backtracked, without_lineage = {}, []
    # funcName_2_score_dict_backtracked: key=String, val=Float(if unique), List of Float(if averaged)
    # fill dict with all given values, these should be unique (funcName has only single value)
    for funcName_2_score in funcName_2_score_list:
        funcName, score = funcName_2_score
        if funcName not in funcName_2_score_dict_backtracked:
            funcName_2_score_dict_backtracked[funcName] = score
        else:
            print("helper_backtrack_funcName_2_score_list", funcName, funcName_2_score_dict_backtracked[funcName], score, " duplicates")

    # add all funcNames to iterable and extend with all parents
    visit_plan = deque()
    for child, score in funcName_2_score_list:
        visit_plan.append(child)

    while visit_plan:
        funcName = visit_plan.pop()
        try:
            direct_parents = lineage_dict_direct_parents[funcName]
        except KeyError:
            without_lineage.append(funcName)
            direct_parents = []
        score = funcName_2_score_dict_backtracked[funcName]
        for parent in direct_parents:
            if parent not in funcName_2_score_dict_backtracked: # propagate score, mark as such by using a list instead of float
                if isinstance(score, list):  # score is a list because it was propagated
                    funcName_2_score_dict_backtracked[parent] = score
                else:
                    funcName_2_score_dict_backtracked[parent] = [score]
                visit_plan.append(parent)
            else:
                if isinstance(funcName_2_score_dict_backtracked[parent], float):
                    continue  # don't change the value, since it is the original value
                elif isinstance(funcName_2_score_dict_backtracked[parent], list):  # add to it
                    if isinstance(score, list): # score is a list because it was propagated
                        funcName_2_score_dict_backtracked[parent] += score
                    else: # score is a float since original TM score
                        funcName_2_score_dict_backtracked[parent].append(score)
                else:
                    print("helper_backtrack_funcName_2_score_list", parent, funcName_2_score_dict_backtracked[parent], " type not known")
                    raise StopIteration

    # now calc median if multiple values exist
    funcName_2_score_list_backtracked = []
    for funcName in funcName_2_score_dict_backtracked:
        val = funcName_2_score_dict_backtracked[funcName]
        if isinstance(val, float):
            funcName_2_score_list_backtracked.append([funcName, int(val * 1e6)])
        else:
            funcName_2_score_list_backtracked.append([funcName, int(median(val) * 1e6)])

    return funcName_2_score_list_backtracked, set(without_lineage)


def Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS(fn_go_basic_obo, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab, fn_in_UniProtID_2_ENSPs_2_KEGGs_2_Taxid, fn_in_Protein_2_Function_and_Score_DOID_BTO_GOCC_STS, fn_out_Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS, fn_out_without_lineage):
    """

    :param fn_go_basic_obo:
    :param fn_in_DOID_obo_Jensenlab:
    :param fn_in_BTO_obo_Jensenlab:
    :param fn_in_UniProtID_2_ENSPs_2_KEGGs_2_Taxid:
    :param fn_in_Protein_2_Function_and_Score_DOID_BTO_GOCC_STS:
    :param fn_out_Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS: outputs normal GO not GOCC terms
    :param fn_out_without_lineage:
    :return:
    """
    alternative_2_current_ID_dict = {}
    alternative_2_current_ID_dict.update(get_alternative_2_current_ID_dict(fn_go_basic_obo, upk=False))  # GOCC not needed yet, lineage_dict has GOCC terms but output file has normal GO terms, conversion happens later
    alternative_2_current_ID_dict.update(get_alternative_2_current_ID_dict(fn_in_DOID_obo_Jensenlab, upk=True))
    alternative_2_current_ID_dict.update(get_alternative_2_current_ID_dict(fn_in_BTO_obo_Jensenlab, upk=True))

    ENSP_2_UniProtID_dict = get_ENSP_2_UniProtID_dict(fn_in_UniProtID_2_ENSPs_2_KEGGs_2_Taxid)
    # lineage_dict has GO as well as GOCC terms
    lineage_dict = get_lineage_dict_for_DOID_BTO_GO(fn_go_basic_obo, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab, GO_CC_textmining_additional_etype=False)

    terms_without_lineage = set()
    with open(fn_out_Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS, "w") as fh_out_Prot_2_func:
        for line in tools.yield_line_uncompressed_or_gz_file(fn_in_Protein_2_Function_and_Score_DOID_BTO_GOCC_STS):
            ENSP, funcName_2_score_arr_str, etype = line.split("\t")
            etype = etype.strip()
            taxid = ENSP.split(".")[0]
            UniProtID_list = ENSP_2_UniProtID_dict[ENSP] # defaultdict
            funcName_list = helper_grep_funcNames(funcName_2_score_arr_str)
            # backtracking of functions
            funcName_list_backtracked = []
            for funcName in funcName_list:
                try: # translate if possible
                    funcName = alternative_2_current_ID_dict[funcName]
                except KeyError:
                    funcName = funcName
                funcName_list_backtracked.append(funcName)
                try:
                    funcName_list_backtracked += list(lineage_dict[funcName])
                except KeyError:
                    # print("{} without a lineage".format(funcName))
                    terms_without_lineage |= set([funcName])
            for UniProtID in UniProtID_list:
                fh_out_Prot_2_func.write(taxid + "\t" + UniProtID + "\t" + format_list_of_string_2_postgres_array(funcName_list_backtracked) + "\t" + etype + "\n")
    with open(fn_out_without_lineage, "w") as fh_out_without_lineage:
        for term in sorted(terms_without_lineage):
            fh_out_without_lineage.write(term + "\n")

def get_ENSP_2_UniProtID_dict(UniprotID_2_ENSPs_2_KEGGs):
    """
    :param UniprotID_2_ENSPs_2_KEGGs: String (input file)
    :return: defaultdict (key: ENSP, val: list of UniProtIDs)
    """
    ENSP_2_UniProtID_dict = defaultdict(lambda: [])
    with open(UniprotID_2_ENSPs_2_KEGGs, "r") as fh_in:
        for line in fh_in:
            taxid, UniProtID, ENSP, KEGG = line.split("\t")
            if len(ENSP) > 0:
                for ENSP in ENSP.split(";"):
                    ENSP_2_UniProtID_dict[ENSP].append(UniProtID)
    return ENSP_2_UniProtID_dict

def Protein_2_Function_table_DOID_BTO_hard_cutoff(Protein_2_Function_and_Score_DOID_GO_BTO, Taxid_2_Proteins_table_STRING, score_cutoff, Protein_2_Function_table_DOID_BTO):
    """
    - remove anything on blacklist (all_hidden.tsv) already happend while creating Functions_table_DOID_BTO (and all terms not present therein will be filtered out)
    - omit GO-CC (etype -22)
    """
    ENSP_set = get_all_ENSPs(Taxid_2_Proteins_table_STRING)
    with open(Protein_2_Function_table_DOID_BTO, "w") as fh_out:
        for line in tools.yield_line_uncompressed_or_gz_file(Protein_2_Function_and_Score_DOID_GO_BTO):
            ENSP, funcName_2_score_arr_str, etype = line.split("\t")
            if ENSP not in ENSP_set: # debug
                continue
            if etype.strip() == "-22": # omit GO-CC (etype -22)
                continue
            else:
                funcs_list = []
                funcName_2_score_list = helper_convert_str_arr_2_nested_list(funcName_2_score_arr_str)
                for an_score in funcName_2_score_list:
                    an, score = an_score # functional_term, score
                    if score >= score_cutoff:
                        funcs_list.append(an)
                if len(funcs_list) == 0: # don't add empty results due to blacklisting or GO-CC terms
                    continue
                fh_out.write(ENSP + "\t" + format_list_of_string_2_postgres_array(funcs_list) + "\t" + etype)

def helper_convert_str_arr_2_nested_list(funcName_2_score_arr_str):
    """
    funcName_2_score_arr_str = '{{"GO:0005777",0.535714},{"GO:0005783",0.214286},{"GO:0016021",3}}'
    --> [['GO:0005777', 0.535714], ['GO:0005783', 0.214286], ['GO:0016021', 3.0]]
    """
    funcName_2_score_list = []
    funcName_2_score_arr_str = [ele[1:] for ele in funcName_2_score_arr_str.replace('"', '').replace("'", "").split("},")]
    if len(funcName_2_score_arr_str) == 1:
        fs = funcName_2_score_arr_str[0][1:-2].split(",")
        funcName_2_score_list.append([fs[0], float(fs[1])])
    else:
        funcName_2_score_list_temp = [funcName_2_score_arr_str[0][1:].split(",")] + [ele.split(",") for ele in funcName_2_score_arr_str[1:-1]] + [funcName_2_score_arr_str[-1][:-2].split(",")]
        for sublist in funcName_2_score_list_temp:
            funcName_2_score_list.append([sublist[0], float(sublist[1])])
    return funcName_2_score_list

def helper_grep_funcNames(funcName_2_score_arr_str):
    """
    funcName_2_score_arr_str = '{{"GO:0005777",0.535714},{"GO:0005783",0.214286},{"GO:0016021",3}}'
    --> ['GO:0005777', 'GO:0005783', 'GO:0016021']
    """
    funcName_2_score_arr_str = [ele[1:] for ele in funcName_2_score_arr_str.replace('"', '').replace("'", "").split("},")]
    if len(funcName_2_score_arr_str) == 1:
        funcName_2_score_list = [funcName_2_score_arr_str[0][1:-2].split(",")[0]]
    else:
        funcName_2_score_list = [funcName_2_score_arr_str[0][1:].split(",")[0]] + [ele.split(",")[0] for ele in funcName_2_score_arr_str[1:-1]] + [funcName_2_score_arr_str[-1][:-2].split(",")[0]]
    return funcName_2_score_list

def Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC(Taxid_2_Proteins_table, Functions_table_STRING, Protein_2_FuncEnum_and_Score_DOID_BTO_GOCC, Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC, number_of_processes=1, verbose=True):
    """
    Protein_2_FuncEnum_and_Score_DOID_BTO_GOCC.txt
    10116.ENSRNOP00000049139  {{{0,2.927737},{3,2.403304},{4,3},{666,3}, ... ,{3000000,0.375}}
    ENSP to functionEnumeration and its respective score
    scores >= 3 --> presence
    scores < 3 --> absence
    multiple ENSPs per taxid --> scores get summed up per Taxid

    Taxid_2_FunctionCountArray_table_BTO_DOID.txt
    9606  19566  {{{0,3},{3,2},{4,3},{666,3}, ... ,{3000000,1}}

    """
    if verbose:
        print("creating Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC")
    # sort table to get group ENSPs of same Taxid
    tools.sort_file(Protein_2_FuncEnum_and_Score_DOID_BTO_GOCC, Protein_2_FuncEnum_and_Score_DOID_BTO_GOCC, number_of_processes=number_of_processes, verbose=verbose)
    # get dict
    taxid_2_total_protein_count_dict = _helper_get_taxid_2_total_protein_count_dict(Taxid_2_Proteins_table)
    num_lines = tools.line_numbers(Functions_table_STRING)
    # reduce to relevant ENSPs
    ENSP_set = get_all_ENSPs(Taxid_2_Proteins_table)

    with open(Protein_2_FuncEnum_and_Score_DOID_BTO_GOCC, "r") as fh_in:
        with open(Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC, "w") as fh_out:
            line = next(fh_in)
            fh_in.seek(0)
            taxid_last, ENSP_last, funcEnum_2_count_list_last = helper_parse_line_protein_2_functionEnum_and_score(line)
            funcEnum_count_background = np.zeros(shape=num_lines, dtype=np.dtype("float64"))
            funcEnum_count_background = helper_count_funcEnum_floats(funcEnum_count_background, funcEnum_2_count_list_last)
            for line in fh_in:
                taxid, ENSP, funcEnum_2_count_list = helper_parse_line_protein_2_functionEnum_and_score(line)
                if ENSP not in ENSP_set:
                    continue
                if taxid == taxid_last:
                    # add to existing arr
                    funcEnum_count_background = helper_count_funcEnum_floats(funcEnum_count_background, funcEnum_2_count_list)
                else:
                    # write to file
                    background_count = taxid_2_total_protein_count_dict[taxid_last]
                    funcEnum_2_count_arr = helper_format_funcEnum(funcEnum_count_background)
                    fh_out.write(taxid_last + "\t" + background_count + "\t" + funcEnum_2_count_arr + "\n")
                    # regenerate arr
                    funcEnum_count_background = np.zeros(shape=num_lines, dtype=np.dtype("float64"))
                    funcEnum_count_background = helper_count_funcEnum_floats(funcEnum_count_background, funcEnum_2_count_list)
                # current becomes last
                taxid_last = taxid

            background_count = taxid_2_total_protein_count_dict[taxid_last]
            funcEnum_2_count_arr = helper_format_funcEnum(funcEnum_count_background)
            fh_out.write(taxid_last + "\t" + background_count + "\t" + funcEnum_2_count_arr + "\n")
    if verbose:
        print("done with Taxid_2_FunctionCountArray_table_BTO_DOID")

def helper_parse_line_protein_2_functionEnum_and_score(line):
    """
    10090.ENSMUSP00000000001        {{26719,1.484633},{26722,1.948048},{26744,1.866082},{26747,2.382463},{26749,1.838262},{26761,1.597329},{26773,1.749074},{26781,1.597329},{26783,0.208875},{26784,2.294204},{26785,1.79201},{26786,2.358938},{26787,0.208875},{26790,1.904616},{26791,1.972038},{26797,1.813061},{26799,1.869913},{26840,2.344152},{26843,1.265298},{26844,1.544971},{26845,1.265298},{26847,1.068671},{26851,1.265298},{26856,0.632311},{26865,1.648461},{26868,1.547682},{26876,1.696821},{26883,1.349304},{26912,1.069535},{26927,0.667956},{26950,2.113912},{26953,0.833023},{26960,1.068671},{26961,1.597329},{26966,0.730319},{26974,1.696821},{26977,0.685772},{26978,1.307823},{26997,1.265298},{27001,1.307823},{27007,1.402294},{27020,2.215},{27026,1.866082},{27032,2.215},{27036,2.163989},{27044,2.05538},{27052,1.734702},{27061,2.382463},{27083,1.022137},{27089,1.069535},{27112,1.959711},{27115,1.959711},{27116,1.527146},{27130,2.113408},{27131,1.544971},{27132,1.544971},{27147,1.85957},{27153,1.696211},{27164,1.092252},{27171,2.382463},{27174,0.743434},{27176,1.769245},{27177,1.325972},{27179,1.681244},{27189,2.647931},{27190,1.79841},{27196,2.382463},{27198,2.05538},{27225,1.972038},{27234,2.321567},{27243,1.704611},{27266,0.825288},{27271,1.869913},{27283,1.597329},{27295,1.09578},{27298,1.263053},{27310,2.031935},{27326,1.263053},{27328,2.215},{27332,1.83149},{27336,1.808592},{27346,1.643376},{27350,1.890247},{27373,2.294204},{27389,1.052408},{27408,1.09578},{27409,1.544971},{27412,0.814002},{27417,2.053422},{27423,1.749074},{27427,0.993573},{27428,1.09578},{27442,1.402294},{27454,2.382463},{27477,1.286511},{27479,0.50214},{27494,1.276615},{27527,2.113912},{27535,1.402294},{27545,1.866082},{27547,2.05538},{27560,1.856561},{27562,1.068671},{27564,1.349304},{27601,1.052408},{27607,1.263053},{27613,2.382463},{27618,0.420739},{27637,0.908134},{27641,1.796064},{27657,1.704611},{27658,0.825288},{27669,2.263856},{27687,2.313626},{27699,0.51079},{27709,2.041018},{27734,0.569971},{27765,2.294204},{27783,1.547682},{27795,0.581894},{27877,0.5868},{27918,1.343355},{27938,0.221769},{27972,1.155432},{27991,0.825288},{28136,2.05538},{28141,2.294204},{28184,1.481154},{28341,0.519311},{28431,1.841047},{28567,1.946206},{28600,1.866082},{28602,1.481154},{28650,2.105637},{28674,0.704542},{29233,1.838262},{29319,1.052408},{29341,1.484633},{29370,1.150767},{29371,0.757662},{29569,0.91183},{29577,1.02504},{29785,2.041018},{29786,2.041018},{29828,1.863492},{29910,1.349304},{29921,1.824307},{30316,0.979101},{30380,2.105637},{30396,0.793137},{30458,1.6611},{30495,2.043764},{30496,2.043764},{30528,1.068671},{30550,2.05538},{30557,1.827531},{30559,2.513419},{30907,0.992954},{31101,1.853277},{31474,2.794547}}
    """
    # funcEnum_2_count_list = literal_eval(funcEnum_2_count_arr.strip().replace("{", "[").replace("}", "]"))
    funcEnum_2_count_list = []
    ENSP, funcEnum_2_count_arr = line.split("\t")
    funcEnum_2_count_arr = [ele[1:] for ele in funcEnum_2_count_arr.strip().split("},")]
    if len(funcEnum_2_count_arr) == 1:
        fs = funcEnum_2_count_arr[0][1:-2].split(",")
        funcEnum_2_count_list.append([int(fs[0]), float(fs[1])])
    else:
        funcName_2_score_list_temp = [funcEnum_2_count_arr[0][1:].split(",")] + [ele.split(",") for ele in funcEnum_2_count_arr[1:-1]] + [funcEnum_2_count_arr[-1][:-2].split(",")]
        for sublist in funcName_2_score_list_temp:
            funcEnum_2_count_list.append([int(sublist[0]), float(sublist[1])])
    taxid = ENSP.split(".")[0]
    return taxid, ENSP, funcEnum_2_count_list

def helper_count_funcEnum_floats(funcEnum_count_background, funcEnum_2_count_list):
    for funcEnum_count in funcEnum_2_count_list:
        funcEnum, count = funcEnum_count
        funcEnum_count_background[funcEnum] += count
    return funcEnum_count_background

def Protein_2_Function__and__Functions_table_WikiPathways(fn_in_WikiPathways_organisms_metadata, fn_in_EntrezGeneID_2_UniProtID, fn_in_WikiPathways_not_a_gmt_file, fn_out_Functions_table_WikiPathways, fn_out_Protein_2_Function_table_WikiPathways, verbose=True): # fn_in_STRING_EntrezGeneID_2_STRING, fn_in_Taxid_2_Proteins_table_STS
    """
    changed to output only UniProtID not AC (AN)
    removed/commented out ENSP output

    link http://data.wikipathways.org
    use gmt = Gene Matrix Transposed, lists of datanodes per pathway, unified to Entrez Gene identifiers.
    map Entrez Gene IDs to UniProt using ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/idmapping/idmapping_selected.tab.gz
    """
    if verbose:
        print("creating Functions_table_WikiPathways and Protein_2_Function_table_WikiPathways")
    df_wiki_meta = pd.read_csv(fn_in_WikiPathways_organisms_metadata, sep="\t")
    df_wiki_meta["Genus species"] = df_wiki_meta["Genus species"].apply(lambda s: "_".join(s.split(" ")))
    TaxName_2_Taxid_dict = pd.Series(df_wiki_meta["Taxid"].values, index=df_wiki_meta["Genus species"]).to_dict()
    year, level = "-1", "-1"
    etype = str(variables.functionType_2_entityType_dict["WikiPathways"])
    EntrezGeneID_2_UniProtID_dict = get_EntrezGeneID_2_UniProtID_dict_from_UniProtIDmapping(fn_in_EntrezGeneID_2_UniProtID) # previously fn_in_UniProt_ID_mapping
    WikiPathways_dir = os.path.dirname(fn_in_WikiPathways_not_a_gmt_file)
    fn_list = [os.path.join(WikiPathways_dir, fn) for fn in os.listdir(WikiPathways_dir) if fn.endswith(".gmt")]
    already_written = []
    with open(fn_out_Functions_table_WikiPathways, "w") as fh_out_functions:  # etype | an | description | year | level
        with open(fn_out_Protein_2_Function_table_WikiPathways, "w") as fh_out_protein_2_function:  # an | func_array | etype
            for fn_wiki in fn_list:
                taxname = fn_wiki.split("-gmt-")[-1].replace(".gmt", "")
                try:
                    taxid = TaxName_2_Taxid_dict[taxname]  # taxid is an integer
                except KeyError:
                    print("WikiPathways, couldn't translate TaxName from file: {}".format(fn_wiki))
                    continue
                # EntrezGeneID_2_UniProtID_dict = get_EntrezGeneID_2_UniProtID_dict(df_UniProt_ID_mapping, taxid)
                with open(fn_wiki, "r") as fh_in: # remove dupliates
                    # remember pathway to proteins mapping --> then translate to ENSP to func_array
                    WikiPathwayID_2_EntrezGeneIDList_dict = {}
                    for line in fh_in:  # DNA Replication%WikiPathways_20190310%WP1223%Anopheles gambiae	http://www.wikipathways.org/instance/WP1223_r68760	1275918	1275917	1282031	3290537	1276035	1280711	1281887
                        pathwayName_version_pathwayID_TaxName, url_, *entrez_ids = line.strip().split("\t")  # 'DNA Replication', 'WikiPathways_20190310', 'WP1223', 'Anopheles gambiae', ['1275918', ... ]
                        pathwayName, version, pathwayID, TaxName = pathwayName_version_pathwayID_TaxName.split("%")
                        description = pathwayName
                        an = pathwayID
                        WikiPathwayID_2_EntrezGeneIDList_dict[pathwayID] = entrez_ids
                        line_2_write = etype + "\t" + an + "\t" + description + "\t" + year + "\t" + level + "\n"
                        if line_2_write not in already_written:
                            fh_out_functions.write(line_2_write) # check for uniqueness of names/ IDs later
                            already_written.append(line_2_write)

                    # map to UniProt and to STRING, single pathway to multiple entrez_ids translate to ENSP/UniProtAN to multiple pathways
                    # ENSP_2_wiki_dict, UniProt_2_wiki_dict = {}, {}
                    UniProt_2_wiki_dict = {}
                    for WikiPathwayID, EntrezGeneID_list in WikiPathwayID_2_EntrezGeneIDList_dict.items():
                        for EntrezGeneID in EntrezGeneID_list:
                            try:
                                UniProtID_list = EntrezGeneID_2_UniProtID_dict[EntrezGeneID]
                            except KeyError:
                                UniProtID_list = []
                            for UniProtID in UniProtID_list:
                                if UniProtID not in UniProt_2_wiki_dict:
                                    UniProt_2_wiki_dict[UniProtID] = [WikiPathwayID]
                                else:
                                    UniProt_2_wiki_dict[UniProtID].append(WikiPathwayID)
                            # try:
                            #     ENSP_list = EntrezGeneID_2_ENSPsList_dict[EntrezGeneID]
                            # except KeyError:
                            #     ENSP_list = []
                            # for ENSP in [ENSP for ENSP in ENSP_list if ENSP in ENSP_set]: # reduce to relevant ENSPs
                            #     if ENSP not in ENSP_2_wiki_dict:
                            #         ENSP_2_wiki_dict[ENSP] = [WikiPathwayID]
                            #     else:
                            #         ENSP_2_wiki_dict[ENSP].append(WikiPathwayID)
                    # for ENSP, wiki_list in ENSP_2_wiki_dict.items():
                    #     an = ENSP
                    #     func_array = format_list_of_string_2_postgres_array(list(set(wiki_list)))
                    #     fh_out_protein_2_function.write(an + "\t" + func_array + "\t" + etype + "\n")
                    for UniProtID, wiki_list in UniProt_2_wiki_dict.items():
                        ID = UniProtID
                        func_array = format_list_of_string_2_postgres_array(list(set(wiki_list)))
                        fh_out_protein_2_function.write(str(taxid) + "\t" + ID + "\t" + func_array + "\t" + etype + "\n")

def get_EntrezGeneID_2_ENSPsList_dict(fn):
    """
    EntrezGeneID
    e.g.
    102619773|102628203
    --> multiple EntrezGeneIDs map to single UniProtAN
    and single EntrezGeneID maps to multiple UniProtAN
    e.g.
    103484309	3656.XP_008439609.1
    103484309	3656.XP_008439546.1
    """
    # fn = r"/Users/dblyon/modules/cpr/agotool/data/PostgreSQL/downloads/STRING_v11_all_organisms_entrez_2_string_2018.tsv.gz"
    df_entrez_2_string = pd.read_csv(fn, sep="\t", names=["Taxid", "EntrezGeneID", "ENSP"], skiprows=1)
    EntrezGeneID_2_ENSPsList_dict = {}
    for row in df_entrez_2_string.itertuples():
        _, _, EntrezGeneIDs, ENSP = row
        for EntrezGeneID in EntrezGeneIDs.split("|"):
            if EntrezGeneID not in EntrezGeneID_2_ENSPsList_dict:
                EntrezGeneID_2_ENSPsList_dict[EntrezGeneID] = [ENSP]
            else:
                EntrezGeneID_2_ENSPsList_dict[EntrezGeneID].append(ENSP)
    return EntrezGeneID_2_ENSPsList_dict

def compile_run_cythonized():
    cmd = "python setup.py build_ext --inplace -f"
    compile_cy = subprocess.Popen(cmd, shell=True)
    compile_cy.wait()

def Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN(Protein_2_FunctionEnum_and_Score_table, Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN):
    """
    Lars TextMining data has e.g. 4932 but UniProt has 559292 as a reference proteome --> translate via variables.py
    since UniProt ref prot for 4932 doesn't exist but does exist for 559292
    4932 Saccharomyces cerevisiae, Jensenlab
    559292 Saccharomyces cerevisiae S288C, UniProt Reference Proteome
    4896 Schizosaccharomyces pombe, JensenlabTaxid_2_FunctionEnum_2_Scores_table_UPS_FIN
    4932 --> 559292
    284812 Schizosaccharomyces pombe 972h-, UniProt Reference Proteome
    4896 --> 284812
    """
    # compile_run_cythonized()
    # from importlib import reload
    # reload(run_cythonized)
    ENSP_2_tuple_funcEnum_score_dict = query.get_proteinAN_2_tuple_funcEnum_score_dict(read_from_flat_files=True, fn=Protein_2_FunctionEnum_and_Score_table)
    with open(Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN, "w") as fh_out:
        for taxid in variables.jensenlab_supported_taxids:
            if taxid in variables.jensenlab_supported_taxids_species_translations_dict:
                taxid = variables.jensenlab_supported_taxids_species_translations_dict[taxid]
            background_ENSPs = query.get_proteins_of_taxid(taxid, read_from_flat_files=variables.READ_FROM_FLAT_FILES)
            if background_ENSPs is None or len(background_ENSPs) == 0:
                print("Taxid_2_funcEnum_2_scores_table_FIN taxid {} without background_ENPSs".format(taxid))
            funcEnum_2_scores_dict_bg = collect_scores_per_term(background_ENSPs, ENSP_2_tuple_funcEnum_score_dict)
            for funcEnum in sorted(funcEnum_2_scores_dict_bg.keys()):
                scores = sorted(funcEnum_2_scores_dict_bg[funcEnum])
                fh_out.write(str(taxid) + "\t" + str(funcEnum) + "\t{" + ",".join([str(ele) for ele in scores]) + "}\n")

def collect_scores_per_term(protein_AN_list, ENSP_2_tuple_funcEnum_score_dict, list_2_array=False):
    """
    ENSP_2_tuple_funcEnum_score_dict['3702.AT1G01010.1']
    (array([ 211,  252,  253], dtype=uint32),
     array([4200000, 4166357, 4195121], dtype=uint32))
    funcEnum_2_scores_dict: key: functionEnumeration, val: list of scores
    """
    funcEnum_2_scores_dict = defaultdict(lambda: [])
    for protein_AN in protein_AN_list:
        try:
            funcEnum_score = ENSP_2_tuple_funcEnum_score_dict[protein_AN]
        except KeyError:
            continue
        funcEnum_arr, score_arr = funcEnum_score
        len_funcEnum_arr = len(funcEnum_arr)
        for index_ in range(len_funcEnum_arr):
            score = score_arr[index_]
            funcEnum_2_scores_dict[funcEnum_arr[index_]].append(score)
    if list_2_array:
        return {funcEnum: np.asarray(scores, dtype=np.dtype(variables.dtype_TM_score)) for funcEnum, scores in funcEnum_2_scores_dict.items()} # float64 --> uint32
    # since concatenating np.arrays later on (for filling with zeros) produces 64 bit array anyway
    else:
        return funcEnum_2_scores_dict

def Functions_table_UPS_FIN(Functions_table_all, Function_2_Protein_table_UPS_reduced, Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS, Functions_table_UPS_FIN, Functions_table_UPS_removed):
    """
    Functions_table_all is the superset
    Function_2_Protein_table_UPS_reduced use all these prefiltered functions
    Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS parse and use all functions since not in above table
    Functions_table_UPS_FIN reduced subset
    Functions_table_UPS_removed removed subset
    """
    functions_2_include = set()
    with open(Function_2_Protein_table_UPS_reduced, "r") as fh_in:
    # 1000565 -51     KW-0003 5       3926    {"1000565.METUNv1_01117","1000565.METUNv1_02206","1000565.METUNv1_02527","1000565.METUNv1_03205","1000565.METUNv1_03227"}
    # 654924  -51     KW-1185 7       -1      014R_FRG3G;015R_FRG3G;017L_FRG3G;018L_FRG3G;019R_FRG3G;020R_FRG3G;021L_FRG3G
        for line in fh_in:
            functions_2_include.update({line.split("\t")[2]})

    with open(Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS, "r") as fh_in:
        for line in fh_in:
            taxid, uniprotid, etype, function_name_set = _helper_parse_line_prot_2_func_UPS(line)
            functions_2_include.update(function_name_set)

    enum = 0
    # prevent redundant entries
    funcNames_already_written = set()
    with open(Functions_table_all, "r") as fh_in: # table already sorted
        # | etype | an | description | year | level |
        # | enum | etype | an | description | year | level |
        with open(Functions_table_UPS_FIN, "w") as fh_out_reduced:
            with open(Functions_table_UPS_removed, "w") as fh_out_removed:
                for line in fh_in:
                    funcName = line.split("\t")[1]
                    if funcName in funcNames_already_written:
                        fh_out_removed.write(line.strip() + "\tredundant\n")
                        continue
                    if funcName in functions_2_include or funcName.startswith("GOCC:"):
                        fh_out_reduced.write(str(enum) + "\t" + line)
                        funcNames_already_written.update({funcName})
                        enum += 1
                    else:
                        fh_out_removed.write(line)

def Protein_2_Function_table_PMID_UPS(fn_in_Protein_2_Function_table_PMID_STS, fn_in_Taxid_2_UniProtID_2_ENSPs_2_KEGGs, fn_out_ENSP_2_UniProtID_without_translation, fn_out_Protein_2_Function_table_PMID_UPS):
    # 287.DR97_1450   {"PMID:28118378","PMID:26729493","PMID:17493134","PMID:16956383"}       -56
    ENSP_2_UniProtID_dict = get_ENSP_2_UniProtID_dict(fn_in_Taxid_2_UniProtID_2_ENSPs_2_KEGGs)
    with open(fn_in_Protein_2_Function_table_PMID_STS, "r") as fh_in:
        with open(fn_out_Protein_2_Function_table_PMID_UPS, "w") as fh_out:
            with open(fn_out_ENSP_2_UniProtID_without_translation, "w") as fh_out_no_translation:
                for line in fh_in:
                    ENSP, PMID_etype_newline = line.split("\t", 1)
                    taxid = ENSP.split(".")[0]
                    UniProtID_list = ENSP_2_UniProtID_dict[ENSP]
                    if len(UniProtID_list) > 0:
                        for UniProtID in UniProtID_list:
                            fh_out.write(taxid + "\t" + UniProtID + "\t" + PMID_etype_newline.strip() + "\n")
                    else:
                        fh_out_no_translation.write(ENSP + "\n")

def ENSP_2_UniProtID_without_translation(fn_in_list, protein_shorthands, ENSP_2_UniProtID_without_translation):
    """
    capture all ENSPs without translation to a UniProt ID that are part of protein_shorthands
    """
    ENSP_set = set()
    with open(protein_shorthands, "r") as fh_in:
        for line in fh_in:
            ENSP = line.split()[0]
            ENSP_set |= {ENSP}

    for fn in fn_in_list:
        with open(fn, "r") as fh_in:
            with open(ENSP_2_UniProtID_without_translation, "w") as fh_out:
                for line in fh_in:
                    ENSP = line.strip()
                    if ENSP in ENSP_set:
                        fh_out.write(ENSP + "\n")

def ENSP_2_UniProt_all(damian_uniprot_2_string, UniProt_ID_mapping, fn_out_ENSP_2_UniProt_all, fn_out_Taxid_UniProtID_2_ENSPs_2_KEGGs, fn_out_Taxid_UniProt_AC_2_ID, fn_out_EntrezGeneID_2_UniProtID, number_of_processes=1):
    """
    output:
    999630.TUZN_2237        F2L675  F2L675_THEU7    STRING
    999630.TUZN_2237        F2L675  F2L675_THEU7    UniProtIDmapping
    999630.TUZN_2237        nm      F2L675_THEU7    UniProtDump

    jensenlab_supported_taxids = [9606, 10090, 10116, 3702, 7227, 6239, 4932, 4896] #559292, 284812]
    4932 Saccharomyces cerevisiae, Jensenlab
    559292 Saccharomyces cerevisiae S288C, UniProt Reference Proteome
    4932 --> 559292
    4896 Schizosaccharomyces pombe, Jensenlab
    284812 Schizosaccharomyces pombe 972h-, UniProt Reference Proteome
    4896 --> 284812
    force 559292 to be 4932
    and 284812 to be 4896
    in order to merge annotation data from Jensenlab with UniProt data and make everything accessible/searchable on tax-rank of species

    $ grep "HIS4_YEAST" Taxid_UniProt_AC_2_ID.txt
    559292  P40545  HIS4_YEAST

    $ grep "HIS4_YEAST" Taxid_UniProtID_2_ENSPs_2_KEGGs.txt
    559292  HIS4_YEAST      4932.YIL020C    sce:YIL020C
    """
    # EntrezGeneID_2_UniProtID_dict = get_EntrezGeneID_2_UniProtID_dict_from_UniProtIDmapping(fn_in_UniProt_ID_mapping)
    EntrezGeneID_2_UniProtID_dict = {}
    with open(fn_out_Taxid_UniProt_AC_2_ID, "w") as fh_out_Taxid_UniProt_AC_2_ID:
        with open(fn_out_Taxid_UniProtID_2_ENSPs_2_KEGGs, "w") as fh_out_Taxid_UniProtID_2_ENSPs_2_KEGGs:
            with open(fn_out_ENSP_2_UniProt_all, "w") as fh_out_ENSP_2_UniProtID_all:
                source = "UniProtIDmapping"
                for UniProtAC, UniProtID, ENSP_list, taxid, KEGG_list, EntrezGeneID_list in _helper_yield_UniProtIDmapping_entry(UniProt_ID_mapping): # source is UniProt ID mapping
                    for geneid in EntrezGeneID_list:
                        if geneid in EntrezGeneID_2_UniProtID_dict:
                            EntrezGeneID_2_UniProtID_dict[geneid].append(UniProtID)
                        else:
                            EntrezGeneID_2_UniProtID_dict[geneid] = [UniProtID]

                    for ENSP in ENSP_list:
                        fh_out_ENSP_2_UniProtID_all.write(ENSP + "\t" + UniProtAC + "\t" + UniProtID + "\t" + source + "\n")
                    if taxid in {"559292", "284812"}:
                        if taxid == "559292":
                            taxid = "4932"
                        elif taxid == "284812":
                            taxid = "4896"
                    fh_out_Taxid_UniProtID_2_ENSPs_2_KEGGs.write("{}\t{}\t{}\t{}\n".format(taxid, UniProtID, ";".join(ENSP_list), ";".join(KEGG_list)))
                    if taxid == "-1" or UniProtID == "-1":
                        pass
                    else:
                        fh_out_Taxid_UniProt_AC_2_ID.write(taxid + "\t" + UniProtAC + "\t" + UniProtID + "\n")

                source = "STRING"
                with open(damian_uniprot_2_string, "r") as fh_in:
                    _header = fh_in.readline()
                    for line in fh_in:
                        taxid, UniProtAC_UniProtID, ENSP, identity, bit_score = line.split("\t")
                        UniProtAC, UniProtID = UniProtAC_UniProtID.split("|")
                        fh_out_ENSP_2_UniProtID_all.write(ENSP + "\t" + UniProtAC + "\t" + UniProtID + "\t" + source + "\n")

    # sort on ENSP and UniProtAC
    tools.sort_file(fn_out_ENSP_2_UniProt_all, fn_out_ENSP_2_UniProt_all, number_of_processes=number_of_processes)

    # write EntrezGeneID_2_UniProtID_dict as flat file
    with open(fn_out_EntrezGeneID_2_UniProtID, "w") as fh_out:
        for EntrezGeneID in sorted(EntrezGeneID_2_UniProtID_dict.keys()):
            UniProtID_list = EntrezGeneID_2_UniProtID_dict[EntrezGeneID]
            fh_out.write(EntrezGeneID + "\t" + ";".join(sorted(set(UniProtID_list))) + "\n")

def _helper_yield_UniProtIDmapping_entry(UniProt_IDmapping):
    """
    P70403  UniProtKB-ID    CASP_MOUSE
    P70403  Gene_Name       Cux1
    P70403  Gene_Synonym    Cutl1
    P70403  GI      32484289
    P70403  GI      1546825
    P70403  GI      85720588
    P70403  GI      81861638
    P70403  GI      15679964
    P70403  UniRef100       UniRef100_P70403
    P70403  UniRef90        UniRef90_P70403
    P70403  UniRef50        UniRef50_P70403
    P53564-3        UniParc UPI00005B2E7C
    P53564-1        UniParc UPI00005B2E22
    P53564-5        UniParc UPI000016D0E8
    P53564-2        UniParc UPI00005B2E7B
    P53564-4        UniParc UPI00005B2E7D
    P70403-1        UniParc UPI000066880C
    P70403  UniParc UPI000066880C
    P70403  EMBL    U68542
    P70403  EMBL    BC014289
    P70403  EMBL    BC054370
    P70403  EMBL-CDS        AAB08430.1
    P70403  EMBL-CDS        AAH14289.1
    P70403  EMBL-CDS        AAH54370.1
    P70403  NCBI_TaxID      10090
    P70403-1        CCDS    CCDS71685.1
    P70403  STRING  10090.ENSMUSP00000004097
    P70403  MGI     MGI:88568
    P70403  eggNOG  KOG0963
    P70403  eggNOG  KOG2252
    P70403  eggNOG  ENOG410XPRP
    P70403  ChiTaRS Cux1
    P70403  CRC64   C04905EE48CC2D37
    """
    AC_2_ID_dict, AC_2_taxid_dict = {}, {}
    for entry in _helper_yield_entry_UniProtIDmapping(UniProt_IDmapping):
        UniProtAC, taxid, ENSP_list, KEGG_list, EntrezGeneID_list = "-1", "-1", [], [], [] # UniProtID,
        for line in entry:  # all mappings for one UniProtAC
            UniProtAC, type_, mapping = line.split("\t")
            UniProtAC = UniProtAC.split("-")[0]
            mapping = mapping.strip()
            if type_ == "UniProtKB-ID":
                UniProtID = mapping
                if UniProtAC not in AC_2_ID_dict:
                    AC_2_ID_dict[UniProtAC] = UniProtID
            elif type_ == "NCBI_TaxID":
                taxid = mapping
                if taxid not in AC_2_taxid_dict:
                    AC_2_taxid_dict[UniProtAC] = taxid
            elif type_ == "STRING":
                ENSP_list.append(mapping)
            elif type_ == "KEGG":
                KEGG_list.append(mapping)
            elif type_ == "GeneID":
                EntrezGeneID_list.append(mapping)
            try:
                UniProtID = AC_2_ID_dict[UniProtAC]
            except KeyError:
                UniProtID = "-1"
            try:
                taxid = AC_2_taxid_dict[UniProtAC]
            except KeyError:
                taxid = "-1"
        yield UniProtAC, UniProtID, ENSP_list, taxid, KEGG_list, EntrezGeneID_list

def get_EntrezGeneID_2_UniProtID_dict_from_UniProtIDmapping_old(fn_in_UniProt_ID_mapping):
    EntrezGeneID_2_UniProtID_dict = {}
    for entry in _helper_yield_UniProtIDmapping_entry(fn_in_UniProt_ID_mapping):
        UniProtAC, UniProtID, ENSP_list, taxid, KEGG_list, EntrezGeneID_list = entry
        for geneid in EntrezGeneID_list:
            if geneid in EntrezGeneID_2_UniProtID_dict:
                EntrezGeneID_2_UniProtID_dict[geneid].append(UniProtID)
            else:
                EntrezGeneID_2_UniProtID_dict[geneid] = [UniProtID]
    return EntrezGeneID_2_UniProtID_dict

def get_EntrezGeneID_2_UniProtID_dict_from_UniProtIDmapping(EntrezGeneID_2_UniProtID):
    EntrezGeneID_2_UniProtID_dict = {}
    with open(EntrezGeneID_2_UniProtID, "r") as fh:
        for line in fh:
            EntrezGeneID, UniProtID_list = line.split("\t")
            EntrezGeneID_2_UniProtID_dict[EntrezGeneID] = UniProtID_list.strip().split(";")
    return EntrezGeneID_2_UniProtID_dict

def _helper_yield_entry_UniProtIDmapping(UniProt_IDmapping):
    lines_2_return = []
    gen = tools.yield_line_uncompressed_or_gz_file(UniProt_IDmapping)
    line = next(gen)
    UniProtAC_last = line.split("\t")[0].split("-")[0]
    lines_2_return.append(line)
    for line in gen:
        UniProtAC = line.split("\t")[0].split("-")[0]
        if UniProtAC != UniProtAC_last:
            yield lines_2_return
            lines_2_return = []
        lines_2_return.append(line)
        UniProtAC_last = UniProtAC
    yield lines_2_return

def STRING_2_UniProt_mapping_discrepancies(ENSP_2_UniProt_all, Taxid_2_Proteins_table_STS, Protein_2_FunctionEnum_table_UPS_FIN, fn_out_ENSP_2_UniProt_2_use, fn_out_ENSPs_of_UniProtIDmapping_not_in_STRINGv11, fn_out_ENSP_2_UniProt_discrepancy):
    """
    ### create file for Damian of discrepancies
    # - ENSPs not in STRING_v11 any more (need be removed or updated in UniProt) --> fn_out_ENSP_in_UniProt_deprecated.txt
    # - if ENSP maps to different AC (not ID since these change) --> fn_out_ENSP_2_UniProt_discrepancy.txt

    ### create file for aGOtool UniProt version
    # - restrict to ENSP in STRING_v11
    # - restrict to UniProtID with annotations
    # - in case of ENSP mapping to multiple UniProt AC or discrepancy between Damian and Uniprot choose Damian mapping (since 1 to 1 mapping)

    999630.TUZN_2237        F2L675  F2L675_THEU7    STRING
    999630.TUZN_2237        F2L675  F2L675_THEU7    UniProtIDmapping
    999630.TUZN_2237        nm      F2L675_THEU7    UniProtDump
    """
    # ENSPs_of_STRING_v11 = set()
    # with open(Taxid_2_Proteins_table_STS, "r") as fh_in:
    #     for line in fh_in:
    #         _taxid, ENSP_arr, _count = line.split("\t")
    #         ENSPs_of_STRING_v11 |= set(ENSP_arr[1:-1].replace('"', "").split(","))
    # df = pd.read_csv(ENSP_2_UniProt_all, sep="\t", names=["ENSP", "UniProtAC", "UniProtID", "source"])
    # cond_UPID = df["source"] == "UniProtIDmapping"
    # ENSP_UPIDmapping = set(df.loc[cond_UPID, "ENSP"].unique())
    # ENSPs_of_UniProtIDmapping_not_in_STRINGv11 = ENSP_UPIDmapping - ENSPs_of_STRING_v11
    # df_ENSPs_of_UniProtIDmapping_not_in_STRINGv11 = df[df["ENSP"].isin(ENSPs_of_UniProtIDmapping_not_in_STRINGv11)]
    # df_ENSPs_of_UniProtIDmapping_not_in_STRINGv11.to_csv(fn_out_ENSPs_of_UniProtIDmapping_not_in_STRINGv11, sep="\t", header=False, index=False)
    # # most cases due to one to many mapping of ENSP UniprotAC. ?check if Damian mapping among them?
    # is_equal = df.groupby("ENSP").apply(_helper_compare_mapping_is_equal)
    # ENSPs_unequal = is_equal[~is_equal].reset_index()["ENSP"].tolist() # select those that are unequal, grep ENSPs
    # df_ENSPs_unequal = df[df["ENSP"].isin(ENSPs_unequal)]
    # # add a column to mark ENSPs that have a one to one mapping from Damian,
    # # if that mapping also exists within UniProt
    # is_one_2_one = df_ENSPs_unequal.groupby("ENSP").apply(_helper_is_one_2_one_Damian)
    # ENSPs_with_one_2_one_mapping = is_one_2_one[is_one_2_one].reset_index()["ENSP"].tolist()
    # cond = df_ENSPs_unequal["ENSP"].isin(ENSPs_with_one_2_one_mapping)
    # df_ENSPs_unequal["1_to_1"] = False
    # df_ENSPs_unequal.loc[cond, "1_to_1"] = True
    # df_ENSPs_unequal.to_csv(fn_out_ENSP_2_UniProt_discrepancy, sep="\t", header=False, index=False)
    # cond_ENSPs_of_STRING_v11 = df["ENSP"].isin(ENSPs_of_STRING_v11)
    # UniProtID_with_annotation = get_all_UniProtIDs_with_annotations(Protein_2_FunctionEnum_table_UPS_FIN)
    # cond_UniProtID_with_annotation = df["UniProtID"].isin(UniProtID_with_annotation)
    # # part1 are equal mappings, reduce redundancy and mark equal
    # df_ENSP_2_UniProt_2_use_part1 = df.loc[(cond_ENSPs_of_STRING_v11 & cond_UniProtID_with_annotation & is_equal), ["ENSP", "UniProtAC", "UniProtID"]].drop_duplicates()
    # df_ENSP_2_UniProt_2_use_part1["source"] = "equal"
    # # part2 chose Damian mapping
    # cond_ENSP_2_UniProt_2_use_part2_damian = cond_ENSPs_of_STRING_v11 & cond_UniProtID_with_annotation & ~is_equal
    # df_ENSP_2_UniProt_2_use_part2 = df[cond_ENSP_2_UniProt_2_use_part2_damian]
    # dfm = pd.concat([df_ENSP_2_UniProt_2_use_part1, df_ENSP_2_UniProt_2_use_part2], ignore_index=True)
    # dfm.to_csv(fn_out_ENSP_2_UniProt_2_use, sep="\t", header=False, index=False)
    ENSPs_of_STRING_v11 = set()
    with open(Taxid_2_Proteins_table_STS, "r") as fh_in:
        for line in fh_in:
            _taxid, ENSP_arr, _count = line.split("\t")
            ENSPs_of_STRING_v11 |= set(ENSP_arr[1:-1].replace('"', "").split(","))

    df = pd.read_csv(ENSP_2_UniProt_all, sep="\t", names=["ENSP", "UniProtAC", "UniProtID", "source"])
    cond_UPID = df["source"] == "UniProtIDmapping"
    ENSP_UPIDmapping = set(df.loc[cond_UPID, "ENSP"].unique())
    ENSPs_of_UniProtIDmapping_not_in_STRINGv11 = ENSP_UPIDmapping - ENSPs_of_STRING_v11
    df_ENSPs_of_UniProtIDmapping_not_in_STRINGv11 = df[df["ENSP"].isin(ENSPs_of_UniProtIDmapping_not_in_STRINGv11)]
    df_ENSPs_of_UniProtIDmapping_not_in_STRINGv11.to_csv(fn_out_ENSPs_of_UniProtIDmapping_not_in_STRINGv11, sep="\t", header=False, index=False)
    # true for most cases due to one to many mapping of ENSP UniprotAC.
    is_equal = df.groupby("ENSP").apply(_helper_compare_mapping_is_equal)
    ENSPs_unequal = is_equal[~is_equal].reset_index()["ENSP"].tolist()  # select those that are unequal, grep ENSPs
    df_ENSPs_unequal = df[df["ENSP"].isin(ENSPs_unequal)]
    # add a column to mark ENSPs that have a one to one mapping from Damian,
    # if that mapping also exists within UniProt
    is_one_2_one = df_ENSPs_unequal.groupby("ENSP").apply(_helper_is_one_2_one_Damian)
    ENSPs_with_one_2_one_mapping = is_one_2_one[is_one_2_one].reset_index()["ENSP"].tolist()
    cond = df_ENSPs_unequal["ENSP"].isin(ENSPs_with_one_2_one_mapping)
    df_ENSPs_unequal["1_to_1"] = False
    df_ENSPs_unequal.loc[cond, "1_to_1"] = True
    df_ENSPs_unequal.to_csv(fn_out_ENSP_2_UniProt_discrepancy, sep="\t", header=False, index=False)
    cond_ENSPs_of_STRING_v11 = df["ENSP"].isin(ENSPs_of_STRING_v11)
    UniProtID_with_annotation = get_all_UniProtIDs_with_annotations(Protein_2_FunctionEnum_table_UPS_FIN)
    cond_UniProtID_with_annotation = df["UniProtID"].isin(UniProtID_with_annotation)
    # part1 are equal mappings, reduce redundancy and mark equal, select if
    # - ENSPs in STRING v11
    # - UniProtID with functional annnotation
    # - UniProtAC to ENSP mapping identical between STRING and UniProt mappings
    ENSPs_equal = is_equal[is_equal].reset_index()["ENSP"].tolist()  # select those that are equal, grep ENSPs
    cond_ENSPs_equal = df["ENSP"].isin(ENSPs_equal)
    df_ENSP_2_UniProt_2_use_part1 = df.loc[(cond_ENSPs_of_STRING_v11 & cond_UniProtID_with_annotation & cond_ENSPs_equal), ["ENSP", "UniProtAC", "UniProtID"]].drop_duplicates()
    df_ENSP_2_UniProt_2_use_part1["source"] = "equal"
    # part2 chose Damian mapping if exists otherwise chose UniProt mapping
    # only select one mapping per ENSP to UniProtAC
    dfx = df[cond_ENSPs_of_STRING_v11 & cond_UniProtID_with_annotation & ~cond_ENSPs_equal]
    indices_2_keep = []
    for name, group in dfx.groupby("ENSP"):
        try:  # try if there is a STRING mapping (only 1 to 1 mappings from STRING)
            index_ = group[group["source"] == "STRING"].index.values[0]
        except IndexError:  # or pick the first UniProt mapping
            index_ = group.index.values[0]
        indices_2_keep.append(index_)
    dfm = pd.concat([df_ENSP_2_UniProt_2_use_part1, df.loc[indices_2_keep]])
    dfm.to_csv(fn_out_ENSP_2_UniProt_2_use, sep="\t", header=False, index=False)

def _helper_is_one_2_one_Damian(group):
    UniProtAC_Damian = group.loc[group["source"] == "STRING", "UniProtAC"].values
    if UniProtAC_Damian.size == 0:
        return False
    else:
        UniProtAC_Damian = UniProtAC_Damian[0]  # should only ever be one, if any at all
    UniProtAC_UP_arr = group.loc[group["source"] == "UniProtIDmapping", "UniProtAC"].values
    if len(UniProtAC_UP_arr) > 1 and UniProtAC_Damian in UniProtAC_UP_arr:
        return True
    else:
        return False

def _helper_compare_mapping_is_equal(group):
    # if UniProt Accessions are equal return True
    if len(set(group["UniProtAC"])) > 1:
        return False
    else:
        return True

def Secondary_2_Primary_ID_UPS_FIN(Protein_2_FunctionEnum_table_UPS_FIN, UniProt_sec_2_prim_AC, ENSP_2_UniProt_2_use, Taxid_UniProt_AC_2_ID, fn_out_Secondary_2_Primary_ID_UPS_FIN, fn_out_Secondary_2_Primary_ID_UPS_no_translation):
    """
    desired output:
    taxid, ENSP, UniProtID
    taxid, UniProtAC, UniProtID
    """
    ac_2_id_dict = {}
    ac_2_taxid_dict = {}
    gen_AC_2_AC = _helper_yield_UniProt_sec_2_prim_AC(UniProt_sec_2_prim_AC)
    gen_AC_2_ID = _helper_yield_gen_AC_2_ID(Taxid_UniProt_AC_2_ID)
    UniProtID_with_annotations = get_all_UniProtIDs_with_annotations(Protein_2_FunctionEnum_table_UPS_FIN)
    with open(fn_out_Secondary_2_Primary_ID_UPS_FIN, "w") as fh_out:
        with open(fn_out_Secondary_2_Primary_ID_UPS_no_translation, "w") as fh_out_no_translation:

            for taxid, ac, id_ in gen_AC_2_ID:
                if id_ in UniProtID_with_annotations:
                    fh_out.write(taxid + "\t" + ac + "\t" + id_ + "\n")  # UniProt AC 2 ID --> AC_2_ID
                ac_2_id_dict[ac] = id_
                ac_2_taxid_dict[ac] = taxid

            for secondary, primary in gen_AC_2_AC: # from secondary AC to primary AC --> secondary AC to ID
                try:
                    id_ = ac_2_id_dict[primary]
                    taxid = ac_2_taxid_dict[primary]
                except KeyError:
                    fh_out_no_translation.write(primary + "\n")
                    continue
                if id_ in UniProtID_with_annotations:
                    fh_out.write(taxid + "\t" + secondary + "\t" + id_ + "\n")  # UniProt AC 2 ID --> AC_2_ID

            with open(ENSP_2_UniProt_2_use, "r") as fh_in:
                for line in fh_in:
                    ENSP, uniprotac, uniprotid, source = line.split("\t")
                    taxid = ENSP.split(".")[0]
                    fh_out.write(taxid + "\t" + ENSP + "\t" + uniprotid + "\n")  # ENSP 2 UniProtID

    tools.sort_file(fn_out_Secondary_2_Primary_ID_UPS_FIN, fn_out_Secondary_2_Primary_ID_UPS_FIN, number_of_processes=NUMBER_OF_PROCESSES_sorting, verbose=True)

def _helper_yield_UniProt_sec_2_prim_AC(fn):
    line_generator = tools.yield_line_uncompressed_or_gz_file(fn)
    line = next(line_generator)
    while not line.startswith("Secondary AC"):
        line = next(line_generator)
        continue
    _ = next(line_generator)
    for line in line_generator:
        secondary, primary = line.strip().split()
        yield secondary, primary

def _helper_yield_Taxid_UniProtID_2_ENSPs_2_KEGGs(fn):
    with open(fn, "r") as fh:
        for line in fh:
            taxid, UniProtID, ENSPs, KEGGs = line.split("\t")
            ENSP_list = ENSPs.split(";")
            if ENSP_list[0]:  # test for empty string
                yield taxid, ENSP_list, UniProtID

def _helper_yield_gen_AC_2_ID(fn):
    with open(fn, "r") as fh:
        for line in fh:
            taxid, UniProtAC, UniProtID = line.split("\t")
            yield taxid, UniProtAC, UniProtID.strip()

# def create_goslimtype_2_cond_arrays(Functions_table_placeholder_for_execution_order, download_GO_slim_subsets_placeholder_for_execution_order):
def create_goslimtype_2_cond_arrays(Functions_table_placeholder_for_execution_order, GO_slim_subsets_file):
    """
    read obo files
    parse all terms and add to dict (key: obo file name, val: list of GO terms)
    translate GOterm function names to bool array
    """
    # year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr = query.get_lookup_arrays(read_from_flat_files=variables.READ_FROM_FLAT_FILES)
    year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr = query.get_lookup_arrays(read_from_flat_files=True)
    #GO_slim_subsets_file = variables.tables_dict["goslim_subsets_file"]
    files = []
    with open(GO_slim_subsets_file, "r") as fh_in:
        for line in fh_in:
            fn_basename = line.strip()
            fn_absolute = os.path.join(DOWNLOADS_DIR, fn_basename)
            files.append([fn_basename, fn_absolute])
            # go_dag = obo_parser.GODag(obo_file=fn_absolute)
            # list_of_go_terms = list(set([go_term_name for go_term_name in go_dag]))
            # np.save(os.path.join(TABLES_DIR, fn_basename.replace(".obo", ".npy")), np.isin(functionalterm_arr, list_of_go_terms))
    for file_base_absolute in files:
        fn_basename, fn_absolute = file_base_absolute
        go_dag = obo_parser.GODag(obo_file=fn_absolute)
        list_of_go_terms = list(set([go_term_name for go_term_name in go_dag]))
        np.save(os.path.join(TABLES_DIR, fn_basename.replace(".obo", ".npy")), np.isin(functionalterm_arr, list_of_go_terms))

def SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN(Protein_2_FunctionEnum_and_Score_table_UPS_FIN, CSC_ENSPencoding_2_FuncEnum_UPS_FIN, ENSP_2_rowIndex_dict_UPS_FIN, rowIndex_2_ENSP_dict_UPS_FIN, verbose=True):
    """
    Protein_2_FunctionEnum_and_Score_table_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["Protein_2_FunctionEnum_and_Score_table"]
    CSC_ENSPencoding_2_FuncEnum_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["CSC_ENSPencoding_2_FuncEnum"]
    ENSP_2_rowIndex_dict_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["ENSP_2_rowIndex_dict"]
    rowIndex_2_ENSP_dict_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["rowIndex_2_ENSP_dict"]
    SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN(Protein_2_FunctionEnum_and_Score_table_UPS_FIN, CSC_ENSPencoding_2_FuncEnum_UPS_FIN, ENSP_2_rowIndex_dict_UPS_FIN, rowIndex_2_ENSP_dict_UPS_FIN, verbose=True)
    1.) sparse matrix for all ENSPs
    2.) slice first matrix to get user matrix
    column index --> function enumeration
    row index --> ENSP (UniProtID) encoding
    values are Scores
    matrix: row_num = number of ENSPs; col_num = funcEnum (exact translation)
    """
    # get proteinAN to functionEnumeration and Score arrays
    assert os.path.exists(Protein_2_FunctionEnum_and_Score_table_UPS_FIN)
    ENSP_2_tuple_funcEnum_score_dict = query.get_proteinAN_2_tuple_funcEnum_score_dict(read_from_flat_files=True, fn=None)
    ENSP_2_rowIndex_dict, rowIndex_2_ENSP_dict = {}, {}
    for rowIndex, ENSP in enumerate(sorted(ENSP_2_tuple_funcEnum_score_dict.keys())):
        ENSP_2_rowIndex_dict[ENSP] = rowIndex
        rowIndex_2_ENSP_dict[rowIndex] = ENSP

    # get cond arrays to know maximum length of KS_funcEnum for matrix size
    # _, _, entitytype_arr, functionalterm_arr, indices_arr = query.get_lookup_arrays(low_memory=True, read_from_flat_files=True)
    year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr = query.get_lookup_arrays(read_from_flat_files=True)
    etype_2_minmax_funcEnum = query.PersistentQueryObject_STRING.get_etype_2_minmax_funcEnum(entitytype_arr)
    function_enumeration_len = functionalterm_arr.shape[0]
    etype_cond_dict = query.get_etype_cond_dict(etype_2_minmax_funcEnum, function_enumeration_len)
    cond_KS_etypes = etype_cond_dict["cond_25"] | etype_cond_dict["cond_26"] | etype_cond_dict["cond_20"]
    KS_funcEnums_arr = indices_arr[cond_KS_etypes]

    matrix = sparse.lil_matrix((len(ENSP_2_tuple_funcEnum_score_dict), max(KS_funcEnums_arr) + 1), dtype=np.dtype(variables.dtype_TM_score))
    for ensp in sorted(ENSP_2_tuple_funcEnum_score_dict.keys()):
        rowIndex = ENSP_2_rowIndex_dict[ensp]
        funcEnum_arr, score_arr = ENSP_2_tuple_funcEnum_score_dict[ensp]
        matrix[rowIndex, funcEnum_arr] = score_arr
    matrix = matrix.tocsc()
    if verbose:
        print("Producing Sparse Matrix CSC_ENSPencoding_2_FuncEnum_UPS_FIN and ENSP_2_rowIndex_dict")
        print("Memory usage of (in bytes): ", matrix.data.nbytes + matrix.indptr.nbytes + matrix.indices.nbytes)

    pickle.dump(ENSP_2_rowIndex_dict, open(ENSP_2_rowIndex_dict_UPS_FIN, "wb"))
    pickle.dump(rowIndex_2_ENSP_dict, open(rowIndex_2_ENSP_dict_UPS_FIN, "wb"))
    sparse.save_npz(CSC_ENSPencoding_2_FuncEnum_UPS_FIN, matrix)

def Pickle_taxid_2_tuple_funcEnum_index_2_associations_counts(Taxid_2_FunctionCountArray_table_UPS_FIN, taxid_2_tuple_funcEnum_index_2_associations_counts_pickle_UPS_FIN):
    """
    Taxid_2_FunctionCountArray_table_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["Taxid_2_FunctionCountArray_table"]
    taxid_2_tuple_funcEnum_index_2_associations_counts_pickle_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["taxid_2_tuple_funcEnum_index_2_associations_counts"]
    Pickle_taxid_2_tuple_funcEnum_index_2_associations_counts(Taxid_2_FunctionCountArray_table_UPS_FIN, taxid_2_tuple_funcEnum_index_2_associations_counts_pickle_UPS_FIN)
    """
    assert os.path.exists(Taxid_2_FunctionCountArray_table_UPS_FIN)
    taxid_2_tuple_funcEnum_index_2_associations_counts = query.get_background_taxid_2_funcEnum_index_2_associations(read_from_flat_files=True)
    pickle.dump(taxid_2_tuple_funcEnum_index_2_associations_counts, open(taxid_2_tuple_funcEnum_index_2_associations_counts_pickle_UPS_FIN, "wb"))

def Pickle_lookup_arrays_UPS_FIN(Functions_table_UPS_FIN, *args):
    """
    additional args passed is only for Snakemake
    """
    assert os.path.exists(Functions_table_UPS_FIN)
    # year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr = query.get_lookup_arrays(read_from_flat_files=True)
    year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr = query.get_lookup_arrays(read_from_flat_files=True)
    arr_list = [year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr]
    name_list = ["year_arr", "hierlevel_arr", "entitytype_arr", "functionalterm_arr", "indices_arr", "description_arr", "category_arr"]
    for index_ in range(len(arr_list)):
        arr_name = name_list[index_]
        arr = arr_list[index_]
        with open(variables.tables_dict[arr_name], "wb") as fh_out:
            pickle.dump(arr, fh_out)

def Pickle_Taxid_2_FunctionEnum_2_Scores_dict(Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN, Taxid_2_FunctionEnum_2_Scores_dict_UPS_FIN):
    """
    import create_SQL_tables_snakemake as cst
    reload(variables)
    Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["Taxid_2_FunctionEnum_2_Scores_table"]
    Taxid_2_FunctionEnum_2_Scores_dict_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["Taxid_2_FunctionEnum_2_Scores_dict"]
    Taxid_2_FuncEnum_2_Score_2_Rank_dict_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["Taxid_2_FuncEnum_2_Score_2_Rank_dict"]
    Taxid_2_FuncEnum_2_medianScore_dict_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["Taxid_2_FuncEnum_2_medianScore_dict"]
    Taxid_2_FuncEnum_2_numBGvals_dict_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["Taxid_2_FuncEnum_2_numBGvals_dict"]
    cst.Pickle_Taxid_2_FunctionEnum_2_Scores_dict(Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN, Taxid_2_FunctionEnum_2_Scores_dict_UPS_FIN, Taxid_2_FuncEnum_2_Score_2_Rank_dict_UPS_FIN, Taxid_2_FuncEnum_2_medianScore_dict_UPS_FIN, Taxid_2_FuncEnum_2_numBGvals_dict_UPS_FIN)
    """
    assert os.path.exists(Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN)
    Taxid_2_FunctionEnum_2_Scores_dict = query.get_Taxid_2_FunctionEnum_2_Scores_dict(read_from_flat_files=True, as_array_or_as_list="array", taxid_2_proteome_count=None)
    pickle.dump(Taxid_2_FunctionEnum_2_Scores_dict, open(Taxid_2_FunctionEnum_2_Scores_dict_UPS_FIN, "wb"))

def add_2_DF_file_dimensions_log():
    """
    read old log and add number of lines of flat files and bytes of data for binary files to log,
    write to disk
    :return: None
    """
    # read old table and add data to it
    LOG_DF_FILE_DIMENSIONS = variables.LOG_DF_FILE_DIMENSIONS
    df_old = pd.read_csv(LOG_DF_FILE_DIMENSIONS, sep="\t")

    fn_list, binary_list, size_list, num_lines_list, date_list = [], [], [], [], []
    for fn in sorted(os.listdir(TABLES_DIR)):
        fn_abs_path = os.path.join(TABLES_DIR, fn)
        if fn.endswith("UPS_FIN.txt"):
            binary_list.append(False)
            num_lines_list.append(tools.line_numbers(fn_abs_path))
        elif fn.endswith("UPS_FIN.p") or fn.endswith("UPS_FIN.npz") or fn.endswith(".npy"):
            binary_list.append(True)
            num_lines_list.append(np.nan)
        else:
            continue
        fn_list.append(fn)
        size_list.append(os.path.getsize(fn_abs_path))
        timestamp = tools.creation_date(fn_abs_path)
        date_list.append(datetime.datetime.fromtimestamp(timestamp))

    df = pd.DataFrame()
    df["fn"] = fn_list
    df["binary"] = binary_list
    df["size"] = size_list
    df["num_lines"] = num_lines_list
    df["date"] = date_list
    df["version"] = max(df_old["version"]) + 1
    df = pd.concat([df_old, df])

    df.to_csv(LOG_DF_FILE_DIMENSIONS, sep="\t", header=True, index=False)

def create_speciesTaxid_2_proteomeTaxid_dict(Taxid_2_Proteins_table_UPS_FIN, TaxidSpecies_2_TaxidProteome_dict_p, TaxidSpecies_2_multipleRefProtTaxid_dict_p, update_NCBI=True):
    """
    Taxid_2_Proteins_table_UPS_FIN = variables.TABLES_DICT_SNAKEMAKE["Taxid_2_Proteins_table"]
    TaxidSpecies_2_TaxidProteome_dict_p = variables.TABLES_DICT_SNAKEMAKE["TaxidSpecies_2_TaxidProteome_dict"]
    TaxidSpecies_2_multipleRefProtTaxid_dict_p = TABLES_DICT_SNAKEMAKE["TaxidSpecies_2_multipleRefProtTaxid_dict"]
    create_speciesTaxid_2_proteomeTaxid_dict(Taxid_2_Proteins_table_UPS_FIN, TaxidSpecies_2_TaxidProteome_dict_p, TaxidSpecies_2_TaxidProteome_dict_json)
    """
    ncbi = taxonomy.NCBI_taxonomy(taxdump_directory=variables.DOWNLOADS_DIR, for_SQL=False, update=update_NCBI)
    taxid_proteome_list = []  # exist as UniProt Ref Prots
    with open(Taxid_2_Proteins_table_UPS_FIN, "r") as fh:
        for line in fh:
            taxid_proteome_list.append(int(line.split()[0].strip()))
    taxid_proteome_list = sorted(taxid_proteome_list)

    speciesTaxid_2_proteomeTaxid_dict = {}
    speciesTaxid_2_multipleRefProtTaxid_dict = defaultdict(lambda: set())
    for taxid in taxid_proteome_list:
        rank = ncbi.get_rank(taxid)
        if rank == "species":  # nothing needs to be done
            continue
        else:
            taxid_mapped = ncbi.get_genus_or_higher(taxid, "species")
            rank = ncbi.get_rank(taxid_mapped)
            if rank != "species":
                print(taxid, taxid_mapped, rank)
            else:
                if not taxid_mapped in speciesTaxid_2_proteomeTaxid_dict:
                    speciesTaxid_2_proteomeTaxid_dict[taxid_mapped] = taxid
                else:
                    # print("speciesTaxid_2_proteomeTaxid_dict with double assignment {} and {} both map to {}".format(speciesTaxid_2_proteomeTaxid_dict[taxid_mapped], taxid_mapped, taxid))
                    speciesTaxid_2_multipleRefProtTaxid_dict[taxid_mapped].update((taxid, ))
                    speciesTaxid_2_multipleRefProtTaxid_dict[taxid_mapped].update((speciesTaxid_2_proteomeTaxid_dict[taxid_mapped], ))
                    speciesTaxid_2_proteomeTaxid_dict.pop(taxid_mapped, None)

    pickle.dump(speciesTaxid_2_proteomeTaxid_dict, open(TaxidSpecies_2_TaxidProteome_dict_p, "wb"))
    pickle.dump(dict(speciesTaxid_2_multipleRefProtTaxid_dict), open(TaxidSpecies_2_multipleRefProtTaxid_dict_p, "wb"))
    # with open(TaxidSpecies_2_TaxidProteome_dict_json, "w") as fh_json:
    #     fh_json.write(json.dumps(speciesTaxid_2_proteomeTaxid_dict))
    #
    return speciesTaxid_2_proteomeTaxid_dict, speciesTaxid_2_multipleRefProtTaxid_dict



##### Taxonomy mapping explanation, for UniProt version
# Taxid_2_Proteins_table_UPS_FIN remains as is, which is UniProt space and their TaxIDs (which are partially on strain level).
# Protein_2_Function_table_UPS has mixed mapping from UniProt ID to Taxid. --> Protein_2_Function_table_UPS_orig.txt and Protein_2_Function_table_UPS.txt.
# Protein_2_FunctionEnum_table_UPS_FIN is on species rank.
# --> Protein_2_FunctionEnum_table_UPS_FIN_for_Taxid_count: is filtered by UniProt ID subset from UniProt reference proteomes, and taxid changed to match UniProt reference proteomes (from species to strain level, since mapping exists from Taxid_2_Proteins_table_UPS_FIN).
# Taxid_2_FunctionCountArray_table_UPS_FIN is on UniProt ref prot level, since only needed for enrichment_method "genome".

if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
    import variables

    # Protein_2_Function_table_UPS_orig_fn = os.path.join(TABLES_DIR, "Protein_2_Function_table_UPS_orig.txt")  # original unmodified version
    # Protein_2_Function_table_UPS_fn = os.path.join(TABLES_DIR, "Protein_2_Function_table_UPS.txt")  # taxids pushed to rank species
    # Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS = os.path.join(TABLES_DIR, "Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS.txt")
    # Taxid_2_Proteins_table_UPS_FIN = variables.tables_dict["Taxid_2_Proteins_table"]
    # Functions_table_all = os.path.join(TABLES_DIR, "Functions_table_all.txt")
    # fn_Functions_table_UPS_FIN = variables.tables_dict["Functions_table"]  # Functions_table_UPS_reduced = os.path.join(TABLES_DIR, "Functions_table_UPS_reduced.txt") # synonymous ?replace?
    # Function_2_Protein_table_UPS_fn = os.path.join(TABLES_DIR, "Function_2_Protein_table_UPS.txt")
    # Function_2_Protein_table_UPS_reduced = os.path.join(TABLES_DIR, "Function_2_Protein_table_UPS_reduced.txt")
    # Function_2_Protein_table_UPS_removed = os.path.join(TABLES_DIR, "Function_2_Protein_table_UPS_removed.txt")
    # Functions_table_UPS_removed = os.path.join(TABLES_DIR, "Functions_table_UPS_removed.txt")
    # Protein_2_Function_table_UniProtDump_UPS = os.path.join(TABLES_DIR, "Protein_2_Function_table_UniProtDump_UPS.txt")
    # Protein_2_Function_table_KEGG_UPS = os.path.join(TABLES_DIR, "Protein_2_Function_table_KEGG_UPS.txt")
    # Protein_2_Function_table_WikiPathways_UPS = os.path.join(TABLES_DIR, "Protein_2_Function_table_WikiPathways_UPS.txt")
    # Protein_2_Function_table_PMID_UPS = os.path.join(TABLES_DIR, "Protein_2_Function_table_PMID_UPS.txt")  # 177.656 lines and 5.305.811 unique PMIDs
    # fn_list = [Protein_2_Function_table_UniProtDump_UPS,
    #                    Protein_2_Function_table_KEGG_UPS,
    #                    Protein_2_Function_table_WikiPathways_UPS,
    #                    Protein_2_Function_table_PMID_UPS]
    # UniProt_background_proteomes_dir = os.path.join(DOWNLOADS_DIR, "UniProt_background_prots")
    # fn_Functions_table = variables.tables_dict["Functions_table"]
    # fn_in_Protein_2_function_table = os.path.join(TABLES_DIR, "Protein_2_Function_table_UPS.txt")
    # fn_out_Protein_2_functionEnum_table_FIN = os.path.join(TABLES_DIR, "Protein_2_FunctionEnum_table_UPS_FIN.txt") #rename  Protein_2_FunctionEnum_table_UPS_FIN_v2.txt #variables.tables_dict["Protein_2_FunctionEnum_table"]
    # fn_out_Protein_2_FunctionEnum_table_UPS_removed = os.path.join(TABLES_DIR, "Protein_2_FunctionEnum_table_UPS_removed.txt")
    # Protein_2_FunctionEnum_table_UPS_FIN = variables.tables_dict["Protein_2_FunctionEnum_table"]
    # Functions_table_UPS_FIN = variables.tables_dict["Functions_table"] #Functions_table_UPS_reduced = os.path.join(TABLES_DIR, "Functions_table_UPS_reduced.txt") # synonymous ?replace?
    # Taxid_2_FunctionCountArray_table_UPS_FIN = variables.tables_dict["Taxid_2_FunctionCountArray_table"]
    # Protein_2_FunctionEnum_table_UPS_FIN_for_Taxid_count = os.path.join(TABLES_DIR, "Protein_2_FunctionEnum_table_UPS_FIN_for_Taxid_count.txt")

    # run single rule Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN
    Protein_2_FunctionEnum_and_Score_table_UPS_FIN = variables.tables_dict["Protein_2_FunctionEnum_and_Score_table"]
    Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN = os.path.join(TABLES_DIR, "Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN.txt")
    Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN(Protein_2_FunctionEnum_and_Score_table_UPS_FIN, Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN)

    # e.g. funcEnum = 69816 with lots of 500000 scores
        # {500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500057, 500070, 500102, 500125, 500190, 50027
    # % grep "^9606" Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN.txt | grep 75069 | cut -c1-150% grep "^9606" Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN.txt | grep 75069 | cut -c1-150