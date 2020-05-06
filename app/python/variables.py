import os, multiprocessing, sys
import numpy as np
import socket
hostname = socket.gethostname()
import yaml # conda install pyyaml NOT yaml

############################
### settings
PRELOAD = True # set True in production
# pre-load objects DB connection necessary, set to False while testing with pytest
# skip_slow_downloads = True # 2 large slow downloads that take >= 30 min to download
# skip_downloads_completely = True # don't download anything
DOCKER = False # app and data directory, within image or shared with local host, adapt accordingly in docker-compose
# FUTURES = False # parallel code disabled
## local (bind-mounted volume if DOCKER=False --> version 1)
## vs. dockerized version (named-volume, copy data to named-volume first, if DOCKER=True --> version 2)
LOW_MEMORY = True # load function_an_2_description_dict or query DB
DB_DOCKER = False # connect to local Postgres or dockerized-Postgres
READ_FROM_FLAT_FILES = True # get data for PQO from flat files instead of from PostgreSQL # set "DOCKER" to True!
DEBUG = False # for flask and some internals for printing, set to False in production
DEBUG_HTML = False # if True: always load example results on submit
PROFILING = False # profiling flaskapp --> check stdout, set to False in production
TESTING = False
# use small testing subset of files for DB import, checking settings when intilizing everything for the first time
VERBOSE = True # print stuff to stdout
PD_WARNING_OFF = True # turn off pandas warning about chained assignment (pd.options.mode.chained_assignment = None)
VERSION_ = "UniProt" # switch between "STRING" and "UniProt" versions of the program
temp_dont_run_analysis = False
# if READ_FROM_FLAT_FILES and LOW_MEMORY:
#     raise NotImplementedError

ARGPARSE = False
############################
entity_types = {-20, -21, -22, -23, -25, -26, -51, -52, -53, -54, -55, -56, -57, -58} # SMART is missing in UniProt version
alpha = 0.05
entity_types_with_data_in_functions_table = entity_types
entity_types_with_ontology = {-20, -21, -22, -23, -25, -26, -51, -57} # Interpro has ontology, but omitted here to turn off filter_parents functionality
PMID = {-56}
# entity_types_rem_foreground_ids = {-52, -53, -54, -55} # all etypes - PMID - ontologies
entity_types_rem_foreground_ids = entity_types - PMID - entity_types_with_ontology # {-52, -53, -54, -55, -56, -58}
entity_types_with_scores = {-20, -25, -26}  # GO-CC, BTO, DOID
enrichment_methods = {"abundance_correction", "compare_samples", "characterize_foreground", "genome", "compare_groups"}
# all except for TM scores "-21;-22;-23;-51;-52;-53;-54;-55;-56-57;-58"

functionType_2_entityType_dict = {"Gene Ontology cellular component TEXTMINING": -20,
                                  "Gene Ontology biological process": -21,
                                  "Gene Ontology cellular component": -22,
                                  "Gene Ontology molecular function": -23,
                                  "Brenda Tissue Ontology": -25,
                                  "Disease Ontology": -26,
                                  "UniProt keywords": -51,
                                  "KEGG (Kyoto Encyclopedia of Genes and Genomes)": -52,
                                  "SMART (Simple Modular Architecture Research Tool)": -53,
                                  "INTERPRO": -54,
                                  "PFAM (Protein FAMilies)": -55,
                                  "PMID": -56,
                                  "Reactome": -57,
                                  "WikiPathways": -58}

entityType_2_functionType_dict = {-20: "Gene Ontology cellular component TEXTMINING",
                                  -21: "Gene Ontology biological process",
                                  -22: "Gene Ontology cellular component",
                                  -23: "Gene Ontology molecular function",
                                  -25: "Brenda Tissue Ontology",
                                  -26: "Disease Ontology",
                                  -51: "UniProt keywords",
                                  -52: "KEGG (Kyoto Encyclopedia of Genes and Genomes)",
                                  -53: "SMART (Simple Modular Architecture Research Tool)",
                                  -54: "INTERPRO",
                                  -55: "PFAM (Protein FAMilies)",
                                  -56: "PMID (PubMed IDentifier)",
                                  -57: "Reactome",
                                  -58: "WikiPathways"}

id_2_entityTypeNumber_dict = {'GOCC:0005575': "-20",  # 'Cellular Component TEXTMINING',
                              'GO:0003674': "-23",  # 'Molecular Function',
                              'GO:0005575': "-22",  # 'Cellular Component',
                              'GO:0008150': "-21",  # 'Biological Process',
                              "GO:OBSOLETE": "-24", # "GO obsolete
                              "BTO tissues": "-25", # Brenda Tissue Ontology
                              "DOID diseases": "-26", # Disease Ontology IDs
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
                              "Reactome": "-57", # Reactome
                              "WikiPathways": "-58"}  # WikiPathways

goslims_subsets_dict = { # key: abbreviation val: description
    "agr": "GO Consortium for the Alliance of Genomes Resources",
    "aspergillus": "Aspergillus subset Aspergillus Genome Data",
    "candida": "Candida albicans by Candida Genome Database",
    "chembl": "Chembl Drug Target",
    "flybase_ribbon": "FlyBase",
    "generic": "Generic GO slim by GO Consortium",
    "metagenomics": "EBI Metagenomics group",
    "mouse": "Mouse Genome Informatics",
    "pir": "Protein Information Resource",
    "plant": "The Arabidopsis Information Resource",
    "pombe": "Schizosaccharomyces pombe subset PomBase",
    "synapse": "Synapse GO slim SynGO",
    "yeast": "Yeast subset Saccharomyces Genome Database"
}

limit_2_entity_types_ALL = ";".join([str(ele) for ele in entity_types_with_data_in_functions_table])
cols_sort_order_genome = ["term", "hierarchical_level", "p_value", "FDR", "category", "etype", "description", "foreground_count", "background_count", "foreground_ids", "year"]
cols_sort_order_charcterize = ['foreground_count', 'foreground_ids', 'ratio_in_foreground', 'term', 'etype', 'category', 'hierarchical_level', 'description', 'year']
cols_sort_order_compare_samples = ["term", "hierarchical_level", "p_value", "FDR", "category", "etype", "description", "foreground_count", "background_count", "foreground_ids", "year"] # should be the same as cols_sort_order_genome

# api_url_ = r"http://aquarius.meringlab.org:5911/api" # aquarius
# api_url = r"http://agotool.meringlab.org/api"  # atlas
api_url = "http://0.0.0.0:5911/api" # local

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

# temp
fn_example = os.path.join(EXAMPLE_FOLDER, "Test_human_compare_samples.txt") #"Test_yeast_compare_samples_small.txt") #"Test_yeast_compare_samples.txt")

# FLASK_DATA = APP_DIR
TEMPLATES_FOLDER_ABSOLUTE = os.path.join(APP_DIR, 'static/templates')

# obo files for PRELOAD/persistent objects
FN_KEYWORDS = os.path.join(DATA_DIR, "PostgreSQL/downloads/keywords-all.obo")
FN_GO_SLIM = os.path.join(DATA_DIR, "PostgreSQL/downloads/goslim_generic.obo")
FN_GO_BASIC = os.path.join(DATA_DIR, "PostgreSQL/downloads/go-basic.obo")

##### Maximum Time for MCL clustering
# MAX_TIMEOUT = 5 # minutes

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
FN_DATABASE_SCHEMA = os.path.join(POSTGRESQL_DIR, "DataBase_Schema.md")
FN_HELP_ENTITY_TYPES = os.path.join(POSTGRESQL_DIR, "example_help_entity_types.md")
FN_HELP_PARAMETERS = os.path.join(POSTGRESQL_DIR, "example_help_parameters.md")

DIRECTORIES_LIST = [os.path.join(DATA_DIR, 'PostgreSQL/downloads'),
                    os.path.join(DATA_DIR, 'logs'),
                    os.path.join(DATA_DIR, 'session')]
FILES_NOT_2_DELETE = [os.path.join(DOWNLOADS_DIR + fn) for fn in ["keywords-all.obo", "goslim_generic.obo", "go-basic.obo"]]

# log files
LOG_DIRECTORY = os.path.join(DATA_DIR, "logs")
LOG_DF_FILE_DIMENSIONS = os.path.join(LOG_DIRECTORY, "DF_file_dimensions_log.txt")
LOG_DIRECTORY_SNAKEMAKE = os.path.join(DATA_DIR_SNAKEMAKE, "logs")
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

### Blacklisted terms
# top level KW except Disease and Developmental stage
# 'KW-9995' 'Disease',
# 'KW-9996' 'Developmental stage'
# 'KW-9990' 'Technical term' and all its children
blacklisted_terms = {'GO:0003674', 'GO:0008150', 'GO:0005575', "GOCC:0005575",
                     'KW-0002', 'KW-0181', 'KW-0308', 'KW-0374', 'KW-0582', 'KW-0614',
                     'KW-0814', 'KW-0895', 'KW-0903', 'KW-0952', 'KW-1185', 'KW-1267',
                     'KW-9990', 'KW-9991', 'KW-9992', 'KW-9993', 'KW-9994', 'KW-9997', 'KW-9998', 'KW-9999',
                     'GOCC:0005623', 'GOCC:0044464', 'GOCC:0005622', 'GOCC:0043226', 'GOCC:0044422',
                     'GOCC:0044424', 'GOCC:0043229', 'GOCC:0043227', 'GOCC:0005737', 'GOCC:0043231', 'GOCC:0016020', 'GOCC:0044444', 'GOCC:0044446',
                     'GOCC:0032991', 'GOCC:0071944', 'GOCC:0044425', 'GOCC:0043232', 'GOCC:0012505', 'GOCC:0070013', 'GOCC:0031224', 'GOCC:0031090',
                     'GOCC:0016021', 'GOCC:0031982'}
# GOCC:0005623 = Cell;
# GOCC:0044464 = Cell part;
# GOCC:0005622 = Intracellular
# GOCC:0043226 = Organelle
# GOCC:0044422 = Organelle part
#       	funcName 	descripion
# 0 	GOCC:0044424 	Intracellular part
# 1 	GOCC:0043229 	Intracellular organelle
# 2 	GOCC:0043227 	Membrane-bounded organelle
# 3 	GOCC:0005737 	Cytoplasm
# 4 	GOCC:0043231 	Intracellular membrane-bounded organelle
# 5 	GOCC:0016020 	Membrane
# 6 	GOCC:0044444 	Cytoplasmic part
# 7 	GOCC:0044446 	Intracellular organelle part
# 8 	GOCC:0032991 	Protein-containing complex
# 9 	GOCC:0071944 	Cell periphery
# 10 	GOCC:0044425 	Membrane part
# 11 	GOCC:0043232 	Intracellular non-membrane-bounded organelle
# 12 	GOCC:0012505 	Endomembrane system
# 13 	GOCC:0070013 	Intracellular organelle lumen
# 14 	GOCC:0031224 	Intrinsic component of membrane
# 15 	GOCC:0031090 	Organelle membrane
# 16 	GOCC:0016021 	Integral component of membrane
# 17 	GOCC:0031982 	Vesicle




##### final Tables / flat-files needed for flask app / PostgreSQL
if VERSION_ == "UniProt":
    appendix = "UPS_FIN"
elif VERSION_ == "STRING":
    appendix = "STS_FIN"
else:
    print("VERSION_ {} not know".format(VERSION_))
    raise sys.exit(2)

tables_dict = {"Entity_types_table": os.path.join(TABLES_DIR, "Entity_types_table_{}.txt".format(appendix)),
    "KEGG_Taxid_2_acronym_table": os.path.join(TABLES_DIR, "KEGG_Taxid_2_acronym_table_{}.txt".format(appendix)),
    "Lineage_table": os.path.join(TABLES_DIR, "Lineage_table_{}.txt".format(appendix)),
    "Functions_table": os.path.join(TABLES_DIR, "Functions_table_{}.txt".format(appendix)), # Functions_table_UPS_reduced
    "Protein_2_FunctionEnum_table": os.path.join(TABLES_DIR, "Protein_2_FunctionEnum_table_{}.txt".format(appendix)), # if not low_mem
    "Protein_2_FunctionEnum_and_Score_table": os.path.join(TABLES_DIR, "Protein_2_FunctionEnum_and_Score_table_{}.txt".format(appendix)),
    "Secondary_2_Primary_ID_table": os.path.join(TABLES_DIR, "Secondary_2_Primary_ID_{}.txt".format(appendix)), # if not low_mem
    "Taxid_2_FunctionCountArray_table": os.path.join(TABLES_DIR, "Taxid_2_FunctionCountArray_table_{}.txt".format(appendix)),
    "Taxid_2_FunctionEnum_2_Scores_table": os.path.join(TABLES_DIR, "Taxid_2_FunctionEnum_2_Scores_table_{}.txt".format(appendix)),
    "Taxid_2_Proteins_table": os.path.join(TABLES_DIR, "Taxid_2_Proteins_table_{}.txt".format(appendix)),
    "taxid_2_tuple_funcEnum_index_2_associations_counts": os.path.join(TABLES_DIR, "taxid_2_tuple_funcEnum_index_2_associations_counts_pickle_{}.p".format(appendix)),
    "CSC_ENSPencoding_2_FuncEnum": os.path.join(TABLES_DIR, "CSC_ENSPencoding_2_FuncEnum_{}.npz".format(appendix)),
    "ENSP_2_rowIndex_dict": os.path.join(TABLES_DIR, "ENSP_2_rowIndex_dict_{}.p".format(appendix)),
    "rowIndex_2_ENSP_dict": os.path.join(TABLES_DIR, "rowIndex_2_ENSP_dict_{}.p".format(appendix)),
    "year_arr": os.path.join(TABLES_DIR, "year_arr_{}.p".format(appendix)),
    "hierlevel_arr": os.path.join(TABLES_DIR, "hierlevel_arr_{}.p".format(appendix)),
    "entitytype_arr": os.path.join(TABLES_DIR, "entitytype_arr_{}.p".format(appendix)),
    "functionalterm_arr": os.path.join(TABLES_DIR, "functionalterm_arr_{}.p".format(appendix)),
    "indices_arr": os.path.join(TABLES_DIR, "indices_arr_{}.p".format(appendix)),
    "description_arr": os.path.join(TABLES_DIR, "description_arr_{}.p".format(appendix)),
    "category_arr": os.path.join(TABLES_DIR, "category_arr_{}.p".format(appendix)),
    "Taxid_2_FunctionEnum_2_Scores_dict": os.path.join(TABLES_DIR, "Taxid_2_FunctionEnum_2_Scores_dict_{}.p".format(appendix)),
    "Taxid_2_FuncEnum_2_Score_2_Rank_dict": os.path.join(TABLES_DIR, "Taxid_2_FuncEnum_2_Score_2_Rank_dict_{}.p".format(appendix)),
    "Taxid_2_FuncEnum_2_medianScore_dict": os.path.join(TABLES_DIR, "Taxid_2_FuncEnum_2_medianScore_dict_{}.p".format(appendix)),
    "Taxid_2_FuncEnum_2_numBGvals_dict": os.path.join(TABLES_DIR, "Taxid_2_FuncEnum_2_numBGvals_dict_{}.p".format(appendix)),
    "goslim_subsets_file": os.path.join(TABLES_DIR, "goslim_subsets_file_{}.txt".format(appendix))
               }
TABLES_DICT_SNAKEMAKE = {tablename: os.path.join(TABLES_DIR_SNAKEMAKE, os.path.basename(fn)) for tablename, fn in tables_dict.items()}


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

fn_functions_table = tables_dict["Functions_table"]
try:
    blacklisted_enum_terms = get_blacklisted_enum_terms(fn_functions_table, blacklisted_terms)
except:
    pass

jensenlab_score_cutoff_list = [4.0, 3.0, 2.0, 1.0, 0.0]
jensenlab_supported_taxids = [9606, 10090, 10116, 3702, 7227, 6239, 4932, 4896] #559292, 284812]
jensenlab_supported_taxids_species_translations_dict = {4932: 559292, 4896: 284812} # Lars TextMining data has e.g. 4932 but UniProt has 559292 as a reference proteome
dtype_TM_score = "uint32" # dtype Jensenlab TextMining score
dtype_functionEnumeration = "uint32"
# human, mouse, rat, arabidopsis, yeast, fly, worm, yeast # ??? anything important missing? preload all of swissprot?
taxids_2_preload = [9606, 10090, 10116, 3702, 4932, 7227, 6239, 4896]

# 4932 Saccharomyces cerevisiae, Jensenlab
# 559292 Saccharomyces cerevisiae S288C, UniProt Reference Proteome
# 4932 --> 559292
# 4896 Schizosaccharomyces pombe, Jensenlab
# 284812 Schizosaccharomyces pombe 972h-, UniProt Reference Proteome
# 4896 --> 284812
# ToDo test if user with query of 4932 gets background proteome for 559292
# ToDo check/do functional annotation transfer from Jensenlab 4932 to 559292 ???
# Only UniProt Reference Proteomes used for enrichment method "genome"
# strain level information duplicated from to 559292 --> 4932 and 284812 --> 4896 (Taxid_2_Proteins_table_UPS_FIN.txt expanded)
# Protein_2_FunctionEnum_and_Score_table_UPS_FIN.txt
# 10090
# 10116
# 3702
# 4896
# 4932
# 6239
# 7227
# 9606
# ToDo: if user enters 284812 or 559292 --> inform and show proper yeast background proteome
# 10090 species 10090 Mus musculus
# 10116 species 10116 Rattus norvegicus
# 3702 species 3702 Arabidopsis thaliana
# 4896 species 4896 Schizosaccharomyces pombe
# 4932 species 4932 Saccharomyces cerevisiae
# 6239 species 6239 Caenorhabditis elegans
# 7227 species 7227 Drosophila melanogaster

### time temp.sh on mnemo5
# temp.sh  2027.61s user 120.36s system 344% cpu 10:23.66 total
### time temp.sh on atlas home
# temp.sh  2163.76s user 137.69s system 1883% cpu 2:02.19 total
### time temp.sh on mnemo5 after cleanup
# temp.sh  2180.76s user 136.73s system 1321% cpu 2:55.40 total

####################################
### Atlas
# agotool v0 STRING v11 (without DB)
# http://127.0.0.1:5912/

# agotool v1 UniProt version running KS with Scipy (using Docker DB)
# http://127.0.0.1:5000/

# agotool v2 UniProt version running KS with Cython (using different Docker DB)
# docker DB on 5914:5432
# http://127.0.0.1:5923/
# python runserver.py 0.0.0.0 5923

# Lars evidence codes being used
# ['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP', 'HTP', 'HDA', 'HMP', 'HGI', 'HEP', 'ISS', 'ISO', 'ISA', 'ISM', 'IGC', 'IBA', 'IBD', 'IKR', 'IMR', 'IRD', 'RCA', 'TAS', 'NAS', 'IC', 'ND', 'IEA', 'NR']
# sources being used SGD, WormBase, and FlyBase

# ######## Docker PostgreSQL port
# AGOTOOL_DIR = os.path.join(APP_DIR, '../')
# def get_Docker_PostgreSQL_port_from_yml():
#     if hostname == "ody":
#         docker_hostspecific_yml = os.path.join(AGOTOOL_DIR, "docker_ody.yml")
#     elif hostname in "aquarius":
#         docker_hostspecific_yml = os.path.join(AGOTOOL_DIR, "docker_aquarius.yml")
#     elif hostname in {"atlas", "gaia"}:
#         docker_hostspecific_yml = os.path.join(AGOTOOL_DIR, "docker_atlas.yml")
#     else:
#         print("hostname {} does not have a specific docker_*.yml file".format(hostname))
#         raise StopIteration
#     try:
#         with open(docker_hostspecific_yml) as fh:
#             text = fh.read()
#         yml_as_dict = yaml.load(text, Loader=yaml.FullLoader)
#     except:
#         return False
#     try:
#         Docker_incoming_PostgreSQL_port = yml_as_dict["services"]["db"]["ports"][0].split(":")[0]
#     except KeyError:
#         print("Can't parse file {} correctly to find Docker port for PostgreSQL".format(docker_hostspecific_yml))
#         return False
#     return Docker_incoming_PostgreSQL_port
#
# Docker_incoming_PostgreSQL_port = get_Docker_PostgreSQL_port_from_yml()

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
try:
    param_2_val_dict = parse_env_file(fn)
except:
    pass