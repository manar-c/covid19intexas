
import pandas as pd
import requests
import io
import numpy as np

#Goal: go through daily reports of JHU to get data for
# Texas, Travis, Harris, Dallas

baseurl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'


#Start from March 1
#March 1 to March 21: jh only reported texas
#March 22 onwards, jh reported county level


results = {}

#JHU changed the formats several times

maxday0 = 9
for i in range(maxday0):
        strbase = '03-0'+str(i+1)+'-2020.csv'
        url = baseurl + strbase
        df = pd.read_csv(url)
        result = df[df['Province/State'].str.contains(', TX', na=False)].Confirmed.sum(axis=0)
        print(result)
        results[strbase] = result
#x = sdfsdfsfd

maxday1 = 21
for i in range(maxday0,maxday1):
        strbase = '03-'
        if i+1 < 10:
                strbase += '0'+str(i+1)
        else:
                strbase += str(i+1)
        strbase += '-2020.csv'
        url = baseurl+strbase
        print(url)
        df = pd.read_csv(url)
        result = df[df['Province/State']=='Texas'].Confirmed.to_numpy()
        if len(result) > 0:
                results[strbase] = np.ndarray.item(result)
#                print(np.size(result))
maxday2 = 31
for i in range(maxday1, maxday2):
        strbase = '03-'+str(i+1) + '-2020.csv'
        url = baseurl + strbase
        print(url)
        df = pd.read_csv(url)
        result = df[df['Province_State'] == 'Texas'].Confirmed.sum(axis=0)
        results[strbase] = result
maxday2 = 5
for i in range(0, maxday2):
        strbase = '04-0'+str(i+1) + '-2020.csv'
        url = baseurl + strbase
        print(url)
        df = pd.read_csv(url)
        result = df[df['Province_State'] == 'Texas'].Confirmed.sum(axis=0)
        results[strbase] = result

print(results)
        
