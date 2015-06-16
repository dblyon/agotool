import os
import time
import itertools
import sys
import logging
import wtforms
import StringIO
import collections
from wtforms import fields, validators
# Setup for flask
import flask
from flask import render_template, request

# import 'back end' scripts
sys.path.append('static/python')
import ks
import penrichment

import gotupk

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
    (u'4932',  u'Saccharomyces cerevisiae'),
    (u'9606',  u'Homo sapiens'),
    (u'10090', u'Mus musculus'),
    (u'10116', u'Rattus norvegicus'),
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
# GOTUPK FILE
################################################################################
class GOTUPK_file_Form(wtforms.Form):

    userinput_file = fields.FileField(u"UserInput File")

    decimal = fields.SelectField("Decimal delimiter",
                                 choices = ((",", "Comma"), (".", "Point")),
                                 description = u"either a ',' or a '.' used for abundance values")

    organism = fields.SelectField(u'Select Organism', choices = organism_choices)



    gocat_upk = fields.SelectField("GO-terms or UniProt-Keywords",
                                choices = (("all_GO", "all 3 GO categories"),
                                           ("BP", "Biological Process"), ("CP", "Celluar Compartment"),
                                           ("MF", "Molecular Function"), ("UPK", "UniProt Keywords")))
    go_slims_or_basic = fields.SelectField("GO basic or slims",
                                 choices = (("basic", "basic"), ("slims", "slims")))

    indent = fields.SelectField("prepend GO-term level by dots",
                                choices = ((True, "Yes"), (False, "No")))

    correction_method = fields.SelectField("Correction for multiple testing Method",
                                choices = (("bonferroni", "Bonferroni"), ("sidak", "Sidak"), ("holm", "Holm")))
    alpha = fields.FloatField("Alpha", default = 0.05, description=u"for multiple testing correction")

    e_or_p_or_both = fields.SelectField("enriched or purified or both",
                                 choices = (("e", "enriched"), ("p", "purified"), ("both", "both"))) #!!! ? why does it switch to 'both' here???

    p_value =  fields.FloatField("p value (report threshold)", default = 0)

    minimum_ratio = fields.FloatField("minimum ratio study / background (report threshold)", default = 0)

    abcorr = fields.SelectField("Abundance correction",
                                choices = ((True, "Yes"), (False, "No")))


@app.route('/GOTUPK_file')
def GOTUPK_file():
    return render_template('GOTUPK_file.html', form=GOTUPK_file_Form())

@app.route('/GOTUPK_file_result', methods=["POST"])
def submit_GOTUPK_file():
    form = GOTUPK_file_Form(request.form)
    # result_file = StringIO.StringIO()
    # results, header = resultfile_to_results(result_file)
    gotupk.run(form.userinput_file, form.decimal.data, form.organism.data,
               form.gocat_upk.data, form.go_slims_or_basic.data, form.indent.data,
               form.correction_method.data, form.alpha.data, form.e_or_p_or_both.data,
               form.p_value.data, form.minimum_ratio.data, form.abcorr.data)

    return render_template('GOTUPK_file_result.html')

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
            default = ("BP", "CC", "MF")    )
    alpha = fields.IntegerField("Alpha", default=0.05)
    correction_method = fields.SelectField(
        "Correction for multiple testing Method",
        choices = (
            ("fdr", "FDR"), ("bonferroni", "Bonferroni"),
            ("sidak", "Sidak"), ("holm", "Holm"),
            ("uncorrected", "None")        )    )

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
            form.alpha.data, form.correction_method.data    )
    tsv = '%s\n%s\n' % ('\t'.join(header), '\n'.join(['\t'.join(x) for x in results]))
    tsv.encode('base64')
    return render_template('result.html', header=header, results=results, tsv=tsv, errors=[])

################################################################################
# GOTUPK copy & paste
################################################################################
class GOTUPK_cap_Form(wtforms.Form):
    organism = fields.SelectField(u'Select Organism', choices = organism_choices)
    foreground_textarea = fields.TextAreaField("Foreground Sites")
    background_textarea = fields.TextAreaField("Background Sites")
    catagories = fields.SelectMultipleField(
            "GO Catagories",
            choices = (("BP", "Biological Processes"), ("CC", "Celluar Compartments"),
                     ("MF", "Molecular Function")),
            widget = wtforms.widgets.ListWidget(prefix_label=False),
            option_widget = wtforms.widgets.CheckboxInput(),
            default = ("BP", "CC", "MF")    )
    alpha = fields.IntegerField("Alpha", default=0.05)
    correction_method = fields.SelectField(
        "Correction for multiple testing Method",
        choices = (
            ("fdr", "FDR"), ("bonferroni", "Bonferroni"),
            ("sidak", "Sidak"), ("holm", "Holm"),
            ("uncorrected", "None")        )    )

@app.route('/GOTUPK_cap')
def GOTUPK_cap():
    return render_template("GOTUPK_cap.html", form=GOTUPK_cap_Form())

@app.route('/phospho_enrichment_result', methods=['POST'])
def GOTUPK_cap_result():
    form = GOTUPK_cap_Form(request.form)
    print '-----' * 10
    print '-----' * 10
    print form.data
    print '-----' * 10
    print '-----' * 10
    results, header = penrichment.run(
            form.organism.data, form.catagories.data,
            form.foreground_textarea.data, form.background_textarea.data,
            form.alpha.data, form.correction_method.data    )
    tsv = '%s\n%s\n' % ('\t'.join(header), '\n'.join(['\t'.join(x) for x in results]))
    tsv.encode('base64')
    return render_template('GOTUPK_cap_result.html', header=header, results=results, tsv=tsv, errors=[])





if __name__ == '__main__':
    app.run(processes=4, debug=True)















