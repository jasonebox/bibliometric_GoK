#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 00:10:12 2021 @author: jason

Fetching Data from the Altmetric API

https://api.altmetric.com/

https://api.altmetric.com/docs/call_citations.html

HTTP status code	Description
200	Success. The body of the response should contain the data you requested.
403	You aren't authorized for this call. Some calls and query types can only be made by holders of an API key and/or a license for the Full Access version of the API.
404	Altmetric doesn't have any details for the article or set of articles you requested.
429	You are being rate limited. If you haven't already then apply for an API key.
502	The Altmetric Details Page API version you are using is currently down for maintenance.

"""

import requests
import json
import pandas as pd
import numpy as np
import time
from datetime import datetime
import os

base_path='/Users/jason/Dropbox/GEUS/bibliometrics_GEUS/bibliometric_GoK/'
os.chdir(base_path)

opath='./output/altmetric/'

api = 'https://api.altmetric.com/v1/doi/'

fn='./input/GoK_publications_all.xlsx'
df=pd.read_excel(fn)#,header=None)
file1 = open(fn, "r")
# DOIs=df.DOI
# journal=df.
# #%%

# journal=df.iloc[:,2]
# ifactor=df.iloc[:,4]

# author=df.iloc[:,37]
# # dept=np.array(df.iloc[:,9])
# glac=df.iloc[:,9]
# paleo=df.iloc[:,16]
# # print(author[5:10])

# Gok_only=0

# if Gok_only:
#     df = df.drop( (df[df.iloc[:,9]!=1].index) & (df[df.iloc[:,16]!=1].index)  )
#     df=df.drop(df.columns[11:15], axis=1)
#     df=df.drop(df.columns[0:2], axis=1)
    
#     for i in range(0,27):
#         df=df.drop(df.columns[df.columns=='drop.'+str(i)], axis=1)
#     df=df.drop(df.columns[df.columns=='drop.'], axis=1)
#     df=df.drop(df.columns[df.columns=='Citations Jul 21'], axis=1)
    
    # df=df.reset_index(drop=True)

# print(df.columns)

# DOI_list=df.DOI

# df['Citations Sep 21']=np.nan
# df['year']=np.nan

n=len(df)

# count citations and record year explicitly

f404=open(opath+'_errors.txt','w')
f404.write("Altmetric doesn't have any details for the article or set of articles you requested.\n")
c_err=0

# for i,doi in enumerate(df.DOI[0]):
for i,doi in enumerate(df.DOI):
    # print()
    print(i,n-i,doi)
    if type(doi)==float:doi="9999"
    if type(doi)==int:doi="9999"
    # if i<=2000: # counter to set to latest value if/when a timeout occurs, i.e. crossref is not reachable
    if i>=0: # counter to set to latest value if/when a timeout occurs, i.e. crossref is not reachable
    # if i==0: # counter to set to latest value if/when a timeout occurs, i.e. crossref is not reachable
        # test doi 
        # doi='10.1088/1748-9326/aaf2ed'
        if doi[0:3]=="10.":
            # if n-i<=3400: # counter to set to latest value if/when a timeout occurs, i.e. crossref is not reachable
            time.sleep(1.1) # delay by one sec since altmetric api is time limited
            responses=requests.get(api + doi)
            # responses=requests.get("https://doi.org/10.1175/MWR-D-18-0366.1")
            print('response code',responses.status_code)
            if responses.status_code==200:
                result=responses.json()
                if (('authors' in result)&('journal' in result)):
                    if len(result['authors'])>0:
                        last_name=result['authors'][0].split(' ')[-1]
            
                        journal = result['journal']#.replace(" ",'_')
                        
                        score = result['score']
                        timestamp = result['published_on']
                        datex = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')#' %H:%M:%S')
                        # print("Converted date and time:", unix_conversion)
                        title=str(last_name+' '+str(datex)+' '+journal+' altmetric score '+f'{score:.1f}')
                        title2=f'{score:.1f} '+str(last_name+' '+str(datex)+' '+journal)
                        # print(title)
                        # print(sorted(result.keys()))
                        # print(doi,api + doi,responses.status_code)
                        result_string=json.dumps((result),sort_keys=True,indent=4)
            
                        with open(opath+title+'.txt','w') as f:
                            f.write(result_string)
                        with open('./output/altmetric/am_score_rank/'+title2+'.txt','w') as f:
                            f.write(result_string)
            if responses.status_code!=200:
                c_err+=1
                err_msg=str(c_err)+','+str(responses.status_code)+','+str(doi)+','+df.article[i]
                print(err_msg)
                f404.write(err_msg+'\n')
                # print(df.article[i])
                
f404.close()             