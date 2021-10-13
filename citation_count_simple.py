#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 07:01:19 2021

@author: jason box

obtains citation count and year of publication

"""

import sys
import urllib.request
from urllib.error import HTTPError
from habanero import counts

# ----------------------------- procedure to obtain Bibtex record
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
        # print(bibtex)
    except HTTPError as e:
        if e.code == 404:
            print('DOI not found.')
        else:
            print('Service unavailable.')
        sys.exit(1)
        
    return(bibtex)
# --------------------

#test doi 
doi='10.1088/1748-9326/aaf2ed'
N_citations=counts.citation_count(doi = doi)
result=do2tobib(doi)
result=result.replace('\n','')
result=result.replace('\t','')
test = result.find('year')
if test>0:
    print('doi:',doi,'N citations:',N_citations,'year:',int(str(result).split("year =")[1][1:5]))

