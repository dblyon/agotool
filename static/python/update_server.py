#!/usr/bin/env python
from __future__ import print_function
import os, sys, zlib
import requests, urllib, time
from subprocess import call
import go_retriever

PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PYTHON_DIR)

PROJECT_DIR = os.path.abspath(os.path.join(PYTHON_DIR, '../..'))
DOWNLOADS_DIR = os.path.abspath(os.path.join(PROJECT_DIR, "static/data/downloads"))

DIRECTORIES_LIST = [os.path.join(PROJECT_DIR, 'static/data', directory) for directory in ["downloads", "session"]]
DIRECTORIES_LIST.append(os.path.join(PROJECT_DIR, 'logs'))

# URL_GENE_ASSOCIATIONS_GOA_UNIPROT = "ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/gene_association.goa_uniprot.gz" # old schema
URL_GENE_ASSOCIATIONS_GOA_UNIPROT = "ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/goa_uniprot_all.gaf.gz" # new schema

url_eggNOG = r"http://eggnogdb.embl.de/download/latest/all_OG_annotations.tsv.gz"
url_UPK_obo = r"http://www.uniprot.org/keywords/?query=&format=obo"

ORGANISMS = {
    3702: 'arabidopsis',
    9031: 'chicken',
    9913: 'cow', # 9913, Bos taurus
    44689: 'dicty', # 44689, Dictyostelium discoideum
    9615: 'dog', # 9615, Canis lupus familiaris
    7227: 'fly',
    9606: 'human',
    10090: 'mouse',
    9823: 'pig',
    10116: 'rat',
    6239: 'worm', # 6239, Caenorhabditis elegans
    559292: 'yeast', # 559292 instead of 4932
    284812: 'fission_yeast',
    7955: 'zebrafish',
    3055: 'chlamy',
    9796: 'horse',
    3880: 'medicago',
    39947: 'rice'}

# update for Vytus
#  4896 [NCBI highest level], Schizosaccharomyces pombe, 284812 UniProt
#  6239 NCBI, Caenorhabditis elegans, 6239 Uniprot


# Schizosaccharomyces pombe 4896
# ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/proteomes/78.S_pombe.goa

# and Caenorhabditis elegans 6239
# ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/proteomes/9.C_elegans.goa

# using TaxID 559292 instead of 4932 for yeast
# 4932=Saccharomyces cerevisiae  559292=Saccharomyces cerevisiae S288c
# Saccharomyces cerevisiae (strain ATCC 204508 / S288c)
# http://www.uniprot.org/uniprot/?query=organism:Saccharomyces cerevisiae (strain ATCC 204508 / S288c)&columns=id,keywords&format=tab

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

def download_file(url, fn_out):
    """
    only works for http not ftp
    """
    r = requests.get(url, stream=True)
    with open(fn_out, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

def download_go_annotations():
    """
    http://stackoverflow.com/questions/2695152/in-python-how-do-i-decode-gzip-encoding
    e.g. of new schema
    ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/MOUSE/goa_mouse.gaf.gz
    :return: None
    """
    taxid_not_retrieved_list = []
    dl_string = "ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/{}/goa_{}.gaf.gz" # new schema
    for tax_id, organism in ORGANISMS.items():
        tmp_f = open(os.path.join(DOWNLOADS_DIR, 'annotation.tmp'), 'w')
        file_name = os.path.join(DOWNLOADS_DIR, '%s.gaf' % tax_id)
        url = dl_string.format(organism.upper(), organism.lower())
        print ('\nDownloading: %s' % url)
        print ('TO: %s' % file_name)
        try:
            tmp_f.write(zlib.decompress(urllib.urlopen(url).read(), 16 + zlib.MAX_WBITS))
            tmp_f.close()
        except IOError:
            taxid_not_retrieved_list.append(str(tax_id))
            print ("Couldn't download {} {} --> using unfiltered goa_uniprot_all.gaf as a resource instead.".format(organism, tax_id))
            os.remove(tmp_f.name)
            continue
        os.rename(tmp_f.name, file_name)
    return taxid_not_retrieved_list

def download_go_annotations_all_unfiltered():
    """
    unfiltered GOA
    """
    url = URL_GENE_ASSOCIATIONS_GOA_UNIPROT
    # tax_id = "goa_uniprot_all"
    basename = os.path.basename(url)
    tax_id = basename[:basename.index(".")]
    tmp_f = open(os.path.join(DOWNLOADS_DIR, 'annotation.tmp'), 'wb')
    file_name = os.path.join(DOWNLOADS_DIR, '%s.gaf.gz' % tax_id)
    print ('\nDownloading: %s' % url)
    print ('TO: %s' % file_name)
    try:
        tmp_f.write(urllib.urlopen(url).read())
    except IOError:
        print ("Couldn't download {} .".format(tax_id))
        os.remove(tmp_f.name)
    os.rename(tmp_f.name, file_name)
    # shellcmd = "gunzip {}".format(file_name) #!!! this fails
    # gunzip /Users/dblyon/modules/cpr/agotool/static/data/downloads/goa_uniprot_all.gaf.gz
    # gunzip: /Users/dblyon/modules/cpr/agotool/static/data/downloads/goa_uniprot_all.gaf.gz: unexpected end of file
    # gunzip: /Users/dblyon/modules/cpr/agotool/static/data/downloads/goa_uniprot_all.gaf.gz: uncompress failed
    # print(shellcmd)
    # call(shellcmd, shell=True)

def download_go_basic_slim_obo():
    """
    http://geneontology.org/ontology/subsets/goslim_generic.obo
    http://geneontology.org/ontology/go-basic.obo
    """
    dl_string_list = [r"http://purl.obolibrary.org/obo/go/go-basic.obo",
                      r"http://purl.obolibrary.org/obo/go/subsets/goslim_generic.obo"]
    for obo_url in dl_string_list:
        url = obo_url.replace(' ', '%20')
        file_name = os.path.join(DOWNLOADS_DIR, os.path.basename(obo_url))
        tmp_f = os.path.join(DOWNLOADS_DIR, 'obo.tmp')
        print('%s\nDownloaded to: %s\n' % (url, file_name))
        download_file(url, tmp_f)
        os.rename(tmp_f, file_name)

def download_UniProt_Keywords():
    for organism in ORGANISMS:
        dl_string = "http://www.uniprot.org/uniprot/?query=organism:%i&columns=id,keywords&format=tab"
        url = (dl_string % organism).replace(' ', '%20')
        file_name = os.path.join(DOWNLOADS_DIR, '%s.upk' % organism)
        tmp_f = os.path.join(DOWNLOADS_DIR, 'keywords.tmp')
        print('%s\nDownloaded to: %s\n' % (url, file_name))
        download_file(url, tmp_f)
        os.rename(tmp_f, file_name)

def download_UniProt_Keywords_obo():
    """
    # ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/docs/keywlist.txt
    # http://www.uniprot.org/keywords/?query=&format=obo
    """
    # url = r"http://www.uniprot.org/keywords/?query=&format=obo"
    url = url_UPK_obo
    file_name = os.path.join(DOWNLOADS_DIR, "keywords-all.obo")
    tmp_f = os.path.join(DOWNLOADS_DIR, 'keywords-all_obo.tmp')
    print('%s\nDownloaded to: %s\n' % (url, file_name))
    download_file(url, tmp_f)
    os.rename(tmp_f, file_name)

def download_and_extract_all_annotations_from_eggNOG():
    """
    all_OG_annotations.tsv.gz
    ENOG41xxxxx = Unsupervised Cluster of Orthologous Group (present in all levels)
    OG_name_short | GroupName | ProteinCount, description, dunno, GO, KEGG, domains, members
    """
    # url_eggNOG = r"http://eggnogdb.embl.de/download/latest/all_OG_annotations.tsv.gz"
    url = url_eggNOG
    fn_out = os.path.join(DOWNLOADS_DIR, url.split('/')[-1])
    download_file(url, fn_out)
    shellcmd = "gunzip {}".format(fn_out)
    print(shellcmd)
    call(shellcmd, shell=True)

def download_bactNOG_annotations():
    url = r"http://eggnogdb.embl.de/download/latest/data/bactNOG/bactNOG.annotations.tsv.gz"
    fn_out = os.path.join(DOWNLOADS_DIR, url.split('/')[-1])
    download_file(url, fn_out)
    shellcmd = "gunzip {}".format(fn_out)
    print(shellcmd)
    call(shellcmd, shell=True)

def get_fn_pickle_Parser_GO_annotations():
    return os.path.abspath(os.path.join(PYTHON_DIR, '../../static/data/GOA/Parser_GO_annotations.p'))

def get_fn_UniProtKeywordsParser():
    return os.path.abspath(os.path.join(PYTHON_DIR, '../../static/data/UniProt_Keywords/UniProtKeywordsParser.p'))

def parse_files_and_pickle(taxid_not_retrieved_list):
    ## parse Gene Ontology annotations: GO-terms for each AccessionNumber
    pgoa = go_retriever.Parser_GO_annotations()
    organisms_set = set([str(taxid) for taxid in ORGANISMS.keys()])
    organisms_specific = organisms_set - set(taxid_not_retrieved_list)
    GOA_folder = os.path.join(PROJECT_DIR, 'static/data/GOA')
    ## 1.) species specific files
    for taxid in organisms_specific:
        fn = os.path.join(GOA_folder, '%s.tsv' % taxid)
        pgoa.parse_goa_ref(fn, organisms_set={taxid})
    ## 2.) the remaining species (in taxid_not_retrieved_list)
    fn = os.path.join(GOA_folder, '%s.gz' % "uniprot_all")
    pgoa.parse_goa_ref(fn, organisms_set=set(taxid_not_retrieved_list))
    fn_p = get_fn_pickle_Parser_GO_annotations()
    pgoa.pickle(fn_p)
    ## parse UniProt-keywords
    upkp = go_retriever.UniProtKeywordsParser()
    UPK_folder = os.path.join(PROJECT_DIR, 'static/data/UniProt_Keywords')
    for taxid in organisms_set:
        fn = os.path.join(UPK_folder, '%s.tab' % taxid)
        upkp.parse_file(fn, taxid)
    fn_p = get_fn_UniProtKeywordsParser()
    upkp.pickle(fn_p)


if __name__ == '__main__':
    # .gaf files are GOA (Gene Ontology Associations)
    # .upk files are UPK (UniProt Keywords)
    # .obo files are Ontology hierarchy
    print('-' * 50, '\n', "updating agotool libraries and cleaning up", '\n')
    print("Current date & time " + time.strftime("%c"))
    create_directories_if_not_exist()
    ### every month
    # taxid_not_retrieved_list = download_go_annotations()
    # download_go_annotations_all_unfiltered()
    download_go_basic_slim_obo()
    download_UniProt_Keywords_obo()
    # download_UniProt_Keywords()

    ### NOT every month
    # download_and_extract_all_annotations_from_eggNOG()
    # download_bactNOG_annotations()

    # taxid_not_retrieved_list = ['9796', '39947', '3880', '3055']
    # parse_files_and_pickle(taxid_not_retrieved_list) #=['9796', '39947', '3880', '3055'])
    cleanup_sessions()
    print("finished update", '\n', '-' * 50, '\n')



################################################################################





