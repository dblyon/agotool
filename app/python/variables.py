import os, sys, multiprocessing

# settings
DEBUG = True
PRELOAD = True
PROFILING = False
DOCKER = True
# platform_ = sys.platform
# if platform_ == "linux":
#     DOCKER = True
# elif platform_ == "darwin":
#     DOCKER = False

PYTHON_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
# sys.path.append(PYTHON_DIR)

if DOCKER:
    PROJECT_DIR = "/agotool_data" # docker volume
else: # relative path on host
    PROJECT_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../')))

WEBSERVER_DATA = os.path.join(PROJECT_DIR, 'data')
EXAMPLE_FOLDER = os.path.join(PROJECT_DIR, 'data/exampledata')
SESSION_FOLDER_ABSOLUTE = os.path.join(PROJECT_DIR, 'data/session')
SESSION_FOLDER_RELATIVE = 'data/session'

FLASK_DATA = "/opt/services/flaskapp/src"
TEMPLATES_FOLDER_ABSOLUTE = os.path.join(FLASK_DATA, 'static/templates')


# obo files for PRELOAD/persistent objects
FN_KEYWORDS = os.path.join(WEBSERVER_DATA, "PostgreSQL/downloads/keywords-all.obo")
FN_GO_SLIM = os.path.join(WEBSERVER_DATA, "PostgreSQL/downloads/goslim_generic.obo")
FN_GO_BASIC = os.path.join(WEBSERVER_DATA, "PostgreSQL/downloads/go-basic.obo")

##### Maximum Time for MCL clustering
MAX_TIMEOUT = 10 # minutes

# Flask app
APP_ROOT = FLASK_DATA
DATA_DIR = os.path.join(APP_ROOT, 'data')
# SCRIPT_DIR = os.path.join(APP_ROOT, 'scripts')
STATIC_DIR = os.path.join(APP_ROOT, 'static')

# automatic updates
POSTGRESQL_DIR = os.path.join(PROJECT_DIR, "data/PostgreSQL")
TABLES_DIR = os.path.join(PROJECT_DIR, "data/PostgreSQL/tables")

#!!! NAME COLLISION
STATIC_POSTGRES_DIR = os.path.join(PROJECT_DIR, "data/PostgreSQL/static")

TEST_DIR = os.path.join(TABLES_DIR, "test")
DOWNLOADS_DIR = os.path.join(PROJECT_DIR, "data/PostgreSQL/downloads")
DIRECTORIES_LIST = [os.path.join(PROJECT_DIR, 'data/PostgreSQL', directory) for directory in ["downloads", "session"]]
DIRECTORIES_LIST.append(os.path.join(PROJECT_DIR, 'logs'))
FILES_NOT_2_DELETE = [os.path.join(DOWNLOADS_DIR + fn) for fn in ["keywords-all.obo", "goslim_generic.obo", "go-basic.obo"]]

# CPU usage during updates (for "sort --parallel")
NUMBER_OF_PROCESSES = multiprocessing.cpu_count()

# log files
LOG_DIRECTORY = os.path.join(PROJECT_DIR, "logs")
LOG_FN_WARNINGS_ERRORS = os.path.join(PROJECT_DIR, "logs/warnings_errors_log.txt")
LOG_FN_ACTIVITY = os.path.join(PROJECT_DIR, "logs/activity_log.txt")
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)
if not os.path.exists(LOG_FN_WARNINGS_ERRORS):
    fh = open(LOG_FN_WARNINGS_ERRORS, "w")
    fh.close()
