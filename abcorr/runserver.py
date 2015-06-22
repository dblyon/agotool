import os, sys, logging, wtforms
from wtforms import fields
# Setup for flask
import flask
from flask import render_template, request, send_from_directory
from werkzeug import secure_filename
import pandas as pd




# import 'back end' scripts
sys.path.append('static/python')
import gotupk

home = os.path.expanduser("~")

app = flask.Flask(__name__)

##### upload file
UPLOAD_FOLDER = home + r'/CloudStation/CPR/Brian_GO/webserver_data/userdata'
EXAMPLE_FOLDER = home + r'/CloudStation/CPR/Brian_GO/webserver_data/exampledata'
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXAMPLE_FOLDER'] = EXAMPLE_FOLDER


# Additional path settings for flask
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_ROOT, 'data')
SCRIPT_DIR = os.path.join(APP_ROOT, 'scripts')

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

def resultfile_to_results(result_file):
    result_file.seek(0)
    header = result_file.readline().rstrip().split('\t')
    results = [line.split('\t') + [''] for line in result_file]
    result_file.seek(0)
    return results, header

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
# gotupk_results_zero.html
################################################################################
@app.route('/results_zero')
def gotupk_results_zero():
    return render_template('gotupk_results_zero.html')

################################################################################
@app.route('/results/<path:filename>', methods=['GET', 'POST'])
def download_results(filename):
    uploads = app.config['UPLOAD_FOLDER']
    return send_from_directory(directory=uploads, filename=filename)

################################################################################
def check_userinput(userinput_fn, decimal, abcorr):
    df = pd.read_csv(userinput_fn, sep='\t', decimal=decimal)
    if abcorr:
        if ['background_an', 'background_int', 'sample_an'] == sorted(df.columns.tolist()):
            return True
    else:
        if ['background_an', 'sample_an'] == sorted(df.columns.tolist()):
            return True
    return False

################################################################################
@app.route('/example')
def example():
    return render_template('example.html')

@app.route('/example/<path:filename>', methods=['GET', 'POST'])
def download_example_data(filename):
    uploads = app.config['EXAMPLE_FOLDER']
    return send_from_directory(directory=uploads, filename=filename)
################################################################################

################################################################################
# UniProtKeywords
################################################################################
class UniProtKeywords_Form(wtforms.Form):
    organism_choices = [
    (u'4932',  u'Saccharomyces cerevisiae'), # Yeast
    (u'9606',  u'Homo sapiens'), # Human
    (u'3702',  u'Arabidopsis thaliana'), # Arabidopsis
    (u'7955',  u'Danio rerio'), # Zebrafish
    (u'7227',  u'Drosophila melanogaster'), # Fly
    (u'9031',  u'Gallus gallus'), # Chicken
    (u'10090', u'Mus musculus'), # Mouse
    (u'10116', u'Rattus norvegicus'), # Rat
    (u'8364',  u'Xenopus (Silurana) tropicalis')] # Frog
    organism = fields.SelectField(u'Select Organism', choices = organism_choices)
    decimal = fields.SelectField("Decimal delimiter",
                                 choices = ((",", "Comma"), (".", "Point")),
                                 description = u"either a ',' or a '.' used for abundance values")
    abcorr = fields.BooleanField("Abundance correction", default = "checked")
    multitest_method = fields.SelectField("Correction for multiple testing Method",
                                choices = (("benjamini_hochberg", "Benjamini Hochberg"), ("sidak", "Sidak"), ("holm", "Holm"), ("bonferroni", "Bonferroni")))
    alpha = fields.FloatField("Alpha", default = 0.05, description=u"for multiple testing correction")
    o_or_e_or_both = fields.SelectField("overrepresented or underrepresented or both",
                                 choices = (("both", "both"), ("o", "overrepresented"), ("u", "underrepresented"))) #!!! ? why does it switch to 'both' here???
    num_bins = fields.IntegerField("Number of bins", default = 100)
    fold_enrichment_study2pop = fields.FloatField("fold enrichment study/background", default = 0)
    p_value_uncorrected =  fields.FloatField("p value uncorrected", default = 0)
    p_value_mulitpletesting =  fields.FloatField("p value multiple testing", default = 0)

@app.route('/UniProtKeywords')
def UniProtKeywords():
    return render_template('UniProtKeywords.html', form=UniProtKeywords_Form())

@app.route('/upk_results', methods=['POST'])
def upk_results():
    form = UniProtKeywords_Form(request.form)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            userinput_fn = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            gocat_upk = "UPK"
            go_slim_or_basic = "basic"
            indent = False
            backtracking = False
            if check_userinput(userinput_fn, form.decimal.data, form.abcorr.data):
                header, results = gotupk.run(userinput_fn, form.decimal.data, form.organism.data,
                                    gocat_upk, go_slim_or_basic, indent, form.multitest_method.data,
                                    form.alpha.data, form.o_or_e_or_both.data, form.abcorr.data, form.num_bins.data,
                                    backtracking, form.fold_enrichment_study2pop.data, form.p_value_uncorrected.data,
                                   form.p_value_mulitpletesting.data)
            else:
                return render_template('info_check_input.html')
            if len(results) == 0:
                return render_template('gotupk_results_zero.html')
            else:
                header = header.split("\t")
                results2display = []
                for res in results:
                    results2display.append(res.split('\t'))
                return render_template('gotupk_results.html', header=header, results=results2display, errors=[]) #tsv=tsv,
    return render_template('UniProtKeywords.html', form=UniProtKeywords_Form())

################################################################################
# GOTerms
################################################################################
class GOTerms_Form(wtforms.Form):
    organism_choices = [
    (u'4932',  u'Saccharomyces cerevisiae'), # Yeast
    (u'9606',  u'Homo sapiens'), # Human
    (u'3702',  u'Arabidopsis thaliana'), # Arabidopsis
    (u'7955',  u'Danio rerio'), # Zebrafish
    (u'7227',  u'Drosophila melanogaster'), # Fly
    (u'9031',  u'Gallus gallus'), # Chicken
    (u'10090', u'Mus musculus'), # Mouse
    (u'10116', u'Rattus norvegicus')] # Rat
    organism = fields.SelectField(u'Select Organism', choices = organism_choices)
    decimal = fields.SelectField("Decimal delimiter",
                                 choices = ((",", "Comma"), (".", "Point")),
                                 description = u"either a ',' or a '.' used for abundance values")
    gocat_upk = fields.SelectField("GO-terms",
                                choices = (("all_GO", "all 3 GO categories"),("BP", "Biological Process"),
                                           ("CP", "Celluar Compartment"),("MF", "Molecular Function")))
    abcorr = fields.BooleanField("Abundance correction", default = "checked")
    go_slim_or_basic = fields.SelectField("GO basic or slim",
                                 choices = (("basic", "basic"), ("slim", "slim")))
    indent = fields.BooleanField("prepend GO-term level by dots", default = "checked")
    multitest_method = fields.SelectField("Correction for multiple testing Method",
                                choices = (("benjamini_hochberg", "Benjamini Hochberg"), ("sidak", "Sidak"), ("holm", "Holm"), ("bonferroni", "Bonferroni")))
    alpha = fields.FloatField("Alpha", default = 0.05, description=u"for multiple testing correction")
    o_or_e_or_both = fields.SelectField("overrepresented or underrepresented or both",
                                 choices = (("both", "both"), ("o", "overrepresented"), ("u", "underrepresented"))) #!!! ? why does it switch to 'both' here???
    num_bins = fields.IntegerField("Number of bins", default = 100)
    backtracking = fields.BooleanField("Backtracking parent GO-terms", default = "checked")
    fold_enrichment_study2pop = fields.FloatField("fold enrichment study/background", default = 0)
    p_value_uncorrected =  fields.FloatField("p value uncorrected", default = 0)
    p_value_mulitpletesting =  fields.FloatField("p value multiple testing", default = 0)

@app.route('/GOTerm')
def GOTerms():
    return render_template('GOTerms.html', form=GOTerms_Form())

@app.route('/got_results', methods=['POST'])
def got_results():
    form = GOTerms_Form(request.form)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            userinput_fn = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if check_userinput(userinput_fn, form.decimal.data, form.abcorr.data):
                header, results = gotupk.run(userinput_fn, form.decimal.data, form.organism.data,
                   form.gocat_upk.data, form.go_slim_or_basic.data, form.indent.data,
                   form.multitest_method.data, form.alpha.data, form.o_or_e_or_both.data,
                   form.abcorr.data, form.num_bins.data, form.backtracking.data,
                   form.fold_enrichment_study2pop.data, form.p_value_uncorrected.data,
                   form.p_value_mulitpletesting.data)
            else:
                return render_template('info_check_input.html')
            if len(results) == 0:
                return render_template('gotupk_results_zero.html')
            else:
                header = header.split("\t")
                results2display = []
                for res in results:
                    results2display.append(res.split('\t'))
                return render_template('gotupk_results.html', header=header, results=results2display, errors=[]) #tsv=tsv,
    return render_template('GOTerms.html', form=GOTerms_Form())

################################################################################






if __name__ == '__main__':
    app.run(processes=4, debug=True)















