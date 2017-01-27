from subprocess import call
from collections import defaultdict

def get_TOC_2_markdown_file(fn_md):
    toc = ""
    counter = 1
    with open(fn_md, "r") as fh_in:
        for line in fh_in:
            if line.startswith("## "):
                line = line.strip()
                line2add = str(counter) + ". [" + line.replace("#", "").strip() + "]" + "(#" + "-".join(line.lower().replace("#", "").strip().split()) + ")\n"
                toc += line2add
                counter += 1
    return toc

def write_TOC_2_file(fn_md, fn_out=None):
    """
    import tools
    fn = r"/Users/dblyon/modules/cpr/metaprot/DataBase_Schema.md"
    tools.write_TOC_2_file(fn)
    """
    toc = get_TOC_2_markdown_file(fn_md)
    with open(fn_md, "r") as fh_in:
        lines = fh_in.readlines()
    if not fn_out:
        fn_out = fn_md
    with open(fn_out, "w") as fh_out:
        fh_out.write(toc)
        for line in lines:
            fh_out.write(line)

def cut_tag_from_html(html_text, tag="style"):
    start_index = html_text.index("<{}>".format(tag))
    stop_index = html_text.index("</{}>".format(tag)) + len("</{}>".format(tag))
    html_tag = html_text[start_index:stop_index]
    html_rest = html_text[:start_index] + html_text[stop_index:]
    return html_tag, html_rest

def update_db_schema(FN_DATABASE_SCHEMA, FN_DATABASE_SCHEMA_WITH_LINKS):
    write_TOC_2_file(FN_DATABASE_SCHEMA, FN_DATABASE_SCHEMA_WITH_LINKS)
    # shutil.copyfile(FN_DATABASE_SCHEMA, FN_DATABASE_SCHEMA_WITH_LINKS)
    # write_TOC_2_file(FN_DATABASE_SCHEMA_WITH_LINKS)
    shellcmd = "grip {} --export --title='Data Base Schema'".format(FN_DATABASE_SCHEMA_WITH_LINKS)
    call(shellcmd, shell=True)
    with open(FN_DATABASE_SCHEMA_WITH_LINKS.replace(".md", ".html"), "r") as fh:
        content = fh.read()
    style_2_prepend, content = cut_tag_from_html(content, tag="style")
    text_before = r'''{% extends "layout.html" %}
        {% block head %}
        <script type="text/javascript">$(document).ready( function() {enrichment_page();});</script>
        {% endblock head %}
        {% block content %}
        <div class="container-fluid">'''
    text_after = r'''</div>
                    {% endblock content %}'''
    with open(FN_DATABASE_SCHEMA_WITH_LINKS.replace(".md", ".html"), "w") as fh:
        fh.write(style_2_prepend + "\n")
        fh.write(text_before)
        fh.write(content)
        fh.write(text_after)

def split_string_or_nan(string_or_nan, sep=";"):
    try:
        ans = string_or_nan.split(sep)
    except AttributeError: # if nan
        ans = []
    return ans

def commaSepCol2uniqueFlatList(df, colname, sep=";", unique=True):
    series_of_lists = df[colname].apply(split_string_or_nan, 1, args=(sep,))
    nested_list = series_of_lists.tolist()
    flat_list = [item for sublist in nested_list for item in sublist]
    if not unique:
        return sorted(flat_list)
    else:
        return sorted(set(flat_list))

def convert_assoc_dict_2_proteinGroupsAssocDict(assoc_dict, proteinGroups_list):
    """
    proteinGroups_list = ['A;B;C']
    assoc_dict = {'A': set(["a", "b", "c", "d"]),
    'B': set(["a", "b", "c"]),
    'C': set(["a", "b", "d"])}
    create a consensus association dictionary.
    If 50% or more GOterms are associated with each AN within proteinGroup --> keep, else discard
    :param assoc_dict: Dict(key: String(UniProt-AccessionNumber), val:SetOfString(e.g.GOterms))
    :param proteinGroups_list: ListOfString
    :return: Dict(String(UniProt-AccessionNumbers comma separated), val:SetOfString(e.g.GOterms))
    """
    assoc_dict_pg = {}
    for proteinGroup in proteinGroups_list:
        nested_associations = []
        for an in proteinGroup.split(";"):
            nested_associations.append(list(assoc_dict[an]))
        number_of_lists = len(nested_associations)
        flat_list = [item for sublist in nested_associations for item in sublist]
        consensus_associations = set()
        for goterm in set(flat_list):
            if flat_list.count(goterm) >= (number_of_lists / 2.0):
                consensus_associations.update([goterm])
        assoc_dict_pg[proteinGroup] = consensus_associations
    return assoc_dict_pg

######### DB part


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

def get_termAN_from_humanName_functionTye(functionType, humanName):
    if humanName is None:
        return ""
    return functionType_term_2_an_dict[functionType][humanName]

def map_secondary_2_primary_ANs(connection, ans_list):
    """
    e.g.
    import db_config, query
    ECHO = False
    TESTING = False
    DO_LOGGING = False
    connection = db_config.Connect(echo=ECHO, testing=TESTING, do_logging=DO_LOGGING)
    ans_list = ["A0A021WW06", "A0A022PF25"]
    query.map_secondary_2_primary_ANs(connection, ans_list)

    map secondary UniProt ANs to primary ANs,
    AN only in dict if mapping exists
    :param connection: data base connection object
    :param ans_list: ListOfString
    :return: Dict (key: String(Secondary AN), val: String(Primary AN))
    """
    ans_list = str(ans_list)[1:-1]
    sql_statement = "SELECT protein_secondary_2_primary_an.sec, protein_secondary_2_primary_an.pri FROM protein_secondary_2_primary_an WHERE protein_secondary_2_primary_an.sec IN({})".format(ans_list)
    session = connection.get_session()
    result = session.execute(sql_statement).fetchall()
    session.close()
    secondary_2_primary_dict = {}
    for res in result:
        secondary = str(res[0])
        primary = str(res[1:][0])
        secondary_2_primary_dict[secondary] = primary
    return secondary_2_primary_dict

def parse_result_child_parent(result):
    return set([item for sublist in result for item in sublist])

def get_association_dict(connection, protein_ans_list, function_type, limit_2_parent=None, basic_or_slim="slim", backtracking=True):
    """
    # def get_association_dict(connection, protein_ans_list, function_type, limit_2_parent=None, basic_or_slim="slim"):
    e.g.
    function_type = "GO"
    limit_2_parent = u"Biological Process"
    basic_or_slim = "basic"
    protein_ans_list = ['Q9XC60', 'P40417']
    assoc_dict = query.get_association_dict(connection, protein_ans_list, function_type, limit_2_parent, basic_or_slim)

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
    session = connection.get_session()
    # print(sql_statement)
    result = session.execute(sql_statement).fetchall()
    session.close() #!!! test if you need to close, performance

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
    session = connection.get_session()
    result += session.execute(sql_statement).fetchall()
    for res in result:
        an = res[0]
        function = res[1:]
        if an not in an_2_functions_dict:
            for func in function:
                an_2_functions_dict[an] = {func}
        else:
            for func in function:
                an_2_functions_dict[an].update([func])

    if limit_2_parent is not None:
        sql_statement = ("SELECT ontologies.child, ontologies.parent\n"
                         "FROM ontologies\n"
                         "WHERE ontologies.parent='{limit_2_parent}'\n").format(**parameters_dict)
        session = connection.get_session()
        limit_2_parent_set = parse_result_child_parent(session.execute(sql_statement).fetchall())
        for an in an_2_functions_dict:
            an_2_functions_dict[an] = an_2_functions_dict[an].intersection(limit_2_parent_set)

    session.close()
    return an_2_functions_dict




