#!/usr/bin/env python
import os, sys, zlib
import requests, time
import urllib.request
from subprocess import call
from retrying import retry

PYTHON_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
sys.path.insert(0, PYTHON_DIR)

PROJECT_DIR = os.path.abspath(os.path.realpath(os.path.join(PYTHON_DIR, '../..')))
DOWNLOADS_DIR = os.path.abspath(os.path.join(PROJECT_DIR, "static/data/PostgreSQL/downloads"))

DIRECTORIES_LIST = [os.path.join(PROJECT_DIR, 'static/data/PostgreSQL', directory) for directory in ["downloads", "session"]]
DIRECTORIES_LIST.append(os.path.join(PROJECT_DIR, 'logs'))

URL_GENE_ASSOCIATIONS_GOA_UNIPROT = "ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/goa_uniprot_all.gaf.gz"
URL_GOA = "ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/{}/goa_{}.gaf.gz"
URL_UNIPROT_SECONDARY_2_PRIMARY_AN = r"ftp://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/docs/sec_ac.txt"
URL_GO_basic = r"http://purl.obolibrary.org/obo/go/go-basic.obo"
URL_GO_slim = r"http://purl.obolibrary.org/obo/go/subsets/goslim_generic.obo"
URL_eggNOG = r"http://eggnogdb.embl.de/download/latest/all_OG_annotations.tsv.gz"
URL_bactNOG = r"http://eggnogdb.embl.de/download/latest/data/bactNOG/bactNOG.annotations.tsv.gz"
URL_UNIPROT_2_KEGG = r"http://www.uniprot.org/uniprot/?query=database:(type:%22KEGG%22)&format=tab&columns=id_,database(KEGG)"
URL_UPK_obo = r"http://www.uniprot.org/keywords/?query=&format=obo"
URL_UNIPROT_KEYWORDS_ALL_ASSOCIATIONS = r"http://www.uniprot.org/uniprot/?columns=id_,keywords&format=tab&compress=yes"
URL_UniProt_KW = r"http://www.uniprot.org/uniprot/?query=organism:%i&columns=id_,keywords&format=tab"

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
    39947: 'rice',
    562: 'ecoli'}
# http://www.uniprot.org/uniprot/?columns=id,keywords&format=tab instead of individual ones

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
# http://www.uniprot.org/uniprot/?query=organism:Saccharomyces cerevisiae (strain ATCC 204508 / S288c)&columns=id_,keywords&format=tab

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_gzip_file(url, file_name):
    """
    :param url: String
    :param file_name: String(Basename of what downloaded file will be named)
    :return: None
    """
    CHUNK = 16 * 1024
    basename = os.path.basename(url)
    temp_fn = os.path.join(DOWNLOADS_DIR, basename + ".tmp")
    file_name = os.path.join(DOWNLOADS_DIR, file_name)
    print('\nDownloading: %s' % url)
    print('TO: %s' % file_name)
    try:
        with open(temp_fn, "wb") as temp_fh:
            response = urllib.request.urlopen(url)
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                temp_fh.write(chunk)
                temp_fh.flush()
    except IOError:
        print("Couldn't download {} .".format(url))
        os.remove(temp_fn.name)
    os.rename(temp_fn, file_name)

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_requests(url, file_name):
    """
    only works for http not ftp
    """
    file_name = os.path.join(DOWNLOADS_DIR, file_name)
    tmp_f = os.path.join(DOWNLOADS_DIR, file_name + ".tmp")
    url = url.replace(' ', '%20')
    print('%s\nDownloading to: %s\n' % (url, file_name))
    r = requests.get(url, stream=True)
    with open(tmp_f, 'wb') as fh:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                fh.write(chunk)
    os.rename(tmp_f, file_name)

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_urllib_urlretrieve(url, file_name):
    file_name = os.path.join(DOWNLOADS_DIR, file_name)
    tmp_f = os.path.join(DOWNLOADS_DIR, file_name + ".tmp")
    print('%s\nDownloading to: %s\n' % (url, file_name))
    with urllib.request.urlopen(url) as url_fh:
        with open(tmp_f, "w") as fh_out:
            fh_out.write(url_fh.read())
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
        except:
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

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_go_annotations():
    """
    http://stackoverflow.com/questions/2695152/in-python-how-do-i-decode-gzip-encoding
    e.g. of new schema
    ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/MOUSE/goa_mouse.gaf.gz
    :return: None
    """
    taxid_not_retrieved_list = []
    dl_string = URL_GOA
    for tax_id, organism in ORGANISMS.items():
        with open(os.path.join(DOWNLOADS_DIR, 'annotation.tmp'), 'wb') as tmp_fh:
            file_name = os.path.join(DOWNLOADS_DIR, '%s.gaf' % tax_id)
            url = dl_string.format(organism.upper(), organism.lower())
            print ('\nDownloading: %s' % url)
            print ('TO: %s' % file_name)
            try:
                with urllib.request.urlopen(url) as url_fh:
                    tmp_fh.write(zlib.decompress(url_fh.read(), 16 + zlib.MAX_WBITS))
            except IOError:
                taxid_not_retrieved_list.append(str(tax_id))
                print ("Couldn't download {} {} --> using unfiltered goa_uniprot_all.gaf as a resource instead.".format(organism, tax_id))
                os.remove(tmp_fh.name)
                continue
            os.rename(tmp_fh.name, file_name)
    return taxid_not_retrieved_list

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_go_annotations_all_unfiltered():
    """
    unfiltered GOA
    # shellcmd = "gunzip {}".format(file_name) #!!! this fails
    # gunzip /Users/dblyon/modules/cpr/agotool/static/data/downloads/goa_uniprot_all.gaf.gz
    # gunzip: /Users/dblyon/modules/cpr/agotool/static/data/downloads/goa_uniprot_all.gaf.gz: unexpected end of file
    # gunzip: /Users/dblyon/modules/cpr/agotool/static/data/downloads/goa_uniprot_all.gaf.gz: uncompress failed
    # print(shellcmd)
    # call(shellcmd, shell=True)

    # shellcmd = "gunzip {}".format(temp_fn)
    # print(shellcmd)
    # call(shellcmd, shell=True)
    """
    CHUNK = 16 * 1024
    url = URL_GENE_ASSOCIATIONS_GOA_UNIPROT
    temp_fn = os.path.join(DOWNLOADS_DIR, "annotation.tmp.gz")
    file_name = os.path.join(DOWNLOADS_DIR, "goa_uniprot_all.gaf.gz")
    print('\nDownloading: %s' % url)
    print('TO: %s' % file_name)
    try:
        with open(temp_fn, "wb") as temp_fh:
            response = urllib.request.urlopen(url)
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                temp_fh.write(chunk)
                temp_fh.flush()
    except IOError:
        print("Couldn't download {} .".format("goa_uniprot_all.gaf.gz"))
        os.remove(temp_fn.name)
    ## todo: parse from gz file to save disk space
    os.rename(temp_fn, file_name)

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_go_basic_slim_obo():
    """
    http://geneontology.org/ontology/subsets/goslim_generic.obo
    http://geneontology.org/ontology/go-basic.obo
    """
    dl_string_list = [URL_GO_basic, URL_GO_slim]
    for obo_url in dl_string_list:
        url = obo_url.replace(' ', '%20')
        file_name = os.path.join(DOWNLOADS_DIR, os.path.basename(obo_url))
        tmp_f = os.path.join(DOWNLOADS_DIR, 'obo.tmp')
        print('%s\nDownloaded to: %s\n' % (url, file_name))
        download_file(url, tmp_f)
        os.rename(tmp_f, file_name)

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_UniProt_Keywords():
    for organism in ORGANISMS:
        dl_string = URL_UniProt_KW
        url = (dl_string % organism).replace(' ', '%20')
        file_name = os.path.join(DOWNLOADS_DIR, '%s.upk' % organism)
        tmp_f = os.path.join(DOWNLOADS_DIR, 'keywords.tmp')
        print('%s\nDownloaded to: %s\n' % (url, file_name))
        download_file(url, tmp_f)
        os.rename(tmp_f, file_name)

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_UniProt_Keywords_obo():
    """
    # ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/docs/keywlist.txt
    # http://www.uniprot.org/keywords/?query=&format=obo
    """
    url = URL_UPK_obo
    file_name = os.path.join(DOWNLOADS_DIR, "keywords-all.obo")
    tmp_f = os.path.join(DOWNLOADS_DIR, 'keywords-all_obo.tmp')
    print('%s\nDownloaded to: %s\n' % (url, file_name))
    download_file(url, tmp_f)
    os.rename(tmp_f, file_name)

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_and_extract_all_annotations_from_eggNOG():
    """
    # URL_eggNOG = r"http://eggnogdb.embl.de/download/latest/all_OG_annotations.tsv.gz"
    all_OG_annotations.tsv.gz
    ENOG41xxxxx = Unsupervised Cluster of Orthologous Group (present in all levels)
    OG_name_short | GroupName | ProteinCount, description, dunno, GO, KEGG, domains, members
    """
    url = URL_eggNOG
    fn_out = os.path.join(DOWNLOADS_DIR, url.split('/')[-1])
    download_file(url, fn_out)
    shellcmd = "gunzip {}".format(fn_out)
    print(shellcmd)
    call(shellcmd, shell=True)

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_bactNOG_annotations():
    url = URL_bactNOG
    fn_out = os.path.join(DOWNLOADS_DIR, url.split('/')[-1])
    download_file(url, fn_out)
    shellcmd = "gunzip {}".format(fn_out)
    print(shellcmd)
    call(shellcmd, shell=True)


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
    # download_go_basic_slim_obo()
    # download_UniProt_Keywords_obo()
    # download_UniProt_Keywords()
    # download_gzip_file(URL_UNIPROT_SECONDARY_2_PRIMARY_AN, "sec_ac.txt")
    # download_gzip_file(URL_UNIPROT_2_KEGG, "uniprot_2_kegg_mapping.tab")  # long and slow
    # ToDo: am I downloading Keywords from UniProt for all and then for specific organisms??
    # download_gzip_file(URL_UNIPROT_KEYWORDS_ALL_ASSOCIATIONS, "uniprot-all-keywords.upk.gz")  # long and slow

    ### NOT every month
    # download_and_extract_all_annotations_from_eggNOG()
    # download_bactNOG_annotations()

    # taxid_not_retrieved_list = ['9796', '39947', '3880', '3055']
    # parse_files_and_pickle(taxid_not_retrieved_list) #=['9796', '39947', '3880', '3055'])
    # cleanup_sessions()
    # copy_essential_modules_and_scripts_from_metaprotRepo_2_agotoolRepo()
    print("finished update", '\n', '-' * 50, '\n')


