import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import variables
import download_resources
import create_SQL_tables

if __name__ == "__main__":
    # debug = False
    # testing = False
    # verbose = True
    if not variables.skip_downloads_completely:
        print("Downloading resources")
        download_resources.run_downloads(debug=variables.DEBUG, skip_slow_downloads=variables.skip_slow_downloads)
        print("finished downloading resources")
    print("Creating SQL tables")
    create_SQL_tables.run_create_tables_for_PostgreSQL(debug=variables.DEBUG, testing=variables.TESTING, verbose=variables.VERBOSE)
    print(create_SQL_tables.sanity_check_table_dimensions(testing=variables.TESTING))
    print("finished creating tables")
    print("*"*50)
