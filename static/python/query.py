from collections import defaultdict
import psycopg2, math

UNSIGNED_2_SIGNED_CONSTANT = int(math.pow(2, 63))

upkTerm_2_functionAN_dict = {u'Biological process': u'UPK:9999',
                             u'Cellular component': u'UPK:9998',
                             u'Coding sequence diversity': u'UPK:9997',
                             u'Developmental stage': u'UPK:9996',
                             u'Disease': u'UPK:9995',
                             u'Domain': u'UPK:9994',
                             u'Ligand': u'UPK:9993',
                             u'Molecular function': u'UPK:9992',
                             u'Post-translational modification': u'UPK:9991',
                             u'PTM': u'UPK:9991',
                             u'Technical term': u'UPK:9990'}

humanName_2_functionAN_dict = {u"BP": u"GO:0008150",
                               u"CP": u"GO:0005575",
                               u"MF": u"GO:0003674",
                               u"Biological Process": u"GO:0008150",
                               u"Cellular Component": u"GO:0005575",
                               u"Molecular Function": u"GO:0003674"}

functionType_term_2_an_dict = {"UPK": upkTerm_2_functionAN_dict,
                               "GO": humanName_2_functionAN_dict}


def get_cursor(host='localhost', dbname='agotool', user='dblyon', password=''):
    """
    :param host:
    :param dbname:
    :param user:
    :param password:
    :return: DB Cursor instance object
    """
    # Define our connection string
    conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, user, password)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    return cursor

def query_example(cursor):
    cursor.execute("SELECT * FROM child_2_parent_table LIMIT 5")
    records = cursor.fetchall()
    print(records)

def map_secondary_2_primary_ANs(ans_list):
    """
    map secondary UniProt ANs to primary ANs,
    AN only in dict if mapping exists
    :param ans_list: ListOfString
    :return: Dict (key: String(Secondary AN), val: String(Primary AN))
    """
    cursor = get_cursor()
    ans_list = str(ans_list)[1:-1]
    sql_statement = "SELECT protein_secondary_2_primary_an.sec, protein_secondary_2_primary_an.pri FROM protein_secondary_2_primary_an WHERE protein_secondary_2_primary_an.sec IN({})".format(ans_list)
    cursor.execute(sql_statement)
    result = cursor.fetchall()
    secondary_2_primary_dict = {}
    for res in result:
        secondary = res[0]
        primary = res[1]
        secondary_2_primary_dict[secondary] = primary
    return secondary_2_primary_dict

def get_association_dict(protein_ans_list, function_type, limit_2_parent=None, basic_or_slim="slim", backtracking=True):
    """
    # def get_association_dict(connection, protein_ans_list, function_type, limit_2_parent=None, basic_or_slim="slim"):
    e.g.
    function_type = "GO"
    limit_2_parent = u"Biological Process"
    basic_or_slim = "basic"
    protein_ans_list = ['Q9XC60', 'P40417']
    cursor = query.get_cursor()
    assoc_dict = query.get_association_dict(cursor, protein_ans_list, function_type, limit_2_parent, basic_or_slim)

    GO-term categories:
        "BP" "GO:0008150"
        "CP" "GO:0005575"
        "MF" "GO:0003674"
    UniProt-Keyword categories:
        Biological process
        Cellular component
        Coding sequence diversity
        Developmental stage
        Disease
        Domain
        Ligand
        Molecular function
        Post-translational modification
        Technical term
    :param cursor: data base connection object
    :param protein_ans_list: ListOfString (AccessionNumbers of Proteins)
    :param function_type: String (one of "GO", "UPK", "KEGG", "DOM")
    :param limit_2_parent: String (e.g. "BP", "CP", "MF", "Technical term", "Biological process", etc.)
    :param basic_or_slim: String (one of "basic", "slim")
    :param backtracking: Bool
    :return: Dict(key=AN, val=set of String)
    """
    cursor = get_cursor()
    protein_ans_list = str(protein_ans_list)[1:-1]
    # an_2_functions_dict = {}
    an_2_functions_dict = defaultdict(lambda: set())
    parameters_dict = {"protein_ans_list": protein_ans_list, "function_type": function_type, "limit_2_parent": get_termAN_from_humanName_functionTye(function_type, limit_2_parent)}

    ##### UniProt proteins

    # !!! do this in java script ToDo
    # Java script:
    # if "UPK": set basic_or_slim to "basic" and hide option
    # if function_type is KEGG or DOM --> set backtracking to False

    if function_type == "KEGG" or function_type == "DOM": #!!! do this in java script ToDo
        backtracking = False
    elif function_type == "UPK": #!!! do this in java script ToDo
        basic_or_slim = "basic"

    if backtracking:
        join_stmt = ("SELECT protein_2_function.an, ontologies.child, ontologies.parent\n"
                     "FROM protein_2_function\n"
                     "INNER JOIN functions ON protein_2_function.function=functions.an\n")
    else:
        join_stmt = ("SELECT protein_2_function.an, protein_2_function.function\n"
                     "FROM protein_2_function\n"
                     "INNER JOIN functions ON protein_2_function.function=functions.an\n")

    where_stmt = ("WHERE protein_2_function.an IN({protein_ans_list})\n"
                  "AND functions.type='{function_type}'\n").format(**parameters_dict)

    if function_type in {"GO", "UPK"}:
        extend_stmt = "INNER JOIN ontologies ON ontologies.child=functions.an\n"
        if basic_or_slim == "slim":
            extend_stmt += "INNER JOIN go_2_slim ON go_2_slim.an=functions.an\n"
    else:
        # pass # do something with KEGG
        extend_stmt = ""
    sql_statement = (join_stmt + extend_stmt + where_stmt + ";").replace('"', "'")
    cursor.execute(sql_statement)
    result = cursor.fetchall()

    ##### OG proteins
    join_stmt = ("SELECT protein_2_og.an, og_2_function.function\n"
                 "FROM protein_2_og\n"
                 "INNER JOIN og_2_function ON protein_2_og.og=og_2_function.og\n"
                 "INNER JOIN functions ON og_2_function.function=functions.an\n")

    where_stmt = ("WHERE protein_2_og.an IN({protein_ans_list})\n"
                  "AND functions.type='{function_type}'\n").format(**parameters_dict)

    extend_stmt = ""
    if limit_2_parent is not None:
        extend_stmt += "INNER JOIN ontologies ON ontologies.child=functions.an\n"
        where_stmt += "AND ontologies.parent='{limit_2_parent}'\n".format(**parameters_dict)
    if basic_or_slim == "slim":
        extend_stmt += "INNER JOIN go_2_slim ON go_2_slim.an=functions.an\n"

    sql_statement = (join_stmt + extend_stmt + where_stmt + ";").replace('"', "'")
    cursor.execute(sql_statement)
    result += cursor.fetchall()
    for res in result:
        an = res[0]
        function_ = res[1:]
        if an not in an_2_functions_dict:
            for func in function_:
                an_2_functions_dict[an] = {func}
        else:
            for func in function_:
                an_2_functions_dict[an].update([func])

    if limit_2_parent is not None:
        sql_statement = ("SELECT ontologies.child, ontologies.parent\n"
                         "FROM ontologies\n"
                         "WHERE ontologies.parent='{limit_2_parent}'\n").format(**parameters_dict)
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        limit_2_parent_set = parse_result_child_parent(result)
        for an in an_2_functions_dict:
            an_2_functions_dict[an] = an_2_functions_dict[an].intersection(limit_2_parent_set)
    return an_2_functions_dict

def get_termAN_from_humanName_functionTye(functionType, humanName):
    if humanName is None:
        return ""
    return functionType_term_2_an_dict[functionType][humanName]

def parse_result_child_parent(result):
    return set([item for sublist in result for item in sublist])


if __name__ == "__main__":
    pass
