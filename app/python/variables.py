import os, multiprocessing

##############
# settings
DEBUG = False
PRELOAD = True
PROFILING = False
DOCKER = True
skip_slow_downloads = False
##############

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
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)
for fn in [LOG_FN_ACTIVITY, LOG_FN_WARNINGS_ERRORS, LOG_FN_UPDATES]:
    if not os.path.exists(fn):
        fh = open(fn, "w")
        fh.close()

# CPU usage during updates (for "sort --parallel")
NUMBER_OF_PROCESSES = multiprocessing.cpu_count()
