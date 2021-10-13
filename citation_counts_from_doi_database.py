#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 07:01:19 2021

@author: jason box

obtains citation count and year of publication

"""

import pandas as pd
import numpy as np
import os
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

base_path='/Users/jason/Dropbox/GEUS/bibliometrics_GEUS/bibliometric_GoK/'
os.chdir(base_path)

fn='./input/GoK_publications_all.xlsx'
df=pd.read_excel(fn)#,header=None)
file1 = open(fn, "r")

df['Citations update']=np.nan

n=len(df)

# for j,DOI in enumerate(df.DOI):
for j,doi in enumerate(df.DOI[70:]):
# for j,doi in enumerate(df.DOI[0:1]):
    if j==200: # counter to set to latest value if/when a timeout occurs, i.e. crossref is not reachable
        # print(j,doi)
        if ((doi!='-')&(type(doi)!=float)):
            if doi[0:3]=="10.":
            # if n-j<=34: # counter to set to latest value if/when a timeout occurs, i.e. crossref is not reachable
                N_citations=counts.citation_count(doi = doi)
                df.loc[j,'Citations update']=N_citations
                # print('N_citations',N_citations)
                # obtain year
                result=do2tobib(doi)
                result=result.replace('\n','')
                result=result.replace('\t','')
                test = result.find('year')
                if test>0:
                    df.loc[j,'year']=int(str(result).split("year =")[1][1:5])
                    print('j:',j,'remaining:',n-j,'doi:',doi,'N citations:',N_citations,'year:',df['year'][j].astype(int))

            # f = open(stats_path+str(count+1).zfill(3)+'.txt', 'w')
            # f.write(str(titlex)+';'+str(DOI)+';'+str(N_citations)+'\n')
            # print(count)

# #%%
# df.columns
# df = df[['year','article', 'DOI', 'Citations Sep 21','Journal', 'IF 2020', 'IF 5Y', 'glac',
#        'glac_lead', 'paleo', 'paleo_lead', ]]
# #%%

# #%%
# ofile='/Users/jason/Dropbox/GEUS/PA05_2021/bibliometrics_GEUS/GoK/output/GoK_pubs_2013-2020.xlsx'
# ofile='/Users/jason/Dropbox/GEUS/PA05_2021/bibliometrics_GEUS/GoK/output/PAO5 database with september citation count and year column.xlsx'
# df.to_excel(ofile,index=None)

