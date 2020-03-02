#!/usr/bin/env python
import os, sys, zlib
import requests, time
import urllib.request, urllib.parse
from subprocess import call
from retrying import retry

PYTHON_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
sys.path.insert(0, PYTHON_DIR)
import tools
import variables as variables

DOWNLOADS_DIR = variables.DOWNLOADS_DIR
DIRECTORIES_LIST = variables.DIRECTORIES_LIST
SESSION_FOLDER_ABSOLUTE = variables.SESSION_FOLDER_ABSOLUTE


@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_requests(url, file_name, verbose=True):
    """
    only works for http not ftp
    """
    file_name = os.path.join(DOWNLOADS_DIR, file_name)
    tmp_f = os.path.join(DOWNLOADS_DIR, file_name + ".tmp")
    url = url.replace(" ", "%20")
    if verbose:
        print("{}\nDownloading to: {}\n".format(url, file_name))
    r = requests.get(url, stream=True)
    with open(tmp_f, "wb") as fh:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                fh.write(chunk)
    os.rename(tmp_f, file_name)

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_gzip_file(url, file_name, verbose=True):
    """
    :param url: String
    :param file_name: String (absolute path of name of downloaded)
    :param verbose: Bool (flag to print infos)
    :return: None
    """
    CHUNK = 16 * 1024
    temp_fn = file_name + ".tmp"
    if verbose:
        print('\nDownloading: {}'.format(url))
        print('TO: {}'.format(file_name))
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
        print("Couldn't download {}".format(url))
        os.remove(temp_fn.name)
    os.rename(temp_fn, file_name)
    if verbose:
        print("finished download")






# def download_file(url, fn_out):
#     """
#     only works for http not ftp
#     """
#     r = requests.get(url, stream=True)
#     with open(fn_out, 'wb') as f:
#         for chunk in r.iter_content(chunk_size=1024):
#             if chunk:  # filter out keep-alive new chunks
#                 f.write(chunk)
#
# @retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
# def download_go_basic_slim_obo(obo_url, fn_out, verbose=True):
#     """
#     http://geneontology.org/ontology/subsets/goslim_generic.obo
#     http://geneontology.org/ontology/go-basic.obo
#     """
#     url = obo_url.replace(' ', '%20')
#     tmp_f = os.path.join(DOWNLOADS_DIR, 'obo.tmp')
#     if verbose:
#         print('{}\nDownloading to: {}\n'.format(url, fn_out))
#     download_file(url, tmp_f)
#     os.rename(tmp_f, fn_out)
#     if verbose:
#         print("done")
