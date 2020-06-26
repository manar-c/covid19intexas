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
#Estimate R0




def getGrowthRate(xt, y, days=7):
    
    #Get overall best bit
    y_log = np.log(y)
    p = np.polyfit(xt, y_log, 1)

    y_estimate = np.polyval(p, xt)

    print('Average Growth Rate for: {}%'.format(100*(np.exp(p[0])-1)))
    print('Starting point: {}'.format(np.exp(p[1])))
    print('tau: {}'.format(p[0]))
    #plt.figure()
    #plt.plot(x, y_log)
    #plt.plot(x, y_estimate)


    #Get average growth rate over moving window of N days
    mv_days = days
    gr = np.zeros(len(xt)-mv_days)
    for i in range(len(xt)-mv_days):
        xtemp = xt[i:(i+mv_days)]
        ytemp = y_log[i:(i+mv_days)]
        #print(xtemp)
        p = np.polyfit(xtemp, ytemp, 1)
        gr[i] = np.exp(p[0])
    

    #plt.figure()
    #plt.plot(gr)
    #plt.ylabel('Growth rate')

    print(xt[mv_days:])
    return xt[mv_days:], gr

def getR0(xt, y):
    newcases = np.diff(y)
    print(newcases)
    [x,yt] = getGrowthRate(np.arange(len(newcases)), newcases, days=7)

    print(x)
    print(yt)

    #Get the log
    print(newcases)
    
    log_new = np.log(newcases)
    
    print(log_new)
    #x = sdfsdf
    mv_days_n0 = 7
    mv_days_nt = 7
    #Basically, fit R0 to the above by creating enough data sets
    ln_n0 = []
    ln_nt = []
    t = []
    r0 = []
    for i in range(len(xt)-mv_days_n0-mv_days_nt):
        ln_n0 = []
        ln_nt = []
        t = []
        for j in range(mv_days_n0):
            for k in range(mv_days_nt):
                ln_n0.append(log_new[i+j])
                ln_nt.append(log_new[i+j+k])
                t.append(k)
        #Do a best fit on this
        #ln(n(t)) = ln(n(0)) + K*t
        #print(t)
        print(ln_nt)
        print(ln_n0)
        p = np.polyfit(np.array(t), np.array(ln_nt)-np.array(ln_n0), 1)
        print(p[0])
        print('R0 = {}'.format(np.exp(p[0]*1)))
        r0.append(np.exp(p[0]*1))
    plt.figure()
    plt.plot(np.array(r0))
    plt.show()

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

print(x)
print(y)
#x - sdfsfd
getR0(x, y)
#plt.plot(np.diff(y))

#x = sdfsfd

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

