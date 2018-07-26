import os, multiprocessing

############################
# settings
PRELOAD = True # pre-load objects DB connection necessary, set to False while testing with pytest
skip_slow_downloads = True # 2 large slow downloads that take >= 30 min to download
skip_downloads_completely = True # don't download anything

### adapt volumes accordingly in docker-compose.yml
DOCKER = False # local (bind-mounted volume if DOCKER=False --> version 1) vs. dockerized version (named-volume, copy data to named-volume first, if DOCKER=True --> version 2)

DB_DOCKER = True # use local vs dockerized Postgres, in query.py
DEBUG = False # for flask and some internals for printing, set to False in production
PROFILING = True # profiling flaskapp --> check stdout, set to False in production
TESTING = False # use small testing subset of files for DB import, checking settings when intilizing everything for the first time
VERBOSE = True # print stuff to stdout
PD_WARNING_OFF = True # turn off pandas warning about chained assignment (pd.options.mode.chained_assignment = None)
VERSION_ = "STRING" # switch between "STRING" and "aGOtool" versions of the program
############################

function_types = ("BP", "CP", "MF", "UPK", "KEGG", "DOM")
entity_types = {'-21', '-22', '-23', '-51', '-52', '-53', '-54', '-55', '-56'}


PYTHON_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
# e.g. '/opt/services/flaskapp/src/python'
if DOCKER:
    APP_DIR = "/opt/services/flaskapp/src"
    # DATA_DIR = "/agotool_data/data"
else: # relative path on host
    APP_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../')))
    # DATA_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../../data')))

DATA_DIR = "/agotool_data"

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
