#!/usr/bin/env python
from __future__ import print_function

# core imports
import os
import sys
import zlib
import urllib
# import shutil

PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(PYTHON_DIR, '../..')
DIRECTORIES_LIST = [os.path.join(PROJECT_DIR, 'static/data', directory) for directory in ["GOA", "OBO", "UniProt_Keywords", "session"]]
sys.path.append(PYTHON_DIR)

# (u'4932',  u'Saccharomyces cerevisiae'), # Yeast
# (u'9606',  u'Homo sapiens'), # Human
# (u'3702',  u'Arabidopsis thaliana'), # Arabidopsis
# (u'7955',  u'Danio rerio'), # Zebrafish
# (u'7227',  u'Drosophila melanogaster'), # Fly
# (u'9031',  u'Gallus gallus'), # Chicken
# (u'10090', u'Mus musculus'), # Mouse
# (u'10116', u'Rattus norvegicus')] # Rat

# http://www.uniprot.org/uniprot/?query=organism:9606&format=tab&columns=id,keywords

organisms = {9606: 'human',
            4932: 'yeast',
            3702: 'arabidopsis',
            7955: 'zebrafish',
            7227: 'fly',
            9031: 'chicken',
            10090: 'mouse',
            10116: 'rat'}

# Saccharomyces cerevisiae (strain ATCC 204508 / S288c)
# http://www.uniprot.org/uniprot/?query=organism:Saccharomyces cerevisiae (strain ATCC 204508 / S288c)&columns=id,keywords&format=tab

def get_uniprot_annotatios():
    for organism in organisms:
        dl_string = "http://www.uniprot.org/uniprot/?query=organism:%i&columns=id,keywords&format=tab"
        _folder = os.path.join(PROJECT_DIR, 'static/data/UniProt_Keywords')
        if organism == 4932:
            dl_string = r"http://www.uniprot.org/uniprot/?query=organism:Saccharomyces cerevisiae (strain ATCC 204508 / S288c)&columns=id,keywords&format=tab"
            url = dl_string.replace(' ', '%20')
        else:
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
    dl_string = "ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/%s/gene_association.goa_%s.gz"
    for tax_id, organism in organisms.items():
        _folder = os.path.join(PROJECT_DIR, 'static/data/GOA')
        tmp_f = open(os.path.join(_folder, 'anotation.tmp'), 'w')
        file_name = os.path.join(_folder, '%s.tsv' % tax_id)
        url = dl_string % (organism.upper(), organism.lower())
        print ('\nDownloading: %s' % url)
        print ('TO: %s' % file_name)
        tmp_f.write(zlib.decompress(urllib.urlopen(url).read(), 16 + zlib.MAX_WBITS))
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


if __name__ == '__main__':
    print('-' * 50, '\n', "updating agotool libraries and cleaning up", '\n')
    create_directories_if_not_exist()
    get_uniprot_annotatios()
    update_go_annotations()
    update_go_basic_slim()
    cleanup_sessions()
    print("finished update", '\n', '-' * 50, '\n')
