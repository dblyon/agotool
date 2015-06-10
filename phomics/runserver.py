import flask, os, time, itertools, sys, logging, wtforms, StringIO, collections
from wtforms import fields, validators
# Setup for flask
from flask import render_template, request

# import 'back end' scripts
sys.path.append('static/python')
import activationloop
import ks
import pdavid
import penrichment
import go_term_enrichment

app = flask.Flask(__name__)

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
organism_choices = [
    (u'9606',  u'Homo sapiens'),
    (u'10090', u'Mus musculus'),
    (u'10116', u'Rattus norvegicus'),
    (u'4932',  u'Saccharomyces cerevisiae'),
    (u'7227',  u'Drosophila melanogaster'),
    (u'7955',  u'Danio rerio'),
    (u'9031',  u'Gallus gallus'),
    (u'8364',  u'Xenopus (Silurana) tropicalis')]

def resultfile_to_results(result_file):
    result_file.seek(0)
    header = result_file.readline().rstrip().split('\t')
    results = [line.split('\t') + [''] for line in result_file]
    result_file.seek(0)
    return results, header
################################################################################
# index.html
################################################################################
@app.route('/')
def index():
    return render_template('index.html')
################################################################################

################################################################################
# about.html
################################################################################
@app.route('/about')
def about():
    return render_template('about.html')
################################################################################

################################################################################
class BaseActivationLoopForm(wtforms.Form):
    organism = fields.SelectField(u'Select Organism', choices = organism_choices)
    input_textarea = fields.TextAreaField(u'Input Sites')
    input_file = fields.FileField(u"Input file")

class ActivationLoopSitesForm(BaseActivationLoopForm):
    example_data = fields.HiddenField(default=open('static/data/examples/site_example.tsv').read())

class ActivationLoopPeptidesForm(BaseActivationLoopForm):
    example_data = fields.HiddenField(default=open('static/data/examples/peptide_example.tsv').read())
    missed_clevages = fields.SelectField(u"Max Missed Clevages", default = '2',
                                         choices = [[str(x)] * 2 for x in range(6)])
    cleave = fields.SelectField(u"Cleave",  default = "after",
                                choices = [("after", "after"), ("before", "before")])

    cleave_res = fields.StringField(u"Cleave at", default='RK')

@app.route('/activation_loop_sites')
def activation_loop_sites():
    return render_template('activation_loop.html', form=ActivationLoopSitesForm(), page_type="sites")

@app.route('/activation_loop_peptides')
def activation_loop_peptides():
    return render_template('activation_loop.html', form=ActivationLoopPeptidesForm(), page_type="peptides")

def get_activation_loop_organism_and_textarea(request):
    textarea = request.form['input_textarea']
    organism = request.form['organism']
    if textarea == "":
        textarea = request.files['input_file'].read()
    return organism, textarea

@app.route('/activation_loop_sites_result', methods=['POST'])
def submit_activation_loop_sites():
    organism, textarea = get_activation_loop_organism_and_textarea(request)
    results, errors = activationloop.parse_positions(textarea, organism)
    header = ['Uniprot Entry', 'Gene Name', 'Loop Sites', 'Other Sites']
    tsv, _results = ['\t'.join(header)], []
    for (acc, gene, loop, kin, des) in results:
        loop = ', '.join(map(str, loop))
        kin  = ', '.join(map(str, kin))
        _results.append([acc, gene, loop, kin, des])
        tsv.append('\t'.join([acc, gene, loop.replace(' ', ''), kin.replace(' ', '')]))
    tsv = u'\n'.join(tsv).encode('base64')
    return render_template('result.html', header=header,
                           results=_results, tsv=tsv, errors=errors)

@app.route('/activation_loop_peptides_result', methods=['POST'])
def submit_activation_loop_peptides():
    form = ActivationLoopPeptidesForm(request.form)
    organism, textarea = get_activation_loop_organism_and_textarea(request)
    results, errors = activationloop.parse_peptides(
        textarea, int(organism), form.cleave_res.data, int(form.missed_clevages.data), form.cleave.data == 'after')
    header = ['Uniprot Entry', 'Gene Name', 'Loop Sites', 'Other Sites', 'Peptide']
    tsv, _results = ['\t'.join(header)], []
    br = '\n'
    print results
    for (acc, gene, loop, kin, seq, des) in results:
        kin = map(str, kin)
        loop = map(str, loop)
        for l, k, s in zip(loop, kin, seq):
            tsv.append('\t'.join((acc, gene, l, k, s)))
        seq = '\n'.join(seq)
        _results.append([acc, gene, '\n'.join(loop), '\n'.join(kin), seq, des])
    tsv = u'\n'.join(tsv).encode('base64')
    return render_template('result.html', header=header,
                           results=_results, tsv=tsv, errors=errors)

################################################################################
# Kinase Enrichment
################################################################################
class EnzymeEnrichmentForm(wtforms.Form):
    forground_file = fields.FileField(u"Forground File")
    background_file = fields.FileField(u"Background File")

@app.route('/enzyme_enrichment')
def enzyme_enrichment():
    return render_template('enzyme_enrichment.html', form=EnzymeEnrichmentForm())

@app.route('/enzyme_enrichment_result', methods=["POST"])
def submit_enzyme_enrichment():
    result_file = StringIO.StringIO()
    fg = '/Users/jcr/Projects/Teaching/UV/reg_UV_networkin.tsv'
    bg = '/Users/jcr/Projects/Teaching/UV/unreg_UV_networkin.tsv'
    ks.ks_test(fg, bg, result_file)
    results, header = resultfile_to_results(result_file)
    return render_template('result.html', header=header, results=results, tsv=result_file.read(),
                    errors=[])

################################################################################
# Enrichment
################################################################################
class PhosphoEnrichmentForm(wtforms.Form):
    organism = fields.SelectField(u'Select Organism', choices = organism_choices)
    foreground_textarea = fields.TextAreaField("Foreground Sites")
    background_textarea = fields.TextAreaField("Background Sites")
    catagories = fields.SelectMultipleField(
            "GO Catagories",
            choices = (("BP", "Biological Processes"), ("CC", "Celluar Compartments"),
                     ("MF", "Molecular Function")),
            widget = wtforms.widgets.ListWidget(prefix_label=False),
            option_widget = wtforms.widgets.CheckboxInput(),
            default = ("BP", "CC", "MF"))
    alpha = fields.IntegerField("Alpha", default=0.05)
    correction_method = fields.SelectField(
        "Correction for multiple testing Method",
        choices = (
            ("fdr", "FDR"), ("bonferroni", "Bonferroni"),
            ("sidak", "Sidak"), ("holm", "Holm"),
            ("uncorrected", "None")))

@app.route('/phospho_enrichment')
def phospho_enrichment():
    return render_template("phospho_enrichment_test.html", form=PhosphoEnrichmentForm())

@app.route('/phospho_enrichment_result', methods=['POST'])
def phospho_enrichment_result():
    form = PhosphoEnrichmentForm(request.form)
    print '-----' * 10
    print '-----' * 10
    print form.data
    print '-----' * 10
    print '-----' * 10
    results, header = penrichment.run(
            form.organism.data, form.catagories.data,
            form.foreground_textarea.data, form.background_textarea.data,
            form.alpha.data, form.correction_method.data)
    tsv = '%s\n%s\n' % ('\t'.join(header), '\n'.join(['\t'.join(x) for x in results]))
    tsv.encode('base64')
    return render_template('result.html', header=header, results=results, tsv=tsv, errors=[])

################################################################################
# GO term enrichment abundance corrected
################################################################################
class GOTermEnrichmentForm(wtforms.Form):
    organism = fields.SelectField(u'Select Organism', choices = organism_choices)
    foreground_textarea = fields.TextAreaField("Study AccessionNumbers")
    background_textarea = fields.TextAreaField("Background AccessionNumbers and Intensities")
    catagories = fields.SelectMultipleField("GO Catagories",
            choices = (("BP", "Biological Processes"), ("CC", "Cellular Compartments"),
                     ("MF", "Molecular Function")),
            widget = wtforms.widgets.ListWidget(prefix_label=False),
            option_widget = wtforms.widgets.CheckboxInput(),
            default = ("BP", "CC", "MF"))
    alpha = fields.IntegerField("Alpha", default=0.05)
    correction_method = fields.SelectField(
        "Correction for multiple testing Method",
        choices = (
            ("fdr", "FDR"), ("bonferroni", "Bonferroni"),
            ("sidak", "Sidak"), ("holm", "Holm"),
            ("uncorrected", "None")))

@app.route('/go_term_enrichment')
def go_term_enrichment():
    return render_template("go_term_enrichment.html", form=GOTermEnrichmentForm())

@app.route('/go_term_enrichment_result', methods=['POST'])
def go_term_enrichment_result():
    form = GOTermEnrichmentForm(request.form)
    print '-----' * 10
    print '-----' * 10
    print form.data
    print '-----' * 10
    print '-----' * 10
    results, header = go_term_enrichment.run(
            form.organism.data, form.catagories.data,
            form.foreground_textarea.data, form.background_textarea.data,
            form.alpha.data, form.correction_method.data)
    tsv = '%s\n%s\n' % ('\t'.join(header), '\n'.join(['\t'.join(x) for x in results]))
    tsv.encode('base64')
    return render_template('result.html', header=header, results=results, tsv=tsv, errors=[])




if __name__ == '__main__':
    app.run(processes=4, debug=True)










