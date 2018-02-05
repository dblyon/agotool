import os, sys, logging, time
from flask import render_template, request, send_from_directory
import flask
import wtforms
from wtforms import fields
sys.path.insert(0, os.path.abspath(os.path.realpath('./python')))
import query, userinput, run, cluster_filter, obo_parser, variables

###############################################################################
WEBSERVER_DATA = variables.WEBSERVER_DATA
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
###############################################################################

###############################################################################
#### bokeh visualisation
# if not DEBUG:
#     from bokeh.embed import components
#     from bokeh.plotting import figure
#     from bokeh.resources import INLINE
#     from bokeh.util.string import encode_utf8
# colors = {
#     'Black': '#000000',
#     'Red':   '#FF0000',
#     'Green': '#00FF00',
#     'Blue':  '#0000FF'}

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]
###############################################################################


###############################################################################
# ToDo:
# - load 'Ontologies_table' once
# - post DataBase schema for RestAPI lookup
# - explain sources and update intervals
# - downloads page for existing fasta
# - create search page for common user input and convert to
## e.g.
## http://localhost:5000/api/functions?q={"filters": [{"name": "type", "val": "DOM", "op": "eq"}]}
## http://localhost:5000/api/proteins?q={"filters": [{"name": "an", "val": "B2RID1", "op": "eq"}]}
# - graphical output of enrichment
# - enter list of TaxIDs --> create fasta for download
# - tool to convert TaxNames to TaxIDs or rather link to NCBI
# - Consenus functional annotation for protein groups
# - check if TaxIDs not in NCBI taxdump, but in HOMD mappings are missing in DB, check if all TaxIDs from Fasta in DB, CHeck if all TaxNames in DB
# - add other types to Ontologies (not only GO, but also UPK)
# - DB schema doesn't have theme
# - userinput report, redundant and unique number of ANs/protein-groups, organisms etc.
# - close up/macro picture of ESI or mass spec or something, combine with a histogram similar to the publication
# - graphical output of
# - Dia Show or nice images in the background, changing every 1min
# - All proteins without abundance data were disregarded --> put into extra bin
# - http://geneontology.org/page/download-ontology --> slim set for Metagenomics
###############################################################################

# ECHO = False
# TESTING = False # which DB are we connecting to ('metaprot' or 'test')
# DO_LOGGING = False
# DEBUG = False # do not attempt connection to PostgreSQL
# volume_mountpoint=None # mount point set at 'docker run -v LocalPath:MountPoint'
# if not DEBUG:
#     connection = db_config.Connect(echo=ECHO, testing=TESTING, do_logging=DO_LOGGING, volume_mountpoint=volume_mountpoint, run_agotool_as_container=False)

### Create the Flask application and the Flask-SQLAlchemy object.
# app = flask.Flask(__name__)
# app = flask.Flask(__name__, template_folder=TEMPLATE_DIR)
app = flask.Flask(__name__, template_folder=TEMPLATES_FOLDER_ABSOLUTE)

if PROFILING:
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.config['PROFILE'] = True
    # app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir=r"/Users/dblyon/Downloads/profiling_agtool") # use qcachegrind to visualize
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[50]) # to view profiled code in shell
    ## from shell call: "qcachegrind"
    ## pyprof2calltree -i somethingsomething.prof -o something.prof
    ## open "something.prof" with qcachegrind -o something.prof

# if not DEBUG:
#     app.config['SQLALCHEMY_DATABASE_URI'] = connection.get_URL()
#     app.config['SQLALCHEMY_ECHO'] = False
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_RECORD_QUERIES'] = False

###################################
# Wrap the Api with swagger.docs. It is a thin wrapper around the Api class that adds some swagger smarts
# api = swagger.docs(Api(app), apiVersion='0.1')
###################################
# if not DEBUG:
#     db = flask_sqlalchemy.SQLAlchemy(app)
#     db.Model.metadata.reflect(db.engine)

# TEMPLATE_DIR = os.path.abspath(os.path.realpath(os.path.join(WORK_DIR, "static/templates")))
# TEMPLATES_FOLDER_ABSOLUTE = os.path.join(current_working_dir + '/web/templates')
# current_working_dir = os.getcwd()
# WEBSERVER_DATA = os.path.join(current_working_dir + '/data')
# EXAMPLE_FOLDER = os.path.join(WEBSERVER_DATA + '/exampledata')
# SESSION_FOLDER_ABSOLUTE = os.path.join(WEBSERVER_DATA + '/session')
# SESSION_FOLDER_RELATIVE = '/data/session'

app.config['EXAMPLE_FOLDER'] = EXAMPLE_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'tsv'}


# HOMEDIR = os.path.expanduser("~")
# FN_DATABASE_SCHEMA = os.path.join(HOMEDIR, "modules/cpr/metaprot/sql/DataBase_Schema_FDRiter.md")
# FN_DATABASE_SCHEMA_WITH_LINKS = os.path.join(TEMPLATES_FOLDER_ABSOLUTE, "db_schema.md")

### Additional path settings for flask
APP_ROOT = variables.APP_ROOT
DATA_DIR = variables.DATA_DIR
SCRIPT_DIR = variables.SCRIPT_DIR
# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(APP_ROOT, 'data')
# SCRIPT_DIR = os.path.join(APP_ROOT, 'scripts')
app.config['MAX_CONTENT_LENGTH'] = 100 * 2 ** 20

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


###############################################################################
##### Create the Flask-Restless API manager.
# manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
### Create API endpoints, which will be available at /api/<tablename> by
### default. Allowed HTTP methods can be specified as well.
# manager.create_api(models.Proteins, methods=['GET'], primary_key="an", include_columns=["an", "header", "aaseq"])
# manager.create_api(models.Peptides, methods=['GET'], primary_key="aaseq", include_columns=["aaseq", "an", "missedcleavages", "length"])
# manager.create_api(models.Taxa, methods=['GET'], primary_key="taxid", include_columns=["taxname", "taxid", "scientific"])
# manager.create_api(models.Taxid_2_rank, methods=['GET'], primary_key="taxid", include_columns=["taxid", "rank"])
# manager.create_api(models.Ogs, methods=['GET'], primary_key="og", include_columns=["og", "taxid", "description"])
# manager.create_api(models.Functions, methods=['GET'], primary_key="an", include_columns=["an", "type", "name"])
# manager.create_api(models.Ontologies, methods=['GET'], primary_key="child", include_columns=["child", "parent", "direct"])
# manager.create_api(models.Protein_2_og, methods=['GET'], primary_key="an", include_columns=["an", "og"])
# manager.create_api(models.Protein_2_version, methods=['GET'], primary_key="an", include_columns=["an", "version"])
# manager.create_api(models.Og_2_function, methods=['GET'], primary_key="og", include_columns=["og", "function"])
# manager.create_api(models.Protein_2_function, methods=['GET'], primary_key="an", include_columns=["an", "function"])
# manager.create_api(models.Function_2_definition, methods=['GET'], primary_key="function", include_columns=["function", "definition"])
# manager.create_api(models.Go_2_slim, methods=['GET'], primary_key="an", include_columns=["an", "slim"])
# manager.create_api(models.Protein_2_taxid, methods=['GET'], primary_key="an", include_columns=["an", "taxid"])

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
##### Maximum Time for MCL clustering
MAX_TIMEOUT = variables.MAX_TIMEOUT
################################################################################

################################################################################
#### pre-load objects
# if PRELOAD:
pqo = query.PersistentQueryObject()
##### pre-load go_dag and goslim_dag (obo files) for speed, also filter objects
upk_dag = obo_parser.GODag(obo_file=FN_KEYWORDS, upk=True)
goslim_dag = obo_parser.GODag(obo_file=FN_GO_SLIM)
go_dag = obo_parser.GODag(obo_file=FN_GO_BASIC)
# KEGG_id_2_name_dict = query.get_KEGG_id_2_name_dict() # delete
KEGG_pseudo_dag = obo_parser.KEGG_pseudo_dag()

for go_term in go_dag.keys():
    parents = go_dag[go_term].get_all_parents()

filter_ = cluster_filter.Filter(go_dag)

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
    return render_template('example.html')

@app.route('/example/<path:filename>', methods=['GET', 'POST'])
def download_example_data(filename):
    uploads = app.config['EXAMPLE_FOLDER']
    return send_from_directory(directory=uploads, filename=filename)

################################################################################
# # db_schema.html
# ################################################################################
# @app.route("/db_schema")
# def db_schema():
#     with open(FN_DATABASE_SCHEMA, "r") as fh:
#         content = fh.read()
#     content = Markup(markdown.markdown(content))
#     return render_template("db_schema.html", **locals())
#
# ################################################################################
# FAQ.html
################################################################################
@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

################################################################################
# helper functions
################################################################################

#####
# validation of user inputs
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

# def validate_inputfile(form, field):
#     filename = request.files['userinput_file'].filename
#     for extension in ALLOWED_EXTENSIONS:
#         if filename.endswith('.' + extension):
#             return True
#     raise wtforms.ValidationError(" file must have a '.txt' or '.tsv' extension")
#####

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
                                      # [validate_inputfile],
                                      description="""Expects a tab-delimited text-file ('.txt' or '.tsv') with the following 3 column-headers:

'population_an': UniProt accession numbers (such as 'P00359') for all proteins

'population_int': Protein abundance (intensity) for all proteins (copy number, iBAQ, or any other measure of abundance)

'sample_an': UniProt accession numbers for all proteins in the test group (the group you want to examine for GO term enrichment,
these identifiers should also be present in the 'population_an' as the test group is a subset of the population)

If "Abundance correction" is deselected "population_int" can be omitted.""")

    foreground_textarea = fields.TextAreaField("Foreground")
    background_textarea = fields.TextAreaField("Background & Intensity")

    gocat_upk = fields.SelectField("GO terms, UniProt keywords, or KEGG pathways",
                                   choices = (("all_GO", "all GO categories"),
                                              ("BP", "GO Biological Process"),
                                              ("CP", "GO Celluar Compartment"),
                                              ("MF", "GO Molecular Function"),
                                              ("UPK", "UniProt keywords"),
                                              ("KEGG", "KEGG pathways")),
                                   description="""Select either one or all three GO categories (molecular function, biological process, cellular component), UniProt keywords, or KEGG pathways.""")

    enrichment_method = fields.SelectField("Select one of the following methods",
                                   choices = (("abundance_correction", "abundance_correction"),
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
                                 description="""Apply the abundance correction as described in the publication. A column named "population_int" (population intensity)
that corresponds to the column "population_an" (population accession number) needs to be provided, when selecting this option.
If "Abundance correction" is deselected "population_int" can be omitted.""")

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

    backtracking = fields.BooleanField("Backtracking parent GO-terms",
                                       default = "checked",
                                       description="Include all parent GO-terms.")

    fold_enrichment_study2pop = fields.FloatField(
        "fold enrichment study/population",
        [validate_number], default = 0,
        description="""Minimum threshold value of "fold_enrichment_foreground_2_background".""")

    p_value_uncorrected =  fields.FloatField(
        "p-value uncorrected",
        [validate_float_between_zero_and_one],
        default = 0,
        description="""Maximum threshold value of "p_uncorrected".""")

    p_value_multipletesting =  fields.FloatField(
        "FDR-cutoff / p-value multiple testing",
        [validate_float_between_zero_and_one],
        default = 0,
        description="""Maximum FDR (for Benjamini-Hochberg) or p-values-corrected threshold value.""")

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
    if request.method == 'POST' and form.validate():
        input_fs = request.files['userinput_file']
        ui = userinput.Userinput(pqo, fn=input_fs, foreground_string=form.foreground_textarea.data, background_string=form.background_textarea.data,
            col_foreground='foreground', col_background='background', col_intensity='intensity',
            num_bins=form.num_bins.data, decimal='.', enrichment_method=form.enrichment_method.data,
            foreground_n=form.foreground_n.data, background_n=form.background_n.data)
        if ui.check:
            ip = request.environ['REMOTE_ADDR']
            string2log = "ip: " + ip + "\n" + "Request: results" + "\n"
            string2log += """gocat_upk: {}\ngo_slim_or_basic: {}\nindent: {}\nmultitest_method: {}\nalpha: {}\n\
o_or_u_or_both: {}\nabcorr: {}\nnum_bins: {}\nbacktracking: {}\nfold_enrichment_foreground_2_background: {}\n\
p_value_uncorrected: {}\np_value_mulitpletesting: {}\n""".format(form.gocat_upk.data,
                form.go_slim_or_basic.data, form.indent.data,
                form.multitest_method.data, form.alpha.data,
                form.o_or_u_or_both.data, form.abcorr.data, form.num_bins.data,
                form.backtracking.data, form.fold_enrichment_study2pop.data,
                form.p_value_uncorrected.data,
                form.p_value_multipletesting.data,
                form.enrichment_method.data,
                form.foreground_n.data, form.background_n.data)

            if not app.debug: # temp  remove line and
                log_activity(string2log) # remove indentation

            # if DEBUG:
            #     print("#"*80)
            #     print(ui.get_foreground_an_set())
            #     print("#" * 80)

            header, results = run.run(pqo, go_dag, goslim_dag, upk_dag, ui, form.gocat_upk.data,
                form.go_slim_or_basic.data, form.indent.data,
                form.multitest_method.data, form.alpha.data,
                form.o_or_u_or_both.data,
                form.backtracking.data, form.fold_enrichment_study2pop.data,
                form.p_value_uncorrected.data,
                form.p_value_multipletesting.data, KEGG_pseudo_dag)

        else:
            return render_template('info_check_input.html')

        if len(results) == 0:
            return render_template('results_zero.html')
        else:
            session_id = generate_session_id()
            return generate_result_page(header, results, form.gocat_upk.data,
                                        form.indent.data, session_id, form=Results_Form())
    return render_template('enrichment.html', form=form)

# @app.route("/bokeh")
# def polynomial():
#     """
#     Very simple embedding of a polynomial chart
#     """
#
#     # Grab the inputs arguments from the URL
#     args = flask.request.args
#
#     # Get all the form arguments in the url with defaults
#     color = colors[getitem(args, 'color', 'Black')]
#     _from = int(getitem(args, '_from', 0))
#     to = int(getitem(args, 'to', 10))
#
#     # Create a polynomial line graph with those arguments
#     x = list(range(_from, to + 1))
#     fig = figure(title="Polynomial")
#     fig.line(x, [i ** 2 for i in x], color=color, line_width=2)
#
#     js_resources = INLINE.render_js()
#     css_resources = INLINE.render_css()
#
#     script, div = components(fig)
#     html = flask.render_template(
#         'bokeh.html',
#         plot_script=script,
#         plot_div=div,
#         js_resources=js_resources,
#         css_resources=css_resources,
#         color=color,
#         _from=_from,
#         to=to
#     )
#     return encode_utf8(html)

def generate_result_page(header, results, gocat_upk, indent, session_id, form, errors=()):
    header = header.rstrip().split("\t")
    ellipsis_indices = elipsis(header)
    results2display = []
    for res in results:
        results2display.append(res.split('\t'))
    file_name = "results_orig" + session_id + ".tsv"
    fn_results_orig_absolute = os.path.join(SESSION_FOLDER_ABSOLUTE, file_name)
    fn_results_orig_relative = os.path.join(SESSION_FOLDER_RELATIVE, file_name)
    tsv = (u'%s\n%s\n' % (u'\t'.join(header), u'\n'.join(results)))
    with open(fn_results_orig_absolute, 'w') as fh:
        fh.write(tsv)
    return render_template('results.html', header=header, results=results2display, errors=errors,
                           file_path=fn_results_orig_relative, ellipsis_indices=ellipsis_indices,
                           gocat_upk=gocat_upk, indent=indent, session_id=session_id, form=form)

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
    gocat_upk = request.form['gocat_upk']
    indent = request.form['indent']
    file_name, fn_results_orig_absolute, fn_results_orig_relative = fn_suffix2abs_rel_path("orig", session_id)
    header, results = read_results_file(fn_results_orig_absolute)
    return generate_result_page(header, results, gocat_upk, indent, session_id, form=Results_Form())

################################################################################
# results_filtered.html
################################################################################
@app.route('/results_filtered', methods=["GET", "POST"])
def results_filtered():
    indent = request.form['indent']
    gocat_upk = request.form['gocat_upk']
    session_id = request.form['session_id']

    # original unfiltered/clustered results
    file_name, fn_results_orig_absolute, fn_results_orig_relative = fn_suffix2abs_rel_path("orig", session_id)
    header, results = read_results_file(fn_results_orig_absolute)

    if not gocat_upk == "UPK":
        results_filtered = filter_.filter_term_lineage(header, results, indent)

        # filtered results
        file_name, fn_results_filtered_absolute, fn_results_filtered_relative = fn_suffix2abs_rel_path("filtered", session_id)
        tsv = (u'%s\n%s\n' % (header, u'\n'.join(results_filtered)))
        with open(fn_results_filtered_absolute, 'w') as fh:
            fh.write(tsv)
        header = header.split("\t")
        ellipsis_indices = elipsis(header)
        results2display = []
        for res in results_filtered:
            results2display.append(res.split('\t'))
        ip = request.environ['REMOTE_ADDR']
        string2log = "ip: " + ip + "\n" + "Request: results_filtered" + "\n"
        string2log += """gocat_upk: {}\nindent: {}\n""".format(gocat_upk, indent)
        log_activity(string2log)
        return render_template('results_filtered.html', header=header, results=results2display, errors=[],
                               file_path_orig=fn_results_orig_relative, file_path_filtered=fn_results_filtered_relative,
                               ellipsis_indices=ellipsis_indices, gocat_upk=gocat_upk, indent=indent, session_id=session_id)
    else:
        return render_template('index.html')

################################################################################
# results_clustered.html
################################################################################
@app.route('/results_clustered', methods=["GET", "POST"])
def results_clustered():
    form = Results_Form(request.form)
    inflation_factor = form.inflation_factor.data
    session_id = request.form['session_id']
    gocat_upk = request.form['gocat_upk']
    indent = request.form['indent']
    file_name, fn_results_orig_absolute, fn_results_orig_relative = fn_suffix2abs_rel_path("orig", session_id)
    header, results = read_results_file(fn_results_orig_absolute)
    if not form.validate():
        return generate_result_page(header, results, gocat_upk, indent, session_id, form=form)
    try:
        mcl = cluster_filter.MCL(SESSION_FOLDER_ABSOLUTE, MAX_TIMEOUT)
        cluster_list = mcl.calc_MCL_get_clusters(session_id, fn_results_orig_absolute, inflation_factor)
    except cluster_filter.TimeOutException:
        return generate_result_page(header, results, gocat_upk, indent, session_id, form=form, errors=['MCL timeout: The maximum time (20min) for clustering has exceeded. Your original results are being displayed.'])

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
    string2log += """gocat_upk: {}\nindent: {}\nnum_clusters: {}\ninflation_factor: {}\n""".format(gocat_upk, indent, num_clusters, inflation_factor)
    log_activity(string2log)
    return render_template('results_clustered.html', header=header, results2display=results2display, errors=[],
                           file_path_orig=fn_results_orig_relative, file_path_mcl=fn_results_clustered_relative,
                           ellipsis_indices=ellipsis_indices, gocat_upk=gocat_upk, indent=indent, session_id=session_id,
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
    # ToDo: All proteins without abundance data are disregarded (will be placed in a separate bin in next update)
    ################################################################################

    # app.run(host='0.0.0.0', DEBUG=True, processes=8)
    app.run(host='0.0.0.0', port=5911, processes=2, debug=variables.DEBUG)

