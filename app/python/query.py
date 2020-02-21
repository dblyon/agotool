from __future__ import print_function
import pickle
import numpy as np
import pandas as pd
import os, sys
from collections import defaultdict
import psycopg2
from scipy import sparse
# import math
# from contextlib import contextmanager

### import user modules
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import variables, obo_parser, taxonomy
# print(os.getcwd())
# print(sorted(os.listdir()))
# print(os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
# print(sorted(os.listdir(os.path.dirname(os.path.abspath(os.path.realpath(__file__))))))
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

def get_cursor(env_dict=None):
    platform_ = sys.platform
    if env_dict is not None:
        USER = env_dict['POSTGRES_USER']
        PWD = env_dict['POSTGRES_PASSWORD']
        DBNAME = env_dict['POSTGRES_DB']
        PORT = '5432'
        HOST = 'db'
        return get_cursor_docker(host=HOST, dbname=DBNAME, user=USER, password=PWD, port=PORT)

    if platform_ == "linux":
        if not variables.DB_DOCKER: # use local Postgres
            try:
                USER = "postgres"
                PWD = os.environ['POSTGRES_PASSWORD']
                DBNAME = os.environ['POSTGRES_DB']
                PORT = '5432'
                HOST = 'db'
            except KeyError:
                print("query.py sais there is something wrong with the Postgres config")
                raise StopIteration
            return get_cursor_docker(host=HOST, dbname=DBNAME, user=USER, password=PWD, port=PORT)
        else: # use dockerized Postgres directly from native OS
            PORT = '5913'
            HOST = 'localhost'
            param_2_val_dict = variables.param_2_val_dict
            return get_cursor_connect_2_docker(host=HOST, dbname=param_2_val_dict["POSTGRES_DB"], user=param_2_val_dict["POSTGRES_USER"], password=param_2_val_dict["POSTGRES_PASSWORD"], port=PORT)

    elif platform_ == "darwin":
        if not variables.DB_DOCKER: # use local Postgres
            return get_cursor_ody()
        else: # connect to docker Postgres container. use dockerized Postgres directly from native OS
            PORT = '5432' # shouldn't this be 5913?
            HOST = 'localhost'
            param_2_val_dict = variables.param_2_val_dict
            return get_cursor_connect_2_docker(host=HOST, dbname=param_2_val_dict["POSTGRES_DB"], user=param_2_val_dict["POSTGRES_USER"], password=param_2_val_dict["POSTGRES_PASSWORD"], port=PORT)
    else:
        print("query.get_cursor() doesn't know how to connect to Postgres")
        raise StopIteration

def get_cursor_docker(host, dbname, user, password, port):
    """
    e.g.
    import os
    user = os.environ['POSTGRES_USER']
    pwd = os.environ['POSTGRES_PASSWORD']
    db = os.environ['POSTGRES_DB']
    host = 'db'
    port = '5432'
    cursor = get_cursor_docker(user=user, password=pwd, host=host, port=port, dbname=db)
    # Sqlalchemy version: engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db))
    """
    # Define our connection string
    # conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, user, password)

    # engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db))
    conn_string = "host='{}' dbname='{}' user='{}' password='{}' port='{}'".format(host, dbname, user, password, port)
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    return cursor

def get_cursor_ody(dbname='agotool'):
    """
    :param dbname:
    :return: DB Cursor instance object
    """
    # Define our connection string
    conn_string = "dbname='{}'".format(dbname)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    return cursor

def get_cursor_connect_2_docker(host, dbname, user, password, port):
    conn_string = "host='{}' dbname='{}' user='{}' password='{}' port='{}'".format(host, dbname, user, password, port)
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
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

# def map_secondary_2_primary_ANs(ans_list):
#     """
#     map secondary UniProt ANs to primary ANs,
#     AN only in dict if mapping exists
#     :param ans_list: ListOfString
#     :return: Dict (key: String(Secondary AN), val: String(Primary AN))
#     """
#     ans_list = str(ans_list)[1:-1]
#     result = get_results_of_statement("SELECT protein_secondary_2_primary_an.sec, protein_secondary_2_primary_an.pri FROM protein_secondary_2_primary_an WHERE protein_secondary_2_primary_an.sec IN({})".format(ans_list))
#     secondary_2_primary_dict = {}
#     for res in result:
#         secondary = res[0]
#         primary = res[1]
#         secondary_2_primary_dict[secondary] = primary
#     cursor.close()
#     return secondary_2_primary_dict


class PersistentQueryObject:
    """
    aGOtool version
    used to query protein 2 functional associations
    only protein_2_function is queried in Postgres,
    everything else is in memory but still deposited in the DB any way
    """
    def __init__(self):
        # self.version_ = VERSION_
        # if self.version_ == "aGOtool":
        self.secondary_2_primary_an_dict = self.get_secondary_2_primary_an_dict()
        # else:
        #     self.secondary_2_primary_an_dict = None
        self.type_2_association_dict = self.get_type_2_association_dict()
        self.go_slim_set = self.get_go_slim_terms()
        self.KEGG_functions_set = self.get_functions_set_from_functions(function_type="KEGG")
        self.DOM_functions_set = self.get_functions_set_from_functions(function_type="DOM")
        # precompute set of functions to restrict funtional associations to
        #  might need speed overhaul #!!!
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
        result = get_results_of_statement("SELECT secondary_2_primary_id.sec, secondary_2_primary_id.pri FROM secondary_2_primary_id;")
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

    # def map_secondary_2_primary_ANs(self, ans_list):
    #     """
    #     def map_secondary_2_primary_ANs_v1_slow(self, ans_list):
    #         secondary_ans_2_replace = set(self.secondary_2_primary_an_dict.keys()).intersection(set(ans_list))
    #         return dict((secondary_an, self.secondary_2_primary_an_dict[secondary_an]) for secondary_an in secondary_ans_2_replace)
    #
    #     :param ans_list: List of String
    #     :return: secondary_2_primary_dict (key: String(Secondary AN), val: String(Primary AN))
    #     """
    #     secondary_2_primary_dict_temp = {}
    #     for secondary in ans_list:
    #         try:
    #             secondary_2_primary_dict_temp[secondary] = self.secondary_2_primary_an_dict[secondary]
    #         except KeyError:
    #             continue
    #     return secondary_2_primary_dict_temp

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
    used to query protein 2 functional associationsfunction_enumeration_len
    only protein_2_function is queried in Postgres,
    everything else is in memory but still deposited in the DB any way
    """
    def __init__(self, low_memory=True, read_from_flat_files=None):
        if read_from_flat_files is None:
            read_from_flat_files = variables.READ_FROM_FLAT_FILES
        if variables.VERBOSE:
            print("#"*80)
            print("initializing PQO")
            print("getting taxid_2_proteome_count")
        self.taxid_2_proteome_count = get_Taxid_2_proteome_count_dict(read_from_flat_files=read_from_flat_files)
        try:
            self.ncbi = taxonomy.NCBI_taxonomy(taxdump_directory=variables.DOWNLOADS_DIR, for_SQL=False, update=False)
        except FileNotFoundError:
            self.ncbi = taxonomy.NCBI_taxonomy(taxdump_directory=variables.DOWNLOADS_DIR, for_SQL=False, update=True)

        if variables.VERBOSE:
            print("getting CSC_ENSPencoding_2_FuncEnum and ENSP_2_rowIndex_dict")
        ### deprecated --> self.ENSP_2_tuple_funcEnum_score_dict = get_proteinAN_2_tuple_funcEnum_score_dict(read_from_flat_files=read_from_flat_files)
        with open(variables.tables_dict["ENSP_2_rowIndex_dict"], "rb") as fh_ENSP_2_rowIndex_dict:
            self.ENSP_2_rowIndex_dict = pickle.load(fh_ENSP_2_rowIndex_dict)
        with open(variables.tables_dict["rowIndex_2_ENSP_dict"], "rb") as fh_rowIndex_2_ENSP_dict:
            self.rowIndex_2_ENSP_dict = pickle.load(fh_rowIndex_2_ENSP_dict)
        self.CSC_ENSPencoding_2_FuncEnum = sparse.load_npz(variables.tables_dict["CSC_ENSPencoding_2_FuncEnum"])
        self.CSR_ENSPencoding_2_FuncEnum = self.CSC_ENSPencoding_2_FuncEnum.tocsr()

        if not low_memory:
            if variables.VERBOSE:
                print("getting Secondary_2_Primary_IDs_dict")
            self.Secondary_2_Primary_IDs_dict = get_Secondary_2_Primary_IDs_dict(read_from_flat_files=read_from_flat_files)

        if variables.VERBOSE:
            print("getting Taxid_2_FunctionEnum_2_Scores_dict")
        #     print("getting Taxid_2_FuncEnum_2_Score_2_Rank_dict")
        #     print("getting Taxid_2_FuncEnum_2_medianScore_dict")
        #     print("getting Taxid_2_FuncEnum_2_numBGvals_dict")
        self.Taxid_2_FunctionEnum_2_Scores_dict = get_Taxid_2_FunctionEnum_2_Scores_dict(read_from_flat_files=read_from_flat_files, as_array_or_as_list="array", taxid_2_proteome_count=None, from_pickle=True)
        # self.Taxid_2_FuncEnum_2_Score_2_Rank_dict = pickle.load(open(variables.tables_dict["Taxid_2_FuncEnum_2_Score_2_Rank_dict"], "rb"))
        # self.Taxid_2_FuncEnum_2_medianScore_dict = pickle.load(open(variables.tables_dict["Taxid_2_FuncEnum_2_medianScore_dict"], "rb"))
        # self.Taxid_2_FuncEnum_2_numBGvals_dict = pickle.load(open(variables.tables_dict["Taxid_2_FuncEnum_2_numBGvals_dict"], "rb"))


        if variables.VERBOSE:
            print("getting KEGG Taxid 2 TaxName acronym translation")
        self.kegg_taxid_2_acronym_dict = get_KEGG_Taxid_2_acronym_dict(read_from_flat_files=True) # small file doesn't make sense to keep in DB for now

        if variables.VERBOSE:
            print("getting lookup arrays")
        # if not low_memory: # override variables if "low_memory" passed to query initialization
        self.year_arr, self.hierlevel_arr, self.entitytype_arr, self.functionalterm_arr, self.indices_arr, self.description_arr, self.category_arr = get_lookup_arrays(read_from_flat_files, from_pickle=True)
        # else:
            # self.year_arr, self.hierlevel_arr, self.entitytype_arr, self.functionalterm_arr, self.indices_arr = get_lookup_arrays(low_memory, read_from_flat_files)
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
            print("getting taxid_2_proteins_dict")
        self.taxid_2_proteins_dict = get_taxid_2_proteins_dict()

        # cond_KS_etypes = self.etype_cond_dict["cond_25"] | self.etype_cond_dict["cond_26"] | self.etype_cond_dict["cond_20"]
        # self.KS_funcEnums_arr = self.indices_arr[cond_KS_etypes]


        if variables.VERBOSE:
            print("finished with PQO init")
            print("go go GO and fly like the wind")
            print("#" * 80)

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
                                        self.goslimtype_2_cond_dict, self.ENSP_2_rowIndex_dict, self.rowIndex_2_ENSP_dict, self.CSC_ENSPencoding_2_FuncEnum, self.CSR_ENSPencoding_2_FuncEnum,
                                        self.Taxid_2_FunctionEnum_2_Scores_dict)
                                        # self.Taxid_2_FunctionEnum_2_Scores_dict, self.Taxid_2_FuncEnum_2_Score_2_Rank_dict, self.Taxid_2_FuncEnum_2_medianScore_dict, self.Taxid_2_FuncEnum_2_numBGvals_dict)
        else:
            static_preloaded_objects = (self.year_arr, self.hierlevel_arr, self.entitytype_arr, self.functionalterm_arr, self.indices_arr,
                                        self.description_arr, self.category_arr,  # high mem --> only 62 MB
                                        self.etype_2_minmax_funcEnum, self.function_enumeration_len, self.etype_cond_dict, self.etype_2_num_functions_dict,
                                        self.taxid_2_proteome_count, self.taxid_2_tuple_funcEnum_index_2_associations_counts, self.lineage_dict_enum, self.blacklisted_terms_bool_arr,
                                        self.cond_etypes_with_ontology, self.cond_etypes_rem_foreground_ids, self.kegg_taxid_2_acronym_dict,
                                        self.goslimtype_2_cond_dict, self.ENSP_2_rowIndex_dict, self.rowIndex_2_ENSP_dict, self.CSC_ENSPencoding_2_FuncEnum, self.CSR_ENSPencoding_2_FuncEnum,
                                        self.Taxid_2_FunctionEnum_2_Scores_dict)
                                        # self.Taxid_2_FunctionEnum_2_Scores_dict, self.Taxid_2_FuncEnum_2_Score_2_Rank_dict, self.Taxid_2_FuncEnum_2_medianScore_dict, self.Taxid_2_FuncEnum_2_numBGvals_dict)
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
    # fn = r"/home/dblyon/agotool/data/PostgreSQL/tables/Lineage_table_hr.txt"
    lineage_dict = {} # key: function name, value: set of function names (all parents)
    if read_from_flat_files:
        fn = os.path.join(variables.TABLES_DIR, "Lineage_table_hr.txt")
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

def map_primary_2_secondary_ANs(ids_2_map, Primary_2_Secondary_IDs_dict=None, read_from_flat_files=False, ENSPs_only=False):
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
    result = get_results_of_statement("SELECT functions.an, functions.etype FROM functions; ")
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


if __name__ == "__main__":
    # pqo = PersistentQueryObject_STRING()

    ensp_list = ['I12R1_HUMAN', 'IL17D_HUMAN', 'GATB_HUMAN', 'ING3_HUMAN', 'GALC_HUMAN', 'HIG1C_HUMAN', 'IRAK2_HUMAN', 'GPR19_HUMAN', 'HXA7_HUMAN', 'IL17F_HUMAN', 'GIMA6_HUMAN', 'GP152_HUMAN', 'HDAC8_HUMAN', 'GNL3_HUMAN', 'ISL1_HUMAN', 'GPAA1_HUMAN', 'GALT_HUMAN', 'IRGQ_HUMAN', 'I17RB_HUMAN', 'GOG8J_HUMAN', 'GTSFL_HUMAN', 'HUTU_HUMAN', 'GNB1L_HUMAN', 'IL33_HUMAN', 'H2AW_HUMAN', 'IFT57_HUMAN', 'INLR1_HUMAN', 'HXB8_HUMAN', 'GLYL3_HUMAN', 'HGFL_HUMAN', 'HXC12_HUMAN', 'IFN21_HUMAN', 'GATA5_HUMAN', 'GRIA3_HUMAN', 'HRH3_HUMAN', 'IFIT1_HUMAN', 'IFM1_HUMAN', 'HEM3_HUMAN', 'IL27A_HUMAN', 'IGS22_HUMAN', 'IGKC_HUMAN', 'IKBD_HUMAN', 'GGNB2_HUMAN', 'GSTCD_HUMAN', 'GOG8H_HUMAN', 'GPS2_HUMAN', 'HCN4_HUMAN', 'IF5A2_HUMAN', 'GPBAR_HUMAN', 'GOG6A_HUMAN', 'GTR2_HUMAN', 'GATD1_HUMAN', 'HXC11_HUMAN', 'GDPD2_HUMAN', 'HV338_HUMAN', 'GPR22_HUMAN', 'HTR5A_HUMAN', 'HS90A_HUMAN', 'HXD13_HUMAN', 'GOG8N_HUMAN', 'IEX1_HUMAN', 'GDPP1_HUMAN', 'HXK2_HUMAN', 'IKZF2_HUMAN', 'HS74L_HUMAN', 'ILVBL_HUMAN', 'GALK1_HUMAN', 'HPSE_HUMAN', 'ITA1_HUMAN', 'IHO1_HUMAN', 'HMMR_HUMAN', 'GRCR2_HUMAN', 'GLIS3_HUMAN', 'IGLO5_HUMAN', 'GPR62_HUMAN', 'HS3S6_HUMAN', 'INT6L_HUMAN', 'GNAO_HUMAN', 'IL2RA_HUMAN', 'HHLA1_HUMAN', 'GRAH_HUMAN', 'GUC2D_HUMAN', 'GNDS_HUMAN', 'IGFL2_HUMAN', 'HME2_HUMAN', 'IMA5_HUMAN', 'HS3S2_HUMAN', 'H1FNT_HUMAN', 'GRIP2_HUMAN', 'GPSM1_HUMAN', 'HUNIN_HUMAN', 'GDF5O_HUMAN', 'HUTH_HUMAN', 'HDGR3_HUMAN', 'GLI4_HUMAN', 'HNRC1_HUMAN', 'ISLR2_HUMAN', 'GPM6B_HUMAN', 'IRX2_HUMAN', 'GUC2C_HUMAN', 'IFNL4_HUMAN', 'GIMA1_HUMAN', 'HXA1_HUMAN', 'GPBL1_HUMAN', 'GEN_HUMAN', 'GPCP1_HUMAN', 'IKIP_HUMAN', 'GG12F_HUMAN', 'HNRH3_HUMAN', 'GPTC4_HUMAN', 'GIMA7_HUMAN', 'IPP2L_HUMAN', 'GLT17_HUMAN', 'GP153_HUMAN', 'IVD_HUMAN', 'GRASP_HUMAN', 'GCYB1_HUMAN', 'IGSF5_HUMAN', 'IFNA8_HUMAN', 'IL1FA_HUMAN', 'HLTF_HUMAN', 'HS905_HUMAN', 'GSX2_HUMAN', 'HBEGF_HUMAN', 'HELQ_HUMAN', 'IFT56_HUMAN', 'GEMI_HUMAN', 'HDHD5_HUMAN', 'GLB1L_HUMAN', 'GBP2_HUMAN', 'GREB1_HUMAN', 'HXD8_HUMAN', 'I20L2_HUMAN', 'GPER1_HUMAN', 'HCN2_HUMAN', 'HV316_HUMAN', 'INT14_HUMAN', 'GCYB2_HUMAN', 'GG6L4_HUMAN', 'HMOX2_HUMAN', 'GMFB_HUMAN', 'GFI1B_HUMAN', 'HBAP1_HUMAN', 'INAR2_HUMAN', 'HV364_HUMAN', 'HV307_HUMAN', 'HASP_HUMAN', 'IFNE_HUMAN', 'GBG4_HUMAN', 'HEAT4_HUMAN', 'GPR78_HUMAN', 'GPC1_HUMAN', 'HNRPD_HUMAN', 'HXB9_HUMAN', 'IL21R_HUMAN', 'IFT25_HUMAN', 'GASP1_HUMAN', 'HEM6_HUMAN', 'GBP4_HUMAN', 'IFI44_HUMAN', 'GATA1_HUMAN', 'IPO7_HUMAN', 'HELLS_HUMAN', 'HLF_HUMAN', 'HPIP_HUMAN', 'IBP1_HUMAN', 'HNRC4_HUMAN', 'GDIB_HUMAN', 'HSPB9_HUMAN', 'GP108_HUMAN', 'IF1AX_HUMAN', 'GOG8S_HUMAN', 'GPHRA_HUMAN', 'HCDH_HUMAN', 'GXLT1_HUMAN', 'HMCES_HUMAN', 'HOP2_HUMAN', 'ITB8_HUMAN', 'GAK_HUMAN', 'IP3KC_HUMAN', 'IFIT3_HUMAN', 'GRIK3_HUMAN', 'GPAN1_HUMAN', 'HDAC2_HUMAN', 'HSF4_HUMAN', 'ITA4_HUMAN', 'HUNK_HUMAN', 'IKBZ_HUMAN', 'IN80B_HUMAN', 'IDHP_HUMAN', 'IQCF1_HUMAN', 'HYALP_HUMAN', 'IL17C_HUMAN', 'IL17B_HUMAN', 'INT12_HUMAN', 'IFNA7_HUMAN', 'GLPK3_HUMAN', 'HEN2_HUMAN', 'GDE1_HUMAN', 'GCNT4_HUMAN', 'IGJ_HUMAN', 'INS_HUMAN', 'IL1RA_HUMAN', 'GARS_HUMAN', 'GOLI4_HUMAN', 'HDGF_HUMAN', 'GSDMB_HUMAN', 'GRB7_HUMAN', 'IF4G1_HUMAN', 'GIPC1_HUMAN', 'GNMT_HUMAN', 'IGF1R_HUMAN', 'ILF2_HUMAN', 'INHBE_HUMAN', 'ITAM_HUMAN', 'GBG10_HUMAN', 'HAUS5_HUMAN', 'GG12G_HUMAN', 'HYKK_HUMAN', 'GUC1B_HUMAN', 'IGDC4_HUMAN', 'INADL_HUMAN', 'IIGP5_HUMAN', 'INT5_HUMAN', 'GP1BA_HUMAN', 'G3ST1_HUMAN', 'HEAT9_HUMAN', 'GP149_HUMAN', 'GP157_HUMAN', 'IMPA1_HUMAN', 'ITPR3_HUMAN', 'IL1B_HUMAN', 'IBP4_HUMAN', 'HLAA_HUMAN', 'ITIH2_HUMAN', 'HS3S4_HUMAN', 'GPR75_HUMAN', 'GRSF1_HUMAN', 'IGS21_HUMAN', 'GSG1_HUMAN', 'HDAC6_HUMAN', 'HPHL1_HUMAN', 'GPR35_HUMAN', 'GNTK_HUMAN', 'GP132_HUMAN', 'IDS_HUMAN', 'GTD2A_HUMAN', 'GATA4_HUMAN', 'HAUS2_HUMAN', 'GAK1A_HUMAN', 'I27L2_HUMAN', 'ITPR2_HUMAN', 'GO45_HUMAN', 'HNRPM_HUMAN', 'GON1_HUMAN', 'ICAM3_HUMAN', 'GCH1_HUMAN', 'GOG6C_HUMAN', 'HUTI_HUMAN', 'INSM1_HUMAN', 'IL9R_HUMAN', 'GTD2B_HUMAN', 'GRHL3_HUMAN', 'GVQW2_HUMAN', 'JAM3_HUMAN', 'HMGX3_HUMAN', 'IMA4_HUMAN', 'I10R2_HUMAN', 'GFRA1_HUMAN', 'GLPB_HUMAN', 'HPCA_HUMAN', 'I11RA_HUMAN', 'GSTT2_HUMAN', 'HDAC3_HUMAN', 'GPHRB_HUMAN', 'INKA1_HUMAN', 'GBRL3_HUMAN', 'GFOD1_HUMAN', 'GOGA2_HUMAN', 'IRF2_HUMAN', 'HERC6_HUMAN', 'GDS1_HUMAN', 'HYLS1_HUMAN', 'IN80C_HUMAN', 'INT6_HUMAN', 'INVS_HUMAN', 'GBG1_HUMAN', 'GPR26_HUMAN', 'HTRA3_HUMAN', 'GLGB_HUMAN', 'HAX1_HUMAN', 'HOME2_HUMAN', 'HIKES_HUMAN', 'IQCF6_HUMAN', 'IQCN_HUMAN', 'ITA7_HUMAN', 'IKKA_HUMAN', 'GPN3_HUMAN', 'GLIS1_HUMAN', 'GPC5D_HUMAN', 'GLTD2_HUMAN', 'GBG12_HUMAN', 'GAGE7_HUMAN', 'GSTP1_HUMAN', 'GNPAT_HUMAN', 'INSY2_HUMAN', 'GGCT_HUMAN', 'GP119_HUMAN', 'GLI2_HUMAN', 'IF2M_HUMAN', 'IL19_HUMAN', 'GPR83_HUMAN', 'ITIH4_HUMAN', 'HSH2D_HUMAN', 'GPR42_HUMAN', 'GRB2_HUMAN', 'IF4E3_HUMAN', 'GBRAP_HUMAN', 'HAUS6_HUMAN', 'HPGDS_HUMAN', 'GP158_HUMAN', 'INT1_HUMAN', 'H31_HUMAN', 'H2B2E_HUMAN', 'GP143_HUMAN', 'HM20A_HUMAN', 'GBRR3_HUMAN', 'HGNAT_HUMAN', 'GALD1_HUMAN', 'GSTT1_HUMAN', 'GZF1_HUMAN', 'GALR1_HUMAN', 'GLRX5_HUMAN', 'HFE_HUMAN', 'GA45G_HUMAN', 'HMGB4_HUMAN', 'GAN_HUMAN', 'HEXA_HUMAN', 'IL25_HUMAN', 'HEYL_HUMAN', 'GIPR_HUMAN', 'GRK5_HUMAN', 'GALT5_HUMAN', 'HBM_HUMAN', 'HNF6_HUMAN', 'G3PT_HUMAN', 'HYAL2_HUMAN', 'HUS1B_HUMAN', 'HXC5_HUMAN', 'IGLC3_HUMAN', 'GOG8K_HUMAN', 'GTR11_HUMAN', 'GATC_HUMAN', 'HIC2_HUMAN', 'IFI6_HUMAN', 'GEMI5_HUMAN', 'HEPS_HUMAN', 'IL13_HUMAN', 'HINT3_HUMAN', 'GOGA7_HUMAN', 'IRF9_HUMAN', 'GSG1L_HUMAN', 'IL31_HUMAN', 'GIMA4_HUMAN', 'GSLG1_HUMAN', 'GSTM1_HUMAN', 'GBP1_HUMAN', 'HECD1_HUMAN', 'IFT46_HUMAN', 'IN80D_HUMAN', 'ISLR_HUMAN', 'GBRL1_HUMAN', 'H2B2F_HUMAN', 'IL36A_HUMAN', 'HHEX_HUMAN', 'IZUM2_HUMAN', 'GBG14_HUMAN', 'HV158_HUMAN', 'ITB2_HUMAN', 'GIT2_HUMAN', 'GBB2_HUMAN', 'GPAT2_HUMAN', 'HNRL1_HUMAN', 'GANC_HUMAN', 'GLRA3_HUMAN', 'IKZF5_HUMAN', 'IRX1_HUMAN', 'H1T_HUMAN', 'GTPB6_HUMAN', 'H2A2A_HUMAN', 'GRM1_HUMAN', 'GAG2A_HUMAN', 'IGHG3_HUMAN', 'IGSF8_HUMAN', 'GA45B_HUMAN', 'IFT1B_HUMAN', 'HFM1_HUMAN', 'GTSF1_HUMAN', 'GLP3L_HUMAN', 'GGTL1_HUMAN', 'GNT2A_HUMAN', 'HIF1N_HUMAN', 'HAGHL_HUMAN', 'HV169_HUMAN', 'IGLC2_HUMAN', 'HNRH1_HUMAN', 'IKBP1_HUMAN', 'IOD3_HUMAN', 'GMEB1_HUMAN', 'GRM7_HUMAN', 'HERC1_HUMAN', 'HENMT_HUMAN', 'IBTK_HUMAN', 'I13R2_HUMAN', 'IFNW1_HUMAN', 'HES7_HUMAN', 'GOG8F_HUMAN', 'HUMMR_HUMAN', 'HACL1_HUMAN', 'IL26_HUMAN', 'HACD2_HUMAN', 'GAST_HUMAN', 'HBE_HUMAN', 'INO80_HUMAN', 'GPAM1_HUMAN', 'H0YIK9_HUMAN', 'GNAI2_HUMAN', 'GTR10_HUMAN', 'HTRA4_HUMAN', 'GABPA_HUMAN', 'GGTA1_HUMAN', 'GOG6B_HUMAN', 'IMP2L_HUMAN', 'HCAR2_HUMAN', 'IF4A1_HUMAN', 'HV349_HUMAN', 'GP148_HUMAN', 'GABR2_HUMAN', 'GGPPS_HUMAN', 'GGTL3_HUMAN', 'HDHD1_HUMAN', 'HMN6_HUMAN', 'HME1_HUMAN', 'GOLP3_HUMAN', 'GDF8_HUMAN', 'IPO8_HUMAN', 'GFRP_HUMAN', 'GTR7_HUMAN', 'GBG2_HUMAN', 'INP4B_HUMAN', 'GNAI1_HUMAN', 'HV330_HUMAN', 'I18RA_HUMAN', 'HAP40_HUMAN', 'HSF2_HUMAN', 'IKBL1_HUMAN', 'GBRA5_HUMAN', 'GALE_HUMAN', 'GPIX_HUMAN', 'GRAK_HUMAN', 'GLIS2_HUMAN', 'HNRL2_HUMAN', 'GHR_HUMAN', 'G6B_HUMAN', 'HMCN2_HUMAN', 'INT7_HUMAN', 'GNL1_HUMAN', 'ITPA_HUMAN', 'IFT80_HUMAN', 'G3ST4_HUMAN', 'INT8_HUMAN', 'HHLA3_HUMAN', 'GRPR_HUMAN', 'GOLI_HUMAN', 'GP179_HUMAN', 'GID4_HUMAN', 'GTSE1_HUMAN', 'HORN_HUMAN', 'HMX1_HUMAN', 'GLYLB_HUMAN', 'IF172_HUMAN', 'HIPL2_HUMAN', 'IGIP_HUMAN', 'GG6L6_HUMAN', 'GORS1_HUMAN', 'IF2B3_HUMAN', 'GPT2L_HUMAN', 'HRK_HUMAN', 'IFN10_HUMAN', 'GNL3L_HUMAN', 'HACE1_HUMAN', 'I23O1_HUMAN', 'G32P1_HUMAN', 'IGFR1_HUMAN', 'ISCU_HUMAN', 'HVD82_HUMAN', 'HERP2_HUMAN', 'GPR18_HUMAN', 'GBA3_HUMAN', 'GLSK_HUMAN', 'GCN1_HUMAN', 'HACD1_HUMAN', 'H3Y_HUMAN', 'IBP2_HUMAN', 'I2BPL_HUMAN', 'IMPA2_HUMAN', 'GLPA_HUMAN', 'IL5_HUMAN', 'IL18_HUMAN', 'IDH3G_HUMAN', 'ITA11_HUMAN', 'GALA_HUMAN', 'G3ST3_HUMAN', 'GRIN2_HUMAN', 'GPT_HUMAN', 'HIPL1_HUMAN', 'H2B1K_HUMAN', 'INT3_HUMAN', 'HDX_HUMAN', 'GARE1_HUMAN', 'GTF2I_HUMAN', 'HV69D_HUMAN', 'GAG13_HUMAN', 'IF4G2_HUMAN', 'GG6L3_HUMAN', 'GSDME_HUMAN', 'GLYG_HUMAN', 'GALK2_HUMAN', 'GSK3B_HUMAN', 'HXD11_HUMAN', 'GSTK1_HUMAN', 'HDAC1_HUMAN', 'GPR52_HUMAN', 'GOGA3_HUMAN', 'IDI1_HUMAN', 'GPX5_HUMAN', 'GPI8_HUMAN', 'HDBP1_HUMAN', 'HV741_HUMAN', 'HSPB6_HUMAN', 'IL10_HUMAN', 'HBG2_HUMAN', 'IL23R_HUMAN', 'GA2L2_HUMAN', 'IF44L_HUMAN', 'HERC2_HUMAN', 'IPO13_HUMAN', 'ITAE_HUMAN', 'HEM2_HUMAN', 'HSBPL_HUMAN', 'GRK4_HUMAN', 'GARE2_HUMAN', 'GP174_HUMAN', 'G6PC_HUMAN', 'GRK7_HUMAN', 'IFIX_HUMAN', 'HV434_HUMAN', 'GDAP2_HUMAN', 'GHDC_HUMAN', 'ITA2B_HUMAN', 'GCP60_HUMAN', 'GBX1_HUMAN', 'GPR63_HUMAN', 'IQCB1_HUMAN', 'JAM1_HUMAN', 'GT251_HUMAN', 'GBRB1_HUMAN', 'HMHB1_HUMAN', 'GMPPA_HUMAN', 'HXA6_HUMAN', 'IMA3_HUMAN', 'HID1_HUMAN', 'GFI1_HUMAN', 'GLOD5_HUMAN', 'I17RC_HUMAN', 'G3BP2_HUMAN', 'HOME3_HUMAN', 'IL32_HUMAN', 'IFT52_HUMAN', 'HSP76_HUMAN', 'H2A1H_HUMAN', 'GCP5_HUMAN', 'GRAM_HUMAN', 'IBPL1_HUMAN', 'INSRR_HUMAN', 'ICOSL_HUMAN', 'IMUP_HUMAN', 'HACD3_HUMAN', 'HV432_HUMAN', 'GGT1_HUMAN', 'GYS1_HUMAN', 'GOG8Q_HUMAN', 'GNLY_HUMAN', 'HXB4_HUMAN', 'IF5AL_HUMAN', 'GSTM5_HUMAN', 'IL3_HUMAN', 'ITA2_HUMAN', 'JAZF1_HUMAN', 'GG12C_HUMAN', 'GBRG2_HUMAN', 'GLSL_HUMAN', 'HMHA1_HUMAN', 'IRF8_HUMAN', 'GAFA1_HUMAN', 'IFT20_HUMAN', 'IGSF6_HUMAN', 'HMN7_HUMAN', 'GPTC1_HUMAN', 'GAG10_HUMAN', 'HV311_HUMAN', 'IL16_HUMAN', 'GDF2_HUMAN', 'HMN12_HUMAN', 'HRG_HUMAN', 'H2B1D_HUMAN', 'GDIR2_HUMAN', 'GIN1_HUMAN', 'GBRD_HUMAN', 'GRIN1_HUMAN', 'HNRPL_HUMAN', 'HXK1_HUMAN', 'GLI1_HUMAN', 'GUSP1_HUMAN', 'HMGA2_HUMAN', 'GOG8C_HUMAN', 'GPAT1_HUMAN', 'HEAS1_HUMAN', 'ITK_HUMAN', 'IGHD_HUMAN', 'H4_HUMAN', 'HDDC2_HUMAN', 'IGLC7_HUMAN', 'HSP13_HUMAN', 'GPR82_HUMAN', 'GLNA_HUMAN', 'GPR55_HUMAN', 'IFT81_HUMAN', 'H31T_HUMAN', 'GABP1_HUMAN', 'GP183_HUMAN', 'HP1B3_HUMAN', 'IPP2_HUMAN', 'IL17_HUMAN', 'GLP2R_HUMAN', 'H3X_HUMAN', 'HBAT_HUMAN', 'HEXI1_HUMAN', 'IRX5_HUMAN', 'GKN1_HUMAN', 'GALT6_HUMAN', 'HV226_HUMAN', 'HM20B_HUMAN', 'JADE3_HUMAN', 'HARB1_HUMAN', 'HNRDL_HUMAN', 'IF2B1_HUMAN', 'H14_HUMAN', 'INHBA_HUMAN', 'IDLC_HUMAN', 'GG12I_HUMAN', 'HGB1A_HUMAN', 'ITIH3_HUMAN', 'GGTL2_HUMAN', 'GDAP1_HUMAN', 'GDF10_HUMAN', 'GBP7_HUMAN', 'IF4B_HUMAN', 'ILDR1_HUMAN', 'IL6RA_HUMAN', 'GML_HUMAN', 'HILS1_HUMAN', 'HPCL4_HUMAN', 'HMX3_HUMAN', 'GCYA2_HUMAN', 'H2B3B_HUMAN', 'GBRG1_HUMAN', 'H2B1O_HUMAN', 'ISPD_HUMAN', 'GSTA3_HUMAN', 'IQEC2_HUMAN', 'HXA4_HUMAN', 'GAG2B_HUMAN', 'HAP28_HUMAN', 'HUWE1_HUMAN', 'I17RD_HUMAN', 'HEXB_HUMAN', 'IGLC1_HUMAN', 'GGT2_HUMAN', 'ISK7_HUMAN', 'ILRL1_HUMAN', 'GDF7_HUMAN', 'GG6L1_HUMAN', 'ISK8_HUMAN', 'HEM1_HUMAN', 'HMN10_HUMAN', 'JAG1_HUMAN', 'ITF2_HUMAN', 'GLTP_HUMAN', 'HSFX3_HUMAN', 'GFRA2_HUMAN', 'GLBL2_HUMAN', 'GCP6_HUMAN', 'I2BP1_HUMAN', 'ITM2B_HUMAN', 'HOOK2_HUMAN', 'INSL5_HUMAN', 'JCAD_HUMAN', 'GNAL_HUMAN', 'GEMI8_HUMAN', 'GLI3_HUMAN', 'ICT1_HUMAN', 'GRB1L_HUMAN', 'HEAT6_HUMAN', 'G3BP1_HUMAN', 'IQCM_HUMAN', 'GSAML_HUMAN', 'GHITM_HUMAN', 'ITM2A_HUMAN', 'GSTM4_HUMAN', 'GIMD1_HUMAN', 'HGD_HUMAN', 'GLT11_HUMAN', 'GYS2_HUMAN', 'HV270_HUMAN', 'IP6K3_HUMAN', 'HLAB_HUMAN', 'GPR88_HUMAN', 'HEM4_HUMAN', 'HIPK1_HUMAN', 'HAUS8_HUMAN', 'GIP_HUMAN', 'IBADT_HUMAN', 'GPR85_HUMAN', 'HSPB1_HUMAN', 'HDA10_HUMAN', 'IQCJ_HUMAN', 'GUAD_HUMAN', 'IDH3B_HUMAN', 'HIRA_HUMAN', 'IF2B2_HUMAN', 'GSHB_HUMAN', 'IF16_HUMAN', 'GLYC_HUMAN', 'GASR_HUMAN', 'GDIA_HUMAN', 'GMDS_HUMAN', 'IKKE_HUMAN', 'HYPK_HUMAN', 'IL2_HUMAN', 'IQGA2_HUMAN', 'GCC2_HUMAN', 'GET4_HUMAN', 'GABP2_HUMAN', 'HRES1_HUMAN', 'GIMA8_HUMAN', 'G37L1_HUMAN', 'HVCN1_HUMAN', 'HV146_HUMAN', 'GTDC1_HUMAN', 'GTR3_HUMAN', 'IGHE_HUMAN', 'HYAS1_HUMAN', 'GCP4_HUMAN', 'HELB_HUMAN', 'IL31R_HUMAN', 'IQGA3_HUMAN', 'GBG3_HUMAN', 'H2B1A_HUMAN', 'ITB7_HUMAN', 'H0YIQ5_HUMAN', 'HMOX1_HUMAN', 'IGF1_HUMAN', 'HCAR3_HUMAN', 'GLPE_HUMAN', 'IGHM_HUMAN', 'GCM1_HUMAN', 'IZUM3_HUMAN', 'GRM6_HUMAN', 'GPHA2_HUMAN', 'IGHA2_HUMAN', 'HNF1A_HUMAN', 'GLUC_HUMAN', 'HMGN2_HUMAN', 'INSR_HUMAN', 'GDF3_HUMAN', 'GSK3A_HUMAN', 'HEP2_HUMAN', 'GP141_HUMAN', 'HNF1B_HUMAN', 'GANP_HUMAN', 'GPDA_HUMAN', 'HLAH_HUMAN', 'HV335_HUMAN', 'IF2P_HUMAN', 'ISK13_HUMAN', 'GSE1_HUMAN', 'GALM_HUMAN', 'IQCF5_HUMAN', 'JAM2_HUMAN', 'IN35_HUMAN', 'HORM2_HUMAN', 'GBRA1_HUMAN', 'H6ST2_HUMAN', 'HMGX4_HUMAN', 'HMSD_HUMAN', 'IFNL3_HUMAN', 'HG2A_HUMAN', 'HERP1_HUMAN', 'GTR1_HUMAN', 'ING2_HUMAN', 'GLT14_HUMAN', 'GRK6_HUMAN', 'H2A1A_HUMAN', 'IFM2_HUMAN', 'IRS4_HUMAN', 'GT2D1_HUMAN', 'H0YIQ3_HUMAN', 'HNMT_HUMAN', 'IBP6_HUMAN', 'GP150_HUMAN', 'I12R2_HUMAN', 'IQCC_HUMAN', 'GPV_HUMAN', 'IL23A_HUMAN', 'G6PT3_HUMAN', 'IFFO1_HUMAN', 'INSI1_HUMAN', 'GPSM3_HUMAN', 'GASP2_HUMAN', 'IPPK_HUMAN', 'IPKG_HUMAN', 'GSHR_HUMAN', 'GP2_HUMAN', 'IRS2_HUMAN', 'HS902_HUMAN', 'IL4RA_HUMAN', 'GP107_HUMAN', 'ITAV_HUMAN', 'GGH_HUMAN', 'IQGA1_HUMAN', 'IDH3A_HUMAN', 'HV103_HUMAN', 'HIG1A_HUMAN', 'H2A2C_HUMAN', 'HAOX2_HUMAN', 'HMGN5_HUMAN', 'GS1L2_HUMAN', 'IRX4_HUMAN', 'GPT11_HUMAN', 'GHRL_HUMAN', 'GGA2_HUMAN', 'GRM4_HUMAN', 'H2AV_HUMAN', 'HIPK4_HUMAN', 'INT2_HUMAN', 'GCNT3_HUMAN', 'HV428_HUMAN', 'HV320_HUMAN', 'GAL3B_HUMAN', 'HV315_HUMAN', 'GL8D1_HUMAN', 'ITCH_HUMAN', 'GT253_HUMAN', 'ISG15_HUMAN', 'IMPG2_HUMAN', 'GALT2_HUMAN', 'GOG8A_HUMAN', 'GPR21_HUMAN', 'IPIL2_HUMAN', 'GST2_HUMAN', 'JADE2_HUMAN', 'GRP3_HUMAN', 'ITA3_HUMAN', 'GNRR2_HUMAN', 'HERC4_HUMAN', 'GLOD4_HUMAN', 'HABP2_HUMAN', 'GRIA2_HUMAN', 'GLP1R_HUMAN', 'GKAP1_HUMAN', 'GLR_HUMAN', 'H2B1J_HUMAN', 'INT10_HUMAN', 'HXA11_HUMAN', 'JAK2_HUMAN', 'HMCN1_HUMAN', 'GANAB_HUMAN', 'GROA_HUMAN', 'HPLN1_HUMAN', 'IPKA_HUMAN', 'HSP7C_HUMAN', 'G45IP_HUMAN', 'IF2B_HUMAN', 'IFNA4_HUMAN', 'IRF5_HUMAN', 'GPHB5_HUMAN', 'ICLN_HUMAN', 'GOG8O_HUMAN', 'IF4E_HUMAN', 'GLT13_HUMAN', 'GOT1A_HUMAN', 'JADE1_HUMAN', 'GLT18_HUMAN', 'GLUCM_HUMAN', 'ILKAP_HUMAN', 'GAB3_HUMAN', 'HAT1_HUMAN', 'HXA13_HUMAN', 'IFNA5_HUMAN', 'HEPN1_HUMAN', 'HSFX1_HUMAN', 'ICEF1_HUMAN', 'GPR4_HUMAN', 'HIP1R_HUMAN', 'GCC1_HUMAN', 'GSTM2_HUMAN', 'HLPDA_HUMAN', 'ID3_HUMAN', 'GBGT2_HUMAN', 'HMGN3_HUMAN', 'INKA2_HUMAN', 'IP3KB_HUMAN', 'GOGA5_HUMAN', 'ISK14_HUMAN', 'INO1_HUMAN', 'GNA11_HUMAN', 'GOG8T_HUMAN', 'GBB1_HUMAN', 'GR6_HUMAN', 'ITGBL_HUMAN', 'GRAN_HUMAN', 'INAVA_HUMAN', 'HEMGN_HUMAN', 'HGS_HUMAN', 'HEMO_HUMAN', 'GRAPL_HUMAN', 'IKZF1_HUMAN', 'ICA69_HUMAN', 'GPR6_HUMAN', 'GNAQ_HUMAN', 'IWS1_HUMAN', 'HEPH_HUMAN', 'ICA1L_HUMAN', 'IL15_HUMAN', 'GPA33_HUMAN', 'GNPTA_HUMAN', 'HV323_HUMAN', 'IL34_HUMAN', 'HECD3_HUMAN', 'ITSN1_HUMAN', 'G3P_HUMAN', 'GA2L3_HUMAN', 'HEY1_HUMAN', 'INGR2_HUMAN', 'HSP1_HUMAN', 'ITLN1_HUMAN', 'HRCT1_HUMAN', 'HSPB8_HUMAN', 'ITB1_HUMAN', 'IMA7_HUMAN', 'IFNA6_HUMAN', 'GPR39_HUMAN', 'ISY1_HUMAN', 'GPN2_HUMAN', 'IL2RB_HUMAN', 'HPS3_HUMAN', 'HSP72_HUMAN', 'GRTP1_HUMAN', 'IDD_HUMAN', 'GPR1_HUMAN', 'HMN4_HUMAN', 'H4G_HUMAN', 'GRPL2_HUMAN', 'GAPR1_HUMAN', 'GLRX1_HUMAN', 'G6PI_HUMAN', 'GOG6D_HUMAN', 'GPX1_HUMAN', 'GLCM_HUMAN', 'GDE_HUMAN', 'GSH1_HUMAN', 'GMPR2_HUMAN', 'GCM2_HUMAN', 'GP101_HUMAN', 'GLYG2_HUMAN', 'IQIP1_HUMAN', 'HIC1_HUMAN', 'HELZ_HUMAN', 'HEXI2_HUMAN', 'HV781_HUMAN', 'HIP1_HUMAN', 'IL36B_HUMAN', 'GSC2_HUMAN', 'HV439_HUMAN', 'HS3S1_HUMAN', 'IKBE_HUMAN', 'GPC4_HUMAN', 'INCE_HUMAN', 'I20RA_HUMAN', 'HAVR2_HUMAN', 'HXK3_HUMAN', 'HS71L_HUMAN', 'I27L1_HUMAN', 'IRS1_HUMAN', 'HEN1_HUMAN', 'INHBC_HUMAN', 'IL11_HUMAN', 'GPR61_HUMAN', 'HIRP3_HUMAN', 'GDPD4_HUMAN', 'H3C_HUMAN', 'GNRHR_HUMAN', 'GMCL1_HUMAN', 'GNPTG_HUMAN', 'GCP2_HUMAN', 'HXC6_HUMAN', 'HTF4_HUMAN', 'HS904_HUMAN', 'IP6K1_HUMAN', 'GBRT_HUMAN', 'GORAB_HUMAN', 'IN80E_HUMAN', 'GAMT_HUMAN', 'GBG13_HUMAN', 'GP162_HUMAN', 'GLYAT_HUMAN', 'IRAK1_HUMAN', 'GP176_HUMAN', 'H17B6_HUMAN', 'GOG8B_HUMAN', 'G5E9R7_HUMAN', 'HD101_HUMAN', 'HINT2_HUMAN', 'HVC33_HUMAN', 'GP182_HUMAN', 'IL37_HUMAN', 'GON2_HUMAN', 'HPSE2_HUMAN', 'GPX6_HUMAN', 'HYOU1_HUMAN', 'HSFX4_HUMAN', 'IFNB_HUMAN', 'GON4L_HUMAN', 'ITA6_HUMAN', 'HNF4A_HUMAN', 'ITLN2_HUMAN', 'GLRA1_HUMAN', 'GPX4_HUMAN', 'G137C_HUMAN', 'ICOS_HUMAN', 'GLCM1_HUMAN', 'HPS5_HUMAN', 'GRDN_HUMAN', 'GTPB1_HUMAN', 'I13R1_HUMAN', 'GRIN3_HUMAN', 'HDA11_HUMAN', 'IPP2B_HUMAN', 'IL1A_HUMAN', 'IF3M_HUMAN', 'GPC6A_HUMAN', 'IL21_HUMAN', 'IL2RG_HUMAN', 'GG12J_HUMAN', 'HBS1L_HUMAN', 'HXB7_HUMAN', 'GPVI_HUMAN', 'IR3IP_HUMAN', 'HNRPF_HUMAN', 'HCFC2_HUMAN', 'GFRA4_HUMAN', 'ITFG2_HUMAN', 'HXB5_HUMAN', 'HMGB2_HUMAN', 'IOD2_HUMAN', 'HTRA1_HUMAN', 'GGT5_HUMAN', 'JAK3_HUMAN', 'IL6_HUMAN', 'HDAC7_HUMAN', 'GLT10_HUMAN', 'GLO2_HUMAN', 'I17RE_HUMAN', 'GBRE_HUMAN', 'IGLL5_HUMAN', 'IF1AY_HUMAN', 'IYD1_HUMAN', 'GBRP_HUMAN', 'IFIH1_HUMAN', 'GPAT3_HUMAN', 'GG6L2_HUMAN', 'INT11_HUMAN', 'GBRR2_HUMAN', 'ITIH1_HUMAN', 'GSDMD_HUMAN', 'GLMP_HUMAN', 'IFAS1_HUMAN', 'GLIP1_HUMAN', 'GPR27_HUMAN', 'HMN8_HUMAN', 'INT13_HUMAN', 'GRAM4_HUMAN', 'H2AJ_HUMAN', 'GDF6_HUMAN', 'IG2AS_HUMAN', 'INGR1_HUMAN', 'HAIR_HUMAN', 'HYPDH_HUMAN', 'HMGB1_HUMAN', 'IFM5_HUMAN', 'GLPC_HUMAN', 'GSKIP_HUMAN', 'IBP3_HUMAN', 'ISK5_HUMAN', 'HXC8_HUMAN', 'IFT43_HUMAN', 'GRP75_HUMAN', 'GRM8_HUMAN', 'HDAC4_HUMAN', 'HSF5_HUMAN', 'GNB5_HUMAN', 'HIG1B_HUMAN', 'GRB10_HUMAN', 'HNF4G_HUMAN', 'GBP3_HUMAN', 'ITIH6_HUMAN', 'ID4_HUMAN', 'GT252_HUMAN', 'HOIL1_HUMAN', 'GLBL3_HUMAN', 'HYCCI_HUMAN', 'GBRA4_HUMAN', 'IGF2_HUMAN', 'GG6LA_HUMAN', 'GBA2_HUMAN', 'IDAS1_HUMAN', 'HNRPC_HUMAN', 'IFNK_HUMAN', 'INSL3_HUMAN', 'HLAF_HUMAN', 'IGHG1_HUMAN', 'HXA3_HUMAN', 'GRIK1_HUMAN', 'I22R1_HUMAN', 'GRM2A_HUMAN', 'HSP77_HUMAN', 'I27RA_HUMAN', 'HDAC5_HUMAN', 'HS3S5_HUMAN', 'HECW2_HUMAN', 'GMEB2_HUMAN', 'H33_HUMAN', 'H90B2_HUMAN', 'ISG20_HUMAN', 'HV309_HUMAN', 'GGYF1_HUMAN', 'GL1D1_HUMAN', 'HIS1_HUMAN', 'HDHD2_HUMAN', 'GRM3_HUMAN', 'GRAB_HUMAN', 'ITB5_HUMAN', 'IQCH_HUMAN', 'GP142_HUMAN', 'HSF1_HUMAN', 'I22R2_HUMAN', 'IL18R_HUMAN', 'ITSN2_HUMAN', 'GRP4_HUMAN', 'HPCL1_HUMAN', 'GDF15_HUMAN', 'H2B1L_HUMAN', 'HECA2_HUMAN', 'GCP3_HUMAN', 'GLYL2_HUMAN', 'GPR34_HUMAN', 'GDF11_HUMAN', 'IL1AP_HUMAN', 'HHATL_HUMAN', 'GVQW1_HUMAN', 'IFIT2_HUMAN', 'GRP2_HUMAN', 'GSDMA_HUMAN', 'ID2_HUMAN', 'GRL1A_HUMAN', 'GRPE2_HUMAN', 'I10R1_HUMAN', 'GUCD1_HUMAN', 'HAUS3_HUMAN', 'GA45A_HUMAN', 'HMR1_HUMAN', 'HIBCH_HUMAN', 'GRWD1_HUMAN', 'GLTL5_HUMAN', 'HMN13_HUMAN', 'GLCI1_HUMAN', 'HPPD_HUMAN', 'GLTL6_HUMAN', 'IDE_HUMAN', 'HACD4_HUMAN', 'GTPB3_HUMAN', 'G2E3_HUMAN', 'GNAT2_HUMAN', 'HPDL_HUMAN', 'GGA2B_HUMAN', 'HNRH2_HUMAN', 'GEMI7_HUMAN', 'HIF3A_HUMAN', 'GPX8_HUMAN', 'HV205_HUMAN', 'GCFC2_HUMAN', 'H1X_HUMAN', 'HRC23_HUMAN', 'ITBP1_HUMAN', 'HEAT1_HUMAN', 'H90B3_HUMAN', 'HS105_HUMAN', 'GC224_HUMAN', 'HPLN3_HUMAN', 'INMT_HUMAN', 'GABR1_HUMAN', 'GRM5_HUMAN', 'GOR_HUMAN', 'GSAS1_HUMAN', 'HPTR_HUMAN', 'GSAP_HUMAN', 'GPAT4_HUMAN', 'GPTC8_HUMAN', 'H6ST3_HUMAN', 'IF4A2_HUMAN', 'INT4_HUMAN', 'H2A1J_HUMAN', 'GBRA3_HUMAN', 'GSX1_HUMAN', 'HV461_HUMAN', 'HAND2_HUMAN', 'HTSF1_HUMAN', 'GD1L1_HUMAN', 'H11_HUMAN', 'HDC_HUMAN', 'ISK9_HUMAN', 'HORM1_HUMAN', 'GGA3_HUMAN', 'GPX7_HUMAN', 'GTR6_HUMAN', 'HOP_HUMAN', 'HMN5_HUMAN', 'GGNB1_HUMAN', 'GPC5_HUMAN', 'GRP_HUMAN', 'H2A3_HUMAN', 'GLHA_HUMAN', 'HV5X1_HUMAN', 'GALT3_HUMAN', 'HRH4_HUMAN', 'GLCNE_HUMAN', 'GOSR2_HUMAN', 'HS71A_HUMAN', 'HV108_HUMAN', 'ISK6_HUMAN', 'IQCE_HUMAN', 'I20RB_HUMAN', 'HNRPK_HUMAN', 'GAS7_HUMAN', 'IL22_HUMAN', 'ICAM2_HUMAN', 'GDPD5_HUMAN', 'GG6LS_HUMAN', 'JAG2_HUMAN', 'IPYR_HUMAN', 'GP156_HUMAN', 'GDC_HUMAN', 'GTPBA_HUMAN', 'GBGT1_HUMAN', 'GFOD2_HUMAN', 'GL8D2_HUMAN', 'GVQW3_HUMAN', 'ISK4_HUMAN', 'GBX2_HUMAN', 'ID2B_HUMAN', 'IFNA2_HUMAN', 'GEPH_HUMAN', 'ITPR1_HUMAN', 'IGS11_HUMAN', 'ITAD_HUMAN', 'IFM3_HUMAN', 'GFY_HUMAN', 'IF140_HUMAN', 'IFM10_HUMAN', 'IMA1_HUMAN', 'GPR87_HUMAN', 'GSTO1_HUMAN', 'GBG11_HUMAN', 'HXD3_HUMAN', 'HV348_HUMAN', 'HEBP2_HUMAN', 'GAPT_HUMAN', 'HCN3_HUMAN', 'GPC2_HUMAN', 'GUC1A_HUMAN', 'HXD4_HUMAN', 'GCNT7_HUMAN', 'GLMN_HUMAN', 'GRD2I_HUMAN', 'HXB3_HUMAN', 'GOSR1_HUMAN', 'GPX3_HUMAN', 'IL20_HUMAN', 'GORS2_HUMAN', 'IG2R_HUMAN', 'HV431_HUMAN', 'IQEC3_HUMAN', 'GAS2_HUMAN', 'HSPB7_HUMAN', 'ISL2_HUMAN', 'GFAP_HUMAN', 'GBRB3_HUMAN', 'GRAP2_HUMAN', 'IER5L_HUMAN', 'GGACT_HUMAN', 'HSPB3_HUMAN', 'IGS10_HUMAN', 'GNAI3_HUMAN', 'GP139_HUMAN', 'IL3RB_HUMAN', 'HIDE1_HUMAN', 'HSP74_HUMAN', 'HES1_HUMAN', 'IREB2_HUMAN', 'ITB4_HUMAN', 'GFRAL_HUMAN', 'GPR20_HUMAN', 'HV374_HUMAN', 'ICMT_HUMAN', 'GPR31_HUMAN', 'HELZ2_HUMAN', 'HPF1_HUMAN', 'IQCF3_HUMAN', 'HIF1A_HUMAN', 'IFFO2_HUMAN', 'H2AX_HUMAN', 'H2A1B_HUMAN', 'GATM_HUMAN', 'GAB1_HUMAN', 'IQUB_HUMAN', 'IASPP_HUMAN', 'HAKAI_HUMAN', 'IMA6_HUMAN', 'GPR33_HUMAN', 'GPTC3_HUMAN', 'GSTA5_HUMAN', 'HMDH_HUMAN', 'GPC5B_HUMAN', 'GSDMC_HUMAN', 'GALT7_HUMAN', 'GAAS1_HUMAN', 'IL9_HUMAN', 'IFI27_HUMAN', 'GHC2_HUMAN', 'GRID2_HUMAN', 'ISM2_HUMAN', 'GLRX2_HUMAN', 'HCK_HUMAN', 'ICK_HUMAN', 'IFN16_HUMAN', 'GTR12_HUMAN', 'HCD2_HUMAN', 'ILRUN_HUMAN', 'HXD12_HUMAN', 'GHC1_HUMAN', 'HV145_HUMAN', 'G6PE_HUMAN', 'ITAX_HUMAN', 'HEPC_HUMAN', 'IGFN1_HUMAN', 'HOT_HUMAN', 'HMGC2_HUMAN', 'HYDIN_HUMAN', 'HEG1_HUMAN', 'HV692_HUMAN', 'HNRC3_HUMAN', 'IPMK_HUMAN', 'HV353_HUMAN', 'GLRB_HUMAN', 'GPM6A_HUMAN', 'GBG5_HUMAN', 'IF122_HUMAN', 'ILDR2_HUMAN', 'HINFP_HUMAN', 'INAM2_HUMAN', 'HGF_HUMAN', 'HIPK3_HUMAN', 'HNRPU_HUMAN', 'IFN14_HUMAN', 'I15RA_HUMAN', 'HCLS1_HUMAN', 'HXC10_HUMAN', 'IF2G_HUMAN', 'GAPD1_HUMAN', 'IPKB_HUMAN', 'I5P1_HUMAN', 'HV118_HUMAN', 'HNRPR_HUMAN', 'GA2L1_HUMAN', 'IPP2C_HUMAN', 'HPS1_HUMAN', 'GRM2B_HUMAN', 'IF_HUMAN', 'IMDH1_HUMAN', 'INF2_HUMAN', 'H2AZ_HUMAN', 'GATA3_HUMAN', 'GGA1_HUMAN', 'HXC4_HUMAN', 'GRM2_HUMAN', 'GBRA2_HUMAN', 'INVO_HUMAN', 'IMDH2_HUMAN', 'IRX6_HUMAN', 'HXC9_HUMAN', 'HIG2A_HUMAN', 'HABP4_HUMAN', 'GIPC2_HUMAN', 'IF5A1_HUMAN', 'GUC2A_HUMAN', 'GBG7_HUMAN', 'GP171_HUMAN', 'GCYA1_HUMAN', 'IL4_HUMAN', 'GULP1_HUMAN', 'GRHL1_HUMAN', 'HTRA2_HUMAN', 'IGDC3_HUMAN', 'HV459_HUMAN', 'GLDN_HUMAN', 'GRIFN_HUMAN', 'HECD2_HUMAN', 'GEMI6_HUMAN', 'INP5K_HUMAN', 'GP151_HUMAN', 'IMPA3_HUMAN', 'H2AY_HUMAN', 'IPSP_HUMAN', 'GRIK5_HUMAN', 'HXD9_HUMAN', 'IPIL1_HUMAN', 'HCAR1_HUMAN', 'HS3SB_HUMAN', 'JAK1_HUMAN', 'GGE2D_HUMAN', 'GOGA4_HUMAN', 'IRF1_HUMAN', 'HBG1_HUMAN', 'HNRPQ_HUMAN', 'HV321_HUMAN', 'HEBP1_HUMAN', 'GBF1_HUMAN', 'H2B1C_HUMAN', 'GAB2_HUMAN', 'GPRL1_HUMAN', 'I17EL_HUMAN', 'GNPI2_HUMAN', 'IL8_HUMAN', 'HYAS2_HUMAN', 'IF4H_HUMAN', 'IFNL1_HUMAN', 'GALT1_HUMAN', 'GRK1_HUMAN', 'GMIP_HUMAN', 'GCST_HUMAN', 'GALR2_HUMAN', 'HES5_HUMAN', 'GTR8_HUMAN', 'HJURP_HUMAN', 'HMGN4_HUMAN', 'HM13_HUMAN', 'ISCA2_HUMAN', 'GADL1_HUMAN', 'GTSC1_HUMAN', 'HXB2_HUMAN', 'ICAM5_HUMAN', 'HCP5_HUMAN', 'H2A1C_HUMAN', 'IF2A_HUMAN', 'HTR5B_HUMAN', 'ILRL2_HUMAN', 'GKN2_HUMAN', 'HIS3_HUMAN', 'GEMI2_HUMAN', 'HEY2_HUMAN', 'HPF1L_HUMAN', 'IBP5_HUMAN', 'IF4G3_HUMAN', 'GLE1_HUMAN', 'IGHG2_HUMAN', 'ILF3_HUMAN', 'ICE2_HUMAN', 'GBP5_HUMAN', 'GOGA1_HUMAN', 'GBP6_HUMAN', 'GPSM2_HUMAN', 'GRHL2_HUMAN', 'IRAK4_HUMAN', 'GRPE1_HUMAN', 'HES3_HUMAN', 'GRAP1_HUMAN', 'HPLN4_HUMAN', 'HTAI2_HUMAN', 'HPS6_HUMAN', 'GGT6_HUMAN', 'HEMK1_HUMAN', 'GBRG3_HUMAN', 'H2B2C_HUMAN', 'IKBA_HUMAN', 'GBRB2_HUMAN', 'IPO4_HUMAN', 'GPR32_HUMAN', 'IRF6_HUMAN', 'GG12H_HUMAN', 'ITB6_HUMAN', 'HSP7E_HUMAN', 'IGHA1_HUMAN', 'GL6D1_HUMAN', 'INCA1_HUMAN', 'GCSH_HUMAN', 'IMP4_HUMAN', 'HYI_HUMAN', 'HERC5_HUMAN', 'HES4_HUMAN', 'ING1_HUMAN', 'GPC3_HUMAN', 'G6PC2_HUMAN', 'HELT_HUMAN', 'HSBP1_HUMAN', 'INSL6_HUMAN', 'INSC_HUMAN', 'H1BP3_HUMAN', 'GELS_HUMAN', 'IFRD1_HUMAN', 'HV124_HUMAN', 'GNAS1_HUMAN', 'GABT_HUMAN', 'IGLL1_HUMAN', 'HXA5_HUMAN', 'GCOM2_HUMAN', 'GLU2B_HUMAN', 'I18BP_HUMAN', 'GTR9_HUMAN', 'HLAG_HUMAN', 'GATA2_HUMAN', 'HXB6_HUMAN', 'GP173_HUMAN', 'GP180_HUMAN', 'IQCK_HUMAN', 'GRIA1_HUMAN', 'HBP1_HUMAN', 'IPO11_HUMAN', 'GOG8M_HUMAN', 'GGN_HUMAN', 'HMBX1_HUMAN', 'GIMA5_HUMAN', 'GOG8I_HUMAN', 'IZUM1_HUMAN', 'GLT12_HUMAN', 'GP135_HUMAN', 'HECD4_HUMAN', 'G6PD_HUMAN', 'GBRA6_HUMAN', 'GON7_HUMAN', 'GP1BB_HUMAN', 'HINT1_HUMAN', 'GALNS_HUMAN', 'GOLM1_HUMAN', 'GG6LV_HUMAN', 'HV64D_HUMAN', 'GRCR1_HUMAN', 'IKZF3_HUMAN', 'IL36G_HUMAN', 'HSDL1_HUMAN', 'IMPCT_HUMAN', 'GATA_HUMAN', 'INHA_HUMAN', 'IPO9_HUMAN', 'HHAT_HUMAN', 'IBP7_HUMAN', 'IF2GL_HUMAN', 'GNAT3_HUMAN', 'HEMH_HUMAN', 'GAS1_HUMAN', 'GPD1L_HUMAN', 'GLRA2_HUMAN', 'GRIK4_HUMAN', 'HV601_HUMAN', 'ITPK1_HUMAN', 'HYAL3_HUMAN', 'GOGB1_HUMAN', 'HBAZ_HUMAN', 'G6PT1_HUMAN', 'GOPC_HUMAN', 'GUC2B_HUMAN', 'HV366_HUMAN', 'HXA2_HUMAN', 'GPTC2_HUMAN', 'GIMA2_HUMAN', 'IOD1_HUMAN', 'H2B1B_HUMAN', 'GCR_HUMAN', 'GUF1_HUMAN', 'GLRX3_HUMAN', 'IGFL1_HUMAN', 'GAG2E_HUMAN', 'GNPI1_HUMAN', 'HECAM_HUMAN', 'GMFG_HUMAN', 'GSC_HUMAN', 'GPR12_HUMAN', 'HDAC9_HUMAN', 'GARL3_HUMAN', 'IL3RA_HUMAN', 'GAK1B_HUMAN', 'HV313_HUMAN', 'IQEC1_HUMAN', 'IKKB_HUMAN', 'GGEE3_HUMAN', 'GILT_HUMAN', 'HMGA1_HUMAN', 'GPR84_HUMAN', 'GEM_HUMAN', 'HCFC1_HUMAN', 'INP4A_HUMAN', 'JAGN1_HUMAN', 'HS12B_HUMAN', 'HS71B_HUMAN', 'HRG1_HUMAN', 'GEMC1_HUMAN', 'H2B1H_HUMAN', 'IDI2_HUMAN', 'GTPB8_HUMAN', 'HV372_HUMAN', 'IQCF2_HUMAN', 'HYES_HUMAN', 'GP160_HUMAN', 'GSTA4_HUMAN', 'IAPP_HUMAN', 'HV343_HUMAN', 'GAK24_HUMAN', 'HECW1_HUMAN', 'IGFL4_HUMAN', 'ITBP2_HUMAN', 'GAK5_HUMAN', 'IL12B_HUMAN', 'GLUT4_HUMAN', 'IRX3_HUMAN', 'HLAC_HUMAN', 'HXD1_HUMAN', 'GA113_HUMAN', 'GRHPR_HUMAN', 'GSTT4_HUMAN', 'HCST_HUMAN', 'HV70D_HUMAN', 'GATA6_HUMAN', 'GNA14_HUMAN', 'IF6_HUMAN', 'GDF5_HUMAN', 'IRPL1_HUMAN', 'HXK4_HUMAN', 'HOGA1_HUMAN', 'GAGE5_HUMAN', 'INPP_HUMAN', 'H2A2B_HUMAN', 'HYPM_HUMAN', 'HPLN2_HUMAN', 'GUC1C_HUMAN', 'INE1_HUMAN', 'GDNF_HUMAN', 'ISX_HUMAN', 'IER5_HUMAN', 'GLYL1_HUMAN', 'HHLA2_HUMAN', 'IF4E2_HUMAN', 'H10_HUMAN', 'HLX_HUMAN', 'HS3SA_HUMAN', 'INT9_HUMAN', 'HXB1_HUMAN', 'HNRC2_HUMAN', 'HAOX1_HUMAN', 'ILK_HUMAN', 'GBG8_HUMAN', 'GPKOW_HUMAN', 'GAS6_HUMAN', 'HYAS3_HUMAN', 'INTU_HUMAN', 'GKN3_HUMAN', 'IGLC6_HUMAN', 'GPBP1_HUMAN', 'GP146_HUMAN', 'GALT9_HUMAN', 'GNA12_HUMAN', 'INSI2_HUMAN', 'HOOK3_HUMAN', 'GAGE1_HUMAN', 'H6ST1_HUMAN', 'GREM2_HUMAN', 'IGSF3_HUMAN', 'HV333_HUMAN', 'GRIA4_HUMAN', 'HMX2_HUMAN', 'HYAL1_HUMAN', 'G6PC3_HUMAN', 'IMPG1_HUMAN', 'HESX1_HUMAN', 'GHSR_HUMAN', 'IGSF1_HUMAN', 'GNA13_HUMAN', 'GCSP_HUMAN', 'GP161_HUMAN', 'IL6RB_HUMAN', 'GBB3_HUMAN', 'IFT22_HUMAN', 'HJ01_HUMAN', 'GFPT2_HUMAN', 'I4E1B_HUMAN', 'IL7RA_HUMAN', 'ITPI1_HUMAN', 'GOG8D_HUMAN', 'GIPC3_HUMAN', 'HAND1_HUMAN', 'GRAA_HUMAN', 'HDGR2_HUMAN', 'HRH2_HUMAN', 'GPR3_HUMAN', 'HVD34_HUMAN', 'HSF2B_HUMAN', 'GPR37_HUMAN', 'INAM1_HUMAN', 'IFT74_HUMAN', 'HMN11_HUMAN', 'HKDC1_HUMAN', 'GBRR1_HUMAN', 'GDPD1_HUMAN', 'GOG7B_HUMAN', 'GNAZ_HUMAN', 'INSL4_HUMAN', 'IAH1_HUMAN', 'HV102_HUMAN', 'HAUS7_HUMAN', 'IST1_HUMAN', 'ISCA1_HUMAN', 'I5P2_HUMAN', 'GAB4_HUMAN', 'JAML_HUMAN', 'HVC05_HUMAN', 'IPP_HUMAN', 'HV551_HUMAN', 'ICAM1_HUMAN', 'IL12A_HUMAN', 'HAP1_HUMAN', 'H15_HUMAN', 'H90B4_HUMAN', 'HBB_HUMAN', 'INAR1_HUMAN', 'GWL_HUMAN', 'H2B1N_HUMAN', 'H2BFM_HUMAN', 'INSR2_HUMAN', 'HOME1_HUMAN', 'IGHG4_HUMAN', 'GPR15_HUMAN', 'GCKR_HUMAN', 'IFNL2_HUMAN', 'GPR17_HUMAN', 'HGH1_HUMAN', 'IFIT5_HUMAN', 'INHBB_HUMAN', 'GPC5C_HUMAN', 'IDUA_HUMAN', 'H2A1D_HUMAN', 'GSH0_HUMAN', 'GLCE_HUMAN', 'IPO5_HUMAN', 'GPN1_HUMAN', 'GLPK2_HUMAN', 'HXB13_HUMAN', 'GLD2_HUMAN', 'IHH_HUMAN', 'IL24_HUMAN', 'GINM1_HUMAN', 'GG6L9_HUMAN', 'GLT15_HUMAN', 'GLYM_HUMAN', 'G6PT2_HUMAN', 'HMN3_HUMAN', 'ITAL_HUMAN', 'IPYR2_HUMAN', 'IFRD2_HUMAN', 'GLPK5_HUMAN', 'GOG8R_HUMAN', 'I2BP2_HUMAN', 'IDHC_HUMAN', 'HD_HUMAN', 'H2BFS_HUMAN', 'GREM1_HUMAN', 'HS12A_HUMAN', 'HOMEZ_HUMAN', 'IGFL3_HUMAN', 'HBA_HUMAN', 'IFN17_HUMAN', 'GXLT2_HUMAN', 'GP155_HUMAN', 'GLT16_HUMAN', 'GRIK2_HUMAN', 'I36RA_HUMAN', 'HMN2_HUMAN', 'GSTM3_HUMAN', 'GAR1_HUMAN', 'INP5E_HUMAN', 'GNS_HUMAN', 'GCDH_HUMAN', 'GFPT1_HUMAN', 'GPC6_HUMAN', 'GTPB2_HUMAN', 'HCN1_HUMAN', 'GTR14_HUMAN', 'IQCAL_HUMAN', 'GNA15_HUMAN', 'H2AB1_HUMAN', 'GRAP_HUMAN', 'GNAT1_HUMAN', 'GPR45_HUMAN', 'ITM2C_HUMAN', 'I23O2_HUMAN', 'HYEP_HUMAN', 'ISM1_HUMAN', 'HPBP1_HUMAN', 'HSC20_HUMAN', 'ITPI2_HUMAN', 'HDGL1_HUMAN', 'GIT1_HUMAN', 'GPNMB_HUMAN', 'IC1_HUMAN', 'GDIR3_HUMAN', 'H2B1M_HUMAN', 'HV43D_HUMAN', 'H1FOO_HUMAN', 'HSFY1_HUMAN', 'HSDL2_HUMAN', 'GMCL2_HUMAN', 'GSTA1_HUMAN', 'HV404_HUMAN', 'IFNG_HUMAN', 'IF5_HUMAN', 'IRF3_HUMAN', 'HIG2B_HUMAN', 'ITA9_HUMAN', 'ICE1_HUMAN', 'HBD_HUMAN', 'HXC13_HUMAN', 'HLAE_HUMAN', 'IL5RA_HUMAN', 'GFRA3_HUMAN', 'IL27B_HUMAN', 'GSTO2_HUMAN', 'H2B2D_HUMAN', 'GCSAM_HUMAN', 'GBB4_HUMAN', 'GMPPB_HUMAN', 'GPDM_HUMAN', 'HAVR1_HUMAN', 'IL7_HUMAN', 'GID8_HUMAN', 'HMGN1_HUMAN', 'IKZF4_HUMAN', 'HMN9_HUMAN', 'GUAA_HUMAN', 'H32_HUMAN', 'HMGB3_HUMAN', 'GDIR1_HUMAN', 'ICAM4_HUMAN', 'ITA10_HUMAN', 'HS90B_HUMAN', 'IER2_HUMAN', 'INSM2_HUMAN', 'IRPL2_HUMAN', 'GCNT1_HUMAN', 'HES6_HUMAN', 'IFT88_HUMAN', 'GRN_HUMAN', 'HSPB2_HUMAN', 'I17RA_HUMAN', 'IMP1L_HUMAN', 'GRIP1_HUMAN', 'IMB1_HUMAN', 'G3ST2_HUMAN', 'H2BWT_HUMAN', 'ID1_HUMAN', 'ISOC2_HUMAN', 'GUC2F_HUMAN', 'GDF9_HUMAN', 'IRF7_HUMAN', 'ING5_HUMAN', 'IMP3_HUMAN', 'HS2ST_HUMAN', 'IKBB_HUMAN', 'IRF4_HUMAN', 'GALT8_HUMAN', 'GLCTK_HUMAN', 'ICAL_HUMAN', 'IL40_HUMAN', 'IP6K2_HUMAN', 'IL1R1_HUMAN', 'JARD2_HUMAN', 'HNRLL_HUMAN', 'HEM0_HUMAN', 'GGYF2_HUMAN', 'HV373_HUMAN', 'H12_HUMAN', 'IFNA1_HUMAN', 'IRG1_HUMAN', 'INSY1_HUMAN', 'ISK2_HUMAN', 'GOT1B_HUMAN', 'GMPR1_HUMAN', 'IGSF2_HUMAN', 'HRH1_HUMAN', 'IPRI_HUMAN', 'GALP_HUMAN', 'HPRT_HUMAN', 'IL1R2_HUMAN', 'H13_HUMAN', 'GDF1_HUMAN', 'HUS1_HUMAN', 'HIPK2_HUMAN', 'GVIN1_HUMAN', 'GPR25_HUMAN', 'H1AS1_HUMAN', 'IFT27_HUMAN', 'GHRHR_HUMAN', 'GBRL2_HUMAN', 'GDN_HUMAN', 'HHIP_HUMAN', 'ITA8_HUMAN', 'GG6L7_HUMAN', 'IP3KA_HUMAN', 'IF4A3_HUMAN', 'ING4_HUMAN', 'GLPK_HUMAN', 'GAGE6_HUMAN', 'GPX2_HUMAN', 'HOOK1_HUMAN', 'GRID1_HUMAN', 'ILEU_HUMAN', 'HEAT3_HUMAN', 'IRAK3_HUMAN', 'GSTA2_HUMAN', 'HYAL4_HUMAN', 'HGFA_HUMAN', 'GLYR1_HUMAN', 'HMCS1_HUMAN', 'HXA9_HUMAN', 'IZUM4_HUMAN', 'HEXD_HUMAN', 'H2A1_HUMAN', 'IGBP1_HUMAN', 'GAL3A_HUMAN', 'HES2_HUMAN', 'HPS4_HUMAN', 'ITIH5_HUMAN', 'GALT4_HUMAN', 'HMN1_HUMAN', 'GEMI4_HUMAN', 'IRGM_HUMAN', 'IGS23_HUMAN', 'GNA1_HUMAN', 'HAUS1_HUMAN', 'ITB3_HUMAN', 'ISK1_HUMAN', 'H2AB2_HUMAN', 'INY2B_HUMAN', 'ISOC1_HUMAN', 'GTR5_HUMAN', 'GGT7_HUMAN', 'IMA8_HUMAN', 'HMGCL_HUMAN', 'GRB14_HUMAN', 'GALR3_HUMAN', 'HERC3_HUMAN', 'GGT3_HUMAN', 'HMCS2_HUMAN', 'HDHD3_HUMAN', 'HXD10_HUMAN', 'HTD2_HUMAN', 'GRP1_HUMAN', 'GDPD3_HUMAN', 'HPT_HUMAN', 'GP15L_HUMAN', 'HXA10_HUMAN', 'ITA5_HUMAN', 'HAUS4_HUMAN']
    ENSP_2_functionEnumArray_dict = get_functionEnumArray_from_proteins(ensp_list, dict_2_array=True)
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


# def __init__(self, low_memory=False):
    #     print("initializing PQO")
    #     # super(PersistentQueryObject, self).__init__() # py2 and py3
    #     # super().__init__() # py3
    #     # self.type_2_association_dict = self.get_type_2_association_dict()
    #     # self.go_slim_set = self.get_go_slim_terms()
    #     # ##### pre-load go_dag and goslim_dag (obo files) for speed, also filter objects
    #     # ### --> obsolete since using functerm_2_level_dict
    #     # self.go_dag = obo_parser.GODag(obo_file=FN_GO_BASIC)
    #     # self.upk_dag = obo_parser.GODag(obo_file=FN_KEYWORDS, upk=True)
    #     #blacklisted_terms_bool_arr
    #     # self.lineage_dict = {}
    #     # # key=GO-term, val=set of GO-terms (parents)
    #     # for go_term_name in self.go_dag:
    #     #     GOTerm_instance = self.go_dag[go_term_name]
    #     #     self.lineage_dict[go_term_name] = GOTerm_instance.get_all_parents().union(GOTerm_instance.get_all_children())
    #     # for term_name in self.upk_dag:
    #     #     Term_instance = self.upk_dag[term_name]
    #     #     self.lineage_dict[term_name] = Term_instance.get_all_parents().union(Term_instance.get_all_children())
    #     #
    #     # fn_hierarchy = os.path.join(variables.DOWNLOADS_DIR, "RCTM_hierarchy.tsv")
    #     # self.lineage_dict.update(get_lineage_Reactome(fn_hierarchy))
    #
    #     # self.goslim_dag = obo_parser.GODag(obo_file=FN_GO_SLIM)
    #     # self.kegg_pseudo_dag = obo_parser.Pseudo_dag(etype="-52")
    #     # self.smart_pseudo_dag = obo_parser.Pseudo_dag(etype="-53")
    #     # self.interpro_pseudo_dag = obo_parser.Pseudo_dag(etype="-54")
    #     # self.pfam_pseudo_dag = obo_parser.Pseudo_dag(etype="-55")
    #     # self.pmid_pseudo_dag = obo_parser.Pseudo_dag(etype="-56")
    #     self.taxid_2_proteome_count = get_Taxid_2_proteome_count_dict()
    #
    #     ### lineage_dict: key: functional_association_term_name val: set of parent terms
    #     ### functional term 2 hierarchical level dict
    #     # self.functerm_2_level_dict = defaultdict(lambda: np.nan)
    #     # self.functerm_2_level_dict.update(self.get_functional_term_2_level_dict_from_dag(self.go_dag))
    #     # self.functerm_2_level_dict.update(self.get_functional_term_2_level_dict_from_dag(self.upk_dag))
    #     # del self.go_dag # needed for cluster_filter
    #     # del self.upk_dag
    #     # self.functerm_2_level_dict = self.get_functional_term_2_level_dict()
    #     if not low_memory: # override variables if "low_memory" passed to query initialization
    #         # low_memory = variables.LOW_MEMORY
    #     # if not low_memory:
    #         ### taxid_2_etype_2_association_2_count_dict[taxid][etype][association] --> count of ENSPs of background proteome from Function_2_ENSP_table_STRING.txt
    #         # self.taxid_2_etype_2_association_2_count_dict_background = get_association_2_counts_split_by_entity() # cf. if association is string
    #         # self.function_an_2_description_dict = defaultdict(lambda: np.nan)
    #         # an_2_name_dict, an_2_description_dict = get_function_an_2_name__an_2_description_dict()
    #         # an_2_description_dict = get_function_an_2_description_dict()
    #         # self.function_an_2_description_dict.update(an_2_description_dict)
    #
    #         self.year_arr, self.hierlevel_arr, self.entitytype_arr, self.functionalterm_arr, self.indices_arr, self.description_arr, self.category_arr = self.get_lookup_arrays(low_memory)
    #     else:
    #         self.year_arr, self.hierlevel_arr, self.entitytype_arr, self.functionalterm_arr, self.indices_arr = self.get_lookup_arrays(low_memory)
    #
    #     self.etype_2_minmax_funcEnum = self.get_etype_2_minmax_funcEnum(self.entitytype_arr)
    #     self.function_enumeration_len = self.functionalterm_arr.shape[0]
    #     if not low_memory:
    #         #foreground
    #         self.ENSP_2_functionEnumArray_dict = get_ENSP_2_functionEnumArray_dict()
    #         #background
    #         self.taxid_2_tuple_funcEnum_index_2_associations_counts = get_background_taxid_2_funcEnum_index_2_associations()
    #
    #     self.etype_cond_dict = get_etype_cond_dict(self.etype_2_minmax_funcEnum, self.function_enumeration_len)
    #     # self.cond_etypes_with_ontology = self.get_cond_bool_array_of_etypes(variables.entity_types_with_ontology)
    #     # self.cond_etypes_rem_foreground_ids = self.get_cond_bool_array_of_etypes(variables.entity_types_rem_foreground_ids)
    #     self.cond_etypes_with_ontology = get_cond_bool_array_of_etypes(variables.entity_types_with_ontology, self.function_enumeration_len, self.etype_cond_dict)
    #     self.cond_etypes_rem_foreground_ids = get_cond_bool_array_of_etypes(variables.entity_types_rem_foreground_ids, self.function_enumeration_len, self.etype_cond_dict)
    #     self.lineage_dict_enum = get_lineage_dict_enum()
    #     self.blacklisted_terms_bool_arr = self.get_blacklisted_terms_bool_arr()
