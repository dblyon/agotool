import os, multiprocessing

############################
# settings
PRELOAD = False # pre-load objects DB connection necessary
skip_slow_downloads = True # 2 large slow downloads that take >= 30 min to download
skip_downloads_completely = True # don't download anything

DOCKER = True # local vs. dockerized version
DB_DOCKER = True # use local vs dockerized Postgres
DEBUG = True # for flask and some internals for printing, set to False in production
PROFILING = False # profiling flaskapp --> check stdout, set to False in production
TESTING = False # small testing subset of files for DB import, checking settings
VERBOSE = True # print stuff to stdout
############################

function_types = ("BP", "CP", "MF", "UPK", "KEGG", "DOM")

PYTHON_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
if DOCKER:
    APP_DIR = "/opt/services/flaskapp/src"
    DATA_DIR = "/agotool_data/data"
else: # relative path on host
    APP_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../')))
    DATA_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../../data')))

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
DOWNLOADS_DIR = os.path.join(POSTGRESQL_DIR, "downloads")

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
