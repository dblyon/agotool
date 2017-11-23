import os, json, sys, re, fnmatch, subprocess, time, multiprocessing
import pandas as pd
from subprocess import call
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import tools

# ToDo
# - filter associations based on their presence in ontologies. e.g. AN123 has GO123, GO234, GO345 but GO345 is not in obo, thus kick it out

BASH_LOCATION = r"/bin/bash"
PYTHON_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
sys.path.append(PYTHON_DIR)
PROJECT_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../..')))
POSTGRESQL_DIR = os.path.join(PROJECT_DIR, "static/data/PostgreSQL")
DOWNLOADS_DIR = os.path.join(POSTGRESQL_DIR, "downloads")
STATIC_DIR = os.path.join(POSTGRESQL_DIR, "static")
TABLES_DIR = os.path.join(POSTGRESQL_DIR, "tables")
TEST_DIR = os.path.join(TABLES_DIR, "test")
FILES_NOT_2_DELETE = [os.path.join(DOWNLOADS_DIR + fn) for fn in ["keywords-all.obo", "goslim_generic.obo", "go-basic.obo"]]
NUMBER_OF_PROCESSES = multiprocessing.cpu_count()

EMPTY_EGGNOG_JSON_DICT = {"KEGG": {"kegg_pathways": [], "kegg_header": ["Pathway", "SeqCount", "Frequency", "relative_fontsize"]}, "go_terms": {"go_terms": {}, "go_header": ["ID", "GO term", "Evidence", "SeqCount", "Frequency", "relative_fontsize"]}, "domains": {"domains": {}, "dom_header": ["Domain ID", "SeqCount", "Frequency", "relative_fontsize"]}}
TYPEDEF_TAG, TERM_TAG = "[Typedef]", "[Term]"
id_2_entityTypeNumber_dict = {'GO:0003674': "-23",  # 'Molecular Function',
                              'GO:0005575': "-22",  # 'Cellular Component',
                              'GO:0008150': "-21",  # 'Biological Process',
                              'UPK:9990': "-51",  # 'Technical term',
                              'UPK:9991': "-51",  # 'PTM',
                              'UPK:9992': "-51",  # 'Molecular function',
                              'UPK:9993': "-51",  # 'Ligand',
                              'UPK:9994': "-51",  # 'Domain',
                              'UPK:9995': "-51",  # 'Disease',
                              'UPK:9996': "-51",  # 'Developmental stage',
                              'UPK:9997': "-51",  # 'Coding sequence diversity',
                              'UPK:9998': "-51",  # 'Cellular component',
                              'UPK:9999': "-51",  # 'Biological process'
                              'KEGG': "-52"}
id_2_entityTypeNumber_dict_keys_set = set(id_2_entityTypeNumber_dict.keys())


##### create test tables for import
def create_test_tables(num_lines=5000, TABLES_DIR_=None):
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
    if TABLES_DIR_ is None:
        TABLES_DIR_ = TABLES_DIR
    fn_list = [os.path.join(TABLES_DIR_, fn) for fn in os.listdir(TABLES_DIR_)]
    fn_list = [fn for fn in fn_list if fn.endswith("_table.txt")]
    for fn in fn_list:
        counter = 0
        with open(fn, "r") as fh_in:
            fn_out = os.path.join(TEST_DIR, os.path.basename(fn))
            with open(fn_out, "w") as fh_out:
                for line in fh_in:
                    if counter >= num_lines:
                        break
                    fh_out.write(line)
                    counter += 1

##### Protein_2_OG_table_static.txt
### only for HOMD-data since the Bacterial proteins are the only ones mapped to OGs
### this relies on previous mapping of bacterial proteins to OGs via Hidden Markov Models from eggNOG using HMMer
def create_Protein_2_OG_table():
    """
    fn_in HOMD_Protein_2_OG_parsed.txt (AN-Protein, OG1;OG2) from HMMER results
    fn_outProtein_2_OG_table_static.txt (AN-Protein, OG1)
    :return: None
    """
    print("create_Protein_2_OG_table")
    fn_in = os.path.join(STATIC_DIR, "results_AN_2_HMMs_HOMD_UPstyle_201607_AND_HOMD_UPstyle_201508_static.txt")  # HMMER results, previously 'HOMD_AN2NOGname_parsed.txt'
    fn_out = os.path.join(STATIC_DIR, "Protein_2_OG_table_static.txt")
    with open(fn_in, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            for line in fh_in:
                try:
                    an, hmm = line.split("\t")
                except ValueError:
                    continue
                try:
                    hmm_list = [ele.split(".")[1] for ele in hmm.split(";")]
                except IndexError:
                    continue
                for hmm in hmm_list:
                    string2write = an + "\t" + hmm + "\n"
                    fh_out.write(string2write)

# #### OG_2_Function_table_static.txt, OGs_table_static.txt, and Functions_table_KEGG_DOM.txt
# http://eggnogdb.embl.de/download/latest/all_OG_annotations.tsv.gz
# #### retrieving eggNOG attributes
def get_og_names():
    """
    return iterable Orthologous Group names
    :return: ArrayOfString
    """
    fn = os.path.join(DOWNLOADS_DIR, "bactNOG.annotations.tsv")
    df = pd.read_csv(fn, sep='\t', names=["bactNOG", "NOGname", "C", "D", "E", "F"])
    og_names = df["NOGname"].unique()
    return og_names

def yield_entry_from_all_annotations():
    """
    ENOG41xxxxx = Unsupervised Cluster of Orthologous Group (present in all levels)
    OG_name_short | GroupName | ProteinCount | description | dunno | GO | KEGG | domains | members |
    """
    fn = os.path.join(DOWNLOADS_DIR, "all_OG_annotations.tsv")
    og_names = get_og_names()
    # og.replace("ENOG41", "") faster but no check below
    og_names_short = {og[6:] for og in og_names}
    with open(fn, "r") as fh:
        for line in fh:
            line_split = line.strip().split("\t")
            if line_split[0] in og_names_short:
                og_name = "ENOG41" + line_split[0]
                description = line_split[3]
                go = line_split[5]
                go = json.loads(go)
                KEGG = line_split[6]
                KEGG = json.loads(KEGG)
                domains = line_split[7]
                domains = json.loads(domains)
                yield (og_name, description, go, KEGG, domains)

def parse_go_terms_or_domains_all_annotations(json_):
    """
    more concise dict coming from all_annotations file
    :param json_:
    :return:
    """
    attributes_list = []
    categories = json_.keys()
    for cat in categories:
        attributes_list += [ele[0] for ele in json_[cat]]
    return attributes_list

def parse_KEGG_all_annotaions(kegg_list):
    pw_name_list, pw_num_list = [], []
    kegg_funcs = [ele[0] for ele in kegg_list]
    for pawthway_name_number in kegg_funcs:
        index_ = pawthway_name_number.index("(")
        pw_name = pawthway_name_number[:index_].strip()
        pw_num = pawthway_name_number[index_ + 1:-1].strip()
        pw_name_list.append(pw_name)
        pw_num_list.append(pw_num)
    return pw_name_list, pw_num_list

def parse_functions(go, KEGG, domains):
    """
    from a single entry in all_OG_annotations.tsv
    parse the GO, KEGG and domain functions and add the appropriate prefix
    :param go: Dict
    :param KEGG: List
    :param domains: Dict
    :return: Tuple(ListOfString Tuple(ListOfString, ListOfString))
    """
    functions = parse_go_terms_or_domains_all_annotations(go)

    domains_list = parse_go_terms_or_domains_all_annotations(domains)
    functions += ["DOM:" + ele for ele in domains_list]

    pw_name_list, pw_num_list = parse_KEGG_all_annotaions(KEGG)
    pw_num_list = ["KEGG:" + ele for ele in pw_num_list]
    functions += pw_num_list

    return functions, zip(pw_name_list, pw_num_list)

def create_OGs_table_and_OG_2_Function_table_and_Functions_table_DOM():
    """
    # OGs_table_static.txt --> complete
    # og, taxid, description (taxid = 2 for all bacterial OGs)

    # OG_2_Function_table_static.txt --> complete
    # og, function

    # Functions_table_KEGG_DOM.txt --> partial
    # type_, description, an
    :return:
    """
    print("create_OGs_table_and_OG_2_Function_table_and_Functions_table_DOM")
    # taxid = "2"
    fn_ogs = os.path.join(STATIC_DIR, "OGs_table_static.txt")
    fn_og_2_func = os.path.join(STATIC_DIR, "OG_2_Function_table_static.txt")
    # fn_func_KEGG = os.path.join(TABLES_DIR, "Functions_table_KEGG_static.txt")
    fn_func_DOM = os.path.join(STATIC_DIR, "Functions_table_DOM_static.txt") # temporary --> merged into Functions_table.txt, therefore not saved
    function_dom_set = set()
    # an_kegg_set = set()
    with open(fn_ogs, "w") as fh_ogs:
        with open(fn_og_2_func, "w") as fh_og_2_func:
            # with open(fn_func_KEGG, "w") as fh_func_KEGG:
            with open(fn_func_DOM, "w") as fh_func_DOM:
                for entry in yield_entry_from_all_annotations():
                    og_name, description, go, KEGG, domains = entry
                    # OGs_table_static.txt
                    # og, taxid, description (taxid = 2 for all bacterial OGs)
                    if description != "NA":
                        # line2write_ogs = og_name + "\t" + taxid + "\t" + description + "\n"
                        line2write_ogs = og_name + "\t" + description + "\n"
                        fh_ogs.write(line2write_ogs)

                    functions, pw_name_num = parse_functions(go, KEGG, domains)
                    functions = set(functions)  # remove redundancies
                    # OG_2_Function_table_static.txt
                    # og, function
                    for function_ in functions:
                        line2write_og_2_func = og_name + "\t" + function_ + "\n"
                        fh_og_2_func.write(line2write_og_2_func)

                    # Functions_table_KEGG_static.txt # obsolete here, since using resource from Lars's frozen KEGG version
                    # type_, description, an
                    # type_ = "KEGG"
                    # for name_num in pw_name_num:
                    #     pw_name, pw_num = name_num
                    #     description_ = pw_name
                    #     an_ = pw_num
                    #     if not an_ in an_kegg_set:
                    #         line2write_func_KEGG = type_ + "\t" + description_ + "\t" + an_ + "\n"
                    #         fh_func_KEGG.write(line2write_func_KEGG)
                    #         an_kegg_set.update([an_])

                    type_ = "DOM"  # this is a bit stupid, since redundant info see DataBase_schema.md
                    for function_ in functions:
                        function_split = function_.split(":")
                        description_ = function_split[1]
                        if function_split[0] == "DOM":
                            if not function_ in function_dom_set:
                                line2write_func_KEGG = type_ + "\t" + description_ + "\t" + function_ + "\n"
                                # fh_func_KEGG.write(line2write_func_KEGG)
                                fh_func_DOM.write(line2write_func_KEGG)
                                function_dom_set.update([function_])

def read_until(fh, start):
    """
    # read each line until it has a certain start, and then puts
    # the start tag back
    """
    while 1:
        pos = fh.tell()
        line = fh.readline()
        if not line:
            break
        if line.startswith(start):
            fh.seek(pos)
            return
    raise EOFError("%s tag cannot be found" % start)

def after_colon(line):
    # macro for getting anything after the :
    return line.split(":", 1)[1].strip()

class OBOReader:
    """
    parse obo file, usually the most updated can be downloaded from
    http://purl.obolibrary.org/obo/go/go-basic.obo
    e.g.
    reader = OBOReader()
    for rec in reader:
        print(rec)
    """

    def __init__(self, obo_file):
        try:
            self._handle = open(obo_file, "r")
        except:
            sys.exit(1)

    def __iter__(self):
        line = self._handle.readline()
        if not line.startswith(TERM_TAG):
            read_until(self._handle, TERM_TAG)
        while 1:
            yield self.__next__()

    def __next__(self):
        lines = []
        line = self._handle.readline()
        if not line or line.startswith(TYPEDEF_TAG):
            raise StopIteration

        # read until the next tag and save everything in between
        while 1:
            pos = self._handle.tell()  # save current postion for roll-back
            line = self._handle.readline()
            if not line or (line.startswith(TYPEDEF_TAG) or line.startswith(TERM_TAG)):
                self._handle.seek(pos)  # roll-back
                break
            lines.append(line)
        id_, name, definition = "", "", ""
        is_a_list = []
        for line in lines:
            # if line.startswith("id_:"):
            if line.startswith("id:"):
                id_ = after_colon(line)
            elif line.startswith("name:"):
                name = after_colon(line)
            elif line.startswith("def:"):
                definition = after_colon(line)
            elif line.startswith("is_a:"):
                is_a_list.append(after_colon(line).split()[0])
        return id_, name, is_a_list, definition


##### Child_2_Parent_table_UPK.txt, Functions_table_UPK.txt and Function_2_definition_table_UPK.txt
def create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK():
    """
    id_, name --> Functions_table.txt
    id_, is_a_list --> UPKChild_2_UPKParent_table.txt
    :return:
    """
    print("create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK")
    fn = os.path.join(DOWNLOADS_DIR, "keywords-all.obo")
    obo = OBOReader(fn)
    fn_child2parent = os.path.join(TABLES_DIR, "Child_2_Parent_table_UPK.txt")
    fn_funcs = os.path.join(TABLES_DIR, "Functions_table_UPK.txt")
    type_ = "UPK"
    # fn_descr = os.path.join(TABLES_DIR, "Function_2_definition_table_UPK.txt")
    with open(fn_funcs, "w") as fh_funcs:
        with open(fn_child2parent, "w") as fh_child2parent:
            # with open(fn_descr, "w") as fh_descr:
            for entry in obo:
                id_, name, is_a_list, definition = entry
                id_ = id_.replace("KW-", "UPK:")
                # line2write_func = type_ + "\t" + name + "\t" + id_ + "\n"
                line2write_func = type_ + "\t" + name + "\t" + id_ + "\t" + definition + "\n"
                fh_funcs.write(line2write_func)
                for parent in is_a_list:
                    parent = parent.replace("KW-", "UPK:")
                    line2write_cp = id_ + "\t" + parent + "\n"
                    fh_child2parent.write(line2write_cp)
                # line2write_descr = id_ + "\t" + definition + "\n"
                # fh_descr.write(line2write_descr)

##### Child_2_Parent_table_GO.txt, Functions_table_GO.txt and Function_2_definition_table_GO.txt
def create_Child_2_Parent_table_GO__and__Functions_table_GO__and__Function_2_definition_GO():
    """
    id_, name --> Functions_table.txt
    id_, is_a_list --> Child_2_Parent_table_GO.txt
    :return:
    """
    print("create_Child_2_Parent_table_GO__and__Functions_table_GO__and__Function_2_definition_GO")
    fn = os.path.join(DOWNLOADS_DIR, "go-basic.obo")
    obo = OBOReader(fn)
    fn_child2parent = os.path.join(TABLES_DIR, "Child_2_Parent_table_GO.txt")
    fn_funcs = os.path.join(TABLES_DIR, "Functions_table_GO.txt")
    type_ = "GO"
    # fn_descr = os.path.join(TABLES_DIR, "Function_2_definition_table_GO.txt")
    with open(fn_funcs, "w") as fh_funcs:
        with open(fn_child2parent, "w") as fh_child2parent:
            # with open(fn_descr, "w") as fh_descr:
            for entry in obo:
                id_, name, is_a_list, definition = entry
                line2write_func = type_ + "\t" + name + "\t" + id_ + "\t" + definition + "\n"
                fh_funcs.write(line2write_func)
                for parent in is_a_list:
                    parent = parent.replace("KW-", "UPK:")
                    line2write_cp = id_ + "\t" + parent + "\n"
                    fh_child2parent.write(line2write_cp)
                # line2write_descr = id_ + "\t" + definition + "\n"
                # fh_descr.write(line2write_descr)

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

##### Ontologies_table
def create_Ontologies_table(fn_list, fn_out):
    """
    get all parents for each node/child, set Boolean if direct or indirect
    :param fn_list: RawString(each with direct child to parent relationship)
    :param fn_out: RawString
    :return: None
    """
    print("create_Ontologies_table")
    child_2_parent_dict = {}  # key=child, val=SetOfString
    for fn in fn_list:
        with open(fn, 'r') as fh:
            for line in fh:
                child, parent = line.strip().split("\t")
                if not child in child_2_parent_dict:
                    child_2_parent_dict[child] = set([parent])
                else:
                    child_2_parent_dict[child].update([parent])

    with open(fn_out, "w") as fh_out:
        for child in sorted(child_2_parent_dict.keys()):
            parents_set = get_parents_iterative(child, child_2_parent_dict)
            entity_type_num = get_entity_type_number_from_parents_set(parents_set)
            for parent in parents_set:
                if parent in child_2_parent_dict[child]:
                    line2write = child + "\t" + parent + "\t" + "1" + "\t" + entity_type_num + "\n"  # direct parent
                    fh_out.write(line2write)
                else:
                    line2write = child + "\t" + parent + "\t" + "0" + "\t" + entity_type_num + "\n"  # indirect parent
                    fh_out.write(line2write)

def get_entity_type_number_from_parents_set(parents_set):
    """
    based on child column of Ontologies table, determine the entity type
     GO terms will have one of three parents
     UPK unfortunately multiple top parents possible
     if conversion to Integer possible, then TaxID
     if DOID: in all parents, then Disease
    :param parents_set: SetOfString
    :return: String
    """
    key = list(parents_set.intersection(id_2_entityTypeNumber_dict_keys_set))
    if len(key) == 1:
        return id_2_entityTypeNumber_dict[key[0]]
    elif len(key) > 1:  # can happen for UPK
        return id_2_entityTypeNumber_dict[key[0]]
    else:
        # check if convertable to Integers --> TaxID
        try:
            [int(ele) for ele in parents_set]
            return "-3"  # for TaxID
        except ValueError:
            if sum([ele.startswith("DOID:") for ele in parents_set]) == len(parents_set):
                return "-26"  # Diseases
    return "-99"

def concatenate_files(fn_list, fn_out):
    with open(fn_out, "w") as fh_out:
        for fn in fn_list:
            with open(fn, "r") as fh_in:
                for line in fh_in:
                    fh_out.write(line)

##### Protein_2_Funtion_table.txt
# for UniProt AccessionNumbers, UniProt-Keywords and GO-terms
# HOMD ANs are mapped via OGs
def yield_line_uncompressed_or_gz_file(fn):
    """
    adapted from
    https://codebright.wordpress.com/2011/03/25/139/
    and
    https://www.reddit.com/r/Python/comments/2olhrf/fast_gzip_in_python/
    http://pastebin.com/dcEJRs1i
    :param fn: String (absolute path)
    :return: GeneratorFunction (yields String)
    """
    if fn.endswith(".gz"):
        ph = subprocess.Popen(["gzcat", fn], stdout=subprocess.PIPE)
        for line in ph.stdout:
            yield line.decode("utf-8")
    else:
        with open(fn, "r") as fh:
            for line in fh:
                yield line

# def parse_goa_gaf(fn_in, fn_out, taxid_2_ignore_set=None, protein_2_taxid=False, an_set=None):  # dependency
def parse_goa_gaf(fn_in, fn_out, functions_set, taxid_2_ignore_set=None):
    """
    parse UniProt goa_ref file, write to table.txt for SQL
    restrict to taxid_2_ignore_set (TaxIDs as String) if provided
    also restrict to Functional annotations (GO-terms and UniProt-keywords) that are present in OBO-files)
    :param fn_in: raw String
    :param fn_out: raw String
    :param functions_set: Set of Strings (Functional annotations (GO-terms and UniProt-keywords) that are present in OBO)
    :param taxid_2_ignore_set: SetOfString (flag to skip TaxIDs)
    :return: None
    """
    with open(fn_out, "w") as fh_out:
        for line in yield_line_uncompressed_or_gz_file(fn_in):
            if line[0] == "!":
                continue
            else:
                line_split = line.split("\t")
                if len(line_split) >= 15:
                    an = line_split[1]  # DB_Object_ID
                    goid = line_split[4]  # GO_ID
                    if goid not in functions_set:
                        continue
                    taxid = re.match(r"taxon:(\d+)", line_split[12]).groups()[0]
                    # reduce to specific TaxIDs
                    if taxid_2_ignore_set is not None:
                        if taxid in taxid_2_ignore_set:
                            continue
                    line2write = an + "\t" + goid + "\n"
                    fh_out.write(line2write)

def get_keyword_2_upkan_dict():
    """
    UniProt-keyword 2 UPK-AccessionNumber
    :return: Dict(String2String)
    """
    fn = os.path.join(TABLES_DIR, 'Functions_table_UPK.txt')
    keyword_2_upkan_dict = {}
    with open(fn, "r") as fh:
        for line in fh:
            line_split = line.strip().split("\t")
            keyword = line_split[1]
            upkan = line_split[2]
            keyword_2_upkan_dict[keyword] = upkan
    return keyword_2_upkan_dict

# def parse_upk(fn_in, fn_out, protein_2_taxid=False, an_set=None):
def parse_upk(fn_in, fn_out, functions_set):
    """
    parse UniProt-Keywords file, write to table.txt for SQL
    :param fn_in: raw String
    :param fn_out: raw String
    :param functions_set: Set of String
    :return: None
    """
    keyword_2_upkan_dict = get_keyword_2_upkan_dict()
    # taxid = os.path.basename(fn_in).replace(".upk", "")
    with open(fn_out, "w") as fh_out:
        # with open(fn_in, "r") as fh_in:
        #     fh_in.next() # skip header
        #     for line in fh_in:
        gen = yield_line_uncompressed_or_gz_file(fn_in)
        next(gen)  # skip header Py3
        for line in gen:
            line_split = line.split('\t')
            an = line_split[0]
            keywords = set([ele.strip() for ele in line_split[-1].split(';')])
            if keywords == {""}:  # !!! is this the proper test?
                continue
            for keyword in keywords:
                try:
                    upk_an = keyword_2_upkan_dict[keyword]
                except KeyError:
                    print("keyword_2_upkan_dict KeyError: {}".format(keyword))
                    continue
                if upk_an not in functions_set:
                    continue
                line2write = an + "\t" + upk_an + "\n"
                fh_out.write(line2write)

def create_Protein_2_Function_table(fn_out_temp, verbose=False):
    """
    check that all associations are in the respective Ontology
    e.g. protein with associations A, B, C but C is not in GOterms Ontology any more, therefore remove the association C from protein
    :return:
    """
    print("create_Protein_2_Function_table")
    fn_list_tables, taxid_list_gaf = [], []
    create_Protein_2_Function_table_KEGG(COLUMN_CROSSREF="kegg")
    fn_list_tables.append(os.path.join(TABLES_DIR, "Protein_2_Function_table_KEGG.txt"))
    fn_list = os.listdir(DOWNLOADS_DIR)
    fn_list = sorted(fn_list)
    if verbose:
        print("#"*90, "parsing START")
    functions_set = get_possible_ontology_functions_set() # GO and UPK not KEGG
    for fn in fn_list:
        if fn.endswith(".gaf"): # do all of these first to collect TaxIDs to ignore when parsing ".gaf.gz"
            taxid = fn.replace(".gaf", "")
            fn_gaf = os.path.join(DOWNLOADS_DIR, fn)
            fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_GO_{}.txt".format(taxid))
            fn_list_tables.append(fn_out)
            parse_goa_gaf(fn_gaf, fn_out, functions_set)
            if verbose:
                print(fn, fn_out)
            taxid_list_gaf.append(taxid)  # these TaxIDs have curated/filtered annotations, therefore skip them in unfiltered big file

    for fn in fn_list:
        if fn.endswith(".gaf.gz"):
            taxid = fn.replace(".gaf.gz", "")
            fn_gaf_gz = os.path.join(DOWNLOADS_DIR, fn)
            fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_GO_{}.txt".format(taxid))
            if verbose:
                print("Parsing {}".format(fn_gaf_gz))
                print(fn, fn_out)
            fn_list_tables.append(fn_out)
            parse_goa_gaf(fn_gaf_gz, fn_out, functions_set, taxid_2_ignore_set=taxid_list_gaf)

        elif fn.endswith(".upk"):
            taxid = fn.replace(".upk", "")
            fn_upk = os.path.join(DOWNLOADS_DIR, fn)
            fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_UPK_{}.txt".format(taxid))
            fn_list_tables.append(fn_out)
            if verbose:
                print(fn, fn_out)
            parse_upk(fn_upk, fn_out, functions_set)

        elif fn.endswith(".upk.gz"):
            taxid = fn.replace(".upk.gz", "")
            fn_upk = os.path.join(DOWNLOADS_DIR, fn)
            fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_UPK_{}.txt".format(taxid))
            fn_list_tables.append(fn_out)
            if verbose:
                print(fn, fn_out)
            parse_upk(fn_upk, fn_out, functions_set)
    if verbose:
        print("#" * 90, "parsing STOP")

    # fn_out_temp = os.path.join(TABLES_DIR, "Protein_2_Function_table_temp.txt")
    if verbose:
        print("concatenate_files")
        # print(fn_list_tables, fn_out_temp)
    concatenate_files(fn_list_tables, fn_out_temp)

def create_Protein_2_Function_table_wide_format(verbose=False):
    fn_out_temp = os.path.join(TABLES_DIR, "Protein_2_Function_table_temp.txt")
    fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table.txt")
    create_Protein_2_Function_table(fn_out_temp, verbose)
    if verbose:
        print("converting Protein_2_Function_table to wide format")
    shellcmd = "LC_ALL=C gsort --parallel {} {} -o {}".format(NUMBER_OF_PROCESSES, fn_out_temp, fn_out_temp)  # sort in-place on first column which is protein_AN
    if verbose:
        print(shellcmd)
    call(shellcmd, shell=True)
    long_2_wide_format(fn_out_temp, fn_out)
    if verbose:
        print("done with Protein_2_Function_table")

def long_2_wide_format(fn_in, fn_out):
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
                    fh_out.write(an_last + "\t{" + ','.join('"' + item + '"' for item in set(function_list)) + "}\n")
                    function_list = []
                    an_last = an
                    function_list.append(function_)
            fh_out.write(an + "\t{" + ','.join('"' + item + '"' for item in set(function_list)) + "}\n")

def parse_secondary_AccessionNumbers(fn):
    line_generator = yield_line_uncompressed_or_gz_file(fn)
    line = next(line_generator)
    while not line.startswith("Secondary AC"):
        line = next(line_generator)
        continue
    _ = next(line_generator)
    for line in line_generator:
        secondary, primary = line.strip().split()
        yield secondary, primary

def create_Protein_Secondary_2_Primary_AN():
    fn_in = os.path.join(DOWNLOADS_DIR, "sec_ac.txt")
    fn_out = os.path.join(TABLES_DIR, "Protein_Secondary_2_Primary_AN_table.txt")
    gen = parse_secondary_AccessionNumbers(fn_in)
    with open(fn_out, "w") as fh:
        for secondary, primary in gen:
            line_2_write = secondary + "\t" + primary + "\n"
            fh.write(line_2_write)

##### GO_2_Slim_table.txt
def create_GO_2_Slim_table():
    print("create_GO_2_Slim_table")
    fn = os.path.join(DOWNLOADS_DIR, "goslim_generic.obo")
    obo = OBOReader(fn)
    fn_out = os.path.join(TABLES_DIR, "GO_2_Slim_table.txt")
    with open(fn_out, "w") as fh_out:
        for entry in obo:
            id_, name, is_a_list, definition = entry
            line2write = id_ + "\t" + "1" + "\n"
            fh_out.write(line2write)

def find_tables_to_remove():
    files_2_remove_list = []
    for fn in os.listdir(TABLES_DIR):
        if not fnmatch.fnmatch(fn, "*_table.txt") and fnmatch.fnmatch(fn, "*.txt"):
            files_2_remove_list.append(os.path.join(TABLES_DIR, fn))
    return files_2_remove_list

def remove_files(fn_list):
    for fn in fn_list:
        if fn in FILES_NOT_2_DELETE:
            continue
        else:
            os.remove(fn)

def parse_kegg_prot_2_path_file_to_dict(fn):
    """
    fn_psm = r"/home/green1/dblyon/kegg_prot_2_path_dict_file.txt"
    kegg_prot_2_path_dict = parse_kegg_prot_2_path_file_to_dict(fn)
    """
    kegg_prot_2_path_dict = {}
    with open(fn, "r") as fh:
        for line in fh:
            prot_an, path_an = line.strip().split("\t")
            kegg_prot_2_path_dict[prot_an] = path_an.split(";")
    return kegg_prot_2_path_dict

def get_df_UniProt_2_KEGG_mapping(fn, COLUMN_CROSSREF): #!!! does this file look the way it should???
    """
    fn = r"/Users/dblyon/modules/cpr/metaprot/sql/downloads/UniProt_2_KEGG_mapping.tab"
    COLUMN_CROSSREF="Cross-reference (KEGG)"
    df = get_df_UniProt_2_KEGG_mapping(fn, COLUMN_CROSSREF)
    """
    df = pd.read_csv(fn, sep='\t')
    # 3 letter code KEGG abbreviation
    df["Abb"] = df[COLUMN_CROSSREF].apply(lambda s: s[0:3])
    df.sort_values(["Abb", COLUMN_CROSSREF], inplace=True)
    return df

def create_Protein_2_Function_table_KEGG(fn_in=None, COLUMN_CROSSREF="Cross-reference (KEGG)"):
    """
    ##### map UniProt AN to KEGG pathways
    ### use UniProt mapping from UniProt protein AN to KEGG protein AN
    ### map KEGG protein AN to KEGG pathway AN via Lars's download of last freely available KEGG:
    ### home/purple1/databases/KEGG/genes/organisms/Specific3CharFolder/*_pathway.list --> parsed into kegg_prot_2_path_dict
    ### map pathway an to pathway name via:
    ###  /home/purple1/databases/KEGG/pathway/pathway.list
    ################################################################################################################
    ##### flow
    an = "P31946"

    UniProt_2_KEGG_mapping.tab
    -->
    "hsa:7529"

    /home/purple1/databases/KEGG/genes/organismns/hsa/hsa_pathways.list
    -->
    hsa:7529    path:hsa04110
    hsa:7529    path:hsa04114
    hsa:7529    path:hsa04722

    # create Protein_2_Function_table_KEGG.txt
    an = "P31946"
    function = "KEGG:04110"

    # create
    /home/purple1/databases/KEGG/pathway/pathway.list
    -->
    04110    Cell cycle
    ################################################################################################################
    # check if Functions_table_KEGG_static.txt is equal or subset of pathway.list
    # add KEGG pathway.list to functions table if not existing yet, or rather only use the this resource and not

    fn_psm = "Protein_2_Function_table_KEGG.txt"
    fn = r"/Users/dblyon/modules/cpr/metaprot/sql/downloads/UniProt_2_KEGG_mapping.tab"
    df_up_2_kegg = get_df_UniProt_2_KEGG_mapping(fn, COLUMN_CROSSREF="Cross-reference (KEGG)")

    kegg_prot_2_path_dict = parse_kegg_prot_2_path_file_to_dict(fn)
    kegg_prot_2_path_dict: key=String(KEGG_protein_an), val=ListOfString(KEGG_path_an)

    # DEBUG:
    no KEGG associations for given protein AN from mouse SwissProt entry
    function_type = "KEGG"
    limit_2_parent = None
    basic_or_slim = "basic"
    protein_ans_list = ["Q6DFV6"]
    assoc_dict = query.get_association_dict(connection, protein_ans_list, function_type, limit_2_parent, basic_or_slim)
    assoc_dict

    but AN in mapping
    grep "Q6DFV6" UniProt_2_KEGG_mapping.tab
    --> Q6DFV6    mmu:333564;

    e.g. debug usage
    import create_SQL_tables as cst
    DOWNLOADS_DIR = r"/Volumes/Speedy/PostgreSQL/downloads"
    COLUMN_CROSSREF="Cross-reference (KEGG)"
    fn = os.path.join(DOWNLOADS_DIR, "UniProt_2_KEGG_mapping.tab")
    df_up_2_kegg = cst.get_df_UniProt_2_KEGG_mapping(fn, COLUMN_CROSSREF)
    fn = os.path.join(DOWNLOADS_DIR, "KEGG_prot_2_path_dict_static.txt")
    kegg_prot_2_path_dict = cst.parse_kegg_prot_2_path_file_to_dict(fn)
    an = "Q6DFV6"
    kegg_an = df_up_2_kegg.loc[df_up_2_kegg["Entry"] == an, "Cross-reference (KEGG)"].values[0].split(";")[0]
    print kegg_an
    print kegg_prot_2_path_dict[kegg_an] # --> key error
    """
    if fn_in is None:
        fn_in = os.path.join(DOWNLOADS_DIR, "UniProt_2_KEGG_mapping.tab")
    df_up_2_kegg = get_df_UniProt_2_KEGG_mapping(fn_in, COLUMN_CROSSREF)
    # column_crossref_index = df_up_2_kegg.columns.tolist().index(COLUMN_CROSSREF) + 1

    fn = os.path.join(STATIC_DIR, "KEGG_prot_2_path_dict_static.txt")
    kegg_prot_2_path_dict = parse_kegg_prot_2_path_file_to_dict(fn)

    fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_KEGG.txt")
    with open(fn_out, "w") as fh:
        for row in df_up_2_kegg.itertuples():
            # up_an = row.Entry
            up_an = row[1]
            # kegg_prot_ans_string = row[column_crossref_index]
            kegg_prot_ans_string = row[2]

            ## three_char_KEGG_code = row["Abb"]
            # potentially multiple Cross-referenced KEGG protein ANs
            # kegg_prot_ans_string = row[COLUMN_CROSSREF]
            # and for each KEGG protein AN, potentially multiple KEGG pathway ANs
            kegg_prot_ans_list = [ele for ele in kegg_prot_ans_string.split(";") if len(ele) > 0]
            for kegg_prot in kegg_prot_ans_list:
                try:
                    kegg_path_an_list = kegg_prot_2_path_dict[kegg_prot]
                except KeyError:
                    continue
                for kegg_path in kegg_path_an_list:
                    string_2_write = up_an + "\t" + "KEGG:{}".format(kegg_path[3:]) + "\n"
                    fh.write(string_2_write)

def create_Functions_table_KEGG(): # STATIC FILE simply provide the finished table
    # static
    type_ = "KEGG"
    fn_in = os.path.join(STATIC_DIR, "KEGG_AN_2_Pathway_static.txt")
    fn_out = os.path.join(STATIC_DIR, "Functions_table_KEGG_static.txt")
    with open(fn_out, "w") as fh_out:
        with open(fn_in, "r") as fh_in:
            for line in fh_in:
                if line.startswith("#"):
                    continue
                an, name = line.strip().split("\t")
                an = "KEGG:" + an
                string_2_write = type_ + "\t" + name + "\t" + an + "\n"
                fh_out.write(string_2_write)

def create_tables(verbose=False):
    """
    :return: None
    """
    ### - OGs
    ### - OG_2_Function
    ### STATIC FILE simply provide the finished table
    ### create_OGs_table_and_OG_2_Function_table_and_Functions_table_DOM()

    ### - Functions
    create_Child_2_Parent_table_GO__and__Functions_table_GO__and__Function_2_definition_GO()
    create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK()
    ### create_Functions_table_KEGG() # STATIC FILE simply provide the finished table
    fn_list = [os.path.join(TABLES_DIR, fn) for fn in ["Functions_table_GO.txt", "Functions_table_UPK.txt"]]
    fn_list += [os.path.join(STATIC_DIR, fn) for fn in ["Functions_table_KEGG_static.txt", "Functions_table_DOM_static.txt"]]
    fn_out = os.path.join(TABLES_DIR, "Functions_table.txt")
    ### dependency on create_OGs_table_and_OG_2_Function_table_and_Functions_table_KEGG_DOM
    concatenate_files(fn_list, fn_out)

    ### - Function_2_definition (obsolete, since definitions added to Functions_table as a column)
    #fn_list = [os.path.join(TABLES_DIR, fn) for fn in ["Function_2_definition_table_UPK.txt", "Function_2_definition_table_GO.txt"]]
    #fn_out = os.path.join(TABLES_DIR, "Function_2_definition_table.txt")
    #concatenate_files(fn_list, fn_out)


    ## - Ontologies (Child_2_Parent)
    fn_list = [os.path.join(TABLES_DIR, fn) for fn in ["Child_2_Parent_table_GO.txt", "Child_2_Parent_table_UPK.txt"]]
    fn_out = os.path.join(TABLES_DIR, "Ontologies_table.txt")
    create_Ontologies_table(fn_list, fn_out)

    ### - Protein_2_OG
    ### STATIC FILE simply provide the finished table
    ### create_Protein_2_OG_table()

    ### - Protein_2_Function (updated, dependency on Ontologies since, only functions that are present in ontology should be assigned)
    create_Protein_2_Function_table_wide_format(verbose=verbose)
    create_Protein_Secondary_2_Primary_AN()

    ### - GO_2_Slim
    create_GO_2_Slim_table()
    if verbose:
        print("#"*80, "finished creating all tables")

def get_possible_ontology_functions_set():
    fn = os.path.join(TABLES_DIR, "Ontologies_table.txt")
    df = pd.read_csv(fn, sep='\t', header=None)
    functions_set = set(df[0].tolist() + df[1].tolist())
    return functions_set

def create_bash_scripts_for_DB(testing=False, foragotool=False):
    """
    psql -h localhost -d agotool -c "CREATE TABLE function_2_definition (
    an text,
    definition text);"

    psql -h localhost -d agotool -c "COPY function_2_definition FROM '{}';"

    psql -h localhost -d agotool -c "CREATE INDEX function_2_definition_an_idx ON function_2_definition(an);"
    psql -h localhost -d agotool -c "CREATE INDEX functions_an_idx ON functions(an);"
    psql -h localhost -d agotool -c "CREATE INDEX go_2_slim_an_idx ON go_2_slim(an);"
    psql -h localhost -d agotool -c "CREATE INDEX ontologies_child_idx ON ontologies(child);"
    psql -h localhost -d agotool -c "CREATE INDEX ontologies_direct_idx ON ontologies(direct);"
    psql -h localhost -d agotool -c "CREATE INDEX ontologies_type_idx ON ontologies(type);"
    psql -h localhost -d agotool -c "CREATE INDEX protein_secondary_2_primary_an_sec_idx ON protein_secondary_2_primary_an(sec);"

    :return: String(executable bash script)
    """
    global TABLES_DIR
    print("creating bash scripts to for PostgreSQL DB creation")
    if testing:
        TABLES_DIR = TEST_DIR
    functions_table = os.path.join(TABLES_DIR, "Functions_table.txt")
    # function_2_definition_table = os.path.join(TABLES_DIR, "Function_2_definition_table.txt")
    go_2_slim_table = os.path.join(TABLES_DIR, "GO_2_Slim_table.txt")
    og_2_function_table = os.path.join(STATIC_DIR, "OG_2_Function_table_static.txt")
    ogs_table = os.path.join(STATIC_DIR, "OGs_table_static.txt")
    ontologies_table = os.path.join(TABLES_DIR, "Ontologies_table.txt")
    protein_2_function_table = os.path.join(TABLES_DIR, "Protein_2_Function_table.txt")
    protein_2_og_table = os.path.join(STATIC_DIR, "Protein_2_OG_table_static.txt")
    protein_secondary_2_primary_an_table = os.path.join(TABLES_DIR, "Protein_Secondary_2_Primary_AN_table.txt")

    if not foragotool:
        postgres_commands = '''#!{}
psql -h localhost -d postgres -c "DROP DATABASE agotool;"
psql -h localhost -d postgres -c "CREATE DATABASE agotool;"

psql -h localhost -d agotool -c "CREATE TABLE functions (
    type text,
    name text,
    an text,
    definition text);"
psql -h localhost -d agotool -c "CREATE TABLE go_2_slim (
    an text,    
    slim boolean);"
psql -h localhost -d agotool -c "CREATE TABLE ogs (
    og text,    
    description text);"
psql -h localhost -d agotool -c "CREATE TABLE og_2_function (
    og text,
    function text);"
psql -h localhost -d agotool -c "CREATE TABLE ontologies (
    child text,
    parent text,
    direct boolean,
    type integer);"
psql -h localhost -d agotool -c "CREATE TABLE protein_2_function (
    an text,
    function text ARRAY);"    
psql -h localhost -d agotool -c "CREATE TABLE protein_secondary_2_primary_an (
    sec text,
    pri text);"
psql -h localhost -d agotool -c "CREATE TABLE protein_2_og (
    an text,
    og text);"

psql -h localhost -d agotool -c "COPY functions FROM '{}';"
psql -h localhost -d agotool -c "COPY go_2_slim FROM '{}';"
psql -h localhost -d agotool -c "COPY ogs FROM '{}';"
psql -h localhost -d agotool -c "COPY og_2_function FROM '{}';"
psql -h localhost -d agotool -c "COPY ontologies FROM '{}';"
psql -h localhost -d agotool -c "COPY protein_2_function FROM '{}';"
psql -h localhost -d agotool -c "COPY protein_secondary_2_primary_an FROM '{}';"
psql -h localhost -d agotool -c "COPY protein_2_og FROM '{}';"

psql -h localhost -d agotool -c "CREATE INDEX ogs_og_idx ON ogs(og);"
psql -h localhost -d agotool -c "CREATE INDEX og_2_function_og_idx ON og_2_function(og);"
psql -h localhost -d agotool -c "CREATE INDEX protein_2_function_an_idx ON protein_2_function(an);"
psql -h localhost -d agotool -c "CREATE INDEX protein_2_og_an_idx ON protein_2_og(an);"'''.format(BASH_LOCATION,
        functions_table, go_2_slim_table,
        ogs_table, og_2_function_table, ontologies_table,
        protein_2_function_table, protein_secondary_2_primary_an_table, protein_2_og_table)
    else: #sudo -u postgres
        postgres_commands = '''#!{}
psql -d postgres -c "DROP DATABASE agotool;"
psql -d postgres -c "CREATE DATABASE agotool;"

psql -d agotool -c "CREATE TABLE functions (
    type text,
    name text,
    an text,
    definition text);"
psql -d agotool -c "CREATE TABLE go_2_slim (
    an text,    
    slim boolean);"
psql -d agotool -c "CREATE TABLE ogs (
    og text,    
    description text);"
psql -d agotool -c "CREATE TABLE og_2_function (
    og text,
    function text);"
psql -d agotool -c "CREATE TABLE ontologies (
    child text,
    parent text,
    direct boolean,
    type integer);"
psql -d agotool -c "CREATE TABLE protein_2_function (
    an text,
    function text ARRAY);"    
psql -d agotool -c "CREATE TABLE protein_secondary_2_primary_an (
    sec text,
    pri text);"
psql -d agotool -c "CREATE TABLE protein_2_og (
    an text,
    og text);"

psql -d agotool -c "\copy functions FROM '{}';"
psql -d agotool -c "\copy go_2_slim FROM '{}';"
psql -d agotool -c "\copy ogs FROM '{}';"
psql -d agotool -c "\copy og_2_function FROM '{}';"
psql -d agotool -c "\copy ontologies FROM '{}';"
psql -d agotool -c "\copy protein_2_function FROM '{}';"
psql -d agotool -c "\copy protein_secondary_2_primary_an FROM '{}';"
psql -d agotool -c "\copy protein_2_og FROM '{}';"

psql -d agotool -c "CREATE INDEX ogs_og_idx ON ogs(og);"
psql -d agotool -c "CREATE INDEX og_2_function_og_idx ON og_2_function(og);"
psql -d agotool -c "CREATE INDEX protein_2_function_an_idx ON protein_2_function(an);"
psql -d agotool -c "CREATE INDEX protein_2_og_an_idx ON protein_2_og(an);"'''.format(BASH_LOCATION, functions_table, go_2_slim_table, ogs_table, og_2_function_table, ontologies_table, protein_2_function_table, protein_secondary_2_primary_an_table, protein_2_og_table)


    if testing:
        postgres_commands = postgres_commands.replace(" agotool", " agotool_test")

    fn_out = os.path.join(POSTGRESQL_DIR, "fn_create_DB_copy_and_index_tables.sh")
    with open(fn_out, "w") as fh:
        fh.write(postgres_commands)
    shellcmd = "chmod 744 {}".format(fn_out)
    call(shellcmd, shell=True)
    return fn_out

def call_script(BASH_LOCATION, script_fn):
    shellcmd = "{} {}".format(BASH_LOCATION, script_fn)
    print(shellcmd)
    call(shellcmd, shell=True)

if __name__ == "__main__":
    debug = True
    if debug:
        start_time = time.time()
        # remove_files(find_tables_to_remove())
        # print(find_tables_to_remove())
        ### PostgreSQL DB creation, copy from file and indexing
        create_test_tables(50000, TABLES_DIR)
        fn_create_DB_copy_and_index_tables = create_bash_scripts_for_DB(testing=False, foragotool=True)
        print("PostgreSQL DB creation, copy from file, and indexing")
        call_script(BASH_LOCATION, fn_create_DB_copy_and_index_tables)
        tools.print_runtime(start_time)
    else:
        start_time = time.time()
        print("Parsing downloaded content and writing tables for PostgreSQL import")
        create_tables(verbose=True)
        create_test_tables(50000, TABLES_DIR)
        remove_files(find_tables_to_remove())

        ### PostgreSQL DB creation, copy from file and indexing
        fn_create_DB_copy_and_index_tables = create_bash_scripts_for_DB(testing=False)
        print("PostgreSQL DB creation, copy from file, and indexing")
        call_script(BASH_LOCATION, fn_create_DB_copy_and_index_tables)
        tools.print_runtime(start_time)

