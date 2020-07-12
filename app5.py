#Creating dashboard of covid cases

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

#Austin: http://www.austintexas.gov/COVID19
#Dallas: https://www.dallascounty.org/covid-19/
#Harris: http://publichealth.harriscountytx.gov/Resources/2019-Novel-Coronavirus/Harris-County-COVID-19-Confirmed-Cases
#Texas : https://txdshs.maps.arcgis.com/apps/opsdashboard/index.html#/ed483ecd702b4298ab01e8b9cafc8b83
#Texas: https://txdshs.maps.arcgis.com/apps/opsdashboard/index.html#/ed483ecd702b4298ab01e8b9cafc8b83
#John hopkins data: https://github.com/CSSEGISandData/COVID-19
#https://public.tableau.com/profile/christopher.paolini#!/vizhome/COVID-19Dashboard_15850633730350/UnitedStatesCOVID-19CaseTracker
#url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
#      https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'


def createLayout(title, xlabel, ylabel):
    
    layout = go.Layout(
        title={'text':title,
           'x':0.5,'y':0.9,
               'xanchor':'center','yanchor':'top'
            },
        yaxis=dict(
            title=ylabel,
            linecolor=colors['text'],
            linewidth=2,
            mirror=True,
            showgrid=False,ticks='outside',fixedrange=True,automargin=False,
            title_standoff=200,
            constrain="domain"),
        xaxis=dict(linewidth=2,linecolor=colors['text'],mirror=True,showgrid=False,ticks='outside', fixedrange=True,automargin=True),
        xaxis_title=xlabel,
        autosize=True,
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['plotbg'],
        font=dict(color=colors['text'],size=14, family='Sans Serif'),
        legend=dict(x=0.02,y=0.85,bgcolor=colors['plotbg'],orientation='v'),
    )
    return layout

def layoutUpdate(fig, pattern1, pattern2, logticks):

    fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{'visible':pattern1},
                          {'yaxis':{'type':'linear', 'title':'Total', 'ticks':'outside', 'fixedrange':True, 'automargin':True,
                                    'linewidth':2, 'mirror':True, 'linecolor':colors['text']}}],
                    
                    label="linear",
                    method="update",
                
                
                    ),
                dict(
                    args=[{'visible':pattern2},
                          {'yaxis':{'type':'log', 'title':'Total', 'tickvals':logticks, 'ticks':'outside', 'fixedrange':True, 'automargin':True,
                                    'linewidth':2, 'mirror':True, 'linecolor':colors['text']}}],
                          #{'yaxis':{'visible':[False,True]}}],
                    label="log",
                    method="update"
                    )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            bgcolor='white',
            
            x=0.02,
            xanchor="auto",
            y=1,
            yanchor="auto"
            )
        ]
    )
    return fig

def getSummary(cases):

    casesToday = int(cases[len(cases)-1])
    newCasesToday = int(np.diff(cases)[-1])
    newCasesYesterday = int(np.diff(cases)[-2])
    if newCasesToday > newCasesYesterday:
        caseIncrease = colors['up']
    else:
        caseIncrease = colors['down']

    return casesToday, newCasesToday, caseIncrease

def getBestFit(data, dates, startpt, tau):
    
    #Get most recent date and increment by 1
    lstdate = (data['Date'][len(data)-1])
    lstdate = datetime.strptime(lstdate, '%m/%d/%y')
    lstdate += dt.timedelta(days=1)
    lstdate = lstdate.strftime('%m/%d/%y')

    #Use multiple best fit lines
    yt = 0
    for idx, d in enumerate(dates):
    
        if idx == len(dates)-1: #If at the end
            xt = np.arange(len(data['Date'][d:])+1)
        else:
            xt = np.arange(len(data['Date'][d:dates[idx+1]]))
            #xt = np.arange(len(data['Date'])+1)
        yt_temp = np.round( np.exp(xt*tau[idx])*startpt[idx])
        if idx == 0:
            yt = yt_temp
        else:
            yt = np.append(yt, yt_temp)            
    newdate = (data['Date'].copy())
    newdate = newdate.append(pd.Series(lstdate))

    return newdate, yt

colors = {
    'background': '#F5F5F5',
    'text': '#484848',
    'plotbg': '#FDFDFD',
    'up': 'red',
    'down': 'green'
    }

#Load all data
gr = pd.read_csv('gr_rate.csv')
texascases = pd.read_csv('texascases.csv')
austincases = pd.read_excel('AustinCases.xlsx', sheet_name='Austin')
houstoncases = pd.read_csv('Harris.csv')
dallascases = pd.read_csv('Dallas.csv')

###############Plot growth rate
grdate = gr['Date']
grt = (gr['Texas']-1)*100
gra = (gr['Austin']-1)*100
grd = (gr['Dallas']-1)*100
grh = (gr['Harris']-1)*100

trace1 = go.Scatter(x = grdate, y = grt, name="Texas", mode="lines+markers")
trace2 = go.Scatter(x = grdate, y = gra, name="Austin", mode="lines+markers")
trace3 = go.Scatter(x = grdate, y = grd, name="Dallas", mode="lines+markers")
trace4 = go.Scatter(x = grdate, y = grh, name="Harris", mode="lines+markers")
data_gr = [trace1, trace2, trace3, trace4]
layout_gr = createLayout('Growth rate (7 day intervals)', 'Date', 'Growth rate [%]')
fig_gr=go.Figure(data_gr, layout=layout_gr)

##############R0 calculation
#x_a = austincases['Date'][1:]
#new_a = np.diff(austincases['Cumulative Cases'])


#####################AUSTIN 
trace1 = go.Scatter(x=austincases['Date'], y=austincases['Cumulative Cases'], name="Linear", mode = 'lines+markers')
trace2 = go.Scatter(x=austincases['Date'], y=austincases['Cumulative Cases'], name="Logarithmic",mode = 'lines+markers', visible=False)

newdate, yt = getBestFit(austincases, [0, 6, 24, 40], [3.2, 57, 554, 1363], [0.5, 0.128, 0.06, 0.028])

trace3 = go.Scatter(x = newdate, y = yt, name='Best Fit+Estimate', visible=False, mode='lines+markers', line={'dash':'dash', 'color':'black'})
#Create trace for new cases
trace4 = go.Bar(x = austincases['Date'][1:], y=np.diff(austincases['Cumulative Cases']), name='New Cases', visible=True)

austinToday, austinNewCasesToday, austinincrease = getSummary(austincases['Cumulative Cases'])

data_austin = [trace1, trace2, trace3, trace4]
layout_austin = createLayout('Total Cases in Travis County', 'Date', 'Total')
fig2=go.Figure(data_austin, layout=layout_austin)
fig2 = layoutUpdate(fig2, [True, False, False, True], [False, True, True, False], [0,10,100,1000])


###############DALLAS

trace1 = go.Scatter(x=dallascases['Date'], y=dallascases['Count'], name="Linear", mode = 'lines+markers')
trace2 = go.Scatter(x=dallascases['Date'], y=dallascases['Count'], name="Logarithmic",mode = 'lines+markers', visible=False)
#trace2 = go.Scatter(x=dallascases['Date'], y=dallascases['Count'], yaxis='y2', name="Logarithmic",mode = 'lines+markers')
#Create trace for new cases
trace3 = go.Bar(x = dallascases['Date'][1:], y=np.diff(dallascases['Count']), name='New Cases', visible=True)

newdate, yt = getBestFit(dallascases, [0, 16, 25, 50], [4, 290, 1050, 3700], [0.27, 0.125, 0.05, 0.03])
trace4 = go.Scatter(x = newdate, y = yt, name='Best Fit+Estimate', visible=False, mode='lines+markers', line={'dash':'dash', 'color':'black'})

dallasToday, dallasNewCasesToday, dallasincrease = getSummary(dallascases['Count'])

data_dallas = [trace1, trace2, trace3, trace4]
layout_dallas = createLayout('Total Cases in Dallas County', 'Date', 'Total')
fig2d=go.Figure(data_dallas, layout=layout_dallas)

fig2d = layoutUpdate(fig2d, [True, False, True, False], [False, True, False, True], [0, 10, 100, 1000])

###############HARRIS
trace1 = go.Scatter(x=houstoncases['Date'], y=houstoncases['Count'], name="Linear", mode = 'lines+markers')
trace2 = go.Scatter(x=houstoncases['Date'], y=houstoncases['Count'], name="Logarithmic",mode = 'lines+markers', visible=False)
trace3 = go.Bar(x = houstoncases['Date'][1:], y=np.diff(houstoncases['Count']), name='New Cases', visible=True)

newdate, yt = getBestFit(houstoncases, [0, 35, 50], [3, 3127, 5482], [0.2, 0.041, 0.028])
trace4 = go.Scatter(x = newdate, y = yt, name='Best Fit+Estimate', visible=False, mode='lines+markers', line={'dash':'dash', 'color':'black'})

harrisToday, harrisNewCasesToday, harrisincrease = getSummary(houstoncases['Count'])

data_harris = [trace1, trace2, trace3, trace4]
layout_harris = createLayout('Total Cases in Harris County', 'Date', 'Total')
fig2h=go.Figure(data_harris, layout=layout_harris)
fig2h = layoutUpdate(fig2h, [True, False, True, False], [False, True, False, True], [0, 10, 100, 1000])


########TEXAS

#Plot texas numbers
x = texascases.iloc[:,0]
y = texascases.iloc[:,1] #Point1Acre
y1 = texascases.iloc[:,2] #Not using, USA Today
y2 = texascases.iloc[:,3] #JHU

texasToday, texasNewCasesToday, texasincrease = getSummary(y)
trace1 = go.Scatter(x=x, y=y, name="Point1-Linear",mode = 'lines+markers')
trace1A = go.Scatter(x = x, y = y2, name="JHU-Linear", mode='lines+markers')
#trace2 = go.Scatter(x=x, y=(y2+y)*0.5, name="Average-Logarithmic",mode = 'lines+markers', visible=False)
trace2 = go.Scatter(x=x, y=(2*y)*0.5, name="Average-Logarithmic",mode = 'lines+markers', visible=False)

trace4 = go.Bar(x = x[1:], y=np.diff(y), name='New Cases', visible=True)
newdate, yt = getBestFit(texascases[3:], [0, 24, 37, 43], [4.57, 2900, 12400, 18000], [0.27, 0.115, 0.0535, 0.03])
trace3 = go.Scatter(x = newdate, y = yt, name='Best Fit+Estimate', visible=False, mode='lines+markers', line={'dash':'dash', 'color':'black'})


data_texas = [trace1, trace1A, trace2, trace3, trace4]
layout_texas = createLayout('Total Cases in Texas', 'Date', 'Total')
fig3=go.Figure(data_texas, layout=layout_texas)
#fig3.update_yaxes(tick0=20)
fig3 = layoutUpdate(fig3, [True, True, False, False, True], [False, False, True, True, False], [0, 10, 100, 1000, 10000])




external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__, assets_external_path='http://assets/')
app.title = 'Tracking COVID-19 cases in Austin and Texas'



spacing="two columns"

app.layout = html.Div(style={'backgroundColor':colors['background'],'textAlign':'center', 'max-width':'1200px',
                             'border':'thick solid black', 'margin-left':'auto', 'margin-right':'auto', 'id':'grid'},
            children=[
                html.H1(children='Keeping track of COVID19 in  Texas',
                        style={'textAlign':'center',
                               'color':colors['text']}),
                #html.H5(style={'color':colors['text']},children='Austin data updated on 4/1/20. Texas data updated 4/1/20.'),
                html.Div([
                    html.Div(),
                    html.Div([html.P(html.B('Texas')),
                              html.P('Updated: 7/11/2020'),
                              html.P('Total: '+str(texasToday)),
                              html.P(['New: ',html.Span(str(texasNewCasesToday), style={'color':texasincrease})])], style={'textAlign':"center",
                                                       'borderRadius':'4px','border':'solid darkgrey',
                                                                                     'margin':'4px',
                                                                                     
                                                       'backgroundColor':'lightgrey'},
                             className=spacing),
                    html.Div([html.P(html.B('Travis County')),
                              html.P('Updated: 7/11/2020'),
                              html.P('Total: '+str(austinToday)),
                              html.P(['New: ',html.Span(str(austinNewCasesToday), style={'color':austinincrease})])],
                             style={'textAlign':"center",
                                                       'borderRadius':'4px',
                                                                                      'border':'solid darkgrey',
                                                       'margin':'4px',
                                                       'backgroundColor':'lightgrey'},
                             className=spacing),
                    html.Div([html.P(html.B('Dallas County')),
                              html.P('Updated: 7/10/2020'),
                              html.P('Total: '+str(dallasToday)),
                               html.P(['New: ',html.Span(str(dallasNewCasesToday), style={'color':dallasincrease})])],
                    
                    style={'textAlign':"center",
                                                       'borderRadius':'4px','border':'solid darkgrey',
                                                       'margin':'4px',
                                                       'backgroundColor':'lightgrey'},
                             className=spacing),
                    html.Div([html.P(html.B('Harris County')),
                              html.P('Updated: 7/11/2020'),
                              html.P('Total: '+str(harrisToday)),
                               html.P(['New: ',html.Span(str(harrisNewCasesToday), style={'color':harrisincrease})])],
                         
                         style={'textAlign':"center",
                                                       'borderRadius':'4px','border':'solid darkgrey',
                                                       'margin':'2px',
                                                       'backgroundColor':'lightgrey'},
                             className=spacing),
                    html.Div([dcc.Graph(figure=fig3,
                        config={'scrollZoom':True,'responsive':True})], className="nine columns"),
                    html.Div([dcc.Graph(figure=fig2,
                        config={'scrollZoom':True,'responsive':True})], className="nine columns"),
                    html.Div([dcc.Graph(figure=fig2d,
                        config={'scrollZoom':True,'responsive':True})], className="nine columns"),
                    html.Div([dcc.Graph(figure=fig2h,
                                        config={'scrollZoom':True,'responsive':True})], className="nine columns"),
                    html.Div([dcc.Graph(figure=fig_gr,
                        config={'scrollZoom':True,'responsive':True})], className="nine columns")],
                         className="row"),
                html.H5(style={'color':colors['text']},children='Data sources:  Texas data obtained from John Hopkins data set (https://github.com/CSSEGISandData) and https://coronavirus.1point3acres.com/. Austin, Dallas, Harris County data obtained from John Hopkins,  Travis County, and USA Facts (https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/).  Delayed reporting results in slight discrepencies.')

]

                      )


#Create responsive site via https://www.w3schools.com/html/html_responsive.asp
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta property="og:title" content="Tracking COVID-19 in Texas">
        <meta property="og:url" content="http://www.covid19intexas.com">
        <meta property="og:type" content="website">
        <meta property="og:image" content="http://www.el-chammas.com/images/preview.jpg">
        <meta property="og:description" content="Daily updates of cases in Texas.">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
<!-- Default Statcounter code for Covid10
http://www.covid19intexas.com -->
<script type="text/javascript">
var sc_project=12224865; 
var sc_invisible=1; 
var sc_security="5c457a33"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics
Made Easy - StatCounter" href="https://statcounter.com/"
target="_blank"><img class="statcounter"
src="https://c.statcounter.com/12224865/0/5c457a33/1/"
alt="Web Analytics Made Easy -
StatCounter"></a></div></noscript>
<!-- End of Statcounter Code -->
    </body>
</html>
'''

'''       <!-- Default Statcounter code for Covid10
http://www.covid19intexas.com -->
<script type="text/javascript">
var sc_project=12224865; 
var sc_invisible=1; 
var sc_security="5c457a33"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics
Made Easy - StatCounter" href="https://statcounter.com/"
target="_blank"><img class="statcounter"
src="https://c.statcounter.com/12224865/0/5c457a33/1/"
alt="Web Analytics Made Easy -
StatCounter"></a></div></noscript>
<!-- End of Statcounter Code -->'''

#This is new
server = app.server

              
        
              
if __name__ == '__main__':
    app.run_server(debug=True)

 #   dcc.
    

            
                            
