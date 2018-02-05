import os, sys, multiprocessing

docker = True

PYTHON_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
# sys.path.append(PYTHON_DIR)
if docker:
    PROJECT_DIR = "/agotool_data" # docker volume
else: # relative path on host
    PROJECT_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../')))
POSTGRESQL_DIR = os.path.join(PROJECT_DIR, "data/PostgreSQL")
DOWNLOADS_DIR = os.path.join(PROJECT_DIR, "data/PostgreSQL/downloads")
DIRECTORIES_LIST = [os.path.join(PROJECT_DIR, 'data/PostgreSQL', directory) for directory in ["downloads", "session"]]
DIRECTORIES_LIST.append(os.path.join(PROJECT_DIR, 'logs'))

# print("Pythondir", PYTHON_DIR)
# print("PROJECT_DIR ", PROJECT_DIR)
# print("DOWNLOADS_DIR", DOWNLOADS_DIR)

# if docker:
#     TABLES_DIR = r"/agotool_data/PostgreSQL/tables"
#     STATIC_DIR = r"/agotool_data/PostgreSQL/static"
# else:
TABLES_DIR = os.path.join(PROJECT_DIR, "data/PostgreSQL/tables")
STATIC_DIR = os.path.join(PROJECT_DIR, "data/PostgreSQL/static")
TEST_DIR = os.path.join(TABLES_DIR, "test")

FILES_NOT_2_DELETE = [os.path.join(DOWNLOADS_DIR + fn) for fn in ["keywords-all.obo", "goslim_generic.obo", "go-basic.obo"]]

NUMBER_OF_PROCESSES = multiprocessing.cpu_count()