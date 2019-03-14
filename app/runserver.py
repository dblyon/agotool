import os, sys, logging, time
from collections import defaultdict
import numpy as np
from lxml import etree
import flask
from flask import render_template, request, send_from_directory, jsonify
from flask_restful import reqparse, Api, Resource
from werkzeug.wrappers import Response
import wtforms
from wtforms import fields
import markdown
from flaskext.markdown import Markdown
sys.path.insert(0, os.path.abspath(os.path.realpath('./python')))
import query, userinput, run, variables, cluster_filter # todo remove cluster_filter
# from profilehooks import profile
###############################################################################
variables.makedirs_()
EXAMPLE_FOLDER = variables.EXAMPLE_FOLDER
SESSION_FOLDER_ABSOLUTE = variables.SESSION_FOLDER_ABSOLUTE
SESSION_FOLDER_RELATIVE = variables.SESSION_FOLDER_RELATIVE
TEMPLATES_FOLDER_ABSOLUTE = variables.TEMPLATES_FOLDER_ABSOLUTE
DOWNLOADS_DIR = variables.DOWNLOADS_DIR
LOG_FN_WARNINGS_ERRORS = variables.LOG_FN_WARNINGS_ERRORS
LOG_FN_ACTIVITY = variables.LOG_FN_ACTIVITY
FN_KEYWORDS = variables.FN_KEYWORDS
FN_GO_SLIM = variables.FN_GO_SLIM
FN_GO_BASIC = variables.FN_GO_BASIC
DEBUG = variables.DEBUG
PRELOAD = variables.PRELOAD
PROFILING = variables.PROFILING
MAX_TIMEOUT = variables.MAX_TIMEOUT # Maximum Time for MCL clustering
functionType_2_entityType_dict = variables.functionType_2_entityType_dict
###############################################################################
# ToDo 2018
# - debug cython filter_parents (cf. old to new version without filter_parents) --> done
# - buy goliath domain?
# - use cProfile on compiled cython --> done but not that great to inspect
# - replace bool array with uint8 array and casting to bool & using prange with nogil
# - reimplement "limit_2_entity_type"

# go_slim_or_basic --> filter for slim terms
# check out DF sorting before returning results, year and FDR not sorted correctly
# - consistency with single and double quotes
# - return unused identifiers
# - adapt functions_table_STRING.txt:
#      GO name from OBO as definition
# - multiple entity type results to be displayed
# - debug copy&paste fields
# - debug file upload field
# - replace example file
# - make KEGG private --> done
# - http://geneontology.org/page/download-ontology --> slim set for Metagenomics --> offer various kinds of slim sets?
# - update "info_check_input.html" with REST API usage infos
# - offer option to omit testing GO-terms with few associations (e.g. 10)
# - offer to user Pax-DB background proteomes
# - offer example to be set automatically
# - graphical output of enrichment
# - update bootstrap version
# - update documentation specifically about foreground and background
# ? - background proteome with protein groups --> does it get mapped to single protein in foreground ?
# ? - protein-groups: is there different functional information for isoforms
###############################################################################
###############################################################################
def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]
###############################################################################
### Create the Flask application
app = flask.Flask(__name__, template_folder=TEMPLATES_FOLDER_ABSOLUTE)
Markdown(app)

if PROFILING:
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.config['PROFILE'] = True
    # app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[50]) # to view profiled code in shell
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir=variables.DATA_DIR) # use qcachegrind to visualize
    ## iterm: "qcachegrind"
    ## source activate agotool
    ## pyprof2calltree -i somethingsomething.prof -o something.prof
    ## open "something.prof" with qcachegrind -o something.prof

app.config['EXAMPLE_FOLDER'] = EXAMPLE_FOLDER
app.config['SESSION_FOLDER'] = SESSION_FOLDER_ABSOLUTE
ALLOWED_EXTENSIONS = {'txt', 'tsv'}
app.config['MAX_CONTENT_LENGTH'] = 100 * 2 ** 20 #* 100

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

if not app.debug:
    #########################
    # log warnings and errors
    from logging import FileHandler
    file_handler = FileHandler(LOG_FN_WARNINGS_ERRORS, mode="a", encoding="UTF-8")
    file_handler.setFormatter(logging.Formatter("#"*80 + "\n" + '%(asctime)s %(levelname)s: %(message)s'))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    #########################
    # log activity
    log_activity_fh = open(LOG_FN_ACTIVITY, "a")

def log_activity(string2log):
    string2log_prefix = "\n" + "Current date & time " + time.strftime("%c") + "\n"
    string2log = string2log_prefix + string2log
    log_activity_fh.write(string2log)
    log_activity_fh.flush()


################################################################################
# pre-load objects
################################################################################
if PRELOAD:
    if variables.VERSION_ == "aGOtool":
        pqo = query.PersistentQueryObject()
    elif variables.VERSION_ == "STRING":
        pqo = query.PersistentQueryObject_STRING()
    else:
        print("VERSION_ {} not implemented".format(variables.VERSION_))
        raise NotImplementedError

    #filter_ = cluster_filter.Filter(pqo.go_dag, pqo.upk_dag)

### from http://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
### API
api = Api(app)
parser = reqparse.RequestParser()

################################################################################
# celery = tasks.celery
# print("no async", tasks.add_together(1111, 8))
# res = tasks.add_together.delay(2222, 8)
# print("async", res.get())

################################################################################

################################################################################
### STRING arguments/parameters
parser.add_argument("taxid", type=int,
    help="NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms).",
    default=None)

parser.add_argument("species", type=int,
    help="deprecated please use 'taxid' instead, NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms).",
    default=None)

parser.add_argument("organism", type=int,
    help="deprecated please use 'taxid' instead, NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms).",
    default=None)

parser.add_argument("output_format", type=str,
    help="The desired format of the output, one of {tsv, tsv-no-header, json, xml}",
    default="tsv")

parser.add_argument("filter_parents", type=str,
    help="Remove parent terms (keep GO terms and UniProt Keywords of lowest leaf) if they are associated with exactly the same foreground.",
    default="True")

parser.add_argument("filter_foreground_count_one", type=str,
    help="Keep only those terms with foreground_count > 1",
    default="True")

parser.add_argument("LOW_MEMORY", type=str, default="True")
parser.add_argument("filter_PMID_top_n", type=int, default=100, help="Filter the top n PMIDs (e.g. 100, default=100), sorting by low p-value and recent publication date.")
parser.add_argument("caller_identity", type=str,
    help="Your identifier for us e.g. www.my_awesome_app.com",
    default=None) # ? do I need default value ?

parser.add_argument("FDR_cutoff", type=float,
    help="False Discovery Rate cutoff (threshold for multiple testing corrected p-values) e.g. 0.05, default=0.05 meaning 5%. Set to 1 for no cutoff.",
    default=0.05)

# parser.add_argument("filter_PMID", type=float,
#     help="Filter the top n PMID (PubMed IDs) sorted by lowest FDR and newest publication date; e.g. 100, default=100.",
#     default=100)

parser.add_argument("limit_2_entity_type", type=str,
    help="Limit the enrichment analysis to a specific or multiple entity types, e.g. '-21' (for GO molecular function) or '-21;-22;-23;-51' (for all GO terms as well as UniProt Keywords",
    default="-21;-22;-23;-51;-52;-53;-54;-55;-56;-57")

parser.add_argument("privileged", type=str,
    default="False")

################################################################################
### aGOtool arguments/parameters
parser.add_argument("foreground", type=str,
    help="ENSP identifiers for all proteins in the test group (the foreground, the sample, the group you want to examine for GO term enrichment) "
         "separate the list of Accession Number using '%0d' e.g. '4932.YAR019C%0d4932.YFR028C%0d4932.YGR092W'",
    default=None)

parser.add_argument("background", type=str,
    help="ENSP identifiers for all proteins in the background (the population, the group you want to compare your foreground to) "
         "separate the list of Accession Number using '%0d'e.g. '4932.YAR019C%0d4932.YFR028C%0d4932.YGR092W'",
    default=None)

parser.add_argument("background_intensity", type=str,
    help="Protein abundance (intensity) for all proteins (copy number, iBAQ, or any other measure of abundance). "
         "Separate the list using '%0d'. The number of items should correspond to the number of Accession Numbers of the 'background'"
         "e.g. '12.3%0d3.4' ",
    default=None)

parser.add_argument("population", type=str,
    help="ENSP identifiers for all proteins detected in both conditions."
         "separate the list of Accession Number using '%0d' e.g. '4932.YAR019C%0d4932.YFR028C%0d4932.YGR092W'",
    default=None)

parser.add_argument("abundance_ratio", type=str,
    help="Fold change, log fold change, ratio, or something similar reflecting abundance or intensity changes between 2 conditions. Values for all proteins identifiers"
         "Separate the list using '%0d'. The number of items should correspond to the number of Accession Numbers of the 'foreground'"
         "e.g. '-1.2%0d4.3%0d1.2' ",
    default=None)

parser.add_argument("compare_2_ratios_only", type=str,
    help="If true: compare to the user provided abundance ratios only. Else: compare to all functional associations.",
    default="True")

parser.add_argument("enrichment_method", type=str,
    help="""'genome': provided foreground vs genome;
    'compare_samples': Foreground vs Background (no abundance correction); 
    'characterize_foreground': list all functional annotations for provided foreground;
    'abundance_correction': Foreground vs Background abundance corrected;
    'compare_groups': Foreground(replicates) vs Background(replicates), --> foreground_n and background_n need to be set; 
    'rank_enrichment': Fold change, log fold change, ratio, or something similar reflecting abundance or intensity changes between 2 conditions. Values for all proteins identifiers.""",
    default="characterize_foreground")

parser.add_argument("foreground_n", type=int,
    help="Foreground_n is an integer, defines the number of sample of the foreground.",
    default=10)

parser.add_argument("background_n", type=int,
    help="Background_n is an integer, defines the number of sample of the background.",
    default=10)

parser.add_argument("go_slim_or_basic", type=str,
    help="GO basic or slim {basic, slim}. Choose between the full Gene Ontology or GO slim subset a subset of GO terms that are less fine grained.",
    default="basic")

parser.add_argument("indent", type=str,
    help="Prepend level of hierarchy by dots. Add dots to GO-terms to indicate the level in the parental hierarchy (e.g. '...GO:0051204' vs 'GO:0051204')",
    default="False") # should be boolean, but this works better

parser.add_argument("multitest_method", type=str,
    help="Method for correction of multiple testing one of {benjamini_hochberg, sidak, holm, bonferroni}. Select a method for multiple testing correction.",
    default="benjamini_hochberg")

parser.add_argument("alpha", type=float,
    help="""Variable used for "Holm" or "Sidak" method for multiple testing correction of p-values.""",
    default=0.05)

parser.add_argument("o_or_u_or_both", type=str,
    help="over- or under-represented or both, one of {overrepresented, underrepresented, both}. Choose to only test and report overrepresented or underrepresented GO-terms, or to report both of them.",
    default="overrepresented")

parser.add_argument("num_bins", type=int,
    help="The number of bins created based on the abundance values provided. Only relevant if 'Abundance correction' is selected.",
    default=100)

parser.add_argument("fold_enrichment_for2background", type=float,
    help="Apply a filter for the minimum threshold value of fold enrichment foreground/background.",
    default=0)

parser.add_argument("p_value_uncorrected", type=float,
    help="Apply a filter (value between 0 and 1) for maximum threshold value of the uncorrected p-value.",
    default=0)


class API_STRING(Resource):
    """
    get enrichment for all available functional associations not 'just' one category
    """

    def get(self): #, output_format="json"):
        return self.post() #output_format)

    def post(self):
        return self.post()

    # @profile
    def post(self): #, output_format="json"):
        """
        watch out for difference between passing parameter through
        - part of the path (url) is variable in resource
        - or parameters of form
        """
        args_dict = defaultdict(lambda: None)
        args_dict["foreground"] = request.form.get("foreground")
        args_dict["output_format"] = request.form.get("output_format")
        args_dict["enrichment_method"] = request.form.get("enrichment_method")
        args_dict["taxid"] = request.form.get("taxid")
        args_dict.update(parser.parse_args())
        args_dict["indent"] = string_2_bool(args_dict["indent"])
        args_dict["privileged"] = string_2_bool(args_dict["privileged"])
        args_dict["filter_parents"] = string_2_bool(args_dict["filter_parents"])
        args_dict["filter_foreground_count_one"] = string_2_bool(args_dict["filter_foreground_count_one"])
        args_dict["LOW_MEMORY"] = string_2_bool(args_dict["LOW_MEMORY"])
        FDR_cutoff = args_dict["FDR_cutoff"]
        args_dict["compare_2_ratios_only"] = string_2_bool(args_dict["compare_2_ratios_only"])
        filter_PMID_top_n = args_dict["filter_PMID_top_n"]
        if FDR_cutoff == 0 or FDR_cutoff >= 1:
            args_dict["FDR_cutoff"] = None
        if filter_PMID_top_n == 0:
            args_dict["filter_PMID_top_n"] = None
        if variables.VERBOSE:
            print("-"*80)
            for key, val in sorted(args_dict.items()):
                print(key, val)
            print("-"*80)
        ui = userinput.REST_API_input(pqo, args_dict)
        if not ui.check:
            args_dict["ERROR_UserInput"] = "ERROR_UserInput: Something went wrong parsing your input, please check your input and/or compare it to the examples."
            return help_page(args_dict)

        if args_dict["enrichment_method"] == "genome":
            background_n = pqo.get_proteome_count_from_taxid(args_dict["taxid"])
            if not background_n:
                args_dict["ERROR_taxid"] = "ERROR_taxid: 'taxid': {} does not exist in the data base, thus enrichment_method 'genome' can't be run, change the species (TaxID) or use 'compare_samples' method instead, which means you have to provide your own background ENSPs".format(args_dict["taxid"])
                return help_page(args_dict)
            ### results are tsv or json
            results_all_function_types = run.run_STRING_enrichment_genome(pqo, ui, background_n, args_dict)

        elif args_dict["enrichment_method"] == "rank_enrichment":
            print("returning help page")
            # results_all_function_types = run.run_rank_enrichment(pqo, ui, args_dict)
            args_dict["ERROR_NotImplementedError"] = "This method is not yet implented (again)"
            return help_page(args_dict)
        else:
            results_all_function_types = run.run_STRING_enrichment(pqo, ui, args_dict)

        if results_all_function_types is False:
            print("returning help page")
            return help_page(args_dict)
        else:
            return format_multiple_results(args_dict, results_all_function_types, pqo)


api.add_resource(API_STRING, "/api", "/api_string", "/api_string/<output_format>", "/api_string/<output_format>/enrichment")


def PMID_description_to_year(string_):
    try:
        return int(string_[1:5])
    except ValueError or IndexError:
        return np.nan

def create_xml_tree(header, rows):
    xml_tree = etree.Element("EnrichmentResult")
    header = header.split("\t")
    for row in rows:
        child = etree.SubElement(xml_tree, "record")
        for tag_content in zip(header, row.split("\t")):
            tag, content = tag_content
            etree.SubElement(child, tag).text = content
    return etree.tostring(xml_tree, pretty_print=True, xml_declaration=True, encoding="utf-8")#.decode("UTF-8")

def check_all_ENSPs_of_given_taxid(protein_ans_list, taxid):
    taxid_string = str(taxid)
    for an in protein_ans_list:
        if not an.startswith(taxid_string):
            return False
    return True

def check_taxids(args_dict):
    taxid = args_dict["taxid"]
    if taxid is not None:
        return taxid
    taxid = args_dict["species"]
    if taxid is not None:
        args_dict["ERROR_species"] = "ERROR_species: argument 'species' is deprecated, please use 'taxid' instead. You've provided is '{}'.".format(args_dict["species"])
        return False
    taxid = args_dict["organism"]
    if taxid is not None:
        args_dict["ERROR_organism"] = "ERROR_organism: argument 'organism' is deprecated, please use 'taxid' instead. You've provided is '{}'.".format(args_dict["organism"])
        return False

def get_function_type__and__limit_2_parent(gocat_upk):
    """
    # choices = (("all_GO", "all GO categories"),
    #            ("BP", "GO Biological Process"),
    #            ("CP", "GO Celluar Compartment"),
    #            ("MF", "GO Molecular Function"),
    #            ("UPK", "UniProt keywords"),
    #            ("KEGG", "KEGG pathways")),
    :param gocat_upk: String
    :return: Tuple(String, Bool)
    """
    if gocat_upk in {"BP", "CP", "MF", "all_GO"}:
        return "GO" #, gocat_upk
    else:
        return gocat_upk #, None

def write2file(fn, tsv):
    with open(fn, 'w') as f:
        f.write(tsv)


class API_STRING_HELP(Resource):
    """
    get enrichment for all available functional associations not 'just' one category
    """

    def get(self, output_format="json"):
        args_dict = defaultdict(lambda: None)
        args_dict.update(parser.parse_args())
        args_dict = parser.parse_args()
        args_dict["1_INFO"] = "INFO: default values are are shown unless you've provided arguments"
        args_dict["2_INFO_Name_2_EntityType"] = variables.functionType_2_entityType_dict
        args_dict["3_INFO_limit_2_entity_type"] = "comma separate desired entity_types e.g. '-21;-51;-52' (for GO biological process; UniProt keyword; SMART), default get all available."
        return help_page(args_dict)

    def post(self, output_format="json"):
        return self.get(output_format)

api.add_resource(API_STRING_HELP, "/api_help", "/api_string_help")


def string_2_bool(string_):
    string_ = string_.strip().lower()
    if string_.lower() == "true" or string_ == "1":
        return True
    elif string_.lower() == "false" or string_ == "0":
        return False
    else:
        raise NotImplementedError

def help_page(args_dict):
    try:
        del args_dict["privileged"]
    except KeyError:
        pass
    return jsonify(args_dict)

def format_multiple_results(args_dict, results_all_entity_types, pqo):
    output_format = args_dict["output_format"]
    if output_format in {"tsv", "tsv_no_header", "tsv-no-header"}:
        # print("format_multiple_results", type(results_all_entity_types))
        return Response(results_all_entity_types, mimetype='text')
    elif output_format == "json":
        return jsonify(results_all_entity_types)
    elif output_format == "xml":
        dict_2_return = {}
        for etype, results in results_all_entity_types.items():
            results = results.to_csv(sep="\t", header=True, index=False) # convert DatFrame to string
            header, rows = results.split("\n", 1) # is df in tsv format
            xml_string = create_xml_tree(header, rows.split("\n"))
            dict_2_return[etype] = xml_string.decode()
        return jsonify(dict_2_return)
    else:
        raise NotImplementedError


################################################################################
# index.html
################################################################################
@app.route('/index')
def index():
    return render_template('index.html')

################################################################################
# about.html
################################################################################
@app.route('/about')
def about():
    return render_template('about.html')

################################################################################
# parameters.html
################################################################################
@app.route('/parameters')
def parameters():
    return render_template('parameters.html')

################################################################################
# results_zero.html
################################################################################
@app.route('/results_zero')
def gotupk_results_zero():
    return render_template('results_zero.html')

################################################################################
# page_not_found.html
################################################################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404

################################################################################
# example.html
################################################################################
@app.route('/example')
def example():
    with open(variables.FN_HELP_ENTITY_TYPES, "r") as fh:
        content = fh.read()
        # content = markdown.markdown(content, extensions=['extra', 'smarty'], output_format='html5')
        # content_entity_types = content.replace(r"<table>", r'<table id="table_id" class="table table-striped hover">').replace("<thead>", '<thead class="table_header">').replace("{", "\{").replace("}", "\}")
        content_entity_types = format_markdown(content)
        # print(content_entity_types)
    with open(variables.FN_HELP_PARAMETERS, "r") as fh:
        content = fh.read()
        # content = markdown.markdown(content, extensions=['extra', 'smarty'], output_format='html5')
        # content_parameters = content.replace(r"<table>", r'<table id="table_id" class="table table-striped hover">').replace("<thead>", '<thead class="table_header">').replace("{", "\{").replace("}", "\}")
        content_parameters = format_markdown(content)
        # print(content_parameters)
    return render_template('example.html', **locals())

@app.route('/example/<path:filename>', methods=['GET', 'POST'])
def download_example_data(filename):
    uploads = app.config['EXAMPLE_FOLDER']
    return send_from_directory(directory=uploads, filename=filename)

@app.route('/results/<path:filename>', methods=['GET', 'POST'])
def download_results_data(filename):
    uploads = app.config['SESSION_FOLDER']
    return send_from_directory(directory=uploads, filename=filename)

################################################################################
# db_schema.html
################################################################################
@app.route("/db_schema")
def db_schema():
    with open(variables.FN_DATABASE_SCHEMA, "r") as fh:
        content = fh.read()
    # content = content.replace("{", "\{").replace("}", "\}")
    # content = markdown.markdown(content, extensions=['extra', 'smarty'], output_format='html5')
    # content = content.replace(r"<table>", r'<table id="table_id" class="table table-striped hover">').replace("<thead>", '<thead class="table_header">').replace("{", "\{").replace("}", "\}")
    content = format_markdown(content)
    return render_template("db_schema.html", **locals())

################################################################################
# FAQ.html
################################################################################
@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

################################################################################
# helper functions
################################################################################
def format_markdown(content):
    content = content.replace("{", "\{").replace("}", "\}")
    content = markdown.markdown(content, extensions=['extra', 'smarty'], output_format='html5')
    return content.replace(r"<table>", r'<table id="table_id" class="table table-striped hover">').replace("<thead>", '<thead class="table_header">')

##### validation of user inputs
def validate_float_larger_zero_smaller_one(form, field):
    if not 0 < field.data < 1:
        raise wtforms.ValidationError(" number must be: 0 < number < 1")

def validate_float_between_zero_and_one(form, field):
    if not 0 <= field.data <= 1:
        raise wtforms.ValidationError(" number must be: 0 <= number <= 1")

def validate_integer(form, field):
    if not isinstance(field.data, int):
        raise wtforms.ValidationError()

def validate_number(form, field):
    if not isinstance(field.data, (int, float)):
        raise wtforms.ValidationError("")

def validate_inflation_factor(form, field):
    if not field.data >= 1.0:
        raise wtforms.ValidationError(" number must be larger than 1")

def generate_session_id():
    pid = str(os.getpid())
    time_ = str(time.time())
    return "_" + pid + "_" + time_

def read_results_file(fn):
    """
    :return: Tuple(header=String, results=ListOfString)
    """
    with open(fn, 'r') as fh:
        lines_split = [ele.strip() for ele in fh.readlines()]
    return lines_split[0], lines_split[1:]

def elipsis(header):
    try:
        ans_index = header.index("ANs_foreground")
    except ValueError:
        ans_index = header.index("ANs_background")
        # let flask throw an internal server error
    try:
        description_index = header.index("description")
        ellipsis_indices=(description_index, ans_index)
    except ValueError:
        ellipsis_indices = (ans_index,)
    return ellipsis_indices

################################################################################
# enrichment.html
################################################################################
class Enrichment_Form(wtforms.Form):
    userinput_file = fields.FileField("Choose File",
                                      description="""Expects a tab-delimited text-file ('.txt' or '.tsv') with the following 3 column-headers:

'background': STRING identifiers (such as '511145.b1260') for all proteins

'background_intensity': Protein abundance (intensity) for all proteins (copy number, iBAQ, or any other measure of abundance)

'foreground': STRING identifiers for all proteins in the test group (the group you want to examine for GO term enrichment,
these identifiers should also be present in the 'background_an' as the test group is a subset of the background)

If "Abundance correction" is deselected "background_int" can be omitted.""")

    foreground_textarea = fields.TextAreaField("Foreground")
    background_textarea = fields.TextAreaField("Background & Intensity")
    limit_2_entity_type = fields.SelectField("GO terms, UniProt keywords, or KEGG pathways",
                                   choices = (("-51", "UniProt keywords"),
                                              ("-21;-22;-23", "all GO categories"),
                                              ("-21", "GO Biological Process"),
                                              ("-22", "GO Celluar Compartment"),
                                              ("-23", "GO Molecular Function"),
                                              ("-52", "KEGG pathways"),
                                              ("-53", "SMART domains"),
                                              ("-54", "InterPro domains"),
                                              ("-55", "PFAM domains"),
                                              ("-56", "PMID (PubMed IDs"),
                                              ("-57", "Reactome"),
                                              ("-21;-22;-23;-51;-52;-53;-54;-55;-56;-57", "All available")),
                                   description="""Select either one or all three GO categories (molecular function, biological process, cellular component), UniProt keywords, or KEGG pathways.""")
    enrichment_method = fields.SelectField("Select one of the following methods",
                                   choices = (("genome", "genome"),
                                              ("abundance_correction", "abundance_correction"),
                                              ("compare_samples", "compare_samples"),
                                              ("compare_groups", "compare_groups"),
                                              ("characterize_foreground", "characterize_foreground")),
                                   description="""abundance_correction: Foreground vs Background abundance corrected
compare_samples: Foreground vs Background (no abundance correction)
compare_groups: Foreground(replicates) vs Background(replicates), --> foreground_n and background_n need to be set
characterize_foreground: Foreground only""")
    foreground_n = fields.IntegerField("Foreground_n", [validate_integer], default=10, description="""Foreground_n is an integer, defines the number of sample of the foreground.""")
    background_n = fields.IntegerField("Background_n", [validate_integer], default=10, description="""Background_n is an integer, defines the number of sample of the background.""")
    abcorr = fields.BooleanField("Abundance correction",
                                 default = "checked",
                                 description="""Apply the abundance correction as described in the background. A column named "background_intensity" (background intensity)
that corresponds to the column "population_an" (background accession number) needs to be provided, when selecting this option.
If "Abundance correction" is deselected "background_intensity" can be omitted.""")
    go_slim_or_basic = fields.SelectField("GO basic or slim",
                                          choices = (("basic", "basic"), ("slim", "slim")),
                                          description="""Choose between the full Gene Ontology or GO slim subset a subset of GO terms that are less fine grained.""")
    indent = fields.BooleanField("prepend level of hierarchy by dots",
                                 default="checked",
                                 description="Add dots to GO-terms to indicate the level in the parental hierarchy (e.g. '...GO:0051204' vs 'GO:0051204'")
    multitest_method = fields.SelectField(
        "Method for correction of multiple testing",
        choices = (("benjamini_hochberg", "Benjamini Hochberg"),
                   ("sidak", "Sidak"), ("holm", "Holm"),
                   ("bonferroni", "Bonferroni")),
        description="""Select a method for multiple testing correction.""")
    alpha = fields.FloatField("Alpha", [validate_float_larger_zero_smaller_one],
                              default = 0.05, description="""Variable used for "Holm" or "Sidak" method for multiple testing correction of p-values.""")
    o_or_u_or_both = fields.SelectField("over- or under-represented or both",
                                        choices = (("overrepresented", "overrepresented"),
                                                   ("underrepresented", "underrepresented"),
                                                   ("both", "both")),
                                        description="""Choose to only test and report overrepresented or underrepresented GO-terms, or to report both of them.""")
    num_bins = fields.IntegerField("Number of bins",
                                   [validate_integer],
                                   default = 100,
                                   description="""The number of bins created based on the abundance values provided. Only relevant if "Abundance correction" is selected.""")
    fold_enrichment_for2background = fields.FloatField(
        "fold enrichment foreground/background",
        [validate_number], default = 0,
        description="""Minimum threshold value of "fold_enrichment_foreground_2_background".""")
    p_value_uncorrected =  fields.FloatField(
        "p-value uncorrected",
        [validate_float_between_zero_and_one],
        default = 0,
        description="""Maximum threshold value of "p_uncorrected".""")
    FDR_cutoff =  fields.FloatField(
        "FDR-cutoff (multiple testing corrected p-values)",
        [validate_float_between_zero_and_one],
        default = 0,
        description="""Maximum FDR (for Benjamini-Hochberg) or p-values-corrected threshold value (default=0 meaning no cutoff)""")

@app.route('/')
def enrichment():
    return render_template('enrichment.html', form=Enrichment_Form())

################################################################################
# results.html
################################################################################
class Results_Form(wtforms.Form):
    inflation_factor = fields.FloatField("inflation factor", [validate_inflation_factor],
                                         default = 2.0, description="""Enter a number higher than 1.
Usually a number between 1.1 and 10 is chosen.
Increasing the value will increase cluster granularity (produce more clusters).
Certain combinations of data and inflation factor can take very long to process. Please be patient.""")

@app.route('/results', methods=["GET", "POST"])
def results():
    """
    cluster_list: nested ListOfString corresponding to indices of results
    results_filtered = filter(header, results, indent)
    results_filtered: reduced version of results
    """
    form = Enrichment_Form(request.form)
    if request.method == 'POST': # ToDo uncomment and debug  # and form.validate():
        try:
            input_fs = request.files['userinput_file']
        except:
            input_fs = None

        ui = userinput.Userinput(pqo, fn=input_fs, foreground_string=form.foreground_textarea.data, background_string=form.background_textarea.data,
            num_bins=form.num_bins.data, decimal='.', enrichment_method=form.enrichment_method.data,
            foreground_n=form.foreground_n.data, background_n=form.background_n.data)

        if ui.check:
            # if limit_2_entity_type is not None:
            # limit_2_entity_type = {int(ele) for ele in form.limit_2_entity_type.data.split(";")}
            ip = request.environ['REMOTE_ADDR']
            string2log = "ip: " + ip + "\n" + "Request: results" + "\n"
            string2log += """limit_2_entity_type: {}\ngo_slim_or_basic: {}\nindent: {}\nmultitest_method: {}\nalpha: {}\n\
o_or_u_or_both: {}\nabcorr: {}\nnum_bins: {}\nfold_enrichment_foreground_2_background: {}\n\
p_value_uncorrected: {}\np_value_mulitpletesting: {}\n""".format(
                form.go_slim_or_basic.data, form.indent.data,
                form.multitest_method.data, form.alpha.data,
                form.o_or_u_or_both.data, form.abcorr.data, form.num_bins.data,
                form.fold_enrichment_for2background.data,
                form.p_value_uncorrected.data,
                form.FDR_cutoff.data,
                form.enrichment_method.data,
                form.foreground_n.data, form.background_n.data)

            if not app.debug: # temp  remove line and
                log_activity(string2log) # remove indentation

            if variables.VERSION_ == "STRING":
                output_format = "tsv"
                results_all_function_types = run.run_STRING_enrichment(pqo, ui,
                    enrichment_method=form.enrichment_method.data,
                    limit_2_entity_type=form.limit_2_entity_type.data,
                    go_slim_or_basic=form.go_slim_or_basic.data,
                    indent=form.indent.data,
                    multitest_method=form.multitest_method.data,
                    alpha=form.alpha.data,
                    o_or_u_or_both=form.o_or_u_or_both.data,
                    fold_enrichment_for2background=form.fold_enrichment_for2background.data,
                    p_value_uncorrected=form.p_value_uncorrected.data,
                    FDR_cutoff=form.FDR_cutoff.data,
                    output_format=output_format)
            elif variables.VERSION_ == "aGOtool":
                header, results = run.run(pqo, ui, form.limit_2_entity_type.data, form.go_slim_or_basic.data, form.indent.data,
                                    form.multitest_method.data, form.alpha.data, form.o_or_u_or_both.data,
                                    form.fold_enrichment_for2background.data, form.p_value_uncorrected.data, form.FDR_cutoff.data)
            else:
                raise NotImplementedError

        else:
            return render_template('info_check_input.html')
        # print("_"*50)
        # print("results_all_function_types", type(results_all_function_types), results_all_function_types.keys())
        # print("form.limit_2_entity_type.data", type(limit_2_entity_type), limit_2_entity_type)
        # print("#%$^")
        # print(form.values)
        # print("_"*50)
        if len(results_all_function_types) == 0:
            return render_template('results_zero.html')
        elif len(results_all_function_types.keys()) == 1:
            # entity_type = next(iter(limit_2_entity_type)) # single element in set
            return generate_result_page(results_all_function_types[entity_type], limit_2_entity_type,
                form.indent.data, generate_session_id(), form=Results_Form())
        elif len(results_all_function_types.keys()) > 1:
            # print("results_all_function_types", type(results_all_function_types), results_all_function_types.keys())
            # print("form.limit_2_entity_type.data", type(form.limit_2_entity_type.data), form.limit_2_entity_type.data)
            # ToDo create multiple results display method a la clustered results
            entity_type = int(form.limit_2_entity_type.data.split(";")[0]) # REPLACE WITH PROPER METHOD later, picked first entry as placeholder
            return generate_result_page(results_all_function_types[entity_type], entity_type,
                form.indent.data, generate_session_id(), form=Results_Form())
        else:
            raise NotImplementedError
    return render_template('enrichment.html', form=form)

def generate_result_page(tsv, entity_type, indent, session_id, form, errors=()):
    # header = header.rstrip().split("\t")
    # if len(results_all_function_types) == 1:
    #     df = results_all_function_types

    # df = df.applymap(str)
    # header = df.columns.tolist()
    # results = df.values.tolist()
    # results_2_display = ["\t".join(row) for row in results]
    header, results = tsv.split("\n", 1)

    # results_2_display = results.split("\n")
    header = header.split("\t")
    results_2_display = [res.split("\t") for res in results.split("\n")]

    ellipsis_indices = elipsis(header)
    # results2display = []
    # for res in results:
    #     results2display.append(res.split('\t'))
    file_name = "results_orig" + session_id + ".tsv"
    fn_results_orig_absolute = os.path.join(SESSION_FOLDER_ABSOLUTE, file_name)
    # fn_results_orig_relative = os.path.join(SESSION_FOLDER_RELATIVE, file_name)
    # tsv = (u'%s\n%s\n' % (u'\t'.join(header), u'\n'.join(results)))
    # tsv = df.to_csv(sep="\t", header=True, index=False)
    with open(fn_results_orig_absolute, 'w') as fh:
        fh.write(tsv)
    return render_template('results.html', header=header, results=results_2_display, errors=errors,
                           file_path=file_name, ellipsis_indices=ellipsis_indices, # was fn_results_orig_relative
                           limit_2_entity_type=str(entity_type), indent=indent,
                           session_id=session_id, form=form, maximum_time=MAX_TIMEOUT)

################################################################################
# results_back.html
################################################################################
@app.route('/results_back', methods=["GET", "POST"])
def results_back():
    """
    renders original un-filtered / un-clustered results
    and remembers user options in order to perform clustering or filtering
    as initially
    """
    session_id = request.form['session_id']
    limit_2_entity_type = request.form['limit_2_entity_type']
    # limit_2_entity_type = {int(ele) for ele in form.limit_2_entity_type.data.split(";")}

    indent = request.form['indent']
    file_name, fn_results_orig_absolute, fn_results_orig_relative = fn_suffix2abs_rel_path("orig", session_id)
    header, results = read_results_file(fn_results_orig_absolute)
    return generate_result_page(header, results, limit_2_entity_type, indent, session_id, form=Results_Form())

################################################################################
# results_filtered.html
################################################################################
# @app.route('/results_filtered', methods=["GET", "POST"])
# def results_filtered():
#     indent = request.form['indent']
#     limit_2_entity_type = request.form['limit_2_entity_type']
#     # limit_2_entity_type = {int(ele) for ele in form.limit_2_entity_type.data.split(";")}
#     session_id = request.form['session_id']
#
#     # original unfiltered/clustered results
#     file_name_orig, fn_results_orig_absolute, fn_results_orig_relative = fn_suffix2abs_rel_path("orig", session_id)
#     header, results = read_results_file(fn_results_orig_absolute)
#
#     if limit_2_entity_type: # in {-21, -22, -23}: # ToDo replace with proper check
#         results_filtered = filter_.filter_term_lineage(header, results, indent)
#
#         # filtered results
#         file_name_filtered, fn_results_filtered_absolute, fn_results_filtered_relative = fn_suffix2abs_rel_path("filtered", session_id)
#         tsv = (u'%s\n%s\n' % (header, u'\n'.join(results_filtered)))
#         with open(fn_results_filtered_absolute, 'w') as fh:
#             fh.write(tsv)
#         header = header.split("\t")
#         ellipsis_indices = elipsis(header)
#         results2display = []
#         for res in results_filtered:
#             results2display.append(res.split('\t'))
#         ip = request.environ['REMOTE_ADDR']
#         string2log = "ip: " + ip + "\n" + "Request: results_filtered" + "\n"
#         string2log += """limit_2_entity_type: {}\nindent: {}\n""".format(limit_2_entity_type, indent)
#         log_activity(string2log)
#         return render_template('results_filtered.html', header=header, results=results2display, errors=[],
#                                file_path_orig=file_name_orig, file_path_filtered=file_name_filtered,
#                                ellipsis_indices=ellipsis_indices, limit_2_entity_type=limit_2_entity_type, indent=indent, session_id=session_id)
#     else:
#         return render_template('index.html')

################################################################################
# results_clustered.html
################################################################################
@app.route('/results_clustered', methods=["GET", "POST"])
def results_clustered():
    form = Results_Form(request.form)
    inflation_factor = form.inflation_factor.data
    session_id = request.form['session_id']
    limit_2_entity_type = request.form['limit_2_entity_type']
    # limit_2_entity_type = {int(ele) for ele in form.limit_2_entity_type.data.split(";")}
    indent = request.form['indent']
    file_name, fn_results_orig_absolute, fn_results_orig_relative = fn_suffix2abs_rel_path("orig", session_id)
    header, results = read_results_file(fn_results_orig_absolute)
    if not form.validate():
        return generate_result_page(header, results, limit_2_entity_type, indent, session_id, form=form)
    try:
        mcl = cluster_filter.MCL(SESSION_FOLDER_ABSOLUTE, MAX_TIMEOUT)
        cluster_list = mcl.calc_MCL_get_clusters(session_id, fn_results_orig_absolute, inflation_factor)
    except cluster_filter.TimeOutException:
        return generate_result_page(header, results, limit_2_entity_type, indent, session_id, form=form, errors=['MCL timeout: The maximum time ({} min) for clustering has exceeded. Your original results are being displayed.'.format(MAX_TIMEOUT)])

    num_clusters = len(cluster_list)
    file_name, fn_results_clustered_absolute, fn_results_clustered_relative = fn_suffix2abs_rel_path("clustered", session_id)
    results2display = []
    with open(fn_results_clustered_absolute, 'w') as fh:
        fh.write(header)
        for cluster in cluster_list:
            results_one_cluster = []
            for res_index in cluster:
                res = results[res_index]
                fh.write(res + '\n')
                results_one_cluster.append(res.split('\t'))
            fh.write('#'*80)
            results2display.append(results_one_cluster)
    header = header.split("\t")
    ellipsis_indices = elipsis(header)
    ip = request.environ['REMOTE_ADDR']
    string2log = "ip: " + ip + "\n" + "Request: results_clustered" + "\n"
    string2log += """limit_2_entity_type: {}\nindent: {}\nnum_clusters: {}\ninflation_factor: {}\n""".format(limit_2_entity_type, indent, num_clusters, inflation_factor)
    log_activity(string2log)
    return render_template('results_clustered.html', header=header, results2display=results2display, errors=[],
                           file_path_orig=fn_results_orig_relative, file_path_mcl=file_name, #fn_results_clustered_relative
                           ellipsis_indices=ellipsis_indices, limit_2_entity_type=limit_2_entity_type, indent=indent, session_id=session_id,
                           num_clusters=num_clusters, inflation_factor=inflation_factor)

def fn_suffix2abs_rel_path(suffix, session_id):
    file_name = "results_" + suffix + session_id + ".tsv"
    fn_results_absolute = os.path.join(SESSION_FOLDER_ABSOLUTE, file_name)
    fn_results_relative = os.path.join(SESSION_FOLDER_RELATIVE, file_name)
    return file_name, fn_results_absolute, fn_results_relative

if __name__ == "__main__":
    # ToDo potential speedup
    # sklearn.metrics.pairwise.pairwise_distances(X, Y=None, metric='euclidean', n_jobs=1, **kwds)
    # --> use From scipy.spatial.distance: jaccard --> profile code cluster_filter
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.pairwise_distances.html
    ################################################################################
    # app.run(host='0.0.0.0', DEBUG=True, processes=8)
    # processes should be "1", otherwise nginx throws 502 errors with large files
    # sun IP 10110
    app.run(host='0.0.0.0', port=5911, processes=1, debug=variables.DEBUG)
