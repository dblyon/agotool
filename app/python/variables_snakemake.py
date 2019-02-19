import os, multiprocessing
import numpy as np
############################
### settings
PRELOAD = False # set True in production
# pre-load objects DB connection necessary, set to False while testing with pytest
skip_slow_downloads = True # 2 large slow downloads that take >= 30 min to download
skip_downloads_completely = True # don't download anything

DOCKER = False # app and data directory, within image or shared with local host, adapt accordingly in docker-compose
# FUTURES = False # parallel code disabled
## local (bind-mounted volume if DOCKER=False --> version 1)
## vs. dockerized version (named-volume, copy data to named-volume first, if DOCKER=True --> version 2)
LOW_MEMORY = False # load function_an_2_description_dict or query DB
DB_DOCKER = True # connect via local port vs via docker, in query.py
DEBUG = False # for flask and some internals for printing, set to False in production
PROFILING = False # profiling flaskapp --> check stdout, set to False in production
TESTING = False
# use small testing subset of files for DB import, checking settings when intilizing everything for the first time
VERBOSE = True # print stuff to stdout
PD_WARNING_OFF = True # turn off pandas warning about chained assignment (pd.options.mode.chained_assignment = None)
VERSION_ = "STRING" # switch between "STRING" and "aGOtool" versions of the program
temp_dont_run_analysis = False
############################
function_types = ("BP", "CP", "MF", "UPK", "KEGG", "DOM")
entity_types = {-21, -22, -23, -51, -52, -53, -54, -55, -56, -57}
alpha = 0.05
# "-21": {},  # | GO:0008150 | -21 | GO biological process |
# "-22": {},  # | GO:0005575 | -22 | GO cellular component |
# "-23": {},  # | GO:0003674 | -23 | GO molecular function |
# "-51": {},  # UniProt keywords
# "-52": {},  # KEGG
# "-53": {},  # SMART
# "-54": {},  # InterPro
# "-55": {},  # PFAM
# "-56": {}   # PMID
# entity_types_with_data_in_functions_table = {"-21", "-22", "-23", "-51", "-52"}
entity_types_with_data_in_functions_table = entity_types  # {-21, -22, -23, -51, -52, -53, -54, -55}
entity_types_with_ontology = {-21, -22, -23, -51, -57}
entity_types_rem_foreground_ids = {-52, -53, -54, -55} # all etypes - PMID - ontologies

functionType_2_entityType_dict = {"Gene Ontology biological process": -21,
                                  "Gene Ontology cellular component": -22,
                                  "Gene Ontology molecular function": -23,
                                  "UniProt keywords": -51,
                                  "KEGG (Kyoto Encyclopedia of Genes and Genomes)": -52,
                                  "SMART (Simple Modular Architecture Research Tool)": -53,
                                  "INTERPRO": -54,
                                  "PFAM (Protein FAMilies)": -55,
                                  "PMID": -56,
                                  "Reactome": -57}

entityType_2_functionType_dict = {-21: "Gene Ontology biological process",
                                  -22: "Gene Ontology cellular component",
                                  -23: "Gene Ontology molecular function",
                                  -51: "UniProt keywords",
                                  -52: "KEGG (Kyoto Encyclopedia of Genes and Genomes)",
                                  -53: "SMART (Simple Modular Architecture Research Tool)",
                                  -54: "INTERPRO",
                                  -55: "PFAM (Protein FAMilies)",
                                  -56: "PMID (PubMed IDentifier)",
                                  -57: "Reactome"}

limit_2_entity_types_ALL = ";".join([str(ele) for ele in entity_types_with_data_in_functions_table])
cols_sort_order_genome = ["term", "hierarchical_level", "p_value", "FDR", "category", "etype", "description", "foreground_count", "background_count", "foreground_ids", "year"]
cols_sort_order_charcterize = ['foreground_count', 'foreground_ids', 'ratio_in_foreground', 'term', 'etype', 'category', 'hierarchical_level', 'description', 'year']
# cols_sort_order_compare_samples = ["term", "hierarchical_level", "p_value", "FDR", "category", "etype", "description", "year", "ratio_in_foreground", "ratio_in_background", "foreground_ids", "background_ids", "foreground_count", "background_count", "foreground_n", "background_n"]
cols_sort_order_compare_samples = ["term", "hierarchical_level", "p_value", "FDR", "category", "etype", "description", "foreground_count", "background_count", "foreground_ids", "year"] # should be the same as cols_sort_order_genome


# api_url_ = r"http://aquarius.meringlab.org:5911/api" # aquarius
# api_url = r"http://agotool.meringlab.org/api"  # atlas
# api_url = "http://localhost:5911/api" # local
api_url = "http://0.0.0.0:5911/api" # local

PYTHON_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
# e.g. '/opt/services/flaskapp/src/python'
if DOCKER:
    APP_DIR = "/opt/services/flaskapp/src"
    DATA_DIR = "/agotool_data"
else: # relative path on host
    APP_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../')))
    DATA_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../../data')))

# DATA_DIR = "/agotool_data"

# WEBSERVER_DATA = DATA_DIR #os.path.join(PROJECT_DIR, 'data')
EXAMPLE_FOLDER = os.path.join(DATA_DIR, "exampledata") #os.path.join(PROJECT_DIR, 'data/exampledata')
SESSION_FOLDER_ABSOLUTE = os.path.join(DATA_DIR, 'session') #os.path.join(PROJECT_DIR, 'data/session')
SESSION_FOLDER_RELATIVE = 'data/session'

# FLASK_DATA = APP_DIR
TEMPLATES_FOLDER_ABSOLUTE = os.path.join(APP_DIR, 'static/templates')

# obo files for PRELOAD/persistent objects
FN_KEYWORDS = os.path.join(DATA_DIR, "PostgreSQL/downloads/keywords-all.obo")
FN_GO_SLIM = os.path.join(DATA_DIR, "PostgreSQL/downloads/goslim_generic.obo")
FN_GO_BASIC = os.path.join(DATA_DIR, "PostgreSQL/downloads/go-basic.obo")

##### Maximum Time for MCL clustering
MAX_TIMEOUT = 5 # minutes

# Flask app
STATIC_DIR_FLASK = os.path.join(APP_DIR, 'static')

# automatic updates
POSTGRESQL_DIR = os.path.join(DATA_DIR, "PostgreSQL")
TABLES_DIR = os.path.join(POSTGRESQL_DIR, "tables")
STATIC_POSTGRES_DIR = os.path.join(POSTGRESQL_DIR, "static")
TEST_DIR = os.path.join(TABLES_DIR, "test")
PYTEST_FN_DIR = os.path.join(PYTHON_DIR, "test")
DOWNLOADS_DIR = os.path.join(POSTGRESQL_DIR, "downloads")
FN_DATABASE_SCHEMA = os.path.join(POSTGRESQL_DIR, "DataBase_Schema_STRING.md")
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

def makedirs_():
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)
    for fn in [LOG_FN_ACTIVITY, LOG_FN_WARNINGS_ERRORS, LOG_FN_UPDATES]:
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
                              "Reactome": "-57"} # Reactome

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

def get_blacklisted_enum_terms(fn_functions_table, blacklisted_terms):
    "| enum | etype | an | description | year | level |"
    blacklisted_enum_terms = []
    with open(fn_functions_table, "r") as fh:
        for line in fh:
            line_split = line.split("\t")
            enum = line_split[0]
            an = line_split[2]
            if an in blacklisted_terms:
                blacklisted_enum_terms.append(int(enum))
    blacklisted_enum_terms = sorted(blacklisted_enum_terms)
    return np.array(blacklisted_enum_terms, dtype=np.dtype("uint32"))

fn_functions_table = os.path.join(TABLES_DIR, "Functions_table_STRING.txt")
try:
    blacklisted_enum_terms = get_blacklisted_enum_terms(fn_functions_table, blacklisted_terms)
except:
    pass
# blacklisted_enum_terms = np.array([45826, 3348, 29853, 44962, 45487, 34225, 45240, 46138, 46149, 46150, 46151, 46152, 45513, 45769, 45130, 46156, 46157, 46158, 46153, 45777, 46056, 45302, 45692], dtype=np.dtype("uint32"))