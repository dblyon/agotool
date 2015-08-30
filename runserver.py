# coding=utf-8
# standard library
import os
import sys
import StringIO
import logging
import time

# third party
import flask
from flask import render_template, request, send_from_directory
import wtforms
from wtforms import fields
import pandas as pd
import numpy as np

# local application
sys.path.append('static/python')
import run
import obo_parser
import cluster_filter

app = flask.Flask(__name__)
webserver_data  = os.getcwd() + '/static/data'
EXAMPLE_FOLDER = webserver_data + '/exampledata'
SESSION_FOLDER_ABSOLUTE = webserver_data + '/session'
SESSION_FOLDER_RELATIVE = '/static/data/session'
app.config['EXAMPLE_FOLDER'] = EXAMPLE_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'tsv'}

# Additional path settings for flask
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_ROOT, 'data')
SCRIPT_DIR = os.path.join(APP_ROOT, 'scripts')
app.config['MAX_CONTENT_LENGTH'] = 100 * 2 ** 20

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

if not app.debug:
    #########################
    # log warnings and errors
    from logging import FileHandler
    file_handler = FileHandler("./logs/log_agotool.txt", mode="a", encoding="UTF-8")
    file_handler.setFormatter(logging.Formatter("#"*80 + "\n" + '%(asctime)s %(levelname)s: %(message)s'))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

profiling = False
if profiling:
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

species2files_dict = {
    "9606": {'goa_ref_fn': webserver_data + r'/GOA/9606.tsv',
           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/9606.tab'},
    "4932": {'goa_ref_fn': webserver_data + r'/GOA/4932.tsv',
           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/4932.tab'},
    "3702": {'goa_ref_fn': webserver_data + r'/GOA/3702.tsv',
           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/3702.tab'},
    "7955": {'goa_ref_fn': webserver_data + r'/GOA/7955.tsv',
           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/7955.tab'},
    "7227": {'goa_ref_fn': webserver_data + r'/GOA/7227.tsv',
           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/7227.tab'},
    "9031": {'goa_ref_fn': webserver_data + r'/GOA/9031.tsv',
           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/9031.tab'},
    "10090": {'goa_ref_fn': webserver_data + r'/GOA/10090.tsv',
       'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/10090.tab'},
    "10116": {'goa_ref_fn': webserver_data + r'/GOA/10116.tsv',
       'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/10116.tab'}
    }

# pre-load go_dag and goslim_dag (obo files) for speed, also filter objects
obo2file_dict = {"slim": webserver_data + r'/OBO/goslim_generic.obo',
                 "basic": webserver_data + r'/OBO/go-basic.obo'}
go_dag = obo_parser.GODag(obo_file=obo2file_dict['basic'])
goslim_dag = obo_parser.GODag(obo_file=obo2file_dict['slim'])
filter_ = cluster_filter.Filter(go_dag)

organism_choices = [
    (u'4932',  u'Saccharomyces cerevisiae'), # Yeast
    (u'9606',  u'Homo sapiens'), # Human
    (u'3702',  u'Arabidopsis thaliana'), # Arabidopsis
    (u'7955',  u'Danio rerio'), # Zebrafish
    (u'7227',  u'Drosophila melanogaster'), # Fly
    (u'9031',  u'Gallus gallus'), # Chicken
    (u'10090', u'Mus musculus'), # Mouse
    (u'10116', u'Rattus norvegicus') # Rat
    ]

################################################################################
# index.html
################################################################################
@app.route('/')
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
# helper functions
################################################################################
# check user input
def check_userinput(userinput_fh, abcorr):
    decimal = '.'
    df = pd.read_csv(userinput_fh, sep='\t', decimal=decimal)
    userinput_fh.seek(0)
    if abcorr:
        if len({'population_an','population_int','sample_an'}.intersection(set(df.columns.tolist()))) == 3:
            try:
                np.histogram(df['population_int'], bins=10)
            except TypeError:
                try:
                    decimal = ','
                    df = pd.read_csv(userinput_fh, sep='\t', decimal=decimal)
                    userinput_fh.seek(0)
                    np.histogram(df['population_int'], bins=10)
                except TypeError:
                    return False, decimal
            return True, decimal
    else:
        if len({'population_an', 'sample_an'}.intersection(set(df.columns.tolist()))) == 2:
            return True, decimal
    return False, decimal

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

def validate_inputfile(form, field):
    filename = request.files['userinput_file'].filename
    for extension in ALLOWED_EXTENSIONS:
        if filename.endswith('.' + extension):
            return True
    raise wtforms.ValidationError(
        " file must have a '.txt' or '.tsv' extension")
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
        ans_index = header.index("ANs_study")
    except ValueError:
        ans_index = header.index("ANs_pop")
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

    organism = fields.SelectField(u'Select Organism',
                                  choices = organism_choices,
                                  description="""Choose the species/organism the identifiers (accession numbers) correspond to.""")

    userinput_file = fields.FileField("Choose File",
                                      [validate_inputfile],
                                      description="""Expects a tab-delimited text-file ('.txt' or '.tsv') with the following 3 column-headers:

'population_an': UniProt accession numbers (such as 'P00359') for all proteins

'population_int': Protein abundance (intensity) for all proteins (copy number, iBAQ, or any other measure of abundance)

'sample_an': UniProt accession numbers for all proteins in the test group (the group you want to examine for GO term enrichment,
these identifiers should also be present in the 'population_an' as the test group is a subset of the population)

If "Abundance correction" is deselected "population_int" can be omitted.""")

    gocat_upk = fields.SelectField("GO-terms / UniProt-keywords",
                                   choices = (("all_GO", "all 3 GO categories"),
                                              ("BP", "Biological Process"),
                                              ("CP", "Celluar Compartment"),
                                              ("MF", "Molecular Function"),
                                              ("UPK", "UniProt-keywords")),
                                   description="""Select either one of three major GO categories (molecular function, biological process, cellular component) or all three or UniProt-keywords.""")

    abcorr = fields.BooleanField("Abundance correction",
                                 default = "checked",
                                 description="""Apply the abundance correction as described in the publication. A column named "population_int" (population intensity)
that corresponds to the column "population_an" (population accession number) needs to be provided, when selecting this option.
If "Abundance correction" is deselected "population_int" can be omitted.""")

    go_slim_or_basic = fields.SelectField("GO basic or slim",
                                          choices = (("basic", "basic"),
                                                     ("slim", "slim")),
                                          description="""Choose between the full Gene Ontology or GO slim subset a subset of GO terms that are less fine grained.""")

    indent = fields.BooleanField("prepend GO-term level by dots",
                                 default="checked",
                                 description="Add dots to GO-terms to indicate the level in the parental hierarchy.")

    multitest_method = fields.SelectField(
        "Method for correction of multiple testing",
        choices = (("benjamini_hochberg", "Benjamini Hochberg"),
                   ("sidak", "Sidak"), ("holm", "Holm"),
                   ("bonferroni", "Bonferroni")),
        description="""Select a method for multiple testing correction.""")

    alpha = fields.FloatField("Alpha", [validate_float_larger_zero_smaller_one],
                              default = 0.05, description="""Applied to multiple correction methods "Sidak" and "Holm" to calculate "corrected" p-values.""")

    o_or_u_or_both = fields.SelectField("over- or under-represented or both",
                                        choices = (("both", "both"),
                                                   ("o", "overrepresented"),
                                                   ("u", "underrepresented")),
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
        description="""Minimum threshold value of "fold_enrichment_study2pop".""")

    p_value_uncorrected =  fields.FloatField(
        "p-value uncorrected",
        [validate_float_between_zero_and_one],
        default = 0,
        description="""Maximum threshold value of "p_uncorrected".""")

    p_value_mulitpletesting =  fields.FloatField(
        "FDR-cutoff / p-value multiple testing",
        [validate_float_between_zero_and_one],
        default = 0,
        description="""Maximum FDR (for Benjamini-Hochberg) or p-values-corrected threshold value.""")

@app.route('/enrichment')
def enrichment():
    return render_template('enrichment.html', form=Enrichment_Form())

################################################################################
# results.html
################################################################################
class Results_Form(wtforms.Form):
    inflation_factor = fields.FloatField("inflation factor", [validate_inflation_factor],
                                         default = 2.0, description="""Clustering can take a long time, depends on size of data and inflation factor.
Please be patient.""")

@app.route('/results', methods=["GET", "POST"])
def results():
    """
    cluster_list: nested ListOfString corresponding to indices of results
    results_filtered = filter(header, results, indent)
    results_filtered: reduced version of results
    """
    form = Enrichment_Form(request.form)
    if request.method == 'POST' and form.validate():
        user_input_file = request.files['userinput_file']
        userinput_fh = StringIO.StringIO(user_input_file.read())
        check, decimal = check_userinput(userinput_fh, form.abcorr.data)
        if check:
            header, results = run.run(
                userinput_fh, decimal, form.organism.data, form.gocat_upk.data,
                form.go_slim_or_basic.data, form.indent.data,
                form.multitest_method.data, form.alpha.data,
                form.o_or_u_or_both.data, form.abcorr.data, form.num_bins.data,
                form.backtracking.data, form.fold_enrichment_study2pop.data,
                form.p_value_uncorrected.data,
                form.p_value_mulitpletesting.data, species2files_dict, go_dag,
                goslim_dag)
        else:
            return render_template('info_check_input.html')

        if len(results) == 0:
            return render_template('results_zero.html')
        else:
            session_id = generate_session_id()
            return generate_result_page(header, results, form.gocat_upk.data,
                                        form.indent.data, session_id, form=Results_Form())
    return render_template('enrichment.html', form=form)

def generate_result_page(header, results, gocat_upk, indent, session_id, form):
    header = header.rstrip().split("\t")
    ellipsis_indices = elipsis(header)
    results2display = []
    for res in results:
        results2display.append(res.split('\t'))
    file_name = "results_orig" + session_id + ".tsv"
    fn_results_orig_absolute = os.path.join(SESSION_FOLDER_ABSOLUTE, file_name)
    fn_results_orig_relative = os.path.join(SESSION_FOLDER_RELATIVE, file_name)
    tsv = (u'%s\n%s\n' % (u'\t'.join(header), u'\n'.join(results)))
    with open(fn_results_orig_absolute, 'w') as f:
        f.write(tsv)
    return render_template('results.html', header=header, results=results2display, errors=[],
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
    # ipdb.set_trace()
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
        with open(fn_results_filtered_absolute, 'w') as f:
            f.write(tsv)
        header = header.split("\t")
        ellipsis_indices = elipsis(header)
        results2display = []
        for res in results_filtered:
            results2display.append(res.split('\t'))
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
    mcl = cluster_filter.MCL(SESSION_FOLDER_ABSOLUTE)
    cluster_list = mcl.calc_MCL_get_clusters(session_id, fn_results_orig_absolute, inflation_factor)
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
    return render_template('results_clustered.html', header=header, results2display=results2display, errors=[],
                           file_path_orig=fn_results_orig_relative, file_path_mcl=fn_results_clustered_relative,
                           ellipsis_indices=ellipsis_indices, gocat_upk=gocat_upk, indent=indent, session_id=session_id,
                           num_clusters=num_clusters, inflation_factor=inflation_factor)

def fn_suffix2abs_rel_path(suffix, session_id):
    file_name = "results_" + suffix + session_id + ".tsv"
    fn_results_absolute = os.path.join(SESSION_FOLDER_ABSOLUTE, file_name)
    fn_results_relative = os.path.join(SESSION_FOLDER_RELATIVE, file_name)
    return file_name, fn_results_absolute, fn_results_relative


if __name__ == '__main__':


    if profiling:
        app.run('localhost', 5000, debug=True)
    else:
        # app.run('0.0.0.0', 5911, processes=4, debug=False)
        # app.run('red', 5911, processes=4, debug=False)
        app.run('localhost', 5000, processes=4, debug=True)
