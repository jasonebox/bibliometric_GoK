#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 13:29:16 2021

@author: jason

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

fn='./input/GoK_publications_all.xlsx'
df=pd.read_excel(fn)#,header=None)
file1 = open(fn, "r")

# for j,DOI in enumerate(df.DOI):
for j,doi in enumerate(df.DOI[70:]):
# for j,doi in enumerate(df.DOI[0:1]):
    print(j,doi)
    if ((doi!='-')&(type(doi)!=float)):
        # test doi 
        # doi='10.1088/1748-9326/aaf2ed'
        result=do2tobib(doi).encode('utf8')
        # print(result)
        
        tmpfile='/tmp/t.bib'
        with open(tmpfile, 'wb') as f:
            f.write(result)
    
        with open(tmpfile) as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        
        # write out .csv of elements of bibtex file used in checking agains G&K database
        df = pd.DataFrame(bib_database.entries)
        l = ['author','title','journal','doi']
        selection = df[df.columns.intersection(l)]
        selection.to_csv('./output/csv/'+df.ID[0]+'.csv', index=False)

        with open('./output/bibtex/'+df.ID[0]+'.bib', 'wb') as f:
            f.write(result)

# authors=bib_database.entries[0]['author'].split(' and ')

# print(authors)
# txt=[]
# for author in authors:
#     author_segments=author.split(" ")
#     # print(author_segments)
#     if len(author_segments)==3:
#         temp=author_segments[2]+", "+author_segments[0][0]+'.'+""+author_segments[1][0]+'.;'
#         txt.append(temp)
#         # print(temp)
#     if len(author_segments)==2:
#         temp=author_segments[1]+", "+author_segments[0][0]+'.;'
#         txt.append(temp)
# print(''.join(txt))
# result=bibtexparser.customization.splitname(df['author'], strict_mode=True)
# print(result)

# df=
# df.set_index('journal',inplace=True)

# txt=str(df['author'])
# print(txt.split('and'))