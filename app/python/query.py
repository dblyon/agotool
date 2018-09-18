import numpy as np
import os, sys
from collections import defaultdict
import psycopg2, math
import pytest # should this be disabled for performance later?

# import user modules
sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
import variables, obo_parser


UNSIGNED_2_SIGNED_CONSTANT = int(math.pow(2, 63))
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
        # HOST = env_dict['HOST']
        # PORT = env_dict['PORT']
        PORT = '5432'
        HOST = 'db'
        return get_cursor_docker(host=HOST, dbname=DBNAME, user=USER, password=PWD, port=PORT)

    if not variables.DB_DOCKER:
        ### use dockerized Postgres directly from native OS
        PORT = '5913'
        HOST = 'localhost'
        param_2_val_dict = variables.param_2_val_dict
        return get_cursor_connect_2_docker(host=HOST, dbname=param_2_val_dict["POSTGRES_DB"], user=param_2_val_dict["POSTGRES_USER"], password=param_2_val_dict["POSTGRES_PASSWORD"], port=PORT)

    if platform_ == "linux":
        try:
            USER = os.environ['POSTGRES_USER']
            PWD = os.environ['POSTGRES_PASSWORD']
            DBNAME = os.environ['POSTGRES_DB']
            PORT = '5432'
            HOST = 'db'
        except KeyError:
            print("query.py sais there is something wrong with the Postgres config")
            raise StopIteration
        return get_cursor_docker(host=HOST, dbname=DBNAME, user=USER, password=PWD, port=PORT)

    elif platform_ == "darwin":
        if not variables.DB_DOCKER:
            ### use local Postgres
            return get_cursor_ody()
        else: # connect to docker Postgres container
            PORT = '5432'
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

def map_secondary_2_primary_ANs(ans_list):
    """
    map secondary UniProt ANs to primary ANs,
    AN only in dict if mapping exists
    :param ans_list: ListOfString
    :return: Dict (key: String(Secondary AN), val: String(Primary AN))
    """
    ans_list = str(ans_list)[1:-1]
    result = get_results_of_statement("SELECT protein_secondary_2_primary_an.sec, protein_secondary_2_primary_an.pri FROM protein_secondary_2_primary_an WHERE protein_secondary_2_primary_an.sec IN({})".format(ans_list))
    secondary_2_primary_dict = {}
    for res in result:
        secondary = res[0]
        primary = res[1]
        secondary_2_primary_dict[secondary] = primary
    cursor.close()
    return secondary_2_primary_dict


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
        result = get_results_of_statement("SELECT protein_secondary_2_primary_an.sec, protein_secondary_2_primary_an.pri FROM protein_secondary_2_primary_an;")
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

    def map_secondary_2_primary_ANs(self, ans_list):
        """
        def map_secondary_2_primary_ANs_v1_slow(self, ans_list):
            secondary_ans_2_replace = set(self.secondary_2_primary_an_dict.keys()).intersection(set(ans_list))
            return dict((secondary_an, self.secondary_2_primary_an_dict[secondary_an]) for secondary_an in secondary_ans_2_replace)

        :param ans_list: List of String
        :return: secondary_2_primary_dict (key: String(Secondary AN), val: String(Primary AN))
        """
        secondary_2_primary_dict_temp = {}
        for secondary in ans_list:
            try:
                secondary_2_primary_dict_temp[secondary] = self.secondary_2_primary_an_dict[secondary]
            except KeyError:
                continue
        return secondary_2_primary_dict_temp

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

class PersistentQueryObject_STRING(PersistentQueryObject):
    """
    used to query protein 2 functional associations
    only protein_2_function is queried in Postgres,
    everything else is in memory but still deposited in the DB any way
    """
    def __init__(self):
        # super(PersistentQueryObject, self).__init__() # py2 and py3
        # super().__init__() # py3
        self.type_2_association_dict = self.get_type_2_association_dict()
        self.go_slim_set = self.get_go_slim_terms()
        ##### pre-load go_dag and goslim_dag (obo files) for speed, also filter objects
        ### --> obsolete since using functerm_2_level_dict
        self.go_dag = obo_parser.GODag(obo_file=FN_GO_BASIC)
        self.upk_dag = obo_parser.GODag(obo_file=FN_KEYWORDS, upk=True)
        # self.goslim_dag = obo_parser.GODag(obo_file=FN_GO_SLIM)
        # self.kegg_pseudo_dag = obo_parser.Pseudo_dag(etype="-52")
        # self.smart_pseudo_dag = obo_parser.Pseudo_dag(etype="-53")
        # self.interpro_pseudo_dag = obo_parser.Pseudo_dag(etype="-54")
        # self.pfam_pseudo_dag = obo_parser.Pseudo_dag(etype="-55")
        # self.pmid_pseudo_dag = obo_parser.Pseudo_dag(etype="-56")
        
        self.taxid_2_proteome_count = get_TaxID_2_proteome_count_dict()

        ### lineage_dict: key: functional_association_term_name val: set of parent terms
        ### functional term 2 hierarchical level dict
        self.functerm_2_level_dict = defaultdict(lambda: np.nan)
        self.functerm_2_level_dict.update(self.get_functional_term_2_level_dict(self.go_dag))
        self.functerm_2_level_dict.update(self.get_functional_term_2_level_dict(self.upk_dag))
        del self.go_dag # needed for cluster_filter
        del self.upk_dag

        ## functions [Functions_table_STRING.txt]
        if not variables.LOW_MEMORY:
            ### taxid_2_etype_2_association_2_count_dict[taxid][etype][association] --> count of ENSPs of background proteome from Function_2_ENSP_table_STRING.txt
            self.taxid_2_etype_2_association_2_count_dict_background = get_association_2_counts_split_by_entity()
            self.function_an_2_description_dict = defaultdict(lambda: np.nan)
            # an_2_name_dict, an_2_description_dict = get_function_an_2_name__an_2_description_dict()
            an_2_description_dict = get_function_an_2_description_dict()
            self.function_an_2_description_dict.update(an_2_description_dict)

    @staticmethod
    def get_functional_term_2_level_dict(dag):
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
        protein_ans_list = str(protein_ans_list)[1:-1]
        result = get_results_of_statement("SELECT protein_2_function.an, protein_2_function.function, protein_2_function.etype FROM protein_2_function WHERE protein_2_function.an IN({});".format(protein_ans_list))
        for res in result:
            an, associations_list, etype = res
            etype_2_association_dict[etype][an] = set(associations_list)
        return etype_2_association_dict


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

def get_termAN_from_humanName_functionType(functionType, humanName):
    if humanName is None:
        return ""
    return functionType_term_2_an_dict[functionType][humanName]

def parse_result_child_parent(result):
    return set([item for sublist in result for item in sublist])

def get_taxids():
    """
    return all TaxIDs from taxid_2_proteins as sorted List of Integers
    :return: List of Integers
    """
    result = get_results_of_statement("SELECT taxid_2_protein.taxid FROM taxid_2_protein")
    return sorted([rec[0] for rec in result])

def get_proteins_of_taxid(taxid):
    result = get_results_of_statement("SELECT taxid_2_protein.an_array FROM taxid_2_protein WHERE taxid_2_protein.taxid={}".format(taxid))
    return sorted(result[0][0])

def get_TaxID_2_proteome_count_dict():
    taxid_2_proteome_count_dict = {}
    result = get_results_of_statement("SELECT taxid_2_protein.taxid, taxid_2_protein.count FROM taxid_2_protein;")
    for res in result:
        taxid, count = res
        taxid_2_proteome_count_dict[taxid] = count
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
        _, etype, association, background_count, background_n, an_array = rec
        # etype = str(etype)
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
        _, etype, association, background_count, background_n, an_array = rec
        # etype = str(etype)
        etype_2_association_2_count_dict[etype][association] = background_count
    return etype_2_association_2_count_dict

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


if __name__ == "__main__":
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
    cursor = get_cursor()
    cursor.execute("SELECT * FROM functions WHERE functions.type='GO' LIMIT 5")
    cursor.execute("SELECT * FROM protein_2_function WHERE protein_2_function.an='A0A009DWB1'")
    records = cursor.fetchall()
    print(records)
    cursor.close()


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
