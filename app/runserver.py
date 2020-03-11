import os, sys, logging, time, argparse
from collections import defaultdict
import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', 300) # in order to prevent 50 character cutoff of to_html export / ellipsis
from lxml import etree
import flask
from flask import render_template, request, send_from_directory, jsonify
from flask_restful import reqparse, Api, Resource
from werkzeug.wrappers import Response
import wtforms
from wtforms import fields
import markdown
from flaskext.markdown import Markdown
from ast import literal_eval
sys.path.insert(0, os.path.abspath(os.path.realpath('./python')))
import query, userinput, run, variables, taxonomy


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
# MAX_TIMEOUT = variables.MAX_TIMEOUT # Maximum Time for MCL clustering
functionType_2_entityType_dict = variables.functionType_2_entityType_dict
ARGPARSE = variables.ARGPARSE
###############################################################################
def error_(parser):
    sys.stderr.write("The arguments passed are invalid.\nPlease check the input parameters.\n\n")
    parser.print_help()
    sys.exit(2)
if ARGPARSE:
    argparse_parser = argparse.ArgumentParser()
    argparse_parser.add_argument("IP", help="IP address without port, e.g. '127.0.0.1' (is also the default)", type=str, default="127.0.0.1", nargs='?')
    argparse_parser.add_argument("port", help="port number, e.g. '10110' (is also the default)", type=str, default="10110", nargs='?')
    argparse_parser.add_argument("verbose", help="add 'verbose' as an argumeqqqqqqnt to print more information", type=str, default="False", nargs="?")
    args = argparse_parser.parse_args()
    for arg in sorted(vars(args)):
        if getattr(args, arg) is None:
            error_(argparse_parser)
    IP, port = args.IP, args.port
    if args.verbose == "verbose" or args.verbose == "v":
        variables.VERBOSE = True
###############################################################################

# ToDo
# - convert Jensenlab scores so that 5 is 0 and 0 is 5.
# - add check to size of downloads. e.g. documents_protein2function.tsv.gz == URL_protein_2_function_PMID
#    --> to be >= previous size
# - buy goliath domain?
# - report userinput 2 mapped ID and make available as download
# - return unused identifiers
# - multiple entity type results to be displayed
# - debug copy&paste fields
# - debug file upload field
# - replace example file
# - update "info_check_input.html" with REST API usage infos
# - offer option to omit testing GO-terms with few associations (e.g. 10)
# - offer to user Pax-DB background proteomes
# - offer example to be set automatically
# - graphical output of enrichment
# - update bootstrap version
# - update documentation specifically about foreground and background
# ? - background proteome with protein groups --> does it get mapped to single protein in foreground ?
# - version of tool/ dates of files downloaded
# - one version per year that is fixed. if you need that particular annotation extra submission with some wait time and email results?
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
    # from werkzeug.contrib.profiler import ProfilerMiddleware
    from werkzeug.middleware.profiler import ProfilerMiddleware
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
    # if variables.VERSION_ == "aGOtool":
    #     pqo = query.PersistentQueryObject()
    if variables.VERSION_ == "STRING":
        pqo = query.PersistentQueryObject_STRING(low_memory=variables.LOW_MEMORY, read_from_flat_files=variables.READ_FROM_FLAT_FILES)
    elif variables.VERSION_ == "UniProt":
        pqo = query.PersistentQueryObject_STRING(low_memory=variables.LOW_MEMORY, read_from_flat_files=variables.READ_FROM_FLAT_FILES)
    else:
        print("VERSION_ {} not implemented".format(variables.VERSION_))
        raise NotImplementedError
    #filter_ = cluster_filter.Filter(pqo.go_dag, pqo.upk_dag)
else:
    pqo = None # just for mocking

### from http://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
### API
api = Api(app)
parser = reqparse.RequestParser()
################################################################################
### API arguments/parameters
parser.add_argument("taxid", type=int,help="NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms).",default=None)
parser.add_argument("species", type=int,help="deprecated please use 'taxid' instead, NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms).",default=None)
parser.add_argument("organism", type=int,help="deprecated please use 'taxid' instead, NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms).",default=None)
parser.add_argument("output_format", type=str, help="The desired format of the output, one of {tsv, tsv-no-header, json, xml}", default="tsv")

### Boolean arguments encoded as str on purpose
parser.add_argument("filter_parents", type=str,
    help="Remove parent terms (keep GO terms and UniProt Keywords of lowest leaf) if they are associated with exactly the same foreground.",
    default="True")
parser.add_argument("filter_foreground_count_one", type=str, help="Keep only those terms with foreground_count > 1", default="True")
parser.add_argument("privileged", type=str, default="False")
parser.add_argument("multiple_testing_per_etype", type=str, help="If True calculate multiple testing correction separately per entity type (functional category), in contrast to performing the correction together for all results.", default="True")

parser.add_argument("filter_PMID_top_n", type=int, default=100, help="Filter the top n PMIDs (e.g. 100, default=100), sorting by low p value and recent publication date.")
parser.add_argument("caller_identity", type=str, help="Your identifier for us e.g. www.my_awesome_app.com", default=None) # ? do I need default value ?
parser.add_argument("FDR_cutoff", type=float, help="False Discovery Rate cutoff (cutoff for multiple testing corrected p values) e.g. 0.05, default=0.05 meaning 5%. Set to 1 for no cutoff.", default=0.05)
parser.add_argument("limit_2_entity_type", type=str, help="Limit the enrichment analysis to a specific or multiple entity types, e.g. '-21' (for GO molecular function) or '-21;-22;-23;-51' (for all GO terms as well as UniProt Keywords).", default="-20;-21;-22;-23;-51;-52;-54;-55;-56;-57;-58") # -53 missing for UniProt version

parser.add_argument("foreground", type=str, help="ENSP identifiers for all proteins in the test group (the foreground, the sample, the group you want to examine for GO term enrichment) "
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
parser.add_argument("enrichment_method", type=str,
    help="""'genome': provided foreground vs genome;
    'compare_samples': Foreground vs Background (no abundance correction); 
    'characterize_foreground': list all functional annotations for provided foreground;
    'abundance_correction': Foreground vs Background abundance corrected""",
    default="characterize_foreground")
parser.add_argument("goslim", type=str, help="GO basic or a slim subset {generic, agr, aspergillus, candida, chembl, flybase_ribbon, metagenomics, mouse, pir, plant, pombe, synapse, yeast}. Choose between the full Gene Ontology ('basic') or one of the GO slim subsets (e.g. 'generic' or 'mouse'). GO slim is a subset of GO terms that are less fine grained. 'basic' does not exclude anything, select 'generic' for a subset of broad GO terms, the other subsets are tailor made for a specific taxons / analysis (see http://geneontology.org/docs/go-subset-guide)", default="basic")
parser.add_argument("o_or_u_or_both", type=str, help="over- or under-represented or both, one of {overrepresented, underrepresented, both}. Choose to only test and report overrepresented or underrepresented GO-terms, or to report both of them.", default="overrepresented")
parser.add_argument("num_bins", type=int, help="The number of bins created based on the abundance values provided. Only relevant if 'Abundance correction' is selected.", default=100)
# parser.add_argument("fold_enrichment_for2background", type=float, help="Apply a filter for the minimum cutoff value of fold enrichment foreground/background.",default=0)
parser.add_argument("p_value_cutoff", type=float, help="Apply a filter (value between 0 and 1) for maximum cutoff value of the uncorrected p value. '1' means nothing will be filtered, '0.01' means all uncorected p_values <= 0.01 will be removed from the results (but still tested for multiple correction).", default=1)
parser.add_argument("score_cutoff", type=float, help="Apply a filter for the minimum cutoff value of the textmining score. This cutoff is only applied to the 'characterize_foreground' method, and does not affect p values. Default = 3.", default=3)
parser.add_argument("foreground_replicates", type=int, help="'foreground_replicates' is an integer, defines the number of samples (replicates) of the foreground.", default=10)
parser.add_argument("background_replicates", type=int, help="'background_replicates' is an integer, defines the number of samples (replicates) of the background.", default=10)
parser.add_argument("simplified_output", type=str, default="False")
parser.add_argument("do_KS", type=str, default="False")


class API_STRING(Resource):
    """
    get enrichment for all available functional associations not 'just' one category
    """
    def get(self): #, output_format="json"):
        return self.post() #output_format)

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
        args_dict = convert_string_2_bool(args_dict)
        if variables.VERBOSE:
            print("-" * 80)
            for key, val in sorted(args_dict.items()):
                print(key, val, type(val))
            print("-" * 80)
        ui = userinput.REST_API_input(pqo, args_dict)
        if not ui.check:
            args_dict["ERROR_UserInput"] = "ERROR_UserInput: Something went wrong parsing your input, please check your input and/or compare it to the examples."
            return help_page(args_dict)

        if args_dict["enrichment_method"] == "genome":
            background_n = pqo.get_proteome_count_from_taxid(args_dict["taxid"])
            if not background_n:
                args_dict["ERROR taxid"] = "taxid: '{}' does not exist in the data base, thus enrichment_method 'genome' can't be run. Please change to a NCBI taxonomic identifier supported by UniProt Reference Proteomes (https://www.uniprot.org/proteomes) with 'Download one protein sequence per gene (FASTA)'."
                return help_page(args_dict)

        ### DEBUG start
        if variables.DEBUG_HTML:
            df_all_etypes = pd.read_csv(variables.fn_example, sep="\t")
            results_all_function_types = df_all_etypes.groupby("etype").head(20)
        else:
            results_all_function_types = run.run_UniProt_enrichment(pqo, ui, args_dict, api_call=True)

        if results_all_function_types is False:
            print("returning help page")
            return help_page(args_dict)
        else:
            return format_multiple_results(args_dict, results_all_function_types, pqo)


# api.add_resource(API_STRING, "/api", "/api_string", "/api_string/<output_format>", "/api_string/<output_format>/enrichment")
api.add_resource(API_STRING, "/api", "/api_string", "/api_agotool", "/api_string/<output_format>", "/api_string/<output_format>/enrichment")


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
    if args_dict["taxid"] is not None:
        return args_dict["taxid"]
    if args_dict["species"] is not None:
        args_dict["ERROR_species"] = "ERROR_species: argument 'species' is deprecated, please use 'taxid' instead. You've provided is '{}'.".format(args_dict["species"])
        return False
    if args_dict["organism"] is not None:
        args_dict["ERROR_organism"] = "ERROR_organism: argument 'organism' is deprecated, please use 'taxid' instead. You've provided is '{}'.".format(args_dict["organism"])
        return False

def convert_string_2_bool(args_dict):
    for key, val in args_dict.items():
        if isinstance(val, str):
            if val.lower() == "true":
                args_dict[key] = True
            elif val.lower() == "false":
                args_dict[key] = False
            else:
                pass
    return args_dict



def write2file(fn, tsv):
    with open(fn, 'w') as f:
        f.write(tsv)

class API_STRING_HELP(Resource):
    """
    get enrichment for all available functional associations not 'just' one category
    """
    @staticmethod
    def get(): # output_format="json"
        args_dict = defaultdict(lambda: None)
        args_dict.update(parser.parse_args())
        args_dict = parser.parse_args()
        args_dict["1_INFO"] = "INFO: default values are are shown unless you've provided arguments"
        args_dict["2_INFO_Name_2_EntityType"] = variables.functionType_2_entityType_dict
        args_dict["3_INFO_limit_2_entity_type"] = "comma separate desired entity_types e.g. '-21;-51;-52' (for GO biological process; UniProt keyword; SMART), default get all available."
        return help_page(args_dict)

    def post(self):
        return self.get()

api.add_resource(API_STRING_HELP, "/api_help", "/api_string_help")


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
        # return jsonify(results_all_entity_types)
        # return results_all_entity_types.to_json(orient="records")
        return results_all_entity_types
    elif output_format == "xml":
        # dict_2_return = {}
        # for etype, results in results_all_entity_types.items():
        # # for etype, df_of_etype in results_all_entity_types.groupby("etype"):
        #     results = df_of_etype.to_csv(sep="\t", header=True, index=False) # convert DatFrame to string
        #     header, rows = results.split("\n", 1) # is df in tsv format
        #     xml_string = create_xml_tree(header, rows.split("\n"))
        #     dict_2_return[etype] = xml_string.decode()
        # return jsonify(dict_2_return)
        return results_all_entity_types
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

@app.route('/doro')
def doro():
    return render_template('doro.html')

################################################################################
# parameters.html
################################################################################
@app.route('/parameters')
def parameters():
    with open(variables.FN_HELP_ENTITY_TYPES, "r") as fh:
        content = fh.read()
        content_entity_types = format_markdown(content)
    return render_template('parameters.html', **locals())

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
    # with open(variables.FN_HELP_ENTITY_TYPES, "r") as fh:
    #     content = fh.read()
    #     content_entity_types = format_markdown(content)
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

@app.route('/API_Help')
def api_help():
    return render_template('API_Help.html')


################################################################################
# helper functions
################################################################################
def format_markdown(content):
    content = content.replace("{", "\{").replace("}", "\}")
    content = markdown.markdown(content, extensions=['extra', 'smarty'], output_format='html5')
    # return content.replace(r"<table>", r'<table id="table_id" class="table table-striped hover">').replace("<thead>", '<thead class="table_header">')
    return content.replace(r"<table>", r'<table id="table_id" class="table table-striped hover text-center">').replace("<thead>", '<thead class="table_header">')

##### validation of user inputs
def validate_float_larger_zero_smaller_one(form, field):
    if not 0 < field.data < 1:
        raise wtforms.ValidationError(" number must be: 0 < number < 1")

def validate_float_between_zero_and_one(form, field):
    if not 0 <= field.data <= 1:
        print("validation failed what's next?")
        raise wtforms.ValidationError(" number must be: 0 <= number <= 1")
    else:
        print('bubu')

def validate_float_between_zero_and_five(form, field):
    if not 0 <= field.data <= 5:
        raise wtforms.ValidationError(" number must be: 0 <= number <= 5")

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

################################################################################
# enrichment.html
################################################################################

class Enrichment_Form(wtforms.Form):
    userinput_file = fields.FileField('Expects a tab-delimited text-file',
                                      description="""see 'Parameters' page for details""")
#     userinput_file = fields.FileField(label=None, description=None)
    foreground_textarea = fields.TextAreaField("Foreground")
    background_textarea = fields.TextAreaField("Background & Intensity")
    limit_2_entity_type = fields.SelectField("Category of functional associations", # # ("-53", "SMART domains"), # not available in UniProt version
                                   choices = ((None, "all available"),
                                              ("-21;-22;-23", "all GO categories"),
                                              ("-51", "UniProt keywords"),
                                              ("-57", "Reactome"),
                                              ("-52", "KEGG pathways"),
                                              ("-58", "Wiki pathways"),
                                              ("-21", "GO Biological Process"),
                                              ("-23", "GO Molecular Function"),
                                              ("-22", "GO Celluar Compartment"),
                                              ("-20", "GOCC from Textmining"),
                                              ("-25", "Brenda Tissue Ontology (BTO)"),
                                              ("-26", "Disease Ontology IDs (DOIDs)"),
                                              ("-56", "PMID (PubMed IDs)"),
                                              ("-54", "InterPro domains"),
                                              ("-55", "PFAM domains")),
                                   description="""Select either a functional category, one or all three GO categories (molecular function, biological process, cellular component), UniProt keywords, KEGG pathways, etc.""")
    enrichment_method = fields.SelectField("Enrichment method",
                                   choices = (("abundance_correction", "abundance_correction"),
                                              ("characterize_foreground", "characterize_foreground"),
                                              ("compare_samples", "compare_samples"),
                                              ("genome", "genome")), # ("compare_groups", "compare_groups"),
                                   description="""abundance_correction: Foreground vs Background abundance corrected
compare_samples: Foreground vs Background (no abundance correction)
characterize_foreground: Foreground only""")
    go_slim_or_basic = fields.SelectField("GO basic or a slim subset",
                                          choices = ((None, "no subset"),
                                                     ("generic", "Generic GO slim by GO Consortium"),
                                                     ("agr", "Alliance of Genomes Resources (AGR)"),
                                                     ("aspergillus", "Aspergillus Genome Data"),
                                                     ("candida", "Candida (albicans) Genome Database"),
                                                     ("chembl", "ChEMBL Drug Target"),
                                                     ("flybase_ribbon", "FlyBase"),
                                                     ("metagenomics", "EBI Metagenomics group"),
                                                     ("mouse", "Mouse Genome Informatics"),
                                                     ("pir", "Protein Information Resource"),
                                                     ("plant", "Plant subset by The Arabidopsis Information Resource (TAIR)"),
                                                     ("pombe", "Schizosaccharomyces pombe subset PomBase"),
                                                     ("synapse", "Synapse GO slim SynGO"),
                                                     ("yeast", "Yeast subset Saccharomyces Genome Database")),
                                          description="""Choose between the full Gene Ontology or GO slim subset a subset of GO terms that are less fine grained.""")
    o_or_u_or_both = fields.SelectField("Over-, under-represented or both", choices = (("overrepresented", "overrepresented"), ("underrepresented", "underrepresented"), ("both", "both")), description="""Choose to only test and report overrepresented or underrepresented GO-terms, or to report both of them.""")
    # num_bins = fields.IntegerField("Number of bins", [validate_integer], default = 100, description="""The number of bins created based on the abundance values provided. Only relevant if "Abundance correction" is selected.""")
    # fold_enrichment_for2background = fields.FloatField("fold enrichment foreground/background", [validate_number], default = 0, description="""Minimum cutoff value of "fold_enrichment_foreground_2_background".""")
    p_value_cutoff = fields.FloatField("p value cutoff", [validate_float_between_zero_and_one], default = 0.01, description="""Maximum cutoff value of uncorrected p value.""")
    FDR_cutoff = fields.FloatField("p value corrected (FDR) cutoff", [validate_float_between_zero_and_one], default = 0.05, description="""Maximum False Discovery Rate (Benjamini-Hochberg corrected p values) cutoff value (1 meaning no cutoff)""")
    filter_foreground_count_one = fields.BooleanField("Filter foreground count one", default="checked", description="Remove all functional terms if they have only a single protein association in the foreground (default=checked)")
    filter_parents = fields.BooleanField("Filter redundant parent terms", default="checked", description="Retain the most specific (deepest hierarchical level) and remove all parent terms if they share the exact same foreground proteins (default=checked)")
    taxid = fields.IntegerField("NCBI TaxID", [validate_integer], default=9606, description="NCBI Taxonomy IDentifier, please use the taxonomic rank of species e.g. '9606' for Homo sapiens. Only relevant if 'enrichment_method' is 'genome' (default=9606)")
    multiple_testing_per_etype = fields.BooleanField("Multiple testing per entity type", default="checked", description="If True calculate multiple testing correction separately per entity type (functional category), in contrast to performing the correction together for all results (default=checked).")
    score_cutoff = fields.FloatField("Text mining score cutoff", [validate_float_between_zero_and_five], default = 3.0, description="""Apply a filter for the minimum cutoff value of the textmining score. This cutoff is only applied to the 'characterize_foreground' method, and does not affect p values. Default = 3.""")
    foreground_replicates = fields.IntegerField("foreground replicates", [validate_integer], default=10, description="'Foreground replicates' is an integer, defines the number of samples (replicates) of the foreground. default=10.")
    background_replicates = fields.IntegerField("background replicates", [validate_integer], default=10, description="'Background replicates' is an integer, defines the number of samples (replicates) of the background. default=10.")



class Example_1(Enrichment_Form):
    """
    example 1: Yeast acetylation,
    abundance_correction. Example_1_Yeast_acetylation_abundance_correction.txt
    """
    df = pd.read_csv(os.path.join(variables.EXAMPLE_FOLDER, "Example_1_Yeast_acetylation_abundance_correction.txt"), sep='\t')
    fg = "\n".join(df.loc[df["Foreground"].notnull(), "Foreground"].tolist())
    bg_int = ""
    for bg_ele, int_ele in zip(df["Background"].values, df["Intensity"].values):
        bg_int += bg_ele + "\t" + str(int_ele) + "\n"
    foreground_textarea = fields.TextAreaField("Foreground", default=fg)
    background_textarea = fields.TextAreaField("Background & Intensity", default=bg_int.strip())
    enrichment_method = fields.SelectField("Enrichment method", choices=(("abundance_correction", "abundance_correction"), ("compare_samples", "compare_samples"), ("genome", "genome"), ("characterize_foreground", "characterize_foreground")), description="""abundance_correction: Foreground vs Background abundance corrected
    compare_samples: Foreground vs Background (no abundance correction)
    characterize_foreground: Foreground only""") # ("compare_groups", "compare_groups"),


class Example_2(Enrichment_Form):
    """
    example 2: Human hemoglobin
    genome
    """
    foreground_textarea = fields.TextAreaField("Foreground", default="""P69905\nP68871\nP02042\nP02100""")
    # foreground_textarea = fields.TextAreaField("Foreground", default="""HBA_HUMAN\nHBB_HUMAN\nHBD_HUMAN\nHBE_HUMAN""")
    background_textarea = fields.TextAreaField("Background & Intensity", default="no data necessary (in this field) since enrichment method 'genome' is being used, which uses pre-selected background reference proteome from UniProt")
    enrichment_method = fields.SelectField("Enrichment method", choices=(("genome", "genome"), ("compare_samples", "compare_samples"), ("abundance_correction", "abundance_correction"), ("characterize_foreground", "characterize_foreground")), description="""abundance_correction: Foreground vs Background abundance corrected
    compare_samples: Foreground vs Background (no abundance correction)
    characterize_foreground: Foreground only""") # ("compare_groups", "compare_groups"),
    taxid = fields.IntegerField("NCBI TaxID", [validate_integer], default=9606, description="NCBI Taxonomy IDentifier e.g. '9606' for Homo sapiens. Only relevant if 'enrichment_method' is 'genome' (default=9606)")



class Example_3(Enrichment_Form):
    """
    example 3: Mouse interferon (STRING network)
    compare_samples
    """
    foreground_textarea = fields.TextAreaField("Foreground", default="""Q9R117\nP33896\nO35664\nO35716\nP01575\nP42225\nP07351\nP52332\nQ9WVL2\nQ61179\nQ61716""")
    background_input = "\n".join(query.get_proteins_of_taxid(10090, read_from_flat_files=True))
    background_textarea = fields.TextAreaField("Background & Intensity", default=background_input)
    enrichment_method = fields.SelectField("Enrichment method", choices=(("compare_samples", "compare_samples"), ("abundance_correction", "abundance_correction"), ("genome", "genome"),  ("characterize_foreground", "characterize_foreground")), description="""abundance_correction: Foreground vs Background abundance corrected
    compare_samples: Foreground vs Background (no abundance correction)
    characterize_foreground: Foreground only""") # ("compare_groups", "compare_groups"),
    taxid = fields.IntegerField("NCBI TaxID", [validate_integer], default=9606, description="NCBI Taxonomy IDentifier e.g. '9606' for Homo sapiens. Only relevant if 'enrichment_method' is 'genome' (default=9606 for Homo sapiens)")


class Example_4(Enrichment_Form):
    """
    example 4: Cation-dependent mannose-6-phosphate receptor, MPRD_HUMAN, Gene M6PR
    characterize_foreground
    """
    foreground_textarea = fields.TextAreaField("Foreground", default="""MPRD_HUMAN""")
    enrichment_method = fields.SelectField("Enrichment method", choices=(("characterize_foreground", "characterize_foreground"), ("compare_samples", "compare_samples"), ("abundance_correction", "abundance_correction"), ("genome", "genome")), description="""abundance_correction: Foreground vs Background abundance corrected
    compare_samples: Foreground vs Background (no abundance correction)
    characterize_foreground: Foreground only""") # ("compare_groups", "compare_groups")


@app.route('/example_1')
def example_1():
    return render_template('enrichment.html', form=Example_1(), example_status="example_1", example_title="Yeast acetylation", example_description="""comparing acetylated yeast (Saccharomyces cerevisiae) proteins to the experimentally observed proteome using the 'abundance_correction' method. Data was taken from the original publication (see 'About' page).""")

@app.route('/example_2')
def example_2():
    return render_template('enrichment.html', form=Example_2(), example_status="example_2", example_title="Human haemoglobin", example_description="""comparing human haemoglobin proteins to the UniProt reference genome. When using the 'genome' method a specific NCBI taxonomic identifier (TaxID) has to be provided. In this case it is '9606' for Homo sapiens. In case don't know the TaxID of your organism of choice, please search at NCBI (link provided below).""")

@app.route('/example_3')
def example_3():
    return render_template('enrichment.html', form=Example_3(), example_status="example_3", example_title="Mouse interferon", example_description="""comparing a couple of mouse interferons to the reference proteome, applying the 'compare_samples' method.""")


@app.route('/example_4')
def example_4():
    return render_template('enrichment.html', form=Example_4(), example_status="example_4", example_title="show functional annotations for the gene M6PR", example_description="""characterize the foreground. Cation-dependent mannose-6-phosphate receptor, MPRD_HUMAN, Gene M6PR.""")

@app.route('/')
def enrichment():
    return render_template('enrichment.html', form=Enrichment_Form(), example_status="example_None")

@app.route('/temp')
def temp():
    return render_template('temp.html', form=Enrichment_Form())


@app.route('/help')
def help():
    return render_template('help.html', form=Enrichment_Form())


################################################################################
# results.html
################################################################################
class Results_Form(wtforms.Form):
#     inflation_factor = fields.FloatField("inflation factor", [validate_inflation_factor], default = 2.0, description="""Enter a number higher than 1.
# Usually a number between 1.1 and 10 is chosen.
# Increasing the value will increase cluster granularity (produce more clusters).
# Certain combinations of data and inflation factor can take very long to process. Please be patient.""")
    pass

@app.route('/results', methods=["GET", "POST"])
def results():
    """
    cluster_list: nested ListOfString corresponding to indices of results
    results_filtered = filter(header, results, indent)
    results_filtered: reduced version of results
    """
    form = Enrichment_Form(request.form)
    if request.method == 'POST':
        try:
            fileobject = request.files['userinput_file']
        except KeyError:
            fileobject = None
        # filename = secure_filename(fileobject.filename) # necessary if saving the file to disk
        args_dict = {"limit_2_entity_type": form.limit_2_entity_type.data,
                     "go_slim_subset": form.go_slim_or_basic.data,
                     "p_value_cutoff": form.p_value_cutoff.data,
                     "FDR_cutoff": form.FDR_cutoff.data,
                     "o_or_u_or_both": form.o_or_u_or_both.data,
                     "filter_PMID_top_n": 100,
                     "filter_foreground_count_one": form.filter_foreground_count_one.data,
                     "filter_parents": form.filter_parents.data,
                     "taxid": form.taxid.data,
                     "output_format": "dataframe",
                     "enrichment_method": form.enrichment_method.data,
                     "multiple_testing_per_etype": form.multiple_testing_per_etype.data,
                     "score_cutoff": form.score_cutoff.data}
        ui = userinput.Userinput(pqo, fn=fileobject,
            foreground_string=form.foreground_textarea.data, background_string=form.background_textarea.data,
            decimal='.', args_dict=args_dict)
        print("-" * 80)
        for key, val in sorted(args_dict.items()):
            print(key, val, type(val))
        print("-" * 80)
        # if variables.DEBUG_HTML:
        #     ui.check = True # ToDo comment #!!! DEBUG
        if ui.check:
            ip = request.environ['REMOTE_ADDR']
            string2log = "ip: " + ip + "\n" + "Request: results" + "\n"
            string2log += """limit_2_entity_type: {}\ngo_slim_or_basic: {}\no_or_u_or_both: {}\np_value_cutoff: {}\np_value_mulitpletesting: {}\n""".format(form.limit_2_entity_type.data, form.go_slim_or_basic.data, form.o_or_u_or_both.data, form.p_value_cutoff.data, form.FDR_cutoff.data, form.enrichment_method.data) # \nnum_bins: {} # form.num_bins.data form.fold_enrichment_for2background.data, \nfold_enrichment_foreground_2_background: {}
            if not app.debug:
                log_activity(string2log)
            ### DEBUG start
            # if variables.DEBUG_HTML:
            #     df_all_etypes = pd.read_csv(variables.fn_example, sep="\t")
            #     df_all_etypes = df_all_etypes.groupby("etype").head(20)
            # else:
            df_all_etypes = run.run_UniProt_enrichment(pqo, ui, args_dict)  # ToDo uncomment #!!! DEBUG
            ### DEBUG stop
        else:
            return render_template('info_check_input.html', args_dict=args_dict)
        if type(df_all_etypes) == bool:
            return render_template('info_check_input.html', args_dict=args_dict)
        elif len(df_all_etypes) == 0:
            return render_template('results_zero.html')
        else:
            return generate_result_page(df_all_etypes, args_dict, generate_session_id(), form=Results_Form())
    return render_template('enrichment.html', form=form)

def generate_result_page(df_all_etypes, args_dict, session_id, form, errors=(), compact_or_comprehensive="compact"):
    file_name = "results_orig" + session_id + ".tsv"
    fn_results_orig_absolute = os.path.join(SESSION_FOLDER_ABSOLUTE, file_name)
    df_all_etypes.to_csv(fn_results_orig_absolute, sep="\t", header=True, index=False)
    if args_dict["enrichment_method"] != "characterize_foreground":
        df_all_etypes = df_all_etypes.sort_values(["etype", "rank"])
    etype_2_rowsCount_dict, etype_2_df_as_html_dict = {}, {}
    p_value = "p value"
    FDR = "p value corrected"
    effect_size = "effect size"
    over_under = "over under"
    hierarchical_level = "level"
    s_value = "s value"
    ratio_in_FG = "ratio in FG"
    ratio_in_BG = "ratio in BG"
    FG_IDs = "FG IDs"
    BG_IDs = "BG IDs"
    FG_count = "FG count"
    BG_count = "BG count"
    FG_n = "FG n"
    BG_n = "BG n"
    rank = "rank"
    df_all_etypes = df_all_etypes.rename(columns={"over_under": over_under, "hierarchical_level": hierarchical_level, "p_value": p_value, "FDR": FDR, "effectSize": effect_size, "s_value": s_value, "ratio_in_FG": ratio_in_FG, "ratio_in_BG": ratio_in_BG, "FG_IDs": FG_IDs, "BG_IDs": BG_IDs, "FG_count": FG_count, "BG_count": BG_count, "FG_n": FG_n, "BG_n": BG_n})
    pd.set_option('colheader_justify', 'center')
    ### compact results
    if compact_or_comprehensive == "compact":
        if args_dict["enrichment_method"] == "characterize_foreground":
            cols_compact = [FG_count, "term", "description", ratio_in_FG]
            for etype, group in df_all_etypes.groupby("etype"):
                num_rows = group.shape[0]
                if num_rows > 0:
                    etype_2_rowsCount_dict[etype] = num_rows
                    if etype in variables.PMID:
                        etype_2_df_as_html_dict[etype] = group[cols_compact + ["year"]].to_html(index=False, border=0, classes=["table table_etype dataTable display"], table_id="table_etype", justify="left", formatters={effect_size: lambda x: "{:.2f}".format(x), FDR: lambda x: "{:.2E}".format(x)})
                    elif etype in variables.entity_types_with_ontology:
                        etype_2_df_as_html_dict[etype] = group[cols_compact + [hierarchical_level]].to_html(index=False, border=0, classes=["table table_etype dataTable display"], table_id="table_etype", justify="left", formatters={effect_size: lambda x: "{:.2f}".format(x), FDR: lambda x: "{:.2E}".format(x)})
                    else:
                        etype_2_df_as_html_dict[etype] = group[cols_compact + [FG_n]].to_html(index=False, border=0, classes=["table table_etype dataTable display"], table_id="table_etype", justify="left", formatters={effect_size: lambda x: "{:.2f}".format(x), FDR: lambda x: "{:.2E}".format(x)})
        else:
            cols_compact = ["rank", "term", "description", FDR, effect_size]
            for etype, group in df_all_etypes.groupby("etype"):
                num_rows = group.shape[0]
                if num_rows > 0:
                    etype_2_rowsCount_dict[etype] = num_rows
                    etype_2_df_as_html_dict[etype] = group[cols_compact].to_html(index=False, border=0, classes=["table table_etype dataTable display"], table_id="table_etype", justify="left", formatters={effect_size: lambda x: "{:.2f}".format(x), FDR: lambda x: "{:.2E}".format(x)})
        return render_template('results_compact.html', etype_2_rowsCount_dict=etype_2_rowsCount_dict, etype_2_df_as_html_dict=etype_2_df_as_html_dict, errors=errors, file_path=file_name, session_id=session_id, form=form, args_dict=args_dict, df_all_etypes=df_all_etypes)

    ### comprehensive results
    elif compact_or_comprehensive == "comprehensive":
        # show year, not hierarchy
        cols_sort_order_PMID = ['rank', 'term', 'description', 'year', over_under, p_value, FDR, effect_size, s_value, ratio_in_FG, ratio_in_BG, FG_count, FG_n, BG_count, BG_n, FG_IDs, BG_IDs]
        # entity_types_with_scores
        cols_sort_order_entity_types_with_scores = ['rank', 'term', 'description', hierarchical_level, over_under, p_value, FDR, effect_size, s_value]
        # show hierarchy, not year
        cols_sort_order_hierarchy = ['rank', 'term', 'description', hierarchical_level, over_under, p_value, FDR, effect_size, s_value, ratio_in_FG, ratio_in_BG, FG_count, FG_n, BG_count, BG_n, FG_IDs, BG_IDs]
        # not hiearachy, not year
        cols_sort_order_rest = ['rank', 'term', 'description', over_under, p_value, FDR, effect_size, s_value, ratio_in_FG, ratio_in_BG, FG_count, FG_n, BG_count, BG_n, FG_IDs, BG_IDs]

        def helper_format_to_html(df):
            return df.to_html(index=False, border=0, classes=["table table_etype dataTable display"], table_id="table_etype", justify="left",
                formatters={"effect size": lambda x: "{:.2f}".format(x), FDR: lambda x: "{:.2E}".format(x), p_value: lambda x: "{:.2E}".format(x), s_value: lambda x: "{:.2f}".format(x),
                            ratio_in_FG: lambda x: "{:.2f}".format(x), ratio_in_BG: lambda x: "{:.2f}".format(x), FG_count: lambda x: "{:.0f}".format(x)})

        if args_dict["o_or_u_or_both"] != "both": # don't hide "over under"
            cols_sort_order_PMID.remove(over_under)
            cols_sort_order_entity_types_with_scores.remove(over_under)
            cols_sort_order_hierarchy.remove(over_under)
            cols_sort_order_rest.remove(over_under)

        if args_dict["enrichment_method"] not in {"compare_samples"}: # "compare_groups"
            cols_sort_order_PMID.remove(BG_IDs)
            cols_sort_order_hierarchy.remove(BG_IDs)
            cols_sort_order_rest.remove(BG_IDs)

        if args_dict["enrichment_method"] == "characterize_foreground":
            cols_2_remove = (BG_IDs, BG_n, BG_count, ratio_in_BG, over_under, p_value, FDR, effect_size, s_value, rank)
            cols_sort_order_PMID = [ele for ele in cols_sort_order_PMID if ele not in cols_2_remove]
            cols_sort_order_entity_types_with_scores = [ele for ele in cols_sort_order_entity_types_with_scores if ele not in cols_2_remove]
            cols_sort_order_hierarchy = [ele for ele in cols_sort_order_hierarchy if ele not in cols_2_remove]
            cols_sort_order_rest = [ele for ele in cols_sort_order_rest if ele not in cols_2_remove]

        for etype, group in df_all_etypes.groupby("etype"):
            num_rows = group.shape[0]
            if num_rows > 0:
                etype_2_rowsCount_dict[etype] = num_rows
                if etype in variables.PMID: # -56 is the only one with "year"
                    etype_2_df_as_html_dict[etype] = helper_format_to_html(group[cols_sort_order_PMID])
                elif etype in variables.entity_types_with_scores:
                    etype_2_df_as_html_dict[etype] = helper_format_to_html(group[cols_sort_order_entity_types_with_scores])
                elif etype in variables.entity_types_with_ontology:
                    etype_2_df_as_html_dict[etype] = helper_format_to_html(group[cols_sort_order_hierarchy])
                else:
                    etype_2_df_as_html_dict[etype] = helper_format_to_html(group[cols_sort_order_rest])

        return render_template('results_comprehensive.html', etype_2_rowsCount_dict=etype_2_rowsCount_dict, etype_2_df_as_html_dict=etype_2_df_as_html_dict, errors=errors, file_path=file_name, session_id=session_id, form=form, args_dict=args_dict)
    else:
        print("compact_or_comprehensive is '{}' {}, which is not understood".format(compact_or_comprehensive, type(compact_or_comprehensive)))

@app.route('/results_comprehensive', methods=["GET", "POST"])
def results_comprehensive():
    file_path = request.form['file_path']
    df_all_etypes = pd.read_csv(os.path.join(SESSION_FOLDER_ABSOLUTE, file_path), sep='\t')
    args_dict = request.form['args_dict']
    args_dict = literal_eval(args_dict)
    # print(args_dict, type(args_dict))
    session_id = request.form['session_id']
    compact_or_comprehensive = request.form['compact_or_comprehensive']
    return generate_result_page(df_all_etypes, args_dict, session_id, Results_Form(), errors=(), compact_or_comprehensive=compact_or_comprehensive)

def fn_suffix2abs_rel_path(suffix, session_id):
    file_name = "results_" + suffix + session_id + ".tsv"
    fn_results_absolute = os.path.join(SESSION_FOLDER_ABSOLUTE, file_name)
    fn_results_relative = os.path.join(SESSION_FOLDER_RELATIVE, file_name)
    return file_name, fn_results_absolute, fn_results_relative

def compact_count_2_n_cols(row):
    return "{}/{}  {}/{}".format(row["FG_count"], row["FG_n"], row["BG_count"], row["BG_n"])

def compact_count_2_n_cols_FG(row):
    return "{}/{}".format(row["FG_count"], row["FG_n"])


if __name__ == "__main__":
    ################################################################################
    # app.run(host='0.0.0.0', DEBUG=True, processes=8)
    # processes should be "1", otherwise nginx throws 502 errors with large files
    ### SAN port 10110
    ### PISCES IP 127.0.0.1 port 10110
    ### ATLAS IP 0.0.0.0 port 5911
    ### Aquarius port 5911 (via docker-compose)
    # print("#" * 80)
    # print("running aGOtool on IP {} port {}".format(IP, port))
    # app.run(host=IP, port=port, processes=1, debug=variables.DEBUG)
    if ARGPARSE:
        print(IP, port)
        print("#" * 80)
        print("running aGOtool on IP {} port {}".format(IP, port))
        app.run(host=IP, port=port, processes=1, debug=variables.DEBUG)
    else:
        app.run(processes=1, debug=variables.DEBUG)

# fix bug for abundance_correction and