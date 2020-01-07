import os, time

import variables

TEST_DIR = variables.TEST_DIR
STATIC_DIR = variables.STATIC_DIR
TABLES_DIR = variables.TABLES_DIR
LOG_DIR = variables.LOG_DIR



def get_table_name_2_absolute_path_dict(testing=False):
    if testing:
        TABLES_DIR = TEST_DIR
    functions_table = os.path.join(TABLES_DIR, "Functions_table.txt")
    go_2_slim_table = os.path.join(TABLES_DIR, "GO_2_Slim_table.txt")
    og_2_function_table = os.path.join(STATIC_DIR, "OG_2_Function_table_static.txt")
    ogs_table = os.path.join(STATIC_DIR, "OGs_table_static.txt")
    ontologies_table = os.path.join(TABLES_DIR, "Ontologies_table.txt")
    protein_2_function_table = os.path.join(TABLES_DIR, "Protein_2_Function_table.txt")
    protein_2_og_table = os.path.join(STATIC_DIR, "Protein_2_OG_table_static.txt")
    protein_secondary_2_primary_an_table = os.path.join(TABLES_DIR, "Protein_Secondary_2_Primary_AN_table.txt")
    table_name_2_absolute_path_dict = {"functions_table": functions_table,
                                       "go_2_slim_table": go_2_slim_table,
                                       "og_2_function_table": og_2_function_table,
                                       "ogs_table": ogs_table,
                                       "ontologies_table": ontologies_table,
                                       "protein_2_function_table": protein_2_function_table,
                                       "protein_2_og_table": protein_2_og_table,
                                       "protein_secondary_2_primary_an_table": protein_secondary_2_primary_an_table}
    return table_name_2_absolute_path_dict

def parse_table_line_numbers_count_log(fn):
    table_name_2_number_of_lines_dict = {}
    with open(fn, "r") as fh:
        for line in fh:
            line_split = line.strip().split(": ")
            if len(line_split) == 2:
                table_name, number_lines = line_split
                table_name_2_number_of_lines_dict[table_name] = int(number_lines)
    return table_name_2_number_of_lines_dict

def count_line_numbers(fn):
    i = 0 # if file can't be opened
    with open(fn, "r") as fh:
        for i, _ in enumerate(fh):
            pass
    return i + 1

def are_current_number_of_lines_larger(previous_dict, current_dict):
    """
    compare line numbers of tables between updates
    :param current_dict: Dict(key=Strin(TableName), val=Int(NumberOfLines))
    :param previous_dict: Dict(key=Strin(TableName), val=Int(NumberOfLines))
    :return: Bool
    """
    # compare dicts, values should be equal or larger
    for table_name, number_lines_previous in previous_dict.items():
        try:
            number_lines_current = current_dict[table_name]
        except KeyError:
            print("Something went wrong while logging for table_line_numbers_count_log.txt")
            return False
        if number_lines_current - number_lines_previous >= 0:
            pass
        else:
            return False
    return True

def sanity_check_table_dimensions(testing=False):
    # get all the table and file names to count line numbers
    table_name_2_absolute_path_dict = get_table_name_2_absolute_path_dict(testing)
    fn_list = sorted(table_name_2_absolute_path_dict.values())
    # count previous line numbers
    line_numbers_count_log = os.path.join(LOG_DIR, "table_line_numbers_count_log.txt")
    try:
        table_name_2_number_of_lines_dict_previous = parse_table_line_numbers_count_log(line_numbers_count_log)
    except FileNotFoundError:
        print("Sanity check for number of lines in PostgreSQL tables could not pass since line_numbers_count_log.txt does not exist.\n")
        return False
    # table_name_2_number_of_lines_dict_previous = parse_table_line_numbers_count_log(line_numbers_count_log)
    with open(line_numbers_count_log, "a+") as fh:
        fh.write("### Current date & time " + time.strftime("%c") + "\n")
        for fn in fn_list:
            lines_count = count_line_numbers(fn)
            basename = os.path.basename(fn)
            fh.write(basename + ": " + str(lines_count) + "\n")
        fh.write("#"*50 + "\n")
    # count current line numbers
    table_name_2_number_of_lines_dict_current = parse_table_line_numbers_count_log(line_numbers_count_log)
    # try:
    #     table_name_2_number_of_lines_dict_current = parse_table_line_numbers_count_log(line_numbers_count_log)
    # except FileNotFoundError:
    #     print("Sanity check for number of lines in PostgreSQL tables could not pass since line_numbers_count_log.txt does not exist.\n")
    #     return False
    # compare line numbers
    if are_current_number_of_lines_larger(table_name_2_number_of_lines_dict_previous, table_name_2_number_of_lines_dict_current):
        print("Sanity check for number of lines in PostgreSQL tables passed.\n")
        return True
    else:
        print("Sanity check for number of lines in PostgreSQL tables DID NOT PASS!!\n")
        return False

# - are all 10 tables there
# - are all numpy files there
# - is the size of the numpy files the same of larger?
# - is the size of the tables the same of larger?
# - number of lines roughly equal?