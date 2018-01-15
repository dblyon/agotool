import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import download_resources
import create_SQL_tables


if __name__ == "__main__":
    debug = False
    testing = False
    foragotool = True
    verbose = True
    print("Downloading resources")
    download_resources.run_downloads(debug=debug)
    print("finished downloading resources")
    print("Creating SQL tables, copying from file, and indexing")
    create_SQL_tables.run_PostgreSQL_create_tables_and_build_DB(debug=debug, testing=testing, foragotool=foragotool, verbose=verbose)
    print("finished with SQL stuff")
    print("*"*50)

