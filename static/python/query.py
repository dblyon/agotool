from __future__ import print_function
import time, datetime




upkTerm_2_functionAN_dict = {u'Biological process': u'UPK:9999',
                             u'Cellular component': u'UPK:9998',
                             u'Coding sequence diversity': u'UPK:9997',
                             u'Developmental stage': u'UPK:9996',
                             u'Disease': u'UPK:9995',
                             u'Domain': u'UPK:9994',
                             u'Ligand': u'UPK:9993',
                             u'Molecular function': u'UPK:9992',
                             u'Technical term': u'UPK:9990'}

humanName_2_functionAN_dict = {u"BP": u"GO:0008150",
                               u"CP": u"GO:0005575",
                               u"MF": u"GO:0003674",
                               u"Biological Process": u"GO:0008150",
                               u"Cellular Component": u"GO:0005575",
                               u"Molecular Function": u"GO:0003674"}

functionType_term_2_an_dict = {"UPK": upkTerm_2_functionAN_dict,
                               "GO": humanName_2_functionAN_dict}


def get_termAN_from_humanName_functionTye(humanName, functionType):
    if humanName is None:
        return ""
    return functionType_term_2_an_dict[functionType][humanName]


# def get_association_dict(connection, protein_ans_list, function_type, limit_2_parent=None, basic_or_slim="slim"):
def get_association_dict(connection, protein_ans_list, function_type, limit_2_parent=None, basic_or_slim="slim", backtracking=True):
    """
    e.g.
    function_type = "GO"
    limit_2_parent = "Biological process"
    basic_or_slim = "basic"
    assoc_dict = query.get_association_dict(protein_ans_list, function_type, limit_2_parent, basic_or_slim)

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
    :param connection: data base connection object
    :param protein_ans_list: ListOfString (AccessionNumbers of Proteins)
    :param function_type: String (one of "GO", "UPK", "KEGG", "DOM")
    :param limit_2_parent: String (e.g. "BP", "CP", "MF", "Technical term", "Biological process", etc.)
    :param basic_or_slim: String (one of "basic", "slim")
    :param backtracking: Bool
    :return: Dict(key=AN, val=set of String)
    """
    protein_ans_list = str(protein_ans_list)[1:-1]
    an_2_functions_dict = {}
    parameters_dict = {"protein_ans_list": protein_ans_list, "function_type": function_type, "limit_2_parent": get_termAN_from_humanName_functionTye(limit_2_parent, function_type)}

    ##### UniProt proteins
    # join_stmt = ("SELECT protein_2_function.an, protein_2_function.function\n"
    #              "FROM protein_2_function\n"
    #              "INNER JOIN functions ON protein_2_function.function=functions.an\n")

    if function_type != "KEGG":
        if backtracking:
            join_stmt = ("SELECT protein_2_function.an, ontologies.child, ontologies.parent\n"
                         "FROM protein_2_function\n"
                         "INNER JOIN functions ON protein_2_function.function=functions.an\n")
        else:
            join_stmt = ("SELECT protein_2_function.an, protein_2_function.function\n"
                         "FROM protein_2_function\n"
                         "INNER JOIN functions ON protein_2_function.function=functions.an\n")
    else:
        join_stmt = ("SELECT protein_2_function.an, protein_2_function.function\n"
                     "FROM protein_2_function\n"
                     "INNER JOIN functions ON protein_2_function.function=functions.an\n")

    # if backtracking:
    #     join_stmt = ("SELECT protein_2_function.an, protein_2_function.function\n"
    #                  "FROM protein_2_function\n"
    #                  "INNER JOIN functions ON protein_2_function.function=functions.an\n")
    # else:
    #     join_stmt = ("SELECT protein_2_function.an, ontologies.child\n"
    #                  "FROM protein_2_function\n"
    #                  "INNER JOIN functions ON protein_2_function.function=functions.an\n")
    # if function_type == "KEGG":
    #     join_stmt = ("SELECT protein_2_function.an, protein_2_function.function\n"
    #                  "FROM protein_2_function\n"
    #                  "INNER JOIN functions ON protein_2_function.function=functions.an\n")
    # elif function_type == "DOM": only for OG_2_Function #!!!

    where_stmt = ("WHERE protein_2_function.an IN({protein_ans_list})\n"
                  "AND functions.type='{function_type}'\n").format(**parameters_dict)

    # !!! start (do the same for OG proteins)
    # extend_stmt = ""
    # if limit_2_parent is not None:
    #     extend_stmt += "INNER JOIN ontologies ON ontologies.child=functions.an\n"
    #     where_stmt += "AND ontologies.parent='{limit_2_parent}'\n".format(**parameters_dict)
    # if basic_or_slim == "slim":
    #     extend_stmt += "INNER JOIN go_2_slim ON go_2_slim.an=functions.an\n"

    if function_type != "KEGG":
        extend_stmt = "INNER JOIN ontologies ON ontologies.child=functions.an\n"
        if limit_2_parent is not None:
            where_stmt += "AND ontologies.parent='{limit_2_parent}'\n".format(**parameters_dict)
        if basic_or_slim == "slim":
            extend_stmt += "INNER JOIN go_2_slim ON go_2_slim.an=functions.an\n"

    # !!! stop


    sql_statement = (join_stmt + extend_stmt + where_stmt + ";").replace('"', "'")

    # session = connection.get_session()
    session = connection.get_session()
    result = session.execute(sql_statement).fetchall()
    session.close()

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

    # session = connection.get_session()
    session = connection.get_session()
    result += session.execute(sql_statement).fetchall()
    for res in result:
        an = res[0]
        function = res[1:]
        if not an in an_2_functions_dict:
            for func in function:
                an_2_functions_dict[an] = {func}
        else:
            for func in function:
                an_2_functions_dict[an].update([func])

        # an, function = res
        # if not an in an_2_functions_dict:
        #     an_2_functions_dict[an] = {function}
        # else:
        #     an_2_functions_dict[an].update([function])

    session.close()
    return an_2_functions_dict

def print_runtime(start_time):
    print("#" * 80, "\n", "--- runtime: {} ---".format(str(datetime.timedelta(seconds=int(time.time() - start_time)))))

if __name__ == "__main__":
    import db_config
    ECHO = False
    TESTING = False
    DO_LOGGING = False
    connection = db_config.Connect(echo=ECHO, testing=TESTING, do_logging=DO_LOGGING)

    start_time = time.time()
    import pandas as pd
    import tools
    fn = r"/Users/dblyon/CloudStation/CPR/Vikings/Daniel/txt_20160429_redFasta_FDR_matchBR/LFQ_Classic/proteinGroups_LCA.txt"
    df = pd.read_csv(fn, sep='\t')
    protein_ans_list = tools.commaSepCol2uniqueFlatList(df, colname="Majority protein IDs")
    function_type = "GO"
    limit_2_parent = None
    basic_or_slim = "slim" # "basic"
    assoc_dict = get_association_dict(connection, protein_ans_list, function_type, limit_2_parent, basic_or_slim)
    print(len(assoc_dict))
    print_runtime(start_time)
    # print(assoc_dict.items()[:3])


# for HOMD ANs
# given ans_list (proteins)
# query: Protein_2_OG, get OGs from ANs
# query: OG_2_Function, get functions from OGs
# limit by Functions.type
# limit by Ontologies.direct
# limit by GO_2_Slim.slim
# --> join




# for UniProt ANs
# query: Protein_2_Function, from protein_an_list 2 function_list
# limit by Functions.type
# limit by Ontologies.direct
# limit by GO_2_Slim.slim

# protein_ans_list = ["belk_c_455_5138", "P31946"]
# function_type = "GO"
# limit_2_parent = None
# basic_or_slim = "basic"

#SELECT stuff from JOIN ... ON Protein_2_OG.og=OG_2_Function.og WHERE Protein_2_OG in () AND GO_2_Function.function_type='BP';
#(join on OG)

# SELECT * FROM functions INNER JOIN og_2_function ON functions.an = og_2_function.function WHERE functions.type = 'DOM' AND og_2_function.function IN (SELECT function FROM og_2_function WHERE og IN (SELECT og FROM protein_2_og WHERE an IN ('belk_c_455_5138') ) );

#sql_statement = "SELECT function FROM og_2_function WHERE og IN (SELECT og FROM protein_2_og WHERE an IN ('belk_c_455_5138', 'P31946') )"
#sql_statement = "SELECT * FROM functions INNER JOIN og_2_function ON functions.an=og_2_function.function LIMIT 10"

# SELECT an FROM functions WHERE functions.type = 'DOM' AND functions.an IN (SELECT function FROM og_2_function WHERE og IN (SELECT og FROM protein_2_og WHERE an IN ('belk_c_455_5138')));
# SELECT an FROM functions WHERE functions.type = 'DOM' AND functions.an IN (SELECT function FROM og_2_function WHERE og IN (SELECT og FROM protein_2_og WHERE an IN ('belk_c_455_5138'))); --> GOOD ONE, WORKING (use for KEGG or DOM)
# SELECT * FROM functions INNER JOIN go_2_slim ON functions.an=go_2_slim.an WHERE functions.type = 'GO' AND functions.an IN (SELECT function FROM og_2_function WHERE og IN (SELECT og FROM protein_2_og WHERE an IN ('belk_c_455_5138')));



##### Working SQL statements
# protein_ans_list = ["belk_c_455_5138", "P31946"]
# function_type = "GO"
# limit_2_parent = None
# basic_or_slim = "basic"
# sql_statement="SELECT function FROM protein_2_og LEFT JOIN og_2_function ON og_2_function.og=protein_2_og.og WHERE protein_2_og.an IN ({});".format(str(protein_ans_list)[1:-1])
# sql_statement = "SELECT og FROM protein_2_og WHERE an IN ({});".format(str(protein_ans_list)[1:-1])
# sql_statement="SELECT * FROM protein_2_og INNER JOIN og_2_function ON protein_2_og.og = og_2_function.og;" #very slow
# sql_statement="SELECT * FROM protein_2_og INNER JOIN og_2_function ON protein_2_og.og = og_2_function.og WHERE an IN ({});".format(str(protein_ans_list)[1:-1])
# sql_statement="SELECT function FROM protein_2_og INNER JOIN og_2_function ON protein_2_og.og = og_2_function.og WHERE an IN ({});".format(str(protein_ans_list)[1:-1])






## Ontologies
##### Child_2_Parent
# use case #1: given a set of GO-terms limit to GO-category Biological Process without backtracking
# Version A:
# SELECT child FROM ontology WHERE child IN ({set of GO-terms}) AND WHERE parent = 'GO:0008150' --> category BP without backtracking
# -->
# | GO:0032259 | GO:0008150 | False |
#
# Version B:
# Select parent category
# | GO:0008152 | GO:0008150 | True |
# | GO:0032259 | GO:0008150 | False |
# from that selection
# select children based on given set
# | GO:0032259 | GO:0008150 | False |
#
#
# use case #2: given a set of GO-terms limit to GO-category Biological Process with backtracking
# version A:
# SELECT child FROM ontology WHERE parent = 'GO:0008150' INNER JOIN ON parent WITH (SELECT * FROM ontology WHERE child IN ({set of GO-terms}))
# | GO:0008152 | GO:0008150 | True |
# | GO:0032259 | GO:0008150 | False |
# JOIN
# | GO:0032259 | GO:0008152 | True |
# | GO:0032259 | GO:0008150 | False |
# -->
# | GO:0008152 | GO:0008150 | True |
# | GO:0032259 | GO:0008150 | False |
#
# Version B:
# SELECT all children of with condition: subset of terms of category parent
# | GO:0032259 | GO:0008150 | False |
# --> GO:0032259
# select children and parent terms where previous selection in child column
# -->
# | GO:0032259 | GO:0008152 | True |
# | GO:0032259 | GO:0008150 | False |
