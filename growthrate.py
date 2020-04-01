import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import datetime as dt
from datetime import datetime

import matplotlib.pyplot as plt

#Look at growth rate




def getGrowthRate(xt, y):
    
    #Get overall best bit
    y_log = np.log(y)
    p = np.polyfit(xt, y_log, 1)

    y_estimate = np.polyval(p, xt)

    print('Average Growth Rate for: {}%'.format(100*(np.exp(p[0])-1)))
    print('Starting point: {}'.format(np.exp(p[1])))
    print('tau: {}'.format(p[0]))
    plt.figure()
    plt.plot(x, y_log)
    plt.plot(x, y_estimate)


    #Get average growth rate over moving window of N days
    mv_days = 7
    gr = np.zeros(len(xt)-mv_days)
    for i in range(len(xt)-mv_days):
        xtemp = xt[i:(i+mv_days)]
        ytemp = y_log[i:(i+mv_days)]
        #print(xtemp)
        p = np.polyfit(xtemp, ytemp, 1)
        gr[i] = np.exp(p[0])
    

    plt.figure()
    plt.plot(gr)
    plt.ylabel('Growth rate')

    print(xt[mv_days:])
    return xt[mv_days:], gr



texascases = pd.read_csv('Dallas.csv')
x = texascases.iloc[:,0]
y = texascases.iloc[:,1]

#print(np.isnan(y))
isnan = ~np.isnan(y)
#print(isnan)
y = y[isnan]
x = x[isnan]

[xdallas, grdallas] = getGrowthRate(np.arange(len(x)), y)
print(x[xdallas])
xd = x[xdallas]

texascases = pd.read_csv('texascases.csv')
x = texascases.iloc[:,0]
y = texascases.iloc[:,1]
y1 = texascases.iloc[:,2]
y2 = texascases.iloc[:,3]

#print(np.isnan(y))
isnan = ~np.isnan(y)
#print(isnan)
y = y[isnan]
x = x[isnan]
print(x)
[xtexas, grtexas] = getGrowthRate(np.arange(len(x)), y)
xt = x[xtexas+3]
print('Texas = {}'.format(xt))

texascases = pd.read_csv('Harris.csv')
x = texascases.iloc[:,0]
y = texascases.iloc[:,1]

#print(np.isnan(y))
isnan = ~np.isnan(y)
#print(isnan)
y = y[isnan]
x = x[isnan]
[xharris, grharris] = getGrowthRate(np.arange(len(x)), y)
xh = x[xharris]

texascases = pd.read_excel('AustinCases.xlsx', sheet_name='Austin')

x = texascases.iloc[:,0]
y = texascases.iloc[:,1]

#print(np.isnan(y))
isnan = ~np.isnan(y)
#print(isnan)
y = y[isnan]
x = x[isnan]
[xaustin, graustin] = getGrowthRate(np.arange(len(x)), y)
xa = x[xaustin]

plt.plot(np.diff(y))


data = pd.DataFrame()
data['Date'] = xt
data['Texas'] = grtexas
temp = np.zeros(len(grtexas))
temp[:(len(grtexas)-len(graustin))] = np.NaN
temp[(len(grtexas) - len(graustin)):] = graustin
data['Austin'] = temp
temp = np.zeros(len(grtexas))
temp[:(len(grtexas)-len(grdallas))] = np.NaN
temp[(len(grtexas) - len(grdallas)):] = grdallas
data['Dallas'] = temp
temp = np.zeros(len(grtexas))
temp[:(len(grtexas)-len(grharris))] = np.NaN
temp[(len(grtexas) - len(grharris)):] = grharris
data['Harris'] = temp


print(data)
data.to_csv('gr_rate.csv')

plt.show()

