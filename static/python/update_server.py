#!/usr/bin/env python
from __future__ import print_function

# core imports
import os
import sys
import zlib
import urllib
import time
# import shutil

# my own modules
import go_retriever

PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(PYTHON_DIR, '../..'))
DIRECTORIES_LIST = [os.path.join(PROJECT_DIR, 'static/data', directory) for directory in ["GOA", "OBO", "UniProt_Keywords", "session"]]
DIRECTORIES_LIST.append(os.path.join(PROJECT_DIR, 'logs'))
sys.path.append(PYTHON_DIR)

# If you would like to download an unfiltered GOA UniProt gene association
# file, please use either the GOA ftp site:
# ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/gene_association.goa_uniprot.gz
URL_GENE_ASSOCIATIONS_GOA_UNIPROT = "ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/gene_association.goa_uniprot.gz"

# organism_choices = [
#     (u'4932',  u'Saccharomyces cerevisiae'), # Yeast
#     (u'9606',  u'Homo sapiens'), # Human
#     (u'7955',  u'Danio rerio'), # Zebrafish
#     (u'7227',  u'Drosophila melanogaster'), # Fly
#     (u'9796', u'Equus caballus'), # Horse
#     (u'9031',  u'Gallus gallus'), # Chicken
#     (u'10090', u'Mus musculus'), # Mouse
#     (u'10116', u'Rattus norvegicus'), # Rat
#     (u'9823', u'Sus scrofa'), # Pig
#     (u'3702',  u'Arabidopsis thaliana'), # Arabidopsis
#     (u'3055', u'Chlamydomonas reinhardtii'), # Chlamy
#     (u'3880', u'Medicago truncatula'), # Medicago
#     (u'39947', u'Oryza sativa subsp. japonica') # Rice
#     ]

# GOA files
# """
# Couldn't download horse 9796
# Couldn't download rice 39947, #  at http://geneontology.org/page/download-annotations
# Couldn't download medicago 3880
# Couldn't download chlamy 3055
# ['9796', '39947', '3880', '3055']
# """

# http://www.uniprot.org/uniprot/?query=organism:9606&format=tab&columns=id,keywords

organisms = {9606: 'human',
            559292: 'yeast', # 559292 instead of 4932
            3702: 'arabidopsis',
            7955: 'zebrafish',
            7227: 'fly',
            9031: 'chicken',
            10090: 'mouse',
            10116: 'rat',
            9796: 'horse',
            9823: 'pig',
            3880: 'medicago',
            3055: 'chlamy',
            39947: 'rice'}

# using TaxID 559292 instead of 4932 for yeast
# 4932=Saccharomyces cerevisiae  559292=Saccharomyces cerevisiae S288c
# Saccharomyces cerevisiae (strain ATCC 204508 / S288c)
# http://www.uniprot.org/uniprot/?query=organism:Saccharomyces cerevisiae (strain ATCC 204508 / S288c)&columns=id,keywords&format=tab

def update_uniprot_annotatios():
    for organism in organisms:
        dl_string = "http://www.uniprot.org/uniprot/?query=organism:%i&columns=id,keywords&format=tab"
        _folder = os.path.join(PROJECT_DIR, 'static/data/UniProt_Keywords')
        # if organism == 4932: # not needed any more if TaxID 559292 instead of 4932
        #     dl_string = r"http://www.uniprot.org/uniprot/?query=organism:Saccharomyces cerevisiae (strain ATCC 204508 / S288c)&columns=id,keywords&format=tab"
        #     url = dl_string.replace(' ', '%20')
        # else:
        #     url = (dl_string % organism).replace(' ', '%20')
        url = (dl_string % organism).replace(' ', '%20')
        file_name = os.path.join(_folder, '%s.tab' % organism)
        tmp_f = os.path.join(_folder, 'keywords.tmp')
        print('%s\nDownloaded to: %s\n' % (url, file_name))
        urllib.urlretrieve(url, tmp_f)
        os.rename(tmp_f, file_name)

def update_go_annotations():
    """
    http://stackoverflow.com/questions/2695152/in-python-how-do-i-decode-gzip-encoding
    :return: None
    """
    taxid_not_retrieved_list = []
    dl_string = "ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/%s/gene_association.goa_%s.gz"
    for tax_id, organism in organisms.items():
        _folder = os.path.join(PROJECT_DIR, 'static/data/GOA')
        tmp_f = open(os.path.join(_folder, 'anotation.tmp'), 'w')
        file_name = os.path.join(_folder, '%s.tsv' % tax_id)
        url = dl_string % (organism.upper(), organism.lower())
        print ('\nDownloading: %s' % url)
        print ('TO: %s' % file_name)
        try:
            tmp_f.write(zlib.decompress(urllib.urlopen(url).read(), 16 + zlib.MAX_WBITS))
        except IOError:
            taxid_not_retrieved_list.append(str(tax_id))
            print ("Couldn't download {} {} --> using unfiltered gene_association.goa_uniprot.gz as a resource instead.".format(organism, tax_id))
            os.remove(tmp_f.name)
            continue
        os.rename(tmp_f.name, file_name)
    return taxid_not_retrieved_list

def update_go_annotations_onebigfile():
    url = URL_GENE_ASSOCIATIONS_GOA_UNIPROT
    tax_id = "uniprot_all"
    organism = "uniprot_all"
    _folder = os.path.join(PROJECT_DIR, 'static/data/GOA')
    tmp_f = open(os.path.join(_folder, 'anotation.tmp'), 'wb')
    file_name = os.path.join(_folder, '%s.gz' % tax_id)
    print ('\nDownloading: %s' % url)
    print ('TO: %s' % file_name)
    try:
        tmp_f.write(urllib.urlopen(url).read())
    except IOError:
        print ("Couldn't download {} {}.".format(organism, tax_id))
        os.remove(tmp_f.name)
    os.rename(tmp_f.name, file_name)

def update_go_basic_slim():
    """
    http://geneontology.org/ontology/subsets/goslim_generic.obo
    http://geneontology.org/ontology/go-basic.obo
    :return: None
    """
    dl_string_list = [r"http://purl.obolibrary.org/obo/go/go-basic.obo",
                      r"http://purl.obolibrary.org/obo/go/subsets/goslim_generic.obo"]
    for obo_url in dl_string_list:
        _folder = os.path.join(PROJECT_DIR, 'static/data/OBO')
        url = obo_url.replace(' ', '%20')
        file_name = os.path.join(_folder, os.path.basename(obo_url))
        tmp_f = os.path.join(_folder, 'obo.tmp')
        print('%s\nDownloaded to: %s\n' % (url, file_name))
        urllib.urlretrieve(url, tmp_f)
        os.rename(tmp_f, file_name)

def create_directories_if_not_exist():
    for directory in DIRECTORIES_LIST:
        if not os.path.isdir(directory):
            os.makedirs(directory)

def cleanup_sessions():
    _folder = os.path.join(PROJECT_DIR, 'static/data/session')
    e = 'could not remove %s from static/data/session'
    for the_file in os.listdir(_folder):
        file_path = os.path.join(_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception:
            print(e % the_file)

def get_fn_pickle_Parser_GO_annotations():
    return os.path.abspath(os.path.join(PYTHON_DIR, '../../static/data/GOA/Parser_GO_annotations.p'))

def get_fn_UniProtKeywordsParser():
    return os.path.abspath(os.path.join(PYTHON_DIR, '../../static/data/UniProt_Keywords/UniProtKeywordsParser.p'))


################################################################################
def parse_files_and_pickle(taxid_not_retrieved_list):
    ### parse Gene Ontology annotations: GO-terms for each AccessionNumber
    # pgoa = go_retriever.Parser_GO_annotations()
    organisms_set = set([str(taxid) for taxid in organisms.keys()])
    # organisms_specific = organisms_set - set(taxid_not_retrieved_list)
    # GOA_folder = os.path.join(PROJECT_DIR, 'static/data/GOA')
    # ### 1.) species specific files
    # for taxid in organisms_specific:
    #     fn = os.path.join(GOA_folder, '%s.tsv' % taxid)
    #     pgoa.parse_goa_ref(fn, organisms_set={taxid})
    # ### 2.) the remaining species (in taxid_not_retrieved_list)
    # fn = os.path.join(GOA_folder, '%s.gz' % "uniprot_all")
    # pgoa.parse_goa_ref(fn, organisms_set=set(taxid_not_retrieved_list))
    # fn_p = get_fn_pickle_Parser_GO_annotations()
    # pgoa.pickle(fn_p)
    ### parse UniProt-keywords
    upkp = go_retriever.UniProtKeywordsParser()
    UPK_folder = os.path.join(PROJECT_DIR, 'static/data/UniProt_Keywords')
    for taxid in organisms_set:
        fn = os.path.join(UPK_folder, '%s.tab' % taxid)
        upkp.parse_file(fn, taxid)
    fn_p = get_fn_UniProtKeywordsParser()
    upkp.pickle(fn_p)





if __name__ == '__main__':
    print('-' * 50, '\n', "updating agotool libraries and cleaning up", '\n')
    print("Current date & time " + time.strftime("%c"))
    # create_directories_if_not_exist()
    # taxid_not_retrieved_list = update_go_annotations()
    # update_go_annotations_onebigfile()
    # update_go_basic_slim()
    # update_uniprot_annotatios()
    parse_files_and_pickle(taxid_not_retrieved_list=['9796', '39947', '3880', '3055'])
    # cleanup_sessions()
    print("finished update", '\n', '-' * 50, '\n')


