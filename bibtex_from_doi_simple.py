#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 13:29:16 2021

@author: jason box

uses:
https://scipython.com/blog/doi-to-bibtex/
conda install -c conda-forge bibtexparser

"""

import sys
import urllib.request
from urllib.error import HTTPError
import os
import bibtexparser
import pandas as pd

def do2tobib(doi):
    # try:
    #     doi = sys.argv[1]
    # except IndexError:
    #     print('Usage:\n{} <doi>'.format(sys.argv[0]))
    #     sys.exit(1)

    BASE_URL = 'http://dx.doi.org/'
    
    url = BASE_URL + doi
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/x-bibtex')
    try:
        with urllib.request.urlopen(req) as f:
            bibtex = f.read().decode()
        print(bibtex)
    except HTTPError as e:
        if e.code == 404:
            print('DOI not found.')
        else:
            print('Service unavailable.')
        sys.exit(1)
        
    return(bibtex)

base_path='/Users/jason/Dropbox/GEUS/bibliometrics_GEUS/bibliometric_GoK/'
os.chdir(base_path)

doi='10.1088/1748-9326/aaf2ed'
result=do2tobib(doi).encode('utf8')
print(result)

# use a temporary file to later rename the .bib file using the 
tmpfile='/tmp/t.bib'
with open(tmpfile, 'wb') as f:f.write(result)

with open(tmpfile) as bibtex_file:bib_database = bibtexparser.load(bibtex_file)

df = pd.DataFrame(bib_database.entries)

with open('./output/bibtex/'+df.ID[0]+'.bib', 'wb') as f:f.write(result)
