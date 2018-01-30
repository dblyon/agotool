import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import download_resources
import create_SQL_tables

if __name__ == "__main__":
    debug = False
    testing = False
    verbose = True
    print("Downloading resources")
#    download_resources.run_downloads(debug=debug)
    print("finished downloading resources")
    print("Creating SQL tables")
    create_SQL_tables.run_create_tables_for_PostgreSQL(debug=debug, testing=testing, verbose=verbose)
    print(create_SQL_tables.sanity_check_table_dimensions(testing=testing))
    print("finished creating tables")
    print("*"*50)
