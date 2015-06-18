import os, sys, logging, wtforms
import StringIO
import collections
import time
import itertools
from wtforms import fields, validators
# Setup for flask
import flask
from flask import render_template, request, Flask, redirect, url_for, send_from_directory
from werkzeug import secure_filename


# import 'back end' scripts
sys.path.append('static/python')
import penrichment
import gotupk

home = os.path.expanduser("~")

app = flask.Flask(__name__)

##### upload file
UPLOAD_FOLDER = home + r'/CloudStation/CPR/Brian_GO/webserver_data/userdata'
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Additional path settings for flask
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_ROOT, 'data')
SCRIPT_DIR = os.path.join(APP_ROOT, 'scripts')

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

################################################################################
# Globals
################################################################################


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

@app.route('/gotupk_results_zero')
def gotupk_results_zero():
    return render_template('gotupk_results_zero.html')


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
    e_or_p_or_both = fields.SelectField("enriched or purified or both",
                                 choices = (("both", "both"), ("e", "enriched"), ("p", "purified"))) #!!! ? why does it switch to 'both' here???
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

            header, results = gotupk.run(userinput_fn, form.decimal.data, form.organism.data,
               gocat_upk, go_slim_or_basic, indent,
               form.multitest_method.data, form.alpha.data, form.e_or_p_or_both.data,
               form.abcorr.data, form.num_bins.data, backtracking,
               form.fold_enrichment_study2pop.data, form.p_value_uncorrected.data,
               form.p_value_mulitpletesting.data)
            if len(results) == 0:
                return render_template('gotupk_results_zero.html')
            else:
                header = header.split("\t")
                results2display = []
                for res in results:
                    results2display.append(res.split('\t'))
                return render_template('gotupk_results.html', header=header, results=results2display, errors=[]) #tsv=tsv,
    return render_template('UniProtKeywords.html', form=GOTUPK_file_upload_Form())

################################################################################
@app.route('/gotupk_results/<path:filename>', methods=['GET', 'POST'])
def download_results(filename):
    uploads = app.config['UPLOAD_FOLDER']
    return send_from_directory(directory=uploads, filename=filename)
################################################################################

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
    e_or_p_or_both = fields.SelectField("enriched or purified or both",
                                 choices = (("both", "both"), ("e", "enriched"), ("p", "purified"))) #!!! ? why does it switch to 'both' here???
    num_bins = fields.IntegerField("Number of bins", default = 100)
    backtracking = fields.BooleanField("Backtracking parent GO-terms", default = "checked")
    fold_enrichment_study2pop = fields.FloatField("fold enrichment study/background", default = 0)
    p_value_uncorrected =  fields.FloatField("p value uncorrected", default = 0)
    p_value_mulitpletesting =  fields.FloatField("p value multiple testing", default = 0)

@app.route('/GOTerms')
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
            header, results = gotupk.run(userinput_fn, form.decimal.data, form.organism.data,
               form.gocat_upk.data, form.go_slim_or_basic.data, form.indent.data,
               form.multitest_method.data, form.alpha.data, form.e_or_p_or_both.data,
               form.abcorr.data, form.num_bins.data, form.backtracking.data,
               form.fold_enrichment_study2pop.data, form.p_value_uncorrected.data,
               form.p_value_mulitpletesting.data)
            if len(results) == 0:
                return render_template('gotupk_results_zero.html')
            else:
                header = header.split("\t")
                results2display = []
                for res in results:
                    results2display.append(res.split('\t'))
                return render_template('gotupk_results.html', header=header, results=results2display, errors=[]) #tsv=tsv,
    return render_template('GOTerms.html', form=GOTUPK_file_upload_Form())

################################################################################







# ###############################################################################
# upload.html
# ###############################################################################

#
# class Upload(wtforms.Form):
#     pass
#
#
# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return render_template('about.html')
#             # return redirect(url_for('uploaded', filename=filename))
#     return render_template('upload.html')
#
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#
# ################################################################################
# ################################################################################
# ################################################################################
# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     problemes = Probleme.query.all()
#     if 'user' not in session:
#         return redirect(url_for('login'))
#     if request.method == 'POST':
#         delete = Probleme.query.filter_by(id=request.form['del_button']).first()
#         db.session.delete(delete)
#         db.session.commit()
#         return redirect(url_for('dashboard'))
#     return render_template('dashboard.html', problemes=problemes)
#
# <td><a href="{{ url_for('download', filename=probleme.facture) }}">Facture</a></td>
#
# @app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
#     uploads = os.path.join(current_app.root_folder, app.config['UPLOAD_FOLDER'])
#     return send_from_directory(directory=uploads, filename=filename)


################################################################################
################################################################################
################################################################################




################################################################################
# GOTUPK FILE UPLOAD
################################################################################
# class GOTUPK_file_upload_Form(wtforms.Form):
#     # userinput_file = fields.FileField(u"Input File")
#     #         <div>{{form.userinput_file.label}}: {{form.userinput_file(class="filestyle btn-info")}}</div>
#
#     organism = fields.SelectField(u'Select Organism', choices = organism_choices)
#     decimal = fields.SelectField("Decimal delimiter",
#                                  choices = ((",", "Comma"), (".", "Point")),
#                                  description = u"either a ',' or a '.' used for abundance values")
#     gocat_upk = fields.SelectField("GO-terms or UniProt-Keywords",
#                                 choices = (("UPK", "UniProt Keywords"),
#                                            ("all_GO", "all 3 GO categories"),("BP", "Biological Process"),
#                                            ("CP", "Celluar Compartment"),("MF", "Molecular Function")))
#     abcorr = fields.BooleanField("Abundance correction", default = "checked")
#     go_slim_or_basic = fields.SelectField("GO basic or slim",
#                                  choices = (("basic", "basic"), ("slim", "slim")))
#     indent = fields.BooleanField("prepend GO-term level by dots", default = "checked")
#     multitest_method = fields.SelectField("Correction for multiple testing Method",
#                                 choices = (("benjamini_hochberg", "Benjamini Hochberg"), ("sidak", "Sidak"), ("holm", "Holm"), ("bonferroni", "Bonferroni")))
#     alpha = fields.FloatField("Alpha", default = 0.05, description=u"for multiple testing correction")
#     e_or_p_or_both = fields.SelectField("enriched or purified or both",
#                                  choices = (("both", "both"), ("e", "enriched"), ("p", "purified"))) #!!! ? why does it switch to 'both' here???
#     num_bins = fields.IntegerField("Number of bins", default = 100)
#     backtracking = fields.BooleanField("Backtracking parent GO-terms", default = "checked")
#     fold_enrichment_study2pop = fields.FloatField("fold enrichment study/background", default = 0)
#     p_value_uncorrected =  fields.FloatField("p value uncorrected", default = 0)
#     p_value_mulitpletesting =  fields.FloatField("p value multiple testing", default = 0)
#
# @app.route('/upload')
# def upload():
#     return render_template('upload.html', form=GOTUPK_file_upload_Form())
#
# @app.route('/GOTUPK_file_upload_result', methods=['POST'])
# def submit_GOTUPK_file_upload():
#     form = GOTUPK_file_Form(request.form)
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             userinput_fn = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             header, results = gotupk.run(userinput_fn, form.decimal.data, form.organism.data,
#                form.gocat_upk.data, form.go_slim_or_basic.data, form.indent.data,
#                form.multitest_method.data, form.alpha.data, form.e_or_p_or_both.data,
#                form.abcorr.data, form.num_bins.data, form.backtracking.data,
#                form.fold_enrichment_study2pop.data, form.p_value_uncorrected.data,
#                form.p_value_mulitpletesting.data)
#             # tsv = '%s\n%s\n' % ('\t'.join(header), '\n'.join(['\t'.join(x) for x in results]))
#             header = header.split("\t")
#             # tsv = '%s\n%s\n' % (header, results)
#             # tsv.encode('base64')
#             results2display = []
#             for res in results:
#                 results2display.append(res.split('\t'))
#             return render_template('GOTUPK_file_upload_result.html', header=header, results=results2display, errors=[]) #tsv=tsv,
#             # return render_template('GOTUPK_file_result.html')
#     return render_template('upload.html', form=GOTUPK_file_upload_Form())
#
# @app.route('/GOTUPK_file_upload_result/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
#     uploads = app.config['UPLOAD_FOLDER'] #+ r'/results.txt'
#     return send_from_directory(directory=uploads, filename=filename)


################################################################################
# GOTUPK FILE
# ################################################################################
# class GOTUPK_file_Form(wtforms.Form):
#     userinput_file = fields.FileField(u"Input File", id=file)
#     organism = fields.SelectField(u'Select Organism', choices = organism_choices)
#     decimal = fields.SelectField("Decimal delimiter",
#                                  choices = ((",", "Comma"), (".", "Point")),
#                                  description = u"either a ',' or a '.' used for abundance values")
#     gocat_upk = fields.SelectField("GO-terms or UniProt-Keywords",
#                                 choices = (("UPK", "UniProt Keywords"),
#                                            ("all_GO", "all 3 GO categories"),("BP", "Biological Process"),
#                                            ("CP", "Celluar Compartment"),("MF", "Molecular Function")))
#     abcorr = fields.BooleanField("Abundance correction", default = "checked")
#     go_slim_or_basic = fields.SelectField("GO basic or slim",
#                                  choices = (("basic", "basic"), ("slim", "slim")))
#     indent = fields.BooleanField("prepend GO-term level by dots", default = "checked")
#     multitest_method = fields.SelectField("Correction for multiple testing Method",
#                                 choices = (("benjamini_hochberg", "Benjamini Hochberg"), ("sidak", "Sidak"), ("holm", "Holm"), ("bonferroni", "Bonferroni")))
#     alpha = fields.FloatField("Alpha", default = 0.05, description=u"for multiple testing correction")
#     e_or_p_or_both = fields.SelectField("enriched or purified or both",
#                                  choices = (("both", "both"), ("e", "enriched"), ("p", "purified"))) #!!! ? why does it switch to 'both' here???
#     num_bins = fields.IntegerField("Number of bins", default = 100)
#     backtracking = fields.BooleanField("Backtracking parent GO-terms", default = "checked")
# ###### Filter rows
#     fold_enrichment_study2pop = fields.FloatField("fold enrichment study/background", default = 0)
#     p_value_uncorrected =  fields.FloatField("p value uncorrected", default = 0)
#     p_value_mulitpletesting =  fields.FloatField("p value multiple testing", default = 0)
#
# @app.route('/GOTUPK_file')
# def GOTUPK_file():
#     return render_template('GOTUPK_file.html', form=GOTUPK_file_Form())
#
# @app.route('/GOTUPK_file_result', methods=["POST"])
# def submit_GOTUPK_file():
#     form = GOTUPK_file_Form(request.form)
#     # result_file = StringIO.StringIO()
#     # results, header = resultfile_to_results(result_file)
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             userinput_fn = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             header, results = gotupk.run(userinput_fn, form.decimal.data, form.organism.data,
#                form.gocat_upk.data, form.go_slim_or_basic.data, form.indent.data,
#                form.multitest_method.data, form.alpha.data, form.e_or_p_or_both.data,
#                form.abcorr.data, form.num_bins.data, form.backtracking.data,
#                form.fold_enrichment_study2pop.data, form.p_value_uncorrected.data,
#                form.p_value_mulitpletesting.data)
#
#             # tsv = '%s\n%s\n' % ('\t'.join(header), '\n'.join(['\t'.join(x) for x in results]))
#             header = header.split("\t")
#             tsv = '%s\n%s\n' % (header, results)
#             tsv.encode('base64')
#             results2display = []
#             for res in results:
#                 results2display.append(res.split('\t'))
#             return render_template('GOTUPK_file_upload_result.html', header=header, results=results2display, tsv=tsv, errors=[])
#             # return render_template('GOTUPK_file_result.html')
#     return render_template('GOTUPK_file.html', form=GOTUPK_file_Form())


################################################################################
# GOTUPK copy & paste
################################################################################
# class GOTUPK_cap_Form(wtforms.Form):
#     organism = fields.SelectField(u'Select Organism', choices = organism_choices)
#     foreground_textarea = fields.TextAreaField("Foreground Sites")
#     background_textarea = fields.TextAreaField("Background Sites")
#     catagories = fields.SelectMultipleField(
#             "GO Catagories",
#             choices = (("BP", "Biological Processes"), ("CC", "Celluar Compartments"),
#                      ("MF", "Molecular Function")),
#             widget = wtforms.widgets.ListWidget(prefix_label=False),
#             option_widget = wtforms.widgets.CheckboxInput(),
#             default = ("BP", "CC", "MF")    )
#     alpha = fields.IntegerField("Alpha", default=0.05)
#     correction_method = fields.SelectField(
#         "Correction for multiple testing Method",
#         choices = (
#             ("fdr", "FDR"), ("bonferroni", "Bonferroni"),
#             ("sidak", "Sidak"), ("holm", "Holm"),
#             ("uncorrected", "None")        )    )
#
# @app.route('/GOTUPK_cap')
# def GOTUPK_cap():
#     return render_template("GOTUPK_cap.html", form=GOTUPK_cap_Form())
#
# @app.route('/phospho_enrichment_result', methods=['POST'])
# def GOTUPK_cap_result():
#     form = GOTUPK_cap_Form(request.form)
#     print '-----' * 10
#     print '-----' * 10
#     print form.data
#     print '-----' * 10
#     print '-----' * 10
#     results, header = penrichment.run(
#             form.organism.data, form.catagories.data,
#             form.foreground_textarea.data, form.background_textarea.data,
#             form.alpha.data, form.correction_method.data    )
#     tsv = '%s\n%s\n' % ('\t'.join(header), '\n'.join(['\t'.join(x) for x in results]))
#     tsv.encode('base64')
#     return render_template('GOTUPK_cap_result.html', header=header, results=results, tsv=tsv, errors=[])

################################################################################
# Enrichment
################################################################################
# class PhosphoEnrichmentForm(wtforms.Form):
#     organism = fields.SelectField(u'Select Organism', choices = organism_choices)
#     foreground_textarea = fields.TextAreaField("Foreground Sites")
#     background_textarea = fields.TextAreaField("Background Sites")
#     catagories = fields.SelectMultipleField(
#             "GO Catagories",
#             choices = (("BP", "Biological Processes"), ("CC", "Celluar Compartments"),
#                      ("MF", "Molecular Function")),
#             widget = wtforms.widgets.ListWidget(prefix_label=False),
#             option_widget = wtforms.widgets.CheckboxInput(),
#             default = ("BP", "CC", "MF")    )
#     alpha = fields.IntegerField("Alpha", default=0.05)
#     correction_method = fields.SelectField(
#         "Correction for multiple testing Method",
#         choices = (
#             ("fdr", "FDR"), ("bonferroni", "Bonferroni"),
#             ("sidak", "Sidak"), ("holm", "Holm"),
#             ("uncorrected", "None")        )    )
#
# @app.route('/phospho_enrichment')
# def phospho_enrichment():
#     return render_template("phospho_enrichment_test.html", form=PhosphoEnrichmentForm())
#
# @app.route('/phospho_enrichment_result', methods=['POST'])
# def phospho_enrichment_result():
#     form = PhosphoEnrichmentForm(request.form)
#     print '-----' * 10
#     print '-----' * 10
#     print form.data
#     print '-----' * 10
#     print '-----' * 10
#     results, header = penrichment.run(
#             form.organism.data, form.catagories.data,
#             form.foreground_textarea.data, form.background_textarea.data,
#             form.alpha.data, form.correction_method.data    )
#     tsv = '%s\n%s\n' % ('\t'.join(header), '\n'.join(['\t'.join(x) for x in results]))
#     tsv.encode('base64')
#     return render_template('result.html', header=header, results=results, tsv=tsv, errors=[])


################################################################################
# Kinase Enrichment
################################################################################
# class EnzymeEnrichmentForm(wtforms.Form):
#     forground_file = fields.FileField(u"Forground File")
#     background_file = fields.FileField(u"Background File")
#
# @app.route('/enzyme_enrichment')
# def enzyme_enrichment():
#     return render_template('enzyme_enrichment.html', form=EnzymeEnrichmentForm())
#
# @app.route('/enzyme_enrichment_result', methods=["POST"])
# def submit_enzyme_enrichment():
#     result_file = StringIO.StringIO()
#     fg = '/Users/jcr/Projects/Teaching/UV/reg_UV_networkin.tsv'
#     bg = '/Users/jcr/Projects/Teaching/UV/unreg_UV_networkin.tsv'
#     ks.ks_test(fg, bg, result_file)
#     results, header = resultfile_to_results(result_file)
#     return render_template('result.html', header=header, results=results, tsv=result_file.read(),
#                     errors=[])



if __name__ == '__main__':
    app.run(processes=4, debug=True)















