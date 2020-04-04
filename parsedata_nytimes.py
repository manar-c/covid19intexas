
import pandas as pd
import requests
import io
import numpy as np
import math

url = "http://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv"
url = 'https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv?_ga=2.95840092.1764237867.1585191885-1918575016.1585191885'

url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

#This function is taken from stackoverflow.  Pretends to be a browser.
def get_sheet(sheet_url):
        # Accesses CME direct URL (at the moment...will add functionality for ICE later)
        # Gets sheet and puts it in dataframe
        #Returns dataframe sheet

#        sheet_url = "http://www.cmegroup.com/CmeWS/exp/voiProductDetailsViewExport.ctl?media=xls&tradeDate="+str(self.date_of_report)+"&reportType="\
#        + str(self.report_type)+"&productId=" + str(self.product)

        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        req = requests.get(url = sheet_url, headers = header).content
        file_object = io.StringIO(req.decode('utf-8'))
        data_sheet = pd.read_csv(file_object)
        return data_sheet
    
#df = (get_sheet(url))
df = pd.read_csv(url)
#print(df.tail)
#x = sdfsdfsd
#s = requests.get(url).content
#df = pd.read_csv(url, error_bad_lines=False)

#Print first 5 column names
#print(list(df.columns[0:4]))

def extractdata(texascases):
        txint = np.zeros(len(texascases))
        for idx,tx in enumerate(texascases):
                if not math.isnan(tx):
                        txint[idx] = int(tx)
                
        casestart =  txint > 0

        print((texascases[casestart]))

        
#Use -1 to remove last day
#Sum over all texas counties
austincases = df[df['county'] == 'Travis']#.iloc[:,4:].sum(axis=0)
print('TOTAL Austin')
print(austincases)
harriscases = df[df['county'] == 'Dallas']
print(harriscases)
harriscases = df[df['county'] == 'Harris']
print(harriscases)

x = sdfsdf
extractdata(texascases)
texascases = df[df['County Name'] == 'Travis County'].iloc[0,4:]
print('TOTAL AUSTIN')
extractdata(texascases)

texascases = df[df['State'] == 'TX'][df['County Name'] == 'Dallas County'].iloc[0,4:]
print('TOTAL DALLAS')
extractdata(texascases)

texascases = df[df['State'] == 'TX'][df['County Name'] == 'Harris County'].iloc[0,4:]
print('TOTAL Harris')
extractdata(texascases)


#print(texascases)
#print(texascases[10])
#Convert all to int since some are string?!
#txint = np.zeros(len(texascases))
#for idx,tx in enumerate(texascases):
#    txint[idx] = int(tx)
#casestart =  txint > 0
#print((texascases[casestart]))
