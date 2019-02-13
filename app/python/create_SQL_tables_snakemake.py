import os, sys, re
import gzip
import pandas as pd
import numpy as np
from collections import defaultdict
# sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
from ast import literal_eval
import obo_parser
import tools, ratio
import variables_snakemake as variables

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

def create_Protein_2_Function_table_InterPro(fn_in_string2interpro, fn_in_Functions_table_InterPro, fn_out_Protein_2_Function_table_InterPro, number_of_processes=1, verbose=True):
    """
    :param fn_in_string2interpro: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/string2interpro.dat.gz)
    :param fn_out_Protein_2_Function_table_InterPro: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/Protein_2_Function_table_InterPro.txt)
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

    df = pd.read_csv(fn_in_Functions_table_InterPro, sep='\t', names=["etype", "AN", "description", "year", "level"]) # names=["etype", "name", "AN", "description"])
    InterPro_AN_superset = set(df["AN"].values.tolist())
    if verbose:
        print("parsing previous result to produce Protein_2_Function_table_InterPro.txt")
    entityType_InterPro = variables.id_2_entityTypeNumber_dict["INTERPRO"]
    with open(fn_out_Protein_2_Function_table_InterPro, "w") as fh_out:
        for ENSP, InterProID_list in parse_string2interpro_yield_entry(fn_in_temp):
            InterProID_list = sorted({id_ for id_ in InterProID_list if id_ in InterPro_AN_superset})
            if len(InterProID_list) >= 1:
                fh_out.write(ENSP + "\t" + "{" + str(InterProID_list)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_InterPro + "\n")
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

    an = "GO:1904767"
    lineage_dict[an] --> {'GO:0031406', 'GO:0005488', 'GO:0036094', 'GO:0043168', 'GO:0008289', 'GO:0005504', 'GO:0033293', 'GO:0043167', 'GO:0003674', 'GO:0043177'}
    child_2_parent_dict[an] --> {'GO:0005504'}
    """
    all_lineages = []
    parents_2_remove = set()
    direct_parents = get_direct_parents(child, child_2_parent_dict)
    while True:
        if len(direct_parents - parents_2_remove) == 0: # {'GO:0005504'} - {} --> {'GO:0005504'} != 0 # 2.iteration {'GO:0005504'} - {"GO:1904767", "GO:0005504", 'GO:0008289', 'GO:0005488', 'GO:0003674'} --> {}
            return all_lineages
        else:
            parent = list(direct_parents - parents_2_remove)[0]  # 'GO:0005504'
            lineage = [child, parent] + get_random_direct_lineage(parent, child_2_parent_dict, lineage=[]) # ["GO:1904767", "GO:0005504"] +  ['GO:0008289', 'GO:0005488', 'GO:0003674']
            all_lineages.append(lineage)
            parents_2_remove.update(set(lineage)) # {"GO:1904767", "GO:0005504", 'GO:0008289', 'GO:0005488', 'GO:0003674'}
            direct_parents.update(get_direct_parents(parent, child_2_parent_dict))

def get_direct_parents(child, child_2_parent_dict):
    try:
        # copy is necessary since child_2_parent_dict is otherwise modified by updating direct_parents in get_all_lineages
        direct_parents = child_2_parent_dict[child].copy()
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
    term_2_level_dict = defaultdict(lambda: 1)
    for child in child_2_parent_dict.keys():
        lineages = get_all_lineages(child, child_2_parent_dict)
        max_lineage = 1
        for lineage in lineages:
            len_lineage = len(lineage)
            if len_lineage > max_lineage:
                max_lineage = len_lineage
        term_2_level_dict[child] = max_lineage
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
    # sort on first two columns in order to get all functional associations for a given ENSP in one block
    tools.sort_file(fn_associations, fn_associations, number_of_processes=number_of_processes, verbose=variables.VERBOSE)
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

def create_Functions_table_SMART(fn_in, fn_out_functions_table_SMART, max_len_description, fn_out_map_name_2_an_SMART):
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

def create_Functions_table_PFAM(fn_in, fn_out_functions_table_PFAM, fn_out_map_name_2_an):
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

def Protein_2_Function_table_map_function_2_function_enumeration(fn_Functions_table_STRING, fn_in_Protein_2_function_table_STRING, fn_out_Protein_2_functionEnum_table_STRING, number_of_processes=1):
    function_2_enum_dict, enum_2_function_dict = get_function_an_2_enum__and__enum_2_function_an_dict_from_flat_file(fn_Functions_table_STRING)
    tools.sort_file(fn_in_Protein_2_function_table_STRING, fn_in_Protein_2_function_table_STRING, number_of_processes=number_of_processes)
    with open(fn_in_Protein_2_function_table_STRING, "r") as fh_in:
        with open(fn_out_Protein_2_functionEnum_table_STRING, "w") as fh_out:
            ENSP_last, function_arr_str, etype = fh_in.readline().strip().split("\t")
            function_arr = literal_eval(function_arr_str)
            functionEnum_list = _helper_format_array(function_arr, function_2_enum_dict)

            for line in fh_in:
                ENSP, function_arr_str, etype = line.strip().split("\t")
                function_arr = literal_eval(function_arr_str)

                if ENSP == ENSP_last:
                    functionEnum_list += _helper_format_array(function_arr, function_2_enum_dict)
                else:
                    if len(functionEnum_list) > 0:
                        fh_out.write(ENSP_last + "\t" + format_list_of_string_2_postgres_array(sorted(functionEnum_list)) + "\n") # etype is removed
                    functionEnum_list = _helper_format_array(function_arr, function_2_enum_dict)

                ENSP_last = ENSP
            fh_out.write(ENSP_last + "\t" + format_list_of_string_2_postgres_array(sorted(functionEnum_list)) + "\n")  # etype is removed

def _helper_format_array(function_arr, function_2_enum_dict):
    functionEnum_list = []
    for ele in function_arr:
        try:
            functionEnum_list.append(function_2_enum_dict[ele])
        except KeyError: # e.g. blacklisted terms
            # print("no translation for: {}".format(ele))
            return []
    return [int(ele) for ele in functionEnum_list]

def create_Lineage_table_STRING(fn_in_go_basic, fn_in_keywords, fn_in_rctm_hierarchy, fn_in_functions, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab, fn_out_lineage_table, fn_out_no_translation):
    lineage_dict = get_lineage_dict_for_all_entity_types_with_ontologies(fn_in_go_basic, fn_in_keywords, fn_in_rctm_hierarchy, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab)
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
    with open(fn_out_no_translation, "w") as fh_out_no_trans:
        for term in term_no_translation_because_obsolete:
            fh_out_no_trans.write(term + "\n")

def get_lineage_dict_for_all_entity_types_with_ontologies(fn_go_basic_obo, fn_keywords_obo, fn_rctm_hierarchy, fn_in_DOID_obo_Jensenlab, fn_in_BTO_obo_Jensenlab):
    lineage_dict = {}
    go_dag = obo_parser.GODag(obo_file=fn_go_basic_obo)
    upk_dag = obo_parser.GODag(obo_file=fn_keywords_obo, upk=True)
    # key=GO-term, val=set of GO-terms (parents)
    for go_term_name in go_dag:
        GOTerm_instance = go_dag[go_term_name]
        lineage_dict[go_term_name] = GOTerm_instance.get_all_parents() # .union(GOTerm_instance.get_all_children()) # wrong #!!!
    for term_name in upk_dag:
        Term_instance = upk_dag[term_name]
        lineage_dict[term_name] = Term_instance.get_all_parents() # .union(Term_instance.get_all_children())

    bto_dag = obo_parser.GODag(obo_file=fn_in_BTO_obo_Jensenlab)
    for term_name in bto_dag:
        Term_instance = bto_dag[term_name]
        lineage_dict[term_name ] = Term_instance.get_all_parents()
    doid_dag = obo_parser.GODag(obo_file=fn_in_DOID_obo_Jensenlab)
    for term_name in doid_dag:
        Term_instance = doid_dag[term_name]
        lineage_dict[term_name ] = Term_instance.get_all_parents()

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

def create_Taxid_2_FunctionCountArray_table_STRING(Protein_2_FunctionEnum_table_STRING, Functions_table_STRING, TaxID_2_Proteins_table, fn_out_Taxid_2_FunctionCountArray_table_STRING, number_of_processes=1, verbose=True):
    # - sort Protein_2_FunctionEnum_table_STRING.txt
    # - create array of zeros of function_enumeration_length
    # - for line in Protein_2_FunctionEnum_table_STRING
    #     add counts to array until taxid_new != taxid_previous
    print("create_Taxid_2_FunctionCountArray_table_STRING")
    tools.sort_file(Protein_2_FunctionEnum_table_STRING, Protein_2_FunctionEnum_table_STRING, number_of_processes=number_of_processes, verbose=verbose)
    taxid_2_total_protein_count_dict = _helper_get_taxid_2_total_protein_count_dict(TaxID_2_Proteins_table)
    num_lines = tools.line_numbers(Functions_table_STRING)
    with open(fn_out_Taxid_2_FunctionCountArray_table_STRING, "w") as fh_out:
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
                    funcEnum_count_background = np.zeros(shape=num_lines, dtype=np.dtype("uint32"))

                funcEnum_count_background = helper_count_funcEnum(funcEnum_count_background, funcEnum_set)
                taxid_previous = taxid
            index_backgroundCount_array_string = helper_format_funcEnum(funcEnum_count_background)
            background_n = taxid_2_total_protein_count_dict[taxid]
            fh_out.write(taxid + "\t" + background_n + "\t" + index_backgroundCount_array_string + "\n")
    print("Taxid_2_FunctionCountArray_table_STRING done :)")

def helper_parse_line_Protein_2_FunctionEnum_table_STRING(line):
    ENSP, funcEnum_set = line.split("\t")
    funcEnum_set = {int(num) for num in literal_eval(funcEnum_set.strip())}
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
        string_2_write += "{{{0},{1}}},".format(ele[0], round(ele[1]))
    index_backgroundCount_array_string = "{" + string_2_write[:-1] + "}"
    return index_backgroundCount_array_string

def create_Protein_2_Function_table_KEGG(fn_in_kegg_benchmarking, fn_out_Protein_2_Function_table_KEGG, fn_out_KEGG_TaxID_2_acronym_table, number_of_processes=1):
    fn_out_temp = fn_out_Protein_2_Function_table_KEGG + "_temp"
    # create long format of ENSP 2 KEGG table
    taxid_2_acronym_dict = {}
    with open(fn_in_kegg_benchmarking, "r") as fh_in:
        with open(fn_out_temp, "w") as fh_out:
            for line in fh_in:
                TaxID, KEGG, num_ENSPs, *ENSPs = line.split()
                if KEGG.startswith("CONN_"):
                    continue
                else: # e.g. bced00190 or rhi00290
                    match = re.search("\d", KEGG)
                    if match:
                        index_ = match.start()
                        acro = KEGG[:index_]
                        taxid_2_acronym_dict[TaxID] = acro
                    KEGG = KEGG[-5:]
                # add TaxID to complete the ENSP
                ENSPs = [TaxID + "." + ENSP for ENSP in ENSPs]
                for ENSP in ENSPs:
                    fh_out.write(ENSP + "\t" + "map" + KEGG + "\n")
    with open(fn_out_KEGG_TaxID_2_acronym_table, "w") as fh_acro:
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

def create_Protein_2_Function_table_SMART_and_PFAM_temp(fn_in_dom_prot_full, fn_out_SMART_temp, fn_out_PFAM_temp, number_of_processes=1, verbose=True):
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

def map_Name_2_AN(fn_in, fn_out, fn_dict, fn_no_mapping):
    """
    SMART and PFAM Protein_2_Function_table(s) contain names from parsing the
    orig source, convert names to accessions
    :param fn_in: String (Protein_2_Function_table_temp_SMART.txt)
    :param fn_out: String (Protein_2_Function_table_SMART.txt)
    :param fn_dict: String (Functions_table_SMART.txt
    :param fn_no_mapping: String (missing mapping)
    :return: NONE
    """
    print("map_Name_2_AN for {}".format(fn_in))
    df = pd.read_csv(fn_dict, sep="\t", names=["name", "an"]) # names=["etype", "name", "an", "definition"])
    name_2_an_dict = pd.Series(df["an"].values, index=df["name"]).to_dict()
    df["name_v2"] = df["name"].apply(lambda x: x.replace("-", "_").lower())
    name_2_an_dict_v2 = pd.Series(df["an"].values, index=df["name_v2"]).to_dict()
    name_2_an_dict.update(name_2_an_dict_v2)
    name_no_mapping_list = []
    with open(fn_in, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            for line in fh_in:
                ENSP, name_array, etype_newline = line.split("\t")
                name_set = literal_eval(name_array)
                an_list = []
                for name in name_set:
                    try:
                        an_list.append(name_2_an_dict[name])
                    except KeyError:
                        # not in the lookup, therefore should be skipped since most likely obsolete in current version
                        name_no_mapping_list.append(name)
                if an_list: # not empty
                    fh_out.write(ENSP + "\t{" + str(sorted(an_list))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + etype_newline)
    with open(fn_no_mapping, "w") as fh_no_mapping:
        fh_no_mapping.write("\n".join(sorted(set(name_no_mapping_list))))

def create_Protein_2_Function_table_GO(fn_in_obo_file, fn_in_knowledge, fn_out_Protein_2_Function_table_GO, number_of_processes=1, verbose=True):
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
        TaxID, ENSP_without_TaxID, EntityType, GOterm, *rest = line.split()
        if not GOterm.startswith("GO:"):
            continue
        ENSP = TaxID + "." + ENSP_without_TaxID
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

def divide_into_categories(GOterm_list, GO_dag,
                           MFs=[], CPs=[], BPs=[], not_in_OBO=[]):
    """
    split a list of GO-terms into the 3 parent categories in the following order MFs, CPs, BPs
    'GO:0003674': "-23",  # 'Molecular Function',
    'GO:0005575': "-22",  # 'Cellular Component',
    'GO:0008150': "-21",  # 'Biological Process',
    :param GOterm_list: List of String
    :param GO_dag: Dict like object
    :return: Tuple (List of String x 3)
    """
#     MFs, CPs, BPs, not_in_OBO = [], [], [], []
    for term in GOterm_list:
        if term == "GO:0003674" or GO_dag[term].has_parent("GO:0003674"):
            MFs.append(GO_dag[term].id)
        elif term == "GO:0005575" or GO_dag[term].has_parent("GO:0005575"):
            CPs.append(GO_dag[term].id)
        elif term == "GO:0008150" or GO_dag[term].has_parent("GO:0008150"):
            BPs.append(GO_dag[term].id)
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

def create_Protein_2_Function_table_UniProtKeyword(fn_in_Functions_table_UPK, fn_in_obo, fn_in_uniprot_SwissProt_dat, fn_in_uniprot_TrEMBL_dat, fn_in_uniprot_2_string, fn_out_Protein_2_Function_table_UPK, number_of_processes=1,  verbose=True):
    if verbose:
        print("\ncreate_Protein_2_Function_table_UniProtKeywords")
    UPK_dag = obo_parser.GODag(obo_file=fn_in_obo, upk=True)
    UPK_Name_2_AN_dict = get_keyword_2_upkan_dict(fn_in_Functions_table_UPK)  # depends on create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK
    uniprot_2_string_missing_mapping = []
    uniprot_2_ENSPs_dict = parse_full_uniprot_2_string(fn_in_uniprot_2_string)
    entityType_UniProtKeywords = variables.id_2_entityTypeNumber_dict["UniProtKeywords"]
    UPKs_not_in_obo_list = []
    # import ipdb
    # ipdb.set_trace()
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
    # OX   NCBI_TaxID=583355 {ECO:0000313|EMBL:ADE54679.1, ECO:0000313|Proteomes:UP000000925};
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
            return None
    else:
        yield lines_list

def parse_textmining_entityID_2_proteinID(fn):
    df = pd.read_csv(fn, sep="\t", names=["textmining_id", "species_id", "protein_id"])# textmining_id = entity_id
    df["ENSP"] = df["species_id"].astype(str) + "." + df["protein_id"].astype(str)
    return df

def parse_textmining_string_matches(fn):
    names=['PMID', 'sentence', 'paragraph', 'location_start', 'location_end', 'matched_string', 'species', 'entity_id']
    df = pd.read_csv(fn, sep="\t", names=names)
    return df

def get_all_ENSPs(TaxID_2_Proteins_table_STRING):
    ENSP_set = set()
    with open(TaxID_2_Proteins_table_STRING, "r") as fh:
        for line in fh:
            ENSP_set |= literal_eval(line.split("\t")[1])
    return ENSP_set

def create_Protein_2_Function_table_PMID__and__reduce_Functions_table_PMID(fn_in_all_entities, fn_in_string_matches, fn_in_TaxID_2_Proteins_table_STRING, fn_out_Protein_2_Function_table_PMID): # fn_in_Functions_table_PMID_temp, fn_out_Functions_table_PMID
    df_txtID = parse_textmining_entityID_2_proteinID(fn_in_all_entities)
    df_stringmatches = parse_textmining_string_matches(fn_in_string_matches)
    # sanity test that df_stringmatches.entity_id are all in df_txtID.textmining_id --> yes. textmining_id is a superset of entity_id --> after filtering df_txtID this is not true
    entity_id = set(df_stringmatches["entity_id"].unique())
    textmining_id = set(df_txtID.textmining_id.unique())
    assert len(entity_id.intersection(textmining_id)) == len(entity_id)

    # sanity check that there is a one to one mapping between textmining_id and ENSP --> no --> first remove all ENSPs that are not in DB
    # --> simpler by filtering based on positive integers in species_id column ?
    # get all ENSPs

    ENSP_set = get_all_ENSPs(fn_in_TaxID_2_Proteins_table_STRING)

    # reduce DF to ENSPs in DB
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

def create_Protein_2_Function_table_STRING(fn_list, fn_in_TaxID_2_Proteins_table_STRING, fn_out_Protein_2_Function_table_STRING, number_of_processes=1):
    # fn_list = fn_list_str.split(" ")
    ### concatenate files
    fn_out_Protein_2_Function_table_STRING_temp = fn_out_Protein_2_Function_table_STRING + "_temp"
    fn_out_Protein_2_Function_table_STRING_rest = fn_out_Protein_2_Function_table_STRING + "_rest"
    tools.concatenate_files(fn_list, fn_out_Protein_2_Function_table_STRING_temp)
    ### sort
    tools.sort_file(fn_out_Protein_2_Function_table_STRING_temp, fn_out_Protein_2_Function_table_STRING_temp, number_of_processes=number_of_processes)
    reduce_Protein_2_Function_table_2_STRING_proteins(
        fn_in_protein_2_function_temp=fn_out_Protein_2_Function_table_STRING_temp,
        fn_in_TaxID_2_Proteins_table_STRING=fn_in_TaxID_2_Proteins_table_STRING,
        fn_out_protein_2_function_reduced=fn_out_Protein_2_Function_table_STRING,
        fn_out_protein_2_function_rest=fn_out_Protein_2_Function_table_STRING_rest,
        number_of_processes=number_of_processes)

def reduce_Protein_2_Function_table_2_STRING_proteins(fn_in_protein_2_function_temp, fn_in_TaxID_2_Proteins_table_STRING, fn_out_protein_2_function_reduced, fn_out_protein_2_function_rest, number_of_processes=1):#, minimum_number_of_annotations=1):
    """
    - reduce Protein_2_Function_table_2_STRING to relevant ENSPs (those that are in fn_in_TaxID_2_Proteins_table_STRING)
    - and remove duplicates
    second reduction step is done elsewhere (minimum number of functional associations per taxon)
    """
    ENSP_set = parse_taxid_2_proteins_get_all_ENSPs(fn_in_TaxID_2_Proteins_table_STRING)
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

def parse_taxid_2_proteins_get_all_ENSPs(fn_TaxID_2_Proteins_table_STRING):
    ENSP_set = set()
    with open(fn_TaxID_2_Proteins_table_STRING, "r") as fh:
        for line in fh:
            ENSP_set |= literal_eval(line.split("\t")[1])  # reduce DF to ENSPs in DB
    return ENSP_set

def create_Function_2_ENSP_table(fn_in_Protein_2_Function_table, fn_in_TaxID_2_Proteins_table, fn_in_Functions_table,
        fn_out_Function_2_ENSP_table, fn_out_Function_2_ENSP_table_reduced, fn_out_Function_2_ENSP_table_removed,
        min_count=1, verbose=True):
    """
    min_count: for each function minimum number of ENSPs per TaxID, e.g. 1 otherwise removed, also from Protein_2_Function_table_STRING
    """
    if verbose:
        print("creating Function_2_ENSP_table this will take a while")

    function_2_ENSPs_dict = defaultdict(list)
    taxid_2_total_protein_count_dict = _helper_get_taxid_2_total_protein_count_dict(fn_in_TaxID_2_Proteins_table)
    _, function_2_etype_dict = _helper_get_function_2_funcEnum_dict__and__function_2_etype_dict(fn_in_Functions_table) # funcenum not correct at this stage since some functions will be removed from Functions_table_STRING and thus the enumeration would be wrong
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
                                try:
                                    etype = function_2_etype_dict[function_an]
                                except KeyError: # for blacklisted terms in variables.py
                                    etype = "-1"
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
                        try:
                            etype = function_2_etype_dict[function_an]
                        except KeyError:  # for blacklisted terms in variables.py
                            etype = "-1"
                        fh_out.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_ENSPs) + "\t" + str(num_ENSPs_total_for_taxid) + "\t" + arr_of_ENSPs + "\n")
                        if num_ENSPs > min_count:
                            fh_out_reduced.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_ENSPs) + "\t" + str(num_ENSPs_total_for_taxid) + "\t" + arr_of_ENSPs + "\n")
                        else:
                            fh_out_removed.write(taxid_last + "\t" + etype + "\t" + function_an + "\t" + str(num_ENSPs) + "\t" + str(num_ENSPs_total_for_taxid) + "\t" + arr_of_ENSPs + "\n")
    tools.sort_file(fn_out_Function_2_ENSP_table_reduced, fn_out_Function_2_ENSP_table_reduced)
    if verbose:
        print("finished creating \n{}\nand\n{}".format(fn_out_Function_2_ENSP_table, fn_out_Function_2_ENSP_table_reduced))

def reduce_Functions_table_STRING(fn_in_Functions_table, fn_in_Function_2_ENSP_table_reduced, fn_out_Functions_table_STRING_removed, fn_out_Functions_table_STRING_reduced):
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
                    elif etype == "-25" or etype == "-26": # include all DOID and BTO terms
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

def _helper_get_taxid_2_total_protein_count_dict(fn_in_TaxID_2_Proteins_table_STRING):
    taxid_2_total_protein_count_dict = {}
    with open(fn_in_TaxID_2_Proteins_table_STRING, "r") as fh_in:
        for line in fh_in:
            taxid, ENSP_arr_str, count = line.split("\t")
            # count = int(count.strip())
            count = count.strip()
            # ENSP_arr = literal_eval(ENSP_arr_str)
            # assert len(ENSP_arr) == count
            taxid_2_total_protein_count_dict[taxid] = count
    return taxid_2_total_protein_count_dict

def _helper_get_function_2_funcEnum_dict__and__function_2_etype_dict(fn_in_Functions_table):
    function_2_funcEnum_dict, function_2_etype_dict = {}, {}
    with open(fn_in_Functions_table, "r") as fh_in:
        for line in fh_in:
            enum, etype, an, description, year, hier_nr = line.split("\t")
            function_2_funcEnum_dict[an] = enum
            function_2_etype_dict[an] = etype
    return function_2_funcEnum_dict, function_2_etype_dict

def reduce_Protein_2_Function_by_subtracting_Function_2_ENSP_rest_and_Functions_table_STRING_reduced(fn_in_protein_2_function, fn_in_function_2_ensp_rest, fn_in_Functions_table_STRING_reduced, fn_out_protein_2_function_reduced, fn_out_protein_2_function_rest):
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

def AFC_KS_enrichment_terms_flat_files(fn_in_Protein_shorthands, fn_in_Functions_table_STRING_reduced, fn_in_Function_2_ENSP_table_STRING_reduced, KEGG_TaxID_2_acronym_table, fn_out_AFC_KS_DIR, verbose=True):
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
    with open(KEGG_TaxID_2_acronym_table, "r") as fh:
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
                    print("no KEGG acronym translation for TaxID: {}".format(taxid))
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
def parse_Function_2_Description_PMID(Function_2_Description_PMID, Functions_table_PMID_temp, max_len_description=250): # string_matches
    # df_stringmatches = parse_textmining_string_matches(string_matches)
    # PMID_set = set(df_stringmatches["PMID"].values)
    hierarchical_level = "-1"
    # with open(Function_2_Description_PMID, "r") as fh_in:
    #         for line in fh_in:
    with open(Functions_table_PMID_temp, "w") as fh_out:
        for line in tools.yield_line_uncompressed_or_gz_file(Function_2_Description_PMID):
            ls = line.split("\t")
            etype, PMID, description, year = ls
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

def merge_Protein_2_Function_table_PMID(TaxID_2_Proteins_table_STRING, Protein_2_Function_table_PMID_abstracts, Protein_2_Function_table_PMID_fulltexts, Protein_2_Function_table_PMID_combi, Protein_2_Function_table_PMID, number_of_processes=1, verbose=True):
    """
    concatenate files, sort and create set of union of functional associations
    filter PMID associations that are not STRING ENSPs. use TaxID_2_Proteins_table_STRING
    :param TaxID_2_Proteins_table_STRING: string
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

    ENSP_set = get_all_ENSPs(TaxID_2_Proteins_table_STRING)

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

def create_Functions_table_DOID_BTO(Function_2_Description_DOID_BTO_GO_down, BTO_obo_Jensenlab, DOID_obo_Jensenlab, Blacklisted_terms_Jensenlab, Functions_table_DOID_BTO):
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
    term_2_level_dict = {}
    term_2_level_dict.update(term_2_level_dict_doid)
    term_2_level_dict.update(term_2_level_dict_bto)
    # get blacklisted terms to exclude them
    blacklisted_ans = []
    with open(Blacklisted_terms_Jensenlab, "r") as fh:
        for line in fh:
            etype, an = line.split("\t")
            blacklisted_ans.append(an.strip())
    blacklisted_ans = set(blacklisted_ans)

    year = "-1" # placeholder
    # with open(Function_2_Description_DOID_BTO_GO_down, "r") as fh_in:
        # for line in fh_in:
    with open(Functions_table_DOID_BTO, "w") as fh_out:
        for line in tools.yield_line_uncompressed_or_gz_file(Function_2_Description_DOID_BTO_GO_down):
            etype, function_an, description = line.split("\t")
            description = description.strip()
            if function_an in blacklisted_ans:
                continue
            try:
                level = term_2_level_dict[function_an] # level is an integer
            except KeyError:
                level = -1
            fh_out.write(etype + "\t" + function_an + "\t" + description + "\t" + year + "\t" + str(level) + "\n")

def create_Protein_2_FunctionEnum_and_Score_table_STRING(Protein_2_Function_and_Score_DOID_GO_BTO, Functions_table_STRING_reduced, Protein_2_FunctionEnum_and_Score_table_STRING, fn_an_without_translation):
    """
    Protein_2_Function_and_Score_DOID_GO_BTO.txt
    6239.C30G4.7    {{"GO:0043226",0.875},{"GO:0043227",0.875},{"GO:0043231",0.875},{"GO:0044424",2.96924}, ... , {"GO:0005737",2.742276},{"GO:0005777",0.703125}}      -22
    10116.ENSRNOP00000049139        {{"GO:0005623",2.927737},{"GO:0044424",2.403304},{"GO:0044425",3},{"GO:0031224",3}, ... ,{"GO:0043232",0.375}}       -22

    Protein_2_FunctionEnum_and_Score_table_STRING.txt
    10116.ENSRNOP00000049139  {{{0,2.927737},{3,2.403304},{4,3},{666,3}, ... ,{3000000,0.375}}

    - remove anything on blacklist (all_hidden.tsv) already happend while creating Functions_table_DOID_BTO (and all terms not present therein will be filtered out)
    - omit GO-CC (etype -22)
    """
    year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr = get_lookup_arrays(Functions_table_STRING_reduced, low_memory=True)
    term_2_enum_dict = {key: val for key, val in zip(functionalterm_arr, indices_arr)}

    # with open(Protein_2_Function_and_Score_DOID_GO_BTO, "r") as fh_in:
        # for line in fh_in:
    an_without_translation = []
    with open(Protein_2_FunctionEnum_and_Score_table_STRING, "w") as fh_out:
        for line in tools.yield_line_uncompressed_or_gz_file(Protein_2_Function_and_Score_DOID_GO_BTO):
            ENSP, funcName_2_score_arr_str, etype = line.split("\t")
            etype = etype.strip()
            if etype == "-22": # omit GO-CC (etype -22)
                continue
            else:
                funcEnum_2_score = []
                funcName_2_score_arr_str = funcName_2_score_arr_str.replace("{", "[").replace("}", "]")
                funcName_2_score_list = literal_eval(funcName_2_score_arr_str)
                for an_score in funcName_2_score_list:
                    an, score = an_score
                    try:
                        anEnum = term_2_enum_dict[an]
                        funcEnum_2_score.append([anEnum, score])
                    except KeyError: # because e.g. blacklisted
                        an_without_translation.append(an)
                funcEnum_2_score.sort(key=lambda sublist: sublist[0]) # sort anEnum in ascending order
                funcEnum_2_score = format_list_of_string_2_postgres_array(funcEnum_2_score)
                funcEnum_2_score = funcEnum_2_score.replace("[", "{").replace("]", "}")
                fh_out.write(ENSP + "\t" + funcEnum_2_score + "\n")
    with open(fn_an_without_translation, "w") as fh_an_without_translation:
        fh_an_without_translation.write("\n".join(sorted(set(an_without_translation))))

def create_Taxid_2_FunctionCountArray_2_merge_BTO_DOID(TaxID_2_Proteins_table, Functions_table_STRING, Protein_2_FunctionEnum_and_Score_table_STRING, Taxid_2_FunctionCountArray_2_merge_BTO_DOID, number_of_processes=1, verbose=True):
    """
    Protein_2_FunctionEnum_and_Score_table_STRING.txt
    10116.ENSRNOP00000049139  {{{0,2.927737},{3,2.403304},{4,3},{666,3}, ... ,{3000000,0.375}}
    ENSP to functionEnumeration and its respective score
    multiple ENSPs per taxid --> scores get summed up per TaxID

    Taxid_2_FunctionCountArray_2_merge_BTO_DOID.txt
    9606  19566  {{{0,3},{3,2},{4,3},{666,3}, ... ,{3000000,1}}

    """
    if verbose:
        print("creating Taxid_2_FunctionCountArray_2_merge_BTO_DOID")
    # sort table to get group ENSPs of same TaxID
    tools.sort_file(Protein_2_FunctionEnum_and_Score_table_STRING, Protein_2_FunctionEnum_and_Score_table_STRING, number_of_processes=number_of_processes, verbose=verbose)
    # get dict
    taxid_2_total_protein_count_dict = _helper_get_taxid_2_total_protein_count_dict(TaxID_2_Proteins_table)
    num_lines = tools.line_numbers(Functions_table_STRING)

    with open(Protein_2_FunctionEnum_and_Score_table_STRING, "r") as fh_in:
        with open(Taxid_2_FunctionCountArray_2_merge_BTO_DOID, "w") as fh_out:
            line = next(fh_in)
            fh_in.seek(0)
            taxid_last, ENSP_last, funcEnum_2_count_list_last = helper_parse_line_protein_2_functionEnum_and_score(line)
            funcEnum_count_background = np.zeros(shape=num_lines, dtype=np.dtype("float64"))
            funcEnum_count_background = helper_count_funcEnum_floats(funcEnum_count_background, funcEnum_2_count_list_last)
            for line in fh_in:
                taxid, ENSP, funcEnum_2_count_list = helper_parse_line_protein_2_functionEnum_and_score(line)
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
        print("done with Taxid_2_FunctionCountArray_2_merge_BTO_DOID")

def helper_parse_line_protein_2_functionEnum_and_score(line):
    ENSP, funcEnum_2_count_arr = line.split("\t")
    funcEnum_2_count_list = literal_eval(funcEnum_2_count_arr.strip().replace("{", "[").replace("}", "]"))
    taxid = ENSP.split(".")[0]
    return taxid, ENSP, funcEnum_2_count_list

def helper_count_funcEnum_floats(funcEnum_count_background, funcEnum_2_count_list):
    for funcEnum_count in funcEnum_2_count_list:
        funcEnum, count = funcEnum_count
        funcEnum_count_background[funcEnum] += count
    return funcEnum_count_background



if __name__ == "__main__":
    # create_table_Protein_2_Function_table_RCTM__and__Function_table_RCTM()

    ### dubugging start
    # fn_in_go_basic = os.path.join(DOWNLOADS_DIR, "go-basic.obo")
    # fn_out_Functions_table_GO = os.path.join(TABLES_DIR, "Functions_table_GO.txt")
    # is_upk = False
    # create_Functions_table_GO_or_UPK(fn_in_go_basic, fn_out_Functions_table_GO, is_upk)

    # string2uniprot = os.path.join(DOWNLOADS_DIR, "full_uniprot_2_string.jan_2018.clean.tsv")
    # uniprot2interpro = os.path.join(DOWNLOADS_DIR, "protein2ipr.dat.gz")
    # string2interpro = os.path.join(DOWNLOADS_DIR, "string2interpro.dat.gz")
    # map_string_2_interpro(string2uniprot, uniprot2interpro, string2interpro)

    # Functions_table_UPK = os.path.join(TABLES_DIR, "Functions_table_UPK.txt")
    # fn_in_obo = os.path.join(DOWNLOADS_DIR, "keywords-all.obo")
    # fn_in_uniprot_SwissProt_dat = os.path.join(DOWNLOADS_DIR, "uniprot_sprot.dat.gz")
    # fn_in_uniprot_TrEMBL_dat= os.path.join(DOWNLOADS_DIR, "uniprot_sprot.dat.gz.1")
    # fn_in_uniprot_2_string = os.path.join(DOWNLOADS_DIR, "full_uniprot_2_string.jan_2018.clean.tsv")
    # fn_out_Protein_2_Function_table_UPK = os.path.join(TABLES_DIR, "Protein_2_Function_table_UPK.txt")
    # create_Protein_2_Function_table_UniProtKeyword(Functions_table_UPK, fn_in_obo, fn_in_uniprot_SwissProt_dat, fn_in_uniprot_TrEMBL_dat, fn_in_uniprot_2_string, fn_out_Protein_2_Function_table_UPK, number_of_processes=1, verbose=True)



    Protein_2_Function_table_STRING = os.path.join(TABLES_DIR, "Protein_2_Function_table_STRING.txt")
    Function_2_ENSP_table_STRING_removed = os.path.join(TABLES_DIR, "Function_2_ENSP_table_STRING_removed.txt")
    Functions_table_STRING_reduced = os.path.join(TABLES_DIR, "Functions_table_STRING_reduced.txt")
    Protein_2_Function_table_STRING_reduced = os.path.join(TABLES_DIR, "Protein_2_Function_table_STRING_reduced.txt")
    Protein_2_Function_table_STRING_removed = os.path.join(TABLES_DIR, "Protein_2_Function_table_STRING_removed.txt")
    reduce_Protein_2_Function_by_subtracting_Function_2_ENSP_rest_and_Functions_table_STRING_reduced(Protein_2_Function_table_STRING, Function_2_ENSP_table_STRING_removed, Functions_table_STRING_reduced, Protein_2_Function_table_STRING_reduced, Protein_2_Function_table_STRING_removed)
    ### dubugging stop


