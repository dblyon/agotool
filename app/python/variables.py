import os, sys, multiprocessing
# import numpy as np
# import pickle
############################
### settings
PRELOAD = False  # set True in production for STRING_v11 (not for UniProt)
# pre-load objects DB connection necessary, set to False while testing with pytest
skip_slow_downloads = True # 2 large slow downloads that take >= 30 min to download
skip_downloads_completely = True # don't download anything

DOCKER = False # app and data directory, within image or shared with local host, adapt accordingly in docker-compose
# FUTURES = False # parallel code disabled
## local (bind-mounted volume if DOCKER=False --> version 1)
## vs. dockerized version (named-volume, copy data to named-volume first, if DOCKER=True --> version 2)
LOW_MEMORY = False # load function_an_2_description_dict or query DB
DB_DOCKER = False # connect via local port vs via docker, in query.py
READ_FROM_FLAT_FILES = True # get data for PQO from flat files instead of from PostgreSQL # set "DOCKER" to True!
FROM_PICKLE = False # read PQO data from pickle instead of flatfiles
DEBUG = False # for flask and some internals for printing, set to False in production
LOG_USERINPUT_DEBUG = False # turn logging for userinput (args_dict) on or off. False in production
PROFILING = False # profiling flaskapp --> check stdout, set to False in production
TESTING = False
# use small testing subset of files for DB import, checking settings when intilizing everything for the first time
VERBOSE = True # print stuff to stdout
PD_WARNING_OFF = True # turn off pandas warning about chained assignment (pd.options.mode.chained_assignment = None)
VERSION_ = "STRING" # switch between "STRING" and "aGOtool" versions of the program
temp_dont_run_analysis = False
if READ_FROM_FLAT_FILES and LOW_MEMORY:
    raise NotImplementedError
ARGPARSE = False # use argparse for IP and port parsing
############################
entity_types = {-20, -21, -22, -23, -25, -26, -51, -52, -53, -54, -55, -56, -57, -58, -78}
PMID = {-56}
alpha = 0.05
entity_types_with_data_in_functions_table = entity_types
entity_types_with_ontology = {-20, -21, -22, -23, -25, -26, -51, -57, -78} # turn InterPro filter off
# entity_types_rem_foreground_ids = {-52, -53, -54, -55}
entity_types_rem_foreground_ids = entity_types - PMID - entity_types_with_ontology # all_etypes - PMID - ontologies
enrichment_methods = {"abundance_correction", "compare_samples", "characterize_foreground", "genome", "compare_groups"}
functionType_2_entityType_dict = {"GOCC TextMining": -20,
                                  "GOBP": -21, # Gene Ontology biological process
                                  "GOCC": -22, # Gene Ontology cellular component
                                  "GOMF": -23, # Gene Ontology molecular function
                                  "Brenda Tissue Ontology": -25,
                                  "Disease Ontology": -26,
                                  "UniProt keywords": -51,
                                  "KEGG": -52, #  (Kyoto Encyclopedia of Genes and Genomes)
                                  "SMART": -53, #  (Simple Modular Architecture Research Tool)
                                  "INTERPRO": -54,
                                  "PFAM": -55, #  (Protein FAMilies)
                                  "PMID": -56,
                                  "Reactome": -57,
                                  "WikiPathways": -58,
                                  "STRING_clusters": -78}

entityType_2_functionType_dict = {-20: "GOCC TextMining",
                                  -21: "Gene Ontology biological process",
                                  -22: "Gene Ontology cellular component",
                                  -25: "Brenda Tissue Ontology",
                                  -26: "Disease Ontology",
                                  -23: "Gene Ontology molecular function",
                                  -51: "UniProt keywords",
                                  -52: "KEGG (Kyoto Encyclopedia of Genes and Genomes)",
                                  -53: "SMART (Simple Modular Architecture Research Tool)",
                                  -54: "INTERPRO",
                                  -55: "PFAM (Protein FAMilies)",
                                  -56: "PMID (PubMed IDentifier)",
                                  -57: "Reactome",
                                  -58: "WikiPathways",
                                  -78: "STRING_clusters"}

limit_2_entity_types_ALL = ";".join([str(ele) for ele in entity_types_with_data_in_functions_table])
cols_sort_order_genome = ["term", "hierarchical_level", "p_value", "FDR", "category", "etype", "description", "foreground_count", "background_count", "foreground_ids", "year"]
cols_sort_order_charcterize = ['foreground_count', 'foreground_ids', 'ratio_in_foreground', 'term', 'etype', 'category', 'hierarchical_level', 'description', 'year']
# cols_sort_order_compare_samples = ["term", "hierarchical_level", "p_value", "FDR", "category", "etype", "description", "year", "ratio_in_foreground", "ratio_in_background", "foreground_ids", "background_ids", "foreground_count", "background_count", "foreground_n", "background_n"]
cols_sort_order_compare_samples = ["term", "hierarchical_level", "p_value", "FDR", "category", "etype", "description", "foreground_count", "background_count", "foreground_ids", "year"] # should be the same as cols_sort_order_genome

# api_url = "http://0.0.0.0:5911/api" # local
url_production = r"http://127.0.0.1:10114/api" # 10114 for PMID autoupdates SAN, Aquarius, Pisces
url_testing = r"http://127.0.0.1:10116/api" # used for testing before chain-reloading

PYTHON_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
if DOCKER:
    APP_DIR = "/opt/services/flaskapp/src"
    DATA_DIR = "/agotool_data"
else: # relative path on host
    APP_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../')))
    DATA_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../../data')))

APP_DIR_SNAKEMAKE = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../')))
DATA_DIR_SNAKEMAKE = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../../data')))

EXAMPLE_FOLDER = os.path.join(DATA_DIR, "exampledata")
SESSION_FOLDER_ABSOLUTE = os.path.join(DATA_DIR, 'session')
SESSION_FOLDER_RELATIVE = 'data/session'
TEMPLATES_FOLDER_ABSOLUTE = os.path.join(APP_DIR, 'static/templates')

# obo files for PRELOAD/persistent objects
FN_KEYWORDS = os.path.join(DATA_DIR, "PostgreSQL/downloads/keywords-all.obo")
FN_GO_SLIM = os.path.join(DATA_DIR, "PostgreSQL/downloads/goslim_generic.obo")
FN_GO_BASIC = os.path.join(DATA_DIR, "PostgreSQL/downloads/go-basic.obo")

# Flask app
STATIC_DIR_FLASK = os.path.join(APP_DIR, 'static')

# automatic updates
POSTGRESQL_DIR = os.path.join(DATA_DIR, "PostgreSQL")
POSTGRESQL_DIR_SNAKEMAKE = os.path.join(DATA_DIR_SNAKEMAKE, "PostgreSQL")
TABLES_DIR = os.path.join(POSTGRESQL_DIR, "tables")
TABLES_DIR_SNAKEMAKE = os.path.join(POSTGRESQL_DIR_SNAKEMAKE, "tables")
STATIC_POSTGRES_DIR = os.path.join(POSTGRESQL_DIR, "static")
TEST_DIR = os.path.join(TABLES_DIR, "test")
PYTEST_FN_DIR = os.path.join(PYTHON_DIR, "testing/user_input_files")
DOWNLOADS_DIR = os.path.join(POSTGRESQL_DIR, "downloads")
DOWNLOADS_DIR_SNAKEMAKE = os.path.join(POSTGRESQL_DIR_SNAKEMAKE, "downloads")
# FN_DATABASE_SCHEMA = os.path.join(POSTGRESQL_DIR, "DataBase_Schema.md")
FN_HELP_ENTITY_TYPES = os.path.join(POSTGRESQL_DIR, "example_help_entity_types.md")
FN_HELP_PARAMETERS = os.path.join(POSTGRESQL_DIR, "example_help_parameters.md")

DIRECTORIES_LIST = [os.path.join(DATA_DIR, 'PostgreSQL/downloads'),
                    os.path.join(DATA_DIR, 'logs'),
                    os.path.join(DATA_DIR, 'session')]
FILES_NOT_2_DELETE = [os.path.join(DOWNLOADS_DIR + fn) for fn in ["keywords-all.obo", "goslim_generic.obo", "go-basic.obo"]]

# log files
LOG_DIRECTORY = os.path.join(DATA_DIR, "logs")
LOG_FN_WARNINGS_ERRORS = os.path.join(LOG_DIRECTORY, "warnings_errors_log.txt")
LOG_FN_ACTIVITY = os.path.join(LOG_DIRECTORY, "activity_log.txt")
LOG_FN_UPDATES = os.path.join(LOG_DIRECTORY, "updates_log.txt")
LOG_FN_USERINPUT_DEBUG = os.path.join(LOG_DIRECTORY, "userinput_log_debug.txt")
log_files = [LOG_FN_ACTIVITY, LOG_FN_UPDATES, LOG_FN_WARNINGS_ERRORS, LOG_FN_USERINPUT_DEBUG]
LOG_DF_FILE_DIMENSIONS = os.path.join(TABLES_DIR_SNAKEMAKE, "DF_file_dimensions_log.txt")
LOG_DF_FILE_DIMENSIONS_GLOBAL_ENRICHMENT = os.path.join(TABLES_DIR_SNAKEMAKE, "DF_global_enrichment_file_stats_log.txt")

def makedirs_():
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)
    for fn in log_files:
        if not os.path.exists(fn):
            fh = open(fn, "w")
            fh.close()

# CPU usage during updates (for "sort --parallel")
NUMBER_OF_PROCESSES = multiprocessing.cpu_count()

def parse_env_file(fn):
    """
    fn = r'/Users/dblyon/modules/cpr/agotool/app/env_file'
    :param fn: String
    :return: Dict
    """
    param_2_val_dict = {}
    with open(fn, "r") as fh:
        for line in fh:
            if not line.startswith("#"):
                try:
                    key, val = line.strip().split("=")
                    param_2_val_dict[key] = val
                except ValueError: # whitespace, empty lines
                    pass
    return param_2_val_dict

# if DB_DOCKER:
#     param_2_val_dict = parse_env_file(os.path.abspath(os.path.join(PYTHON_DIR, os.pardir, "env_file")))
# else:
#     param_2_val_dict = parse_env_file(os.path.join(APP_DIR, "env_file"))
fn = os.path.abspath(os.path.join(PYTHON_DIR, os.pardir, "env_file"))
# print("VARIABLES env_file bubu: ", fn)
param_2_val_dict = parse_env_file(fn)


id_2_entityTypeNumber_dict = {'GO:0003674': "-23",  # 'Molecular Function',
                              'GO:0005575': "-22",  # 'Cellular Component',
                              'GO:0008150': "-21",  # 'Biological Process',
                              "GO:OBSOLETE": "-24", # "GO obsolete
                              # 'UPK:9990': "-51",  # 'Technical term',
                              # 'UPK:9991': "-51",  # 'PTM',
                              # 'UPK:9992': "-51",  # 'Molecular function',
                              # 'UPK:9993': "-51",  # 'Ligand',
                              # 'UPK:9994': "-51",  # 'Domain',
                              # 'UPK:9995': "-51",  # 'Disease',
                              # 'UPK:9996': "-51",  # 'Developmental stage',
                              # 'UPK:9997': "-51",  # 'Coding sequence diversity',
                              # 'UPK:9998': "-51",  # 'Cellular component',
                              # 'UPK:9999': "-51",  # 'Biological process'
                              'KW-9990': "-51",  # 'Technical term',
                              'KW-9991': "-51",  # 'PTM',
                              'KW-9992': "-51",  # 'Molecular function',
                              'KW-9993': "-51",  # 'Ligand',
                              'KW-9994': "-51",  # 'Domain',
                              'KW-9995': "-51",  # 'Disease',
                              'KW-9996': "-51",  # 'Developmental stage',
                              'KW-9997': "-51",  # 'Coding sequence diversity',
                              'KW-9998': "-51",  # 'Cellular component',
                              'KW-9999': "-51",  # 'Biological process'
                              "UniProtKeywords": "-51",
                              'KEGG': "-52", # KEGG
                              "SMART": "-53", # SMART domains
                              "INTERPRO": "-54", # Interpro domains
                              "PFAM": "-55", # Pfam domains
                              "PMID": "-56", # Pubmed identifiers
                              "Reactome": "-57",
                              "STRING_clusters": "-78"}

# function_enumeration_len = 6815598 # ?deprecated?
#blacklisted_terms = ['GO:0003674', 'GO:0005575', 'GO:0008150', 'KW-9990', 'KW-9991', 'KW-9992', 'KW-9993', 'KW-9994', 'KW-9995', 'KW-9996', 'KW-9997', 'KW-9998', 'KW-9999']
# top level KW except Disease and Developmental stage
# 'KW-9995' 'Disease',
# 'KW-9996' 'Developmental stage'
blacklisted_terms = {'GO:0003674', 'GO:0005575', 'GO:0008150',
                     'KW-0002', 'KW-0181', 'KW-0308', 'KW-0374', 'KW-0582', 'KW-0614',
                     'KW-0814', 'KW-0895', 'KW-0903', 'KW-0952', 'KW-1185', 'KW-1267',
                     'KW-9990', 'KW-9991', 'KW-9992', 'KW-9993', 'KW-9994', 'KW-9997', 'KW-9998', 'KW-9999'}
# 'KW-9990' 'Technical term' and all its children

##### final Tables / flat-files needed for flask app / PostgreSQL
if VERSION_ == "UniProt":
    appendix = "UPS_FIN"
elif VERSION_ == "STRING":
    appendix = "STS_FIN"
else:
    print("VERSION_ {} not know".format(VERSION_))
    raise sys.exit(2)

tables_dict = {"taxid_2_proteome_count_dict": os.path.join(TABLES_DIR, "taxid_2_proteome_count_dict_{}.p".format(appendix)),
               "kegg_taxid_2_acronym_dict": os.path.join(TABLES_DIR, "kegg_taxid_2_acronym_dict_{}.p".format(appendix)),
               "kegg_taxid_2_acronym_table": os.path.join(TABLES_DIR, "kegg_taxid_2_acronym_table_{}.txt".format(appendix)),
               "year_arr": os.path.join(TABLES_DIR, "year_arr_{}.p".format(appendix)),
               "hierlevel_arr": os.path.join(TABLES_DIR, "hierlevel_arr_{}.p".format(appendix)),
               "entitytype_arr": os.path.join(TABLES_DIR, "entitytype_arr_{}.p".format(appendix)),
               "functionalterm_arr": os.path.join(TABLES_DIR, "functionalterm_arr_{}.p".format(appendix)),
               "indices_arr": os.path.join(TABLES_DIR, "indices_arr_{}.p".format(appendix)),
               "description_arr": os.path.join(TABLES_DIR, "description_arr_{}.p".format(appendix)),
               "category_arr": os.path.join(TABLES_DIR, "category_arr_{}.p".format(appendix)),
               "lineage_dict_enum": os.path.join(TABLES_DIR, "lineage_dict_enum_{}.p".format(appendix)),
               "blacklisted_terms_bool_arr": os.path.join(TABLES_DIR, "blacklisted_terms_bool_arr_{}.p".format(appendix)),
               "ENSP_2_functionEnumArray_dict": os.path.join(TABLES_DIR, "ENSP_2_functionEnumArray_dict_{}.p".format(appendix)),
               "taxid_2_tuple_funcEnum_index_2_associations_counts": os.path.join(TABLES_DIR, "taxid_2_tuple_funcEnum_index_2_associations_counts_{}.p".format(appendix)),
               "etype_2_minmax_funcEnum": os.path.join(TABLES_DIR, "etype_2_minmax_funcEnum_{}.p".format(appendix)),
               "etype_cond_dict": os.path.join(TABLES_DIR, "etype_cond_dict_{}.p".format(appendix)),
               "cond_etypes_with_ontology": os.path.join(TABLES_DIR, "cond_etypes_with_ontology_{}.p".format(appendix)),
               "cond_etypes_rem_foreground_ids": os.path.join(TABLES_DIR, "cond_etypes_rem_foreground_ids_{}.p".format(appendix)),
               "populate_classification_schema_current_sql_gz": os.path.join(TABLES_DIR, "populate_classification_schema_current.sql.gz"),
               "global_enrichment_data_DIR": os.path.join(TABLES_DIR, "global_enrichment_data"),
               "global_enrichment_data_current_tar_gz": os.path.join(TABLES_DIR, "global_enrichment_data_current.tar.gz"),
               "Taxid_2_Proteins_table_STRING": os.path.join(TABLES_DIR, "Taxid_2_Proteins_table_STS_FIN.txt"),
               "Functions_table_STRING": os.path.join(TABLES_DIR, "Functions_table_STS_FIN.txt"),
               "Lineage_table_STRING": os.path.join(TABLES_DIR, "Lineage_table_STS_FIN.txt"),
               "Protein_2_FunctionEnum_table_STRING": os.path.join(TABLES_DIR, "Protein_2_FunctionEnum_table_STS_FIN.txt"),
               "Taxid_2_FunctionCountArray_table_STRING": os.path.join(TABLES_DIR, "Taxid_2_FunctionCountArray_table_STS_FIN.txt"),
               }
               # "Taxid_2_Proteins_table": os.path.join(TABLES_DIR, "Taxid_2_Proteins_table_{}.txt".format(appendix)),
               # "blacklisted_enum_terms": os.path.join(TABLES_DIR, "blacklisted_enum_terms_{}.p".format(appendix)),
               # os.path.join(TABLES_DIR, "Functions_table_STRING.txt") --> STS_FIN

TABLES_DICT_SNAKEMAKE = {tablename: os.path.join(TABLES_DIR_SNAKEMAKE, os.path.basename(fn)) for tablename, fn in tables_dict.items()}


# def get_blacklisted_enum_terms(fn_functions_table, blacklisted_terms, FROM_PICKLE=True):
#     "| enum | etype | an | description | year | level |"
#     if FROM_PICKLE:
#         with open(tables_dict["blacklisted_enum_terms"], "rb") as fh:
#             blacklisted_enum_terms = pickle.load(fh)
#         return blacklisted_enum_terms
#     blacklisted_enum_terms = []
#     with open(fn_functions_table, "r") as fh:
#         for line in fh:
#             line_split = line.split("\t")
#             enum = line_split[0]
#             an = line_split[2]
#             if an in blacklisted_terms:
#                 blacklisted_enum_terms.append(int(enum))
#     blacklisted_enum_terms = sorted(blacklisted_enum_terms)
#     return np.array(blacklisted_enum_terms, dtype=np.dtype("uint32"))
#
# fn_functions_table = os.path.join(TABLES_DIR, "Functions_table_STRING.txt")
# blacklisted_enum_terms = get_blacklisted_enum_terms(fn_functions_table, blacklisted_terms)
# blacklisted_enum_terms = np.array([45826, 3348, 29853, 44962, 45487, 34225, 45240, 46138, 46149, 46150, 46151, 46152, 45513, 45769, 45130, 46156, 46157, 46158, 46153, 45777, 46056, 45302, 45692], dtype=np.dtype("uint32"))


