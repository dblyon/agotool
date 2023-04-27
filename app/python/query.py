from __future__ import print_function
import pickle
import numpy as np
import pandas as pd
import os, sys, datetime
from collections import defaultdict
import psycopg2
import socket
hostname = socket.gethostname()
import time
### import user modules
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import variables, obo_parser, taxonomy, tools
import run_cythonized

# UNSIGNED_2_SIGNED_CONSTANT = int(math.pow(2, 63))
FN_KEYWORDS = variables.FN_KEYWORDS
FN_GO_SLIM = variables.FN_GO_SLIM
FN_GO_BASIC = variables.FN_GO_BASIC
VERSION_ = variables.VERSION_

upkTerm_2_functionAN_dict = {u'Biological process': u'UPK:9999',
                             u'Cellular component': u'UPK:9998',
                             u'Coding sequence diversity': u'UPK:9997',
                             u'Developmental stage': u'UPK:9996',
                             u'Disease': u'UPK:9995',
                             u'Domain': u'UPK:9994',
                             u'Ligand': u'UPK:9993',
                             u'Molecular function': u'UPK:9992',
                             u'Post-translational modification': u'UPK:9991',
                             u'PTM': u'UPK:9991',
                             u'Technical term': u'UPK:9990'}

humanName_2_functionAN_dict = {u"BP": u"GO:0008150",
                               u"CP": u"GO:0005575",
                               u"MF": u"GO:0003674",
                               u"Biological Process": u"GO:0008150",
                               u"Cellular Component": u"GO:0005575",
                               u"Molecular Function": u"GO:0003674"}

functionType_term_2_an_dict = {"UPK": upkTerm_2_functionAN_dict,
                               "GO": humanName_2_functionAN_dict}


def get_cursor():

    if hostname in {"aquarius.meringlab.org", "atlas", "gaia", "phobos", "deimos", "pisces"}: # use agotool/app/env_file, which isn't in git repo for security, using local Postgres
        env_dict = variables.param_2_val_dict
        USER = env_dict['POSTGRES_USER']
        PWD = env_dict['POSTGRES_PASSWORD']
        DBNAME = env_dict['POSTGRES_DB']
        PORT = env_dict['PORT_NUMBER']
        HOST = 'localhost'
        return get_cursor_connect(host=HOST, dbname=DBNAME, user=USER, port=PORT, password=PWD)

    platform_ = sys.platform
    if platform_ == "linux":
        if not variables.DB_DOCKER: # use local Postgres
            try:
                USER = "postgres"
                PWD = os.environ['POSTGRES_PASSWORD']
                DBNAME = os.environ['POSTGRES_DB']
                PORT = '5432'
                HOST = 'db'
            except KeyError:
                print("query.py says there is something wrong with the Postgres config")
                raise StopIteration
            return get_cursor_connect(host=HOST, dbname=DBNAME, user=USER, port=PORT, password=PWD)
        else: # use dockerized Postgres directly from native OS
            PORT = variables.Docker_incoming_PostgreSQL_port # '5913'
            HOST = 'localhost'
            param_2_val_dict = variables.param_2_val_dict
            return get_cursor_connect(host=HOST, dbname=param_2_val_dict["POSTGRES_DB"], user=param_2_val_dict["POSTGRES_USER"], password=param_2_val_dict["POSTGRES_PASSWORD"], port=PORT)

    elif platform_ == "darwin":
        if not variables.DB_DOCKER: # use local Postgres
            return get_cursor_ody()
        else: # connect to docker Postgres container. use dockerized Postgres directly from native OS
            PORT = variables.Docker_incoming_PostgreSQL_port # '5913'
            HOST = 'localhost'
            param_2_val_dict = variables.param_2_val_dict
            return get_cursor_connect(host=HOST, dbname=param_2_val_dict["POSTGRES_DB"], user=param_2_val_dict["POSTGRES_USER"], password=param_2_val_dict["POSTGRES_PASSWORD"], port=PORT)
    else:
        print("query.get_cursor() doesn't know how to connect to Postgres")
        raise StopIteration

def get_cursor_ody(dbname='agotool'):
    """
    :param dbname:
    :return: DB Cursor instance object
    """
    conn_string = "dbname='{}'".format(dbname)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return cursor

def get_cursor_connect(host, dbname, user, password, port):
    conn_string = "host='{}' dbname='{}' user='{}' password='{}' port='{}'".format(host, dbname, user, password, port)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return cursor

def query_example():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM functions LIMIT 5")
    records = cursor.fetchall()
    cursor.close()
    print(records)

def get_results_of_statement(sql_statement):
    cursor = get_cursor()
    cursor.execute(sql_statement)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_function_type_id_2_name_dict(function_type):
    result = get_results_of_statement("SELECT functions.an, functions.name FROM functions WHERE functions.etype='{}'".format(function_type))
    id_2_name_dict = {}
    for res in result:
        id_ = res[0]
        name = res[1]
        id_2_name_dict[id_] = name
    return id_2_name_dict

class PersistentQueryObject:
    """
    aGOtool version
    used to query protein 2 functional associations
    only protein_2_function is queried in Postgres,
    everything else is in memory but still deposited in the DB any way
    """
    def __init__(self):
        self.secondary_2_primary_an_dict = self.get_secondary_2_primary_an_dict()
        self.type_2_association_dict = self.get_type_2_association_dict()
        self.go_slim_set = self.get_go_slim_terms()
        self.KEGG_functions_set = self.get_functions_set_from_functions(function_type="KEGG")
        self.DOM_functions_set = self.get_functions_set_from_functions(function_type="DOM")
        self.UPK_functions_set = self.get_ontology_set_of_type("UPK", "")
        self.BP_basic_functions_set = self.get_ontology_set_of_type("BP", "basic")
        self.MF_basic_functions_set = self.get_ontology_set_of_type("MF", "basic")
        self.CP_basic_functions_set = self.get_ontology_set_of_type("CP", "basic")

        ##### pre-load go_dag and goslim_dag (obo files) for speed, also filter objects
        upk_dag = obo_parser.GODag(obo_file=FN_KEYWORDS, upk=True)
        self.upk_dag = upk_dag

        goslim_dag = obo_parser.GODag(obo_file=FN_GO_SLIM)
        self.goslim_dag = goslim_dag

        # go_dag.update_association() #???
        go_dag = obo_parser.GODag(obo_file=FN_GO_BASIC)
        for go_term in go_dag.keys():
            _ = go_dag[go_term].get_all_parents()
        self.go_dag = go_dag

        # for backtracking
        self.child_2_parent_dict = self.get_child_2_parent_dict()

        KEGG_pseudo_dag = obo_parser.KEGG_pseudo_dag()
        self.KEGG_pseudo_dag = KEGG_pseudo_dag

        DOM_pseudo_dag = obo_parser.DOM_pseudo_dag()
        self.DOM_pseudo_dag = DOM_pseudo_dag


    @staticmethod
    def get_secondary_2_primary_an_dict():
        secondary_2_primary_dict = {}
        result = get_results_of_statement("SELECT secondary_2_primary_id.sec, secondary_2_primary_id.prim FROM secondary_2_primary_id;")
        for res in result:
            secondary = res[0]
            primary = res[1]
            secondary_2_primary_dict[secondary] = primary
        return secondary_2_primary_dict

    @staticmethod
    def get_type_2_association_dict():
        result = get_results_of_statement("SELECT ontologies.child, ontologies.parent, ontologies.etype FROM ontologies;")
        type_2_association_dict = {}
        for res in result:
            child = res[0]
            parent = res[1]
            type_ = res[2]
            if type_ in type_2_association_dict:
                type_2_association_dict[type_].update([child, parent])
            else:
                type_2_association_dict[type_] = {child, parent}
        return type_2_association_dict

    @staticmethod
    def get_go_slim_terms():
        result = get_results_of_statement("SELECT go_2_slim.an FROM go_2_slim;")
        go_slim_set = set()
        for res in result:
            go_slim_set.update([res[0]])
        return go_slim_set

    @staticmethod
    def get_functions_set_from_functions(function_type):
        result = get_results_of_statement("SELECT functions.an FROM functions WHERE functions.type='{}'".format(function_type))
        functions_set = set()
        for res in result:
            functions_set.update([res[0]])
        return functions_set

    def get_ontology_set_of_type(self, function_type, go_slim_or_basic):
        """
        select all parents and children of given type_
        "UPK": -51
        "BP": -21
        "MF": -22
        "CP": -23
        "all_GO": [-21, -22, -23]

        # choices = (("all_GO", "all GO categories"), ("BP", "GO Biological Process"),
        ("CP", "GO Celluar Compartment"), ("MF", "GO Molecular Function"),
        ("UPK", "UniProt keywords"))

        'GO:0003674': "-23",  # 'Molecular Function',
        'GO:0005575': "-22",  # 'Cellular Component',
        'GO:0008150': "-21",  # 'Biological Process',
        'UPK:9990': "-51",  # 'Technical term',

        :param function_type: String (one of "all_GO", "UPK", "BP", "MF", "CP")
        :param go_slim_or_basic: String ("slim" or "basic")
        :return: Set of String
        """
        #!!! potential speed up with "|=" instead of ".union()"
        if function_type == "all_GO":
            if go_slim_or_basic == "basic":
                return self.type_2_association_dict[-21].union(self.type_2_association_dict[-22]).union(self.type_2_association_dict[-23])
            else: # slim
                return self.go_slim_set

        elif function_type == "UPK":
            return self.type_2_association_dict[-51]

        elif function_type == "BP":
            if go_slim_or_basic == "basic":
                return self.type_2_association_dict[-21]
            else:
                return self.type_2_association_dict[-21].intersection(self.go_slim_set)

        elif function_type == "MF":
            if go_slim_or_basic == "basic":
                return self.type_2_association_dict[-22]
            else:
                return self.type_2_association_dict[-22].intersection(self.go_slim_set)

        elif function_type == "CP":
            if go_slim_or_basic == "basic":
                return self.type_2_association_dict[-23]
            else:
                return self.type_2_association_dict[-23].intersection(self.go_slim_set)
        else:
            print("entity_type: '{}' does not exist".format(function_type))
            raise StopIteration

    def get_association_dict(self, protein_ans_list, gocat_upk, basic_or_slim): #, backtracking=True):
        """
        :param protein_ans_list: ListOfString
        :param gocat_upk: String (one of "GO", "UPK", "KEGG", "DOM")
        :param basic_or_slim: String (one of "basic" or "slim")
        :param backtracking: Bool (Flag to add parents of functional terms)
        :return: Dict(key: AN, val: SetOfAssociations)
        """
        an_2_functions_dict = defaultdict(lambda: set())
        if gocat_upk in {"GO", "UPK", "all_GO", "BP", "MF", "CP"}:
            association_set_2_restrict = self.get_ontology_set_of_type(gocat_upk, basic_or_slim)
        elif gocat_upk == "KEGG":
            association_set_2_restrict = self.KEGG_functions_set
        elif gocat_upk == "DOM":
            association_set_2_restrict = self.DOM_functions_set
        else:
            raise NotImplementedError
        protein_ans_list = str(protein_ans_list)[1:-1]
        result = get_results_of_statement("SELECT protein_2_function.an, protein_2_function.function FROM protein_2_function WHERE protein_2_function.an IN({});".format(protein_ans_list))
        for res in result:
            an = res[0]
            associations_list = res[1]
            an_2_functions_dict[an] = set(associations_list).intersection(association_set_2_restrict)
        # if backtracking:
        an_2_functions_dict = self.backtrack_child_terms(an_2_functions_dict, self.child_2_parent_dict)
            # for an, functions in an_2_functions_dict.items():
            #     parents_temp = set()
            #     for function_ in functions:
            #         try:
            #             parents_temp = parents_temp.union(self.child_2_parent_dict[function_])
            #         except KeyError:
            #             pass
            #     an_2_functions_dict[an] = an_2_functions_dict[an].union(parents_temp)
        return an_2_functions_dict

    @staticmethod
    def get_child_2_parent_dict(direct=False, type_=None, verbose=False):
        """
        SELECT ontologies.child, ontologies.parent FROM ontologies WHERE ontologies.type='-23' AND ontologies.direct=TRUE;
        :param direct: Bool (Flag to retrieve only direct parents or not)
        :param type_: None or Integer (restrict to entity-type, e.g. -21 for GO-terms of 'Biological process'
        :param verbose: Bool (Flag to print infos)
        :return: Dictionary ( key=child (String), val=set of parents (String) )
        """
        select_statement = "SELECT ontologies.child, ontologies.parent FROM ontologies"
        extend_stmt = ""
        if type_ is not None:
            extend_stmt += " WHERE ontologies.type='{}'".format(type_)
            if direct:
                extend_stmt += " AND ontologies.direct=TRUE"
        else:
            if direct:
                extend_stmt += " WHERE ontologies.direct=TRUE"

        sql_statement = select_statement + extend_stmt + ";"
        result = get_results_of_statement(sql_statement)
        child_2_parent_dict = {}
        if verbose:
            print(sql_statement)
            print("Number of rows fetched: ", len(result))
        for res in result:
            child, parent = res
            if child not in child_2_parent_dict:
                child_2_parent_dict[child] = {parent}
            else:
                child_2_parent_dict[child].update([parent])
        return child_2_parent_dict

    @staticmethod
    def backtrack_child_terms(an_2_functions_dict, child_2_parent_dict):
        for an, functions in an_2_functions_dict.items():
            parents_temp = set()
            for function_ in functions:
                try:
                    parents_temp = parents_temp.union(child_2_parent_dict[function_])
                except KeyError:
                    pass
            an_2_functions_dict[an] = an_2_functions_dict[an].union(parents_temp)
        return an_2_functions_dict


# from profilehooks import profile
# from profilehooks import timecall
# from profilehooks import coverage

class PersistentQueryObject_STRING(PersistentQueryObject):
    """
    used to query protein 2 functional associations function_enumeration_len
    only protein_2_function is queried in Postgres,
    everything else is in memory but still deposited in the DB any way
    """
    def __init__(self, low_memory=True, read_from_flat_files=None):
        # should have a call like this: super().__init() and then other things below
        if read_from_flat_files is None:
            read_from_flat_files = variables.READ_FROM_FLAT_FILES
        if variables.VERBOSE:
            print("#"*80)
            print("initializing PQO")
            print("getting taxid_2_proteome_count")
        self.taxid_2_proteome_count = get_Taxid_2_proteome_count_dict(read_from_flat_files=read_from_flat_files)

        if variables.VERBOSE:
            print("getting taxid_2_proteins_dict")
        self.taxid_2_proteins_dict = get_taxid_2_proteins_dict()

        if variables.VERBOSE:
            print("getting NCBI_taxonomy and TaxidSpecies_2_TaxidProteome_dict")
        try:
            self.ncbi = taxonomy.NCBI_taxonomy(taxdump_directory=variables.DOWNLOADS_DIR, for_SQL=False, update=False)
        except FileNotFoundError:
            self.ncbi = taxonomy.NCBI_taxonomy(taxdump_directory=variables.DOWNLOADS_DIR, for_SQL=False, update=True)
        with open(variables.tables_dict["TaxidSpecies_2_TaxidProteome_dict"], "rb") as fh_TaxidSpecies_2_TaxidProteome_dict:
            self.TaxidSpecies_2_TaxidProteome_dict = pickle.load(fh_TaxidSpecies_2_TaxidProteome_dict)

        if not low_memory:
            if variables.VERBOSE:
                print("getting Secondary_2_Primary_IDs_dict")
            self.Secondary_2_Primary_IDs_dict = get_Secondary_2_Primary_IDs_dict(read_from_flat_files=read_from_flat_files)

            print("getting KEGG Taxid 2 TaxName acronym translation")
        self.kegg_taxid_2_acronym_dict = get_KEGG_Taxid_2_acronym_dict(read_from_flat_files=True) # small file doesn't make sense to keep in DB for now

        if variables.VERBOSE:
            print("getting lookup arrays")
        # if not low_memory: # override variables if "low_memory" passed to query initialization
        self.year_arr, self.hierlevel_arr, self.entitytype_arr, self.functionalterm_arr, self.indices_arr, self.description_arr, self.category_arr = get_lookup_arrays(read_from_flat_files, from_pickle=True)
        self.function_enumeration_len = self.functionalterm_arr.shape[0]

        if variables.VERBOSE:
            print("getting cond arrays")
        self.etype_2_minmax_funcEnum = self.get_etype_2_minmax_funcEnum(self.entitytype_arr)
        self.etype_cond_dict = get_etype_cond_dict(self.etype_2_minmax_funcEnum, self.function_enumeration_len)
        self.etype_2_num_functions_dict = {}
        for etype, min_max in self.etype_2_minmax_funcEnum.items():
            self.etype_2_num_functions_dict["cond_{}".format(str(etype)[1:])] = min_max[1] - min_max[0] + 1
        self.cond_etypes_with_ontology = get_cond_bool_array_of_etypes(variables.entity_types_with_ontology, self.function_enumeration_len, self.etype_cond_dict)
        self.cond_etypes_rem_foreground_ids = get_cond_bool_array_of_etypes(variables.entity_types_rem_foreground_ids, self.function_enumeration_len, self.etype_cond_dict)
        self.goslimtype_2_cond_dict = get_goslimtype_2_cond_dict()

        if variables.VERBOSE:
            print("getting lineage dict")
        self.lineage_dict_enum = get_lineage_dict_enum(False, read_from_flat_files) # default is a set not array, check if this is necessary later
        self.lineage_dict = pickle.load(open(variables.tables_dict["lineage_dict_direct"], "rb"))

        if variables.VERBOSE:
            print("getting blacklisted terms")
        self.blacklisted_terms_bool_arr = self.get_blacklisted_terms_bool_arr()

        if not low_memory:
            # foreground
            if variables.VERBOSE:
                print("getting get_ENSP_2_functionEnumArray_dict")
            self.ENSP_2_functionEnumArray_dict = get_ENSP_2_functionEnumArray_dict(read_from_flat_files)

        if variables.VERBOSE:
            print("getting taxid_2_tuple_funcEnum_index_2_associations_counts")
        # background
        self.taxid_2_tuple_funcEnum_index_2_associations_counts = get_background_taxid_2_funcEnum_index_2_associations(read_from_flat_files, from_pickle=True) # from_pickle should reduce start-up time

        # set all versions of preloaded_objects_per_analysis
        if variables.VERBOSE:
            print("getting preloaded objects per analysis")
        self.reset_preloaded_objects_per_analysis()

        if variables.VERBOSE:
            print("finished with PQO init")
            print("go go GO and fly like the wind")
            print("#" * 80)

    def __repr__(self):
        return f"{self.__class__.__name__} @ {hex(id(self))}"

    def get_preloaded_objects_per_analysis(self):
        self.reset_preloaded_objects_per_analysis()
        return self.preloaded_objects_per_analysis

    def reset_preloaded_objects_per_analysis(self):
        self.preloaded_objects_per_analysis = run_cythonized.get_preloaded_objects_for_single_analysis(self.blacklisted_terms_bool_arr, self.function_enumeration_len)

    def get_static_preloaded_objects(self, low_memory=False):
        if not low_memory: # removed self.ENSP_2_tuple_funcEnum_score_dict
            static_preloaded_objects = (self.ENSP_2_functionEnumArray_dict, # high mem --> the only difference between low_memory versions
                                        self.year_arr, self.hierlevel_arr, self.entitytype_arr, self.functionalterm_arr, self.indices_arr,
                                        self.description_arr, self.category_arr, # previously high mem but only 62MB
                                        self.etype_2_minmax_funcEnum, self.function_enumeration_len, self.etype_cond_dict, self.etype_2_num_functions_dict,
                                        self.taxid_2_proteome_count, self.taxid_2_tuple_funcEnum_index_2_associations_counts, self.lineage_dict_enum, self.blacklisted_terms_bool_arr,
                                        self.cond_etypes_with_ontology, self.cond_etypes_rem_foreground_ids, self.kegg_taxid_2_acronym_dict,
                                        self.goslimtype_2_cond_dict) # DEPRECATED self.ENSP_2_rowIndex_dict, self.rowIndex_2_ENSP_dict, self.CSC_ENSPencoding_2_FuncEnum, self.CSR_ENSPencoding_2_FuncEnum,
                                        # self.Taxid_2_FunctionEnum_2_Scores_dict)
        else: # year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, etype_2_num_functions_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict, goslimtype_2_cond_dict
            static_preloaded_objects = (self.year_arr, self.hierlevel_arr, self.entitytype_arr, self.functionalterm_arr, self.indices_arr,
                                        self.description_arr, self.category_arr,  # high mem --> only 62 MB
                                        self.etype_2_minmax_funcEnum, self.function_enumeration_len, self.etype_cond_dict, self.etype_2_num_functions_dict,
                                        self.taxid_2_proteome_count, self.taxid_2_tuple_funcEnum_index_2_associations_counts, self.lineage_dict_enum, self.blacklisted_terms_bool_arr,
                                        self.cond_etypes_with_ontology, self.cond_etypes_rem_foreground_ids, self.kegg_taxid_2_acronym_dict,
                                        self.goslimtype_2_cond_dict) # DEPRECATED self.ENSP_2_rowIndex_dict, self.rowIndex_2_ENSP_dict, self.CSC_ENSPencoding_2_FuncEnum, self.CSR_ENSPencoding_2_FuncEnum,
                                        # self.Taxid_2_FunctionEnum_2_Scores_dict)
        return static_preloaded_objects

    def get_blacklisted_terms_bool_arr(self):
        blacklisted_terms_bool_arr = np.zeros(self.function_enumeration_len, dtype=np.dtype("uint8"))
        # use uint8 and code as 0, 1 instead to make into mem view
        for term_enum in variables.blacklisted_enum_terms:
            blacklisted_terms_bool_arr[term_enum] = True
        blacklisted_terms_bool_arr.flags.writeable = False
        return blacklisted_terms_bool_arr

    @staticmethod
    def get_etype_2_minmax_funcEnum(entitytype_arr):
        """
        start and stop positions of funcEnum_array grouped by entity type
        """
        etype_2_minmax_funcEnum = {}
        s = pd.Series(entitytype_arr)
        for name, group in s.groupby(s):
            etype_2_minmax_funcEnum[name] = (min(group.index), max(group.index))
        return etype_2_minmax_funcEnum

    def get_functional_term_2_level_dict(self):
        go_dag = obo_parser.GODag(obo_file=FN_GO_BASIC)
        upk_dag = obo_parser.GODag(obo_file=FN_KEYWORDS, upk=True)
        functerm_2_level_dict = defaultdict(lambda: np.nan)
        functerm_2_level_dict.update(self.get_functional_term_2_level_dict_from_dag(go_dag))
        functerm_2_level_dict.update(self.get_functional_term_2_level_dict_from_dag(upk_dag))
        return functerm_2_level_dict

    @staticmethod
    def get_functional_term_2_level_dict_from_dag(dag):
        functerm_2_level_dict = {}
        for name, term_object in dag.items():
            functerm_2_level_dict[name] = term_object.level
        return functerm_2_level_dict

    @staticmethod
    def get_GO_lineage_dict(go_dag):
        go_lineage_dict = {}
        # key=GO-term, val=set of GO-terms
        for go_term_name in go_dag:
            GOTerm_instance = go_dag[go_term_name]
            go_lineage_dict[go_term_name] = GOTerm_instance.get_all_parents().union(GOTerm_instance.get_all_children())
        return go_lineage_dict

    def get_proteome_count_from_taxid(self, taxid):
        try:
            return self.taxid_2_proteome_count[taxid]
        except KeyError:
            return False

    @staticmethod
    def get_association_dict_split_by_category(protein_ans_list):
        """
        backtracking is always True, since already backtracked functional associations in DB
        :param protein_ans_list: ListOfString
        :return: etype_2_association_dict(key=entity_type(String), val=Dict(key=AN(String), val=SetOfFunctions(String)))
        """
        etype_2_association_dict = {}
        for etype in variables.entity_types:
            etype_2_association_dict[etype] = {}
        result = get_results_of_statement("SELECT protein_2_function.an, protein_2_function.function, protein_2_function.etype FROM protein_2_function WHERE protein_2_function.an IN({});".format(str(protein_ans_list)[1:-1]))
        for res in result:
            an, associations_list, etype = res
            etype_2_association_dict[etype][an] = set(associations_list)
        return etype_2_association_dict

def get_lookup_arrays(read_from_flat_files=False, from_pickle=False):
    """
    low_memory=False --> doesn't pay to save mem here
    funcEnum_2_hierarchical_level
    simple numpy array of hierarchical levels
    if -1 in DB --> convert to np.nan since these are missing values
    # - funcEnum_2_year
    # - funcEnum_2_hierarchical_level
    # - funcEnum_2_etype
    # - funcEnum_2_description
    # - funcEnum_2_term
    :param low_memory: Bool flag to return description_array
    :param read_from_flat_files: Bool flag to get data from DB or flat files
    :return: immutable numpy array of int
    """
    if from_pickle:
        year_arr = pickle.load(open(variables.tables_dict["year_arr"], "rb"))
        hierlevel_arr = pickle.load(open(variables.tables_dict["hierlevel_arr"], "rb"))
        entitytype_arr = pickle.load(open(variables.tables_dict["entitytype_arr"], "rb"))
        functionalterm_arr = pickle.load(open(variables.tables_dict["functionalterm_arr"], "rb"))
        indices_arr = pickle.load(open(variables.tables_dict["indices_arr"], "rb"))
        description_arr = pickle.load(open(variables.tables_dict["description_arr"], "rb"))
        category_arr = pickle.load(open(variables.tables_dict["category_arr"], "rb"))
        return year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr
    if read_from_flat_files:
        # fn = os.path.join(variables.TABLES_DIR, "Functions_table_STRING.txt")
        fn = variables.tables_dict["Functions_table"]
        result = get_results_of_statement_from_flat_file(fn)
        result = list(result)
    else:
        result = get_results_of_statement("SELECT * FROM functions")
    shape_ = len(result)
    year_arr = np.full(shape=shape_, fill_value=-1, dtype="int16")  # Integer (-32768 to 32767)
    entitytype_arr = np.full(shape=shape_, fill_value=0, dtype="int8")
    # if not low_memory:
    #     description_arr = np.empty(shape=shape_, dtype=object) # ""U261"))
    #     category_arr = np.empty(shape=shape_, dtype=object)  # description of functional category (e.g. "Gene Ontology biological process") # category_arr = np.empty(shape=shape_, dtype=np.dtype("U49"))  # description of functional category (e.g. "Gene Ontology biological process")
    description_arr = np.empty(shape=shape_, dtype=object) # ""U261"))
    category_arr = np.empty(shape=shape_, dtype=object)  # description of functional category (e.g. "Gene Ontology biological process") # category_arr = np.empty(shape=shape_,
    functionalterm_arr = np.empty(shape=shape_, dtype=object) #np.dtype("U13"))
    hierlevel_arr = np.full(shape=shape_, fill_value=-1, dtype="int8")  # Byte (-128 to 127)
    indices_arr = np.arange(shape_, dtype=np.dtype("uint32"))
    indices_arr.flags.writeable = False

    for i, res in enumerate(result):
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
        # if not low_memory:
        #     description_arr[func_enum] = description
        #     category_arr[func_enum] = variables.entityType_2_functionType_dict[etype]
        description_arr[func_enum] = description
        category_arr[func_enum] = variables.entityType_2_functionType_dict[etype]

    year_arr.flags.writeable = False # make it immutable
    hierlevel_arr.flags.writeable = False
    entitytype_arr.flags.writeable = False
    functionalterm_arr.flags.writeable = False
    # if not low_memory:
        # description_arr.flags.writeable = False
        # category_arr.flags.writeable = False
        # return year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr
    # else:
    #     return year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr
    description_arr.flags.writeable = False
    category_arr.flags.writeable = False
    return year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr

def get_Taxid_2_FunctionEnum_2_Scores_dict(read_from_flat_files=False, as_array_or_as_list="array", taxid_2_proteome_count=None, from_pickle=False):
    """
    :param read_from_flat_files: strig flag
    :param as_array_or_as_list: string flag
    :param taxid_2_proteome_count: dict but if None it is a flag to not fill with zeros
    :return: dict
    """
    if from_pickle:
        with open(variables.tables_dict["Taxid_2_FunctionEnum_2_Scores_dict"], "rb") as fh:
            Taxid_2_FunctionEnum_2_Scores_dict = pickle.load(fh)
        return Taxid_2_FunctionEnum_2_Scores_dict

    Taxid_2_FunctionEnum_2_Scores_dict = {} #defaultdict(lambda: False)
    if read_from_flat_files:
        results = get_results_of_statement_from_flat_file(variables.tables_dict["Taxid_2_FunctionEnum_2_Scores_table"])
    else:
        raise NotImplementedError
    for res in results:
        taxid, functionEnumeration, scores_arr = res
        taxid = int(taxid)
        functionEnumeration = int(functionEnumeration)
        scores_list = [int(float(score)) for score in scores_arr[1:-1].split(",")]
        if taxid_2_proteome_count is not None:
            try:
                zeros_2_add = taxid_2_proteome_count[taxid] - len(scores_list)
                if zeros_2_add > 0:
                    scores_list = sorted(zeros_2_add*[0] + scores_list)
            except KeyError:
                print("get_Taxid_2_FunctionEnum_2_Scores_dict --> taxid_2_proteome_count taxid '{}' unknown".format(taxid))
        scores_list = sorted(scores_list)
        if as_array_or_as_list == "array":
            scores_arr = np.array(scores_list, dtype=np.dtype(variables.dtype_TM_score))  # previously ("float32")) # float16 would probably be sufficient
        elif as_array_or_as_list == "list":
            scores_arr = scores_list
        else:
            print("as_array_or_as_list: '{}' not known, please provide proper args".format(as_array_or_as_list))
            raise StopIteration
        if taxid not in Taxid_2_FunctionEnum_2_Scores_dict:
            Taxid_2_FunctionEnum_2_Scores_dict[taxid] = {functionEnumeration: scores_arr}
        else:
            Taxid_2_FunctionEnum_2_Scores_dict[taxid][functionEnumeration] = scores_arr
    return Taxid_2_FunctionEnum_2_Scores_dict

def get_proteinAN_2_tuple_funcEnum_score_dict(read_from_flat_files=True, fn=None): # SLOW ~ 26% of startup time
    """
    key = ENSP
    val = tuple(arr of function Enumeration, arr of scores)
    for BTO, DOID, and GO-CC terms

    exampe of return value {'3702.AT1G01010.1': (array([ 213,  254,  255], dtype=uint32),
          array([4.2     , 4.166357, 4.195121], dtype=float32)), ...
                 }

    Protein_2_FunctionEnum_and_Score_table_UPS_FIN.txt
    | 3702 | NAC1_ARATH | {211,252,253, ... } | {4.2,4.166357,4.195121, ... } |
    :return: dict (key = ENSP, val = tuple(arr of function Enumeration, arr of scores))
    """
    if variables.VERSION_ != "UniProt":
        print("Not implemented version {}".format(variables.VERSION_))
        raise StopIteration

    ENSP_2_tuple_funcEnum_score_dict = {}
    if read_from_flat_files:
        if fn is None:
            fn = variables.tables_dict["Protein_2_FunctionEnum_and_Score_table"]
        results = get_results_of_statement_from_flat_file(fn)
    else:
        results = get_results_of_statement("SELECT * FROM protein_2_functionenum_and_score;")

    for res in results:
        if read_from_flat_files:
            taxid, protein_AN, funcEnum_arr_orig, score_arr_orig = res
            score_arr_orig = score_arr_orig.strip()
            if score_arr_orig == "{}":
                continue
            funcEnum_list = funcEnum_arr_orig[1:-1].split(",")
            score_list = score_arr_orig[1:-1].split(",")
        else:
            taxid, protein_AN, funcEnum_list, score_list = res
        assert len(funcEnum_list) == len(score_list)
        funcEnum_arr = np.array(funcEnum_list, dtype=np.dtype(variables.dtype_functionEnumeration))
        score_arr = np.array(score_list, dtype=np.dtype(variables.dtype_TM_score)) # previously from 0-5 as np.dtype("float32")), but now scaled by e6 and as integer
        score_arr.flags.writeable = False
        funcEnum_arr.flags.writeable = False
        ENSP_2_tuple_funcEnum_score_dict[protein_AN] = (funcEnum_arr, score_arr)
    return ENSP_2_tuple_funcEnum_score_dict

def get_KEGG_Taxid_2_acronym_dict(read_from_flat_files=True):
    KEGG_Taxid_2_acronym_dict = {}
    if read_from_flat_files:
        # fn = os.path.join(variables.TABLES_DIR, "KEGG_Taxid_2_acronym_table.txt")
        fn = variables.tables_dict["KEGG_Taxid_2_acronym_table"]
        results = get_results_of_statement_from_flat_file(fn)
    else:
        raise NotImplementedError # result = get_results_of_statement()
    for res in results:
        taxid, taxname = res
        # taxname, taxid = res
        taxname = taxname.strip()
        KEGG_Taxid_2_acronym_dict[int(taxid)] = taxname
    return KEGG_Taxid_2_acronym_dict

def get_results_of_statement_from_flat_file(file_name, columns=[]):
    with open(file_name, "r") as fh_in:
        for line in fh_in:
            ls = line.split("\t")
            ls[-1] = ls[-1].strip()
            if columns:
                yield [ls[num] for num in columns]
            else:
                yield ls

def get_function_description_from_funcEnum(funcEnum_list):
    funcEnum_2_description_dict = {}
    if len(funcEnum_list) == 0:
        return funcEnum_2_description_dict
    funcEnum_list = str(funcEnum_list)[1:-1]
    result = get_results_of_statement("SELECT functions.enum, functions.description FROM functions WHERE functions.enum IN({});".format(funcEnum_list))
    for res in result:
        funcEnum, description = res
        funcEnum_2_description_dict[funcEnum] = description
    return funcEnum_2_description_dict

def get_cond_bool_array_of_etypes(etypes, function_enumeration_len, etype_cond_dict):
    cond_etypes = np.zeros(function_enumeration_len, dtype=bool)
    for etype in etypes:
        try:
            etype_cond = etype_cond_dict["cond_{}".format(str(etype)[1:])]
        except KeyError: # e.g. new etype which not implemented yet, already in variable.py documentation
            continue
        cond_etypes = cond_etypes | etype_cond
    cond_etypes.flags.writeable = False
    return cond_etypes

def get_lineage_Reactome(fn_hierarchy):
    child_2_parent_dict = get_child_2_parent_dict_RCTM_hierarchy(fn_hierarchy)
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

def get_child_2_parent_dict_RCTM_hierarchy(fn_in):
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

def get_term_2_hierarchical_level_Reactome(fn_RCTM_term_2_level):
    term_2_level_dict = {}
    with open(fn_RCTM_term_2_level, "r") as fh_in:
        for line in fh_in:
            term, level = line.split("\t")
            level = level.strip() # cast to int ?
            term_2_level_dict[term] = level
    return term_2_level_dict

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

def get_lineage_dict_enum(as_array=False, read_from_flat_files=False, cast_2_int=True):
    """
    lineage_dict = {} # key: function enumeration, value: set of func enum array all parents
    """
    lineage_dict = {} # key: function enumeration, value: set of func enum array all parents
    if read_from_flat_files:
        # fn = os.path.join(variables.TABLES_DIR, "Lineage_table_STRING.txt")
        fn = variables.tables_dict["Lineage_table"]
        results = get_results_of_statement_from_flat_file(fn)
        for res in results:
            term, lineage = res
            term = int(term)
            lineage = lineage[1:-1].split(",")
            if len(lineage[0]) > 0:
                if cast_2_int:  # string to integer
                    lineage = [int(ele) for ele in lineage]
                if as_array:
                    lineage_dict[term] = np.array(sorted(lineage), dtype=np.dtype("uint32"))
                else:
                    lineage_dict[term] = set(lineage)
    else:
        results = get_results_of_statement("SELECT * FROM lineage;")
        for res in results:
            term, lineage = res
            if as_array:
                lineage_dict[term] = np.array(sorted(lineage), dtype=np.dtype("uint32"))
            else:
                lineage_dict[term] = set(lineage)
    return lineage_dict

def get_lineage_dict_hr(read_from_flat_files=True):
    """
    child 2 all parents dict
    """
    # fn = r"/home/dblyon/agotool/data/PostgreSQL/tables/Lineage_table_hr.txt"
    lineage_dict = {} # key: function name, value: set of function names (all parents)
    if read_from_flat_files:
        fn = os.path.join(variables.TABLES_DIR, "Lineage_table_UPS_hr.txt")
        # fn = variables.tables_dict["Lineage_table_hr"]
        results = get_results_of_statement_from_flat_file(fn)
        for res in results:
            term, lineage = res
            lineage = [ele[1:-1] for ele in lineage.replace(" ", "").replace("'", '"')[1:-1].split(",")]
            if len(lineage[0]) > 0:
                lineage_dict[term] = set(lineage)
    return lineage_dict

def get_etype_cond_dict(etype_2_minmax_funcEnum, function_enumeration_len):
    """
    :return: Dict (key: Str(entity type e.g. 'cond_57'), val: Bool array of len function_enumeration_len)
    """
    # etype_2_minmax_funcEnum = self.etype_2_minmax_funcEnum # etype_2_minmax_funcEnum = pqo.get_etype_2_minmax_funcEnum(pqo.entitytype_arr)
    # function_enumeration_len = self.function_enumeration_len # function_enumeration_len = pqo.entitytype_arr.shape[0]
    etype_cond_dict = {}
    for etype, min_max in etype_2_minmax_funcEnum.items():
        min_, max_ = min_max
        cond_name = "cond_{}".format(str(etype)[1:])
        cond_arr = np.zeros(function_enumeration_len, dtype=bool)
        cond_arr[min_:max_ + 1] = True
        cond_arr.flags.writeable = False
        etype_cond_dict[cond_name] = cond_arr
    return etype_cond_dict

def get_functionEnumArray_from_proteins(protein_ans_list, dict_2_array=False):
    """
    ENSP_2_functionEnumArray_dict =
    {'1000565.METUNv1_00006': array([45130, 46056, 46149, 50102, 83861, 95081, 95232], dtype=uint32),
    '1000565.METUNv1_00011': array([45130, 46056, 46149, 70030, 83861, 95232], dtype=uint32), ...
    ENSP_2_funcEnumAssociations =
    [('10090.ENSMUSP00000001812', [52, 280, 282, 405, ...
    which functional associations are present for the given proteins
    variable length array of Integers, each codes for a specific function (enumeration of function)
    int32 Integer (-2147483648 to 2147483647), since enumeration between 0 and 6.815.598 (variables.function_enumeration_len)
    :param protein_ans_list: List of String
    :param dict_2_array: Bool (flag to get a dict of ENSPs with func enum arr as values, otherwise nested list of tuples (ENSP, list of func enums))
    :return: List of Tuple( String(ENSP), List of Integers(function enumeration) )
    """
    # result = get_results_of_statement("SELECT protein_2_functionenum.an, protein_2_functionenum.functionenum FROM protein_2_functionenum WHERE protein_2_functionenum.an IN({});".format(str(protein_ans_list)[1:-1]))
    result = get_results_of_statement("SELECT protein_2_functionenum.id, protein_2_functionenum.functionenum FROM protein_2_functionenum WHERE protein_2_functionenum.id IN({});".format(str(protein_ans_list)[1:-1]))
    if not dict_2_array:
        return result
    else:
        dict_2_return = {}
        for res in result:
            ENSP, list_of_funcEnums = res
            dict_2_return[ENSP] = np.array(list_of_funcEnums, dtype=np.dtype("uint32"))
        return dict_2_return


     # matrix = lil_matrix((len(ENSP_2_tuple_funcEnum_score_dict), max(KS_funcEnums_arr)+1), dtype=np.dtype(variables.dtype_TM_score))

    # for ensp in sorted(ENSP_2_tuple_funcEnum_score_dict.keys()):
    #     rowIndex = ENSP_2_rowIndex_dict[ensp]
    #     funcEnum_arr, score_arr = ENSP_2_tuple_funcEnum_score_dict[ensp]
    #     matrix[rowIndex, funcEnum_arr] = score_arr
    # matrix = matrix.tocsc()


def get_ENSP_2_functionEnumArray_dict(read_from_flat_files=False):
    """
    debug : ORDER BY bubu LIMIT 100 OFFSET 50;
    21.839.546 Protein_2_FunctionEnum_table_STRING.txt
    slow
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1   56.979   56.979  479.601  479.601 query.py:774(get_ENSP_2_functionEnumArray_dict)
    which functioal associations are present for the given proteins
    variable length array of Integers, each codes for a specific function (enumeration of function)
    int32 Integer (-2147483648 to 2147483647), since enumeration between 0 and 6.815.598 (variables.function_enumeration_len)
    :return: List of Tuple( String(ENSP), List of Integers(function enumeration) )
    """
    ENSP_2_functionEnumArray_dict = {} # key: String (ENSP), val: np.array(uint32) of function enumerations
    if read_from_flat_files:
        # fn = os.path.join(variables.TABLES_DIR, "Protein_2_FunctionEnum_table_STRING.txt")
        fn = variables.tables_dict["Protein_2_FunctionEnum_table"]
        result = get_results_of_statement_from_flat_file(fn)
        for res in result:
            # ENSP, funcEnumArray = res # STRING_v11
            taxid, ENSP, funcEnumArray = res # UniProt
            funcEnumArray = funcEnumArray[1:-1].split(",")
            if len(funcEnumArray[0]) > 0: # debug # remove when tables fixed
                funcEnumArray = [int(ele) for ele in funcEnumArray]
                ENSP_2_functionEnumArray_dict[ENSP] = np.array(funcEnumArray, dtype=np.dtype("uint32"))
    else:
        limit = 500000
        for offset_ in range(0, 21839547, limit): # 21.500.000 # 21839547
            if variables.VERBOSE:
                print(".", end="")
            result = get_results_of_statement("SELECT protein_2_functionenum.id, protein_2_functionenum.functionenum FROM protein_2_functionenum ORDER BY protein_2_functionenum.id LIMIT {} OFFSET {};".format(limit, offset_))
            for res in result:
                ENSP, funcEnumArray = res
                ENSP_2_functionEnumArray_dict[ENSP] = np.array(funcEnumArray, dtype=np.dtype("uint32"))
    return ENSP_2_functionEnumArray_dict

def get_UniProtID_2_functionEnumArray_dict(UniProtID_list): # rename to state not all UniProtIDs are retrieved
    """
    """
    UniProtID_2_functionEnumArray_dict = {} # key: String (ENSP), val: np.array(uint32) of function enumerations
    result = get_results_of_statement("SELECT protein_2_functionenum.id, protein_2_functionenum.functionenum FROM protein_2_functionenum WHERE protein_2_functionenum.id IN({});".format(str(UniProtID_list)[1:-1]))
    for res in result:
        UniProtID, funcEnumArray = res
        UniProtID_2_functionEnumArray_dict [UniProtID] = np.array(funcEnumArray, dtype=np.dtype("uint32"))
    return UniProtID_2_functionEnumArray_dict

def get_ENSP_2_functionEnumArray_dict_old():
    """
    debug : ORDER BY bubu LIMIT 100 OFFSET 50;
    52.930.904 lines in Protein_2_Function_table_STRING.txt
    slow
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1   56.979   56.979  479.601  479.601 query.py:774(get_ENSP_2_functionEnumArray_dict)
    which functioal associations are present for the given proteins
    variable length array of Integers, each codes for a specific function (enumeration of function)
    int32 Integer (-2147483648 to 2147483647), since enumeration between 0 and 6.815.598 (variables.function_enumeration_len)
    :return: List of Tuple( String(ENSP), List of Integers(function enumeration) )
    """
    ENSP_2_functionEnumArray_dict = {} # key: String (ENSP), val: np.array(uint32) of function enumerations
    result = get_results_of_statement("SELECT protein_2_functionenum.id, protein_2_functionenum.functionenum FROM protein_2_functionenum;")
    for res in result:
        ENSP, funcEnumArray = res
        ENSP_2_functionEnumArray_dict[ENSP] = np.array(funcEnumArray, dtype=np.dtype("uint32"))
    return ENSP_2_functionEnumArray_dict

def get_background_taxid_2_funcEnum_index_2_associations(read_from_flat_files=False, from_pickle=False): # SLOW ~60% of startup time
    """
    SLOW ~60% of startup time --> pickle it
    --> reformatted flat file
    output format changed from
    1000565 3919    {{3936,9},{3945,1},{3949,7}, ... }
    to
    1000565 3919 {3936,3945,3949, ... } {9,1,7, ... }
    taxid, background_n, background_index_positions_arr, background_counts_arr
    """
    if from_pickle:
        taxid_2_tuple_funcEnum_index_2_associations_counts = pickle.load(open(variables.tables_dict["taxid_2_tuple_funcEnum_index_2_associations_counts"], "rb"))
        for taxid, funcEnum_assoc in taxid_2_tuple_funcEnum_index_2_associations_counts.items():
            index_positions_arr, counts_arr = funcEnum_assoc
            index_positions_arr.flags.writeable = False
            counts_arr.flags.writeable = False
        return taxid_2_tuple_funcEnum_index_2_associations_counts

    taxid_2_tuple_funcEnum_index_2_associations_counts = {} # for background preloaded
    if not read_from_flat_files:
        for taxid in get_taxids():
            background_index_positions_list, background_counts_arr_list = get_background_count_array(taxid)
            # need be uint32 not uint16 since funcEnum is 0 to 7mio
            assert len(background_index_positions_list) == len(background_counts_arr_list)
            index_positions_arr = np.array(background_index_positions_list, dtype=np.dtype(variables.dtype_functionEnumeration))
            counts_arr = np.array(background_counts_arr_list, dtype=np.dtype(variables.dtype_functionEnumeration))
            index_positions_arr.flags.writeable = False
            counts_arr.flags.writeable = False
            taxid_2_tuple_funcEnum_index_2_associations_counts[taxid] = [index_positions_arr, counts_arr]
    else:
        fn = variables.tables_dict["Taxid_2_FunctionCountArray_table"]
        results = get_results_of_statement_from_flat_file(fn)
        for res in results:
            taxid, background_count, background_index_positions_arr_str, background_counts_arr_str = res
            taxid = int(taxid)
            background_index_positions_list = background_index_positions_arr_str[1:-1].split(",")
            background_counts_arr_list = background_counts_arr_str.strip()[1:-1].split(",")
            assert len(background_index_positions_list) == len(background_counts_arr_list)
            index_positions_arr = np.array(background_index_positions_list, dtype=np.dtype(variables.dtype_functionEnumeration))
            # counts_arr = np.array(background_counts_arr_list, dtype=np.dtype("uint16"))
            counts_arr = np.array(background_counts_arr_list, dtype=np.dtype(variables.dtype_functionEnumeration)) # switch from uint16 to uint23 since this was being used all along (conversion in function call)
            index_positions_arr.flags.writeable = False
            counts_arr.flags.writeable = False
            taxid_2_tuple_funcEnum_index_2_associations_counts[taxid] = [index_positions_arr, counts_arr]
    return taxid_2_tuple_funcEnum_index_2_associations_counts

def get_background_count_array(taxid):
    """
    # max_background_count: 58324 (from function_enumeration 47403 "47403   -51     KW-0181 Complete proteome       -1      1")
    # (irrelevant but just for reference max_background_n: 98897)
    old version:
    np.array (of 32bit integer, fixed length and immutable, sparse matrix with 0 as default, otherwise counts of functional associations at index positions corresponding to functionalterm_arr)
    new version:
    list of tuples (index_position, count)
    :param taxid: Integer (NCBI Taxid)
    :return: List of tuples of Integers (index_position, count)

    taxid | background_n | background_index_positions_arr | background_counts_arr |
    """
    return get_results_of_statement("SELECT taxid_2_functioncountarray.background_index_positions_arr, taxid_2_functioncountarray.background_count_arr FROM taxid_2_functioncountarray WHERE taxid_2_functioncountarray.taxid='{}';".format(taxid))[0]#[0]

def get_function_an_2_name__an_2_description_dict():
    result = get_results_of_statement("SELECT functions.an, functions.name, functions.description FROM functions; ")
    an_2_name_dict, an_2_description_dict = {}, {}
    for res in result:
        an, name, description = res
        an_2_name_dict[an] = name
        an_2_description_dict[an] = description
    return an_2_name_dict, an_2_description_dict

def get_function_an_2_description_dict():
    result = get_results_of_statement("SELECT functions.an, functions.description FROM functions; ")
    an_2_description_dict = {}
    for res in result:
        an, description = res
        an_2_description_dict[an] = description
    return an_2_description_dict

def get_description_from_an(term_list):
    result = get_results_of_statement("SELECT functions.an, functions.description FROM functions WHERE functions.an IN({});".format(str(term_list)[1:-1]))
    an_2_description_dict = defaultdict(lambda: np.nan)
    for res in result:
        an, description = res
        an_2_description_dict[an] = description
    return an_2_description_dict

def get_function_an_2_enum__and__enum_2_function_an_dict():
    result = get_results_of_statement("SELECT functions.enum, functions.an FROM functions")
    function_2_enum_dict, enum_2_function_dict = {}, {}
    for res in result:
        enum, function_ = res
        function_2_enum_dict[function_] = enum
        enum_2_function_dict[enum] = function_
    return function_2_enum_dict, enum_2_function_dict

def get_function_arr():
    result = get_results_of_statement("SELECT functions.enum, functions.an FROM functions")
    term_arr = np.empty((len(result),), dtype=np.dtype('U13'))
    for i, res in enumerate(result):
        enum, function_ = res
        assert i == enum
        term_arr[i] = function_
    term_arr.flags.writeable = False # make it immutable
    return term_arr

def get_termAN_from_humanName_functionType(functionType, humanName):
    if humanName is None:
        return ""
    return functionType_term_2_an_dict[functionType][humanName]

def parse_result_child_parent(result):
    return set([item for sublist in result for item in sublist])

def get_taxids(read_from_flat_files=False, fn=None):
    """
    return all Taxids from taxid_2_proteins as sorted List of Integers
    :return: List of Integers
    """
    if read_from_flat_files:
        taxids = []
        if fn is None:
            # Taxid_2_Proteins_table_STRING = os.path.join(variables.TABLES_DIR, "Taxid_2_Proteins_table_STRING.txt")
            Taxid_2_Proteins_table_STRING = variables.tables_dict["Taxid_2_Proteins_table"]
        with open(Taxid_2_Proteins_table_STRING, "r") as fh:
            for line in fh:
                taxids.append(line.split("\t")[0])
        return taxids
    else:
        result = get_results_of_statement("SELECT taxid_2_protein.taxid FROM taxid_2_protein;")
        return sorted([rec[0] for rec in result])

def map_secondary_2_primary_ANs(ids_2_map, Secondary_2_Primary_IDs_dict=None, read_from_flat_files=False):
    """
    reading from flat file is super slow, DB makes a lot of sense here. Only relevant if low_memory is True
    """
    if Secondary_2_Primary_IDs_dict is None:
        ### don't read this from flat files (VERY slow) if there is a DB and low_memory then use DB
        Secondary_2_Primary_IDs_dict = get_Secondary_2_Primary_IDs_dict_from_sec(ids_2_map, read_from_flat_files)
    Secondary_2_Primary_IDs_dict_userquery = {}
    for id_ in ids_2_map:
        try:
            prim = Secondary_2_Primary_IDs_dict[id_]
        except KeyError:
            prim = False
        if prim:
            Secondary_2_Primary_IDs_dict_userquery[id_] = prim
    return Secondary_2_Primary_IDs_dict_userquery

def map_primary_2_secondary_ANs(ids_2_map, Primary_2_Secondary_IDs_dict=None, read_from_flat_files=False, ENSPs_only=False, no_ENSPs=False):
    """
    only maps UniProtID to UniProtAC
    """
    if Primary_2_Secondary_IDs_dict is None:
        ### don't read this from flat files (VERY slow) if there is a DB and low_memory then use DB
        Primary_2_Secondary_IDs_dict = get_Primary_2_Secondary_IDs_dict_from_prim(ids_2_map, read_from_flat_files)
    Primary_2_Secondary_IDs_dict_userquery = {}
    for id_ in ids_2_map:
        try:
            sec = Primary_2_Secondary_IDs_dict[id_]
        except KeyError:
            sec = False
        if sec: # sec is a list
            if ENSPs_only:
                for sec_id in sec:
                    try:
                        if int(sec_id.split(".")[0]) > 1:
                            Primary_2_Secondary_IDs_dict_userquery[id_] = sec_id
                    except:
                        pass
            elif no_ENSPs:
                for sec_id in sec:
                    try:
                        if not int(sec_id.split(".")[0]) > 1:
                            Primary_2_Secondary_IDs_dict_userquery[id_] = sec_id
                    except:
                        pass
            else: # take all IDs
                Primary_2_Secondary_IDs_dict_userquery[id_] = sec
    return Primary_2_Secondary_IDs_dict_userquery

def get_Secondary_2_Primary_IDs_dict(read_from_flat_files=False):
    Secondary_2_Primary_IDs_dict = {}
    if read_from_flat_files:
        result = get_results_of_statement_from_flat_file(variables.tables_dict["Secondary_2_Primary_ID_table"], columns=[1, 2])
    else:
        result = get_results_of_statement("SELECT secondary_2_primary_id.sec, secondary_2_primary_id.prim FROM secondary_2_primary_id;")
    for sec, prim in result:
        Secondary_2_Primary_IDs_dict[sec] = prim
    return Secondary_2_Primary_IDs_dict

def get_Secondary_2_Primary_IDs_dict_from_sec(ids_2_map, read_from_flat_files=False):
    Secondary_2_Primary_IDs_dict = {}
    if read_from_flat_files:
        ids_2_map = set(ids_2_map)
        result = get_results_of_statement_from_flat_file(variables.tables_dict["Secondary_2_Primary_ID_table"], columns=[1, 2])
        for sec, prim in result:
            if sec in ids_2_map:
                Secondary_2_Primary_IDs_dict[sec] = prim
    else:
        result = get_results_of_statement("SELECT secondary_2_primary_id.sec, secondary_2_primary_id.prim FROM secondary_2_primary_id WHERE secondary_2_primary_id.sec IN ({});".format(str(ids_2_map)[1:-1]))
        for sec, prim in result:
            Secondary_2_Primary_IDs_dict[sec] = prim
    return Secondary_2_Primary_IDs_dict

def get_Primary_2_Secondary_IDs_dict_from_prim(ids_2_map, read_from_flat_files=False):
    Primary_2_Secondary_IDs_dict = {}
    if read_from_flat_files:
        ids_2_map = set(ids_2_map)
        result = get_results_of_statement_from_flat_file(variables.tables_dict["Secondary_2_Primary_ID_table"], columns=[1, 2])
        for sec, prim in result:
            if prim in ids_2_map:
                if prim not in Primary_2_Secondary_IDs_dict:
                    Primary_2_Secondary_IDs_dict[prim] = [sec]
                else:
                    Primary_2_Secondary_IDs_dict[prim].append(sec)

    else: # -- CREATE INDEX secondary_2_primary_id_prim_idx ON secondary_2_primary_id (prim);
        result = get_results_of_statement("SELECT secondary_2_primary_id.sec, secondary_2_primary_id.prim FROM secondary_2_primary_id WHERE secondary_2_primary_id.prim IN ({});".format(str(ids_2_map)[1:-1]))
        for sec, prim in result:
            if prim not in Primary_2_Secondary_IDs_dict:
                Primary_2_Secondary_IDs_dict[prim] = [sec]
            else:
                Primary_2_Secondary_IDs_dict[prim].append(sec)
    return Primary_2_Secondary_IDs_dict

def get_proteins_of_taxid(taxid, read_from_flat_files=False, fn_Taxid_2_Proteins_table_STRING=None):
    if not read_from_flat_files:
        result = get_results_of_statement("SELECT taxid_2_protein.an_array FROM taxid_2_protein WHERE taxid_2_protein.taxid={}".format(taxid))
        return sorted(result[0][0])
    else:
        if fn_Taxid_2_Proteins_table_STRING is None:
            fn_Taxid_2_Proteins_table_STRING = variables.tables_dict["Taxid_2_Proteins_table"]
        with open(fn_Taxid_2_Proteins_table_STRING, "r") as fh:
            for line in fh:
                # taxid_line, prot_arr, background_count = line.split("\t") # STRING_v11
                taxid_line, background_count, prot_arr = line.split("\t") # UniProt
                if taxid_line == str(taxid):
                    prot_arr = prot_arr.strip()[1:-1].replace("'", "").replace('"', "").split(",")
                    return sorted(prot_arr)

def get_proteins_of_human(fn=None):
    if fn is None:
        fn = os.path.join(variables.TABLES_DIR, "9606_proteins_ENSPs_STRINGv11.txt")
    ENSPs_human = []
    with open(fn) as fh:
        for line in fh:
            ENSPs_human.append(line.strip())
    return sorted(ENSPs_human)

def get_taxid_2_proteins_dict(fn_Taxid_2_Proteins_table_STRING=None):
    """
    taxid_2_proteins_dict: key: Int(Taxid), val: set of String(UniProt ID)
    """
    # if not read_from_flat_files:
    #     result = get_results_of_statement("SELECT taxid_2_protein.an_array FROM taxid_2_protein")
    #     return sorted(result[0][0])
    # else:
    taxid_2_proteins_dict = {}
    if fn_Taxid_2_Proteins_table_STRING is None:
        fn_Taxid_2_Proteins_table_STRING = variables.tables_dict["Taxid_2_Proteins_table"]
    with open(fn_Taxid_2_Proteins_table_STRING, "r") as fh:
        for line in fh:
            # taxid_line, prot_arr, background_count = line.split("\t") # STRING_v11
            taxid, background_count, prot_arr = line.split("\t") # UniProt
            taxid = int(taxid)
            prot_arr = prot_arr.strip()[1:-1].replace("'", "").replace('"', "").split(",")
            taxid_2_proteins_dict[taxid] = set(prot_arr)
    return taxid_2_proteins_dict

def get_Taxid_2_proteome_count_dict(read_from_flat_files=False, fn=None): #, searchspace=None):
    """
    :param read_from_flat_files: Bool flag
    :param fn: None or String (file to read or default)
    # :param searchspace: None or String (variables.searchspace_2_entityType_dict "STRING" or "UniProt" / "aGOtool")
    :return: dict
    """
    if fn is None:
        fn = variables.tables_dict["Taxid_2_Proteins_table"]
    taxid_2_proteome_count_dict = {}
    if read_from_flat_files:
        # result = get_results_of_statement_from_flat_file(fn, columns=[0, 2])
        result = get_results_of_statement_from_flat_file(fn, columns=[0, 1])
    else:
        result = get_results_of_statement("SELECT taxid_2_protein.taxid, taxid_2_protein.count FROM taxid_2_protein;")
    for res in result:
        taxid, count = res
        taxid_2_proteome_count_dict[int(taxid)] = int(count)
    return taxid_2_proteome_count_dict

def get_association_2_count_ANs_background_split_by_entity(taxid):
    result = get_results_of_statement("SELECT * FROM function_2_ensp WHERE function_2_ensp.taxid={}".format(taxid))

    # to avoid checking for etype for each record, #!!!
    etype_2_association_2_count_dict_background, etype_2_association_2_ANs_dict_background, etype_2_background_n = {}, {}, {}
    for etype in variables.entity_types_with_data_in_functions_table:
        etype_2_association_2_count_dict_background[etype] = {}
        etype_2_association_2_ANs_dict_background[etype] = {}
        etype_2_background_n[etype] = {}

    for rec in result:
        _, etype, association, enum, background_count, background_n, an_array = rec
        etype_2_association_2_count_dict_background[etype][association] = background_count
        etype_2_association_2_ANs_dict_background[etype][association] = set(an_array)
        etype_2_background_n[etype] = background_n
    return etype_2_association_2_count_dict_background, etype_2_association_2_ANs_dict_background, etype_2_background_n

def from_taxid_get_association_2_count_split_by_entity(taxid):
    result = get_results_of_statement("SELECT * FROM function_2_ensp WHERE function_2_ensp.taxid={}".format(taxid))

    etype_2_association_2_count_dict = {}
    for etype in variables.entity_types_with_data_in_functions_table:
        etype_2_association_2_count_dict[etype] = {}

    for rec in result:
        # _, etype, association, background_count, background_n, an_array = rec
        _, etype, association, enum, background_count, background_n, an_array = rec
        # etype = str(etype)
        etype_2_association_2_count_dict[etype][association] = background_count
    return etype_2_association_2_count_dict

def from_taxid_and_association_get_association_2_count_dict(taxid, association_list):
    result = get_results_of_statement("SELECT function_2_ensp.association, function_2_ensp.background_count FROM function_2_ensp WHERE (function_2_ensp.taxid={} AND function_2_ensp.association IN({}));".format(taxid, str(association_list)[1:-1]))
    association_2_count_dict = {}
    for rec in result:
        association, background_count = rec
        association_2_count_dict[association] = background_count
    return association_2_count_dict

def from_taxid_and_association_get_association_2_ENSP(taxid, association_list):
    result = get_results_of_statement("SELECT function_2_ensp.association, function_2_ensp.an_array FROM function_2_ensp WHERE (function_2_ensp.taxid={} AND function_2_ensp.association IN({}));".format(taxid, str(association_list)[1:-1]))
    association_2_ENSPset_dict = {}
    for rec in result:
        association, an_array = rec
        association_2_ENSPset_dict[association] = set(an_array)
    return association_2_ENSPset_dict

def get_association_2_counts_split_by_entity():
    # get all taxids to create a taxid to entity type and associations lookup
    taxids = [taxid for taxid in get_taxids()]
    taxid_2_etype_2_association_2_count_dict = {taxid: {} for taxid in taxids}
    # create dict for each entity type of relevance (in order to avoid checking for existence each time afterwards)
    for taxid in taxids:
        etype_2_association_2_count_dict = taxid_2_etype_2_association_2_count_dict[taxid]
        for etype in variables.entity_types_with_data_in_functions_table:
            etype_2_association_2_count_dict[etype] = {}

    result = get_results_of_statement("SELECT function_2_ensp.taxid, function_2_ensp.etype, function_2_ensp.association, function_2_ensp.background_count FROM function_2_ensp;")
    for rec in result:
        taxid, etype, association, background_count= rec
        # etype = str(etype)
        taxid = taxid
        taxid_2_etype_2_association_2_count_dict[taxid][etype][association] = background_count
    return taxid_2_etype_2_association_2_count_dict

def get_functionAN_2_etype_dict():
    result = get_results_of_statement("SELECT functions.an, functions.etype FROM functions;")
    an_2_etype_dict = {}
    for res in result:
        an, etype = res
        an_2_etype_dict[an] = etype
    return an_2_etype_dict

def get_goslimtype_2_cond_dict():
    """
    read obo files
    parse all terms and add to dict (key: obo file name, val: list of GO terms)
    translate GOterm function names to bool array
    """
    GOslimType_2_cond_dict = {}
    # GO_slim_subsets_file = variables.tables_dict["goslim_subsets_file"]
    GO_slim_subsets_file = variables.tables_dict["goslim_subsets_file"] #!!! ToDo make into UPS_FIN.txt file
    with open(GO_slim_subsets_file, "r") as fh_in:
        for line in fh_in:
            fn_basename = line.strip()
            GOslimType_2_cond_dict[fn_basename.replace(".obo", "").replace("goslim_", "")] = np.load(os.path.join(variables.TABLES_DIR, fn_basename.replace(".obo", ".npy")))
    return GOslimType_2_cond_dict

def get_random_protein(ENSP_or_UniProtID="UniProtID", taxid="9606", number_of_proteins=1):
    """
    too slow
    :param ENSP_or_UniProtID: String(Flag), 'ENSP' or 'UniProtID'
    :param taxid: Int, e.g. 9606
    :param number_of_proteins: Int
    :return: List of String
    """
    result = get_results_of_statement("SELECT * FROM secondary_2_primary_id ORDER BY random() LIMIT 10;")
    return result

def get_funcName_2_funcEnum_dict():
    funcName_2_funcEnum_dict = {}
    fn_functions_table = os.path.join(variables.TABLES_DIR, "Functions_table_UPS_FIN.txt")
    with open(fn_functions_table, "r") as fh_in:
        for line in fh_in:
            funcEnum, _, funcName, *rest = line.split("\t")
            funcName_2_funcEnum_dict[funcName] = int(funcEnum)
    return funcName_2_funcEnum_dict

def check_if_TaxID_valid_for_GENOME_and_try_2_map_otherwise(taxid, pqo, args_dict=dict()):
    """
    figure out if given taxid is part of UniProt Reference Proteomes
    if not try to map it via static dictionary (from variables.py) or via NCBI (from lower than species to species rank)
    :param taxid: Integer
    :param pqo: Persistent Query Object
    :param args_dict: Dictionary with parameters
    :return: (Integer, Bool)
    """
    if taxid in pqo.taxid_2_proteome_count:
        return taxid, True # taxid is part of UniProt Ref Prots
    else:
        # try to find a parent that is in of UniProt Ref Prots
        for taxid_parent in pqo.ncbi.iter_direct_parent(taxid):  # relevant for e.g. Taxid 511145; Escherichia coli str. K-12 substr. MG1655 --> should match to 83333 not 83334!
            taxid_parent = int(taxid_parent)
            if taxid_parent in pqo.taxid_2_proteome_count:
                return taxid_parent, True  # taxid is part of UniProt Ref Prots
            elif pqo.TaxidSpecies_2_TaxidProteome_dict.get(taxid_parent, False):
                taxid = pqo.TaxidSpecies_2_TaxidProteome_dict[taxid_parent]
                return taxid, True
        try:
            taxid_mapped = pqo.TaxidSpecies_2_TaxidProteome_dict[taxid]
            return taxid_mapped, True # taxid can easily be mapped, if ambiguous will be mapped to the reference proteome with the highest number of proteins
        except KeyError:
            pass
    args_dict["ERROR TaxID"] = "The Taxid '{}' you've provided is not a valid UniProt Reference Proteome TaxID (https://www.uniprot.org/proteomes). Unfortunately, we can't map your taxid input to an NCBI taxid that has a UniProt Reference Proteome. Please use a valid taxid and try again.".format(taxid)
    return taxid, False

def get_last_updated_text():
    fn = os.path.join(variables.TABLES_DIR, "aGOtool_flatfiles_current.tar.gz")
    time_ = tools.creation_date(fn)
    return datetime.datetime.fromtimestamp(time_).strftime("%d %B %Y")

def get_current_time_and_date():
    return time.strftime('%l:%M%p %Z on %b %d, %Y') # '1:36PM EDT on Oct 18, 2010'

def get_UniProt_NCBI_TaxID_and_TaxName_for_autocomplete_list():
    '''
    "organism_name", "taxid", "proteome_ID", "num_proteins"
    '''
    fn = variables.tables_dict["UniProt_NCBI_TaxID_and_TaxName_for_autocomplete"]
    list_of_autocomplete_tags = []
    with open(fn, "r") as fh:
        for line in fh:
            list_of_autocomplete_tags.append(", ".join(line.strip().split("\t")))
    return list_of_autocomplete_tags


if __name__ == "__main__":
    # pass
    pqo = PersistentQueryObject()
    pqos = PersistentQueryObject_STRING()
    #
    # ENSP_2_functionEnumArray_dict = get_functionEnumArray_from_proteins(ensp_list, dict_2_array=True)
    # pqo = PersistentQueryObject_STRING(low_memory=True, read_from_flat_files=True)
    # get_background_taxid_2_funcEnum_index_2_associations(read_from_flat_files=False)
    # get_proteinAN_2_tuple_funcEnum_score_dict(read_from_flat_files=True, fn=None)


    # import os
    # user = os.environ['POSTGRES_USER']
    # pwd = os.environ['POSTGRES_PASSWORD']
    # db = os.environ['POSTGRES_DB']
    # host = 'db'
    # port = '5432'
    # print("user", user)
    # print("pwd", pwd)
    # print("db", db)

    # cursor = get_cursor()
    # cursor = get_cursor(host=host, dbname=db, user=user, password="postgres")
    # cursor = get_cursor()
    # cursor.execute("SELECT * FROM functions WHERE functions.type='GO' LIMIT 5")
    # cursor.execute("SELECT * FROM protein_2_function WHERE protein_2_function.an='A0A009DWB1'")
    # records = cursor.fetchall()
    # print(records)
    # cursor.close()


    # print(get_cursor())
    # print(query_example(get_cursor()))
    # print(PersistentQueryObject())
    # pass
    # import pandas as pd
    # import tools
    # # fn = r"/Users/dblyon/modules/cpr/agotool/static/data/exampledata/exampledata_human.txt"
    # fn = r"/Users/dblyon/Downloads/1A_Data_for_web_tool_test_AbundaceCorrection_fUbi.txt"
    # df = pd.read_csv(fn, sep='\t')
    # ans_list = list(df["background"].unique())
    # ans_list = tools.commaSepCol2uniqueFlatList(df, "background", sep=";", unique=True)
    # print(len(ans_list))
    # pqo = PersistentQueryObject()
    # ### 1.)
    # protein_ans_list = ans_list # ['P62805']
    # gocat_upk = "all_GO"
    # basic_or_slim = "basic"
    # association_dict = pqo.get_association_dict(protein_ans_list, gocat_upk, basic_or_slim)
    # print(len(association_dict))
    # # ### 2.)
    # secondary_2_primary_dict = pqo.map_secondary_2_primary_ANs(ans_list)
    # # print(len(secondary_2_primary_dict))
    # # secondary_2_primary_dict = pqo.map_secondary_2_primary_ANs_v2(ans_list)
