#Creating dashboard of covid cases

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#Austin: http://www.austintexas.gov/COVID19
#Dallas: https://www.dallascounty.org/covid-19/
#Harris: http://publichealth.harriscountytx.gov/Resources/2019-Novel-Coronavirus/Harris-County-COVID-19-Confirmed-Cases
#Texas : https://txdshs.maps.arcgis.com/apps/opsdashboard/index.html#/ed483ecd702b4298ab01e8b9cafc8b83

#John hopkins data: https://github.com/CSSEGISandData/COVID-19
#https://public.tableau.com/profile/christopher.paolini#!/vizhome/COVID-19Dashboard_15850633730350/UnitedStatesCOVID-19CaseTracker
#url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
#      https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'

loadnewdata = False

if loadnewdata:
    #globalcases = pd.read_csv(url, error_bad_lines=False)
    globalcases = pd.read_csv('jhdata_20200323.csv')
    texascases = globalcases[globalcases['Province/State']=='Texas'].iloc[0,4:]

    #Find first data for texas
    casestart = texascases > 0
    texascases = texascases[casestart]
    texascases.to_csv('texascases.csv')


texascases = pd.read_csv('texascases.csv')
x = texascases.iloc[:,0]
y = texascases.iloc[:,1]
y1 = texascases.iloc[:,2]
y2 = texascases.iloc[:,3]
#x = texascases[casestart].index.values
#y = texascases[casestart]

#x = texascases.index.values
#y = texascases

#print(x)

#x = sdfsfdsfs


austincases = pd.read_excel('AustinCases.xlsx', sheet_name='Austin')
houstoncases = pd.read_csv('Harris.csv')
dallascases = pd.read_csv('Dallas.csv')
#print(austincases.head())

colors = {
    'background': '#F5F5F5',
    'text': '#484848',
    'plotbg': '#FDFDFD'
    }



#####################AUSTIN #Linear
trace1 = go.Scatter(x=austincases['Date'], y=austincases['Cumulative Cases'], name="Linear", mode = 'lines+markers')
#trace2 = go.Scatter(x=austincases['Date'], y=austincases['Cumulative Cases'], yaxis='y2', name="Logarithmic",mode = 'lines+markers', visible=False)
trace2 = go.Scatter(x=austincases['Date'], y=austincases['Cumulative Cases'], name="Logarithmic",mode = 'lines+markers', visible=False)


data = [trace1, trace2]
layout = go.Layout(
    title={'text':'Total Cases in Austin, TX',
           'x':0.5,'y':0.9,
           'xanchor':'center','yanchor':'top'},
    yaxis=dict(
        title='Total',
        linecolor=colors['text'],
        linewidth=2,
        mirror=True,
        #type="linear",
        showgrid=False,ticks='outside',fixedrange=True,automargin=True),
        #type='log'),
 #   yaxis2=dict(
 #       title='Count',
 #       overlaying='y',
        #side='right',
 #       type='log',
 #       showgrid=False,ticks='outside',tickvals=[0,10,100],fixedrange=True,automargin=True,visible=False
 #       ),
    xaxis=dict(linewidth=2,linecolor=colors['text'],mirror=True,showgrid=False,ticks='outside', fixedrange=True,automargin=True),
    xaxis_title='Date',
    autosize=True,
    #width=1000,
    #height=1000,
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['plotbg'],
    font=dict(color=colors['text'],size=10),
    legend=dict(x=0,y=1,bgcolor=colors['plotbg'],orientation='h')
    )

fig2=go.Figure(data, layout=layout)
fig2.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{'visible':[True, False]},
                          {'yaxis':{'type':'linear', 'title':'Total', 'ticks':'outside', 'fixedrange':True, 'automargin':True,
                                    'linewidth':2, 'mirror':True, 'linecolor':colors['text']}}],
                         # {'yaxis':{'visible':[True, False]}}],
                    label="linear",
                    method="update",
                
                    ),
                dict(
                    args=[{'visible':[False, True]},
                          {'yaxis':{'type':'log', 'title':'Total', 'tickvals':[0,10,100], 'ticks':'outside', 'fixedrange':True, 'automargin':True,
                                    'linewidth':2, 'mirror':True, 'linecolor':colors['text']}}],
                          #{'yaxis':{'visible':[False,True]}}],
                    label="log",
                    method="update"
                    )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            bgcolor='white',
            
            x=0.04,
            xanchor="left",
            y=0.95,
            yanchor="top"
            )
        ]
    )


###############DALLAS

trace1 = go.Scatter(x=dallascases['Date'], y=dallascases['Count'], name="Linear", mode = 'lines+markers')
trace2 = go.Scatter(x=dallascases['Date'], y=dallascases['Count'], name="Logarithmic",mode = 'lines+markers', visible=False)
#trace2 = go.Scatter(x=dallascases['Date'], y=dallascases['Count'], yaxis='y2', name="Logarithmic",mode = 'lines+markers')

data = [trace1, trace2]
layout_d = go.Layout(
    title={'text':'Total Cases in Dallas, TX',
           'x':0.5,'y':0.9,
           'xanchor':'center','yanchor':'top'},
    yaxis=dict(
        title='Total',
        linecolor=colors['text'],
        linewidth=2,
        mirror=True,
        showgrid=False,ticks='outside',fixedrange=True,automargin=True),
        #type='log'),
 #   yaxis2=dict(
 #       title='Log',
 #       overlaying='y',
 #       side='right',
 #       type='log',
 #       showgrid=False,ticks='outside',tickvals=[0,10,100],fixedrange=True,automargin=True
 #       ),
    xaxis=dict(linewidth=2,linecolor=colors['text'],mirror=True,showgrid=False,ticks='outside',fixedrange=True,automargin=True),
    xaxis_title='Date',
    autosize=True,
    #width=1000,
    #height=1000,
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['plotbg'],
    font=dict(color=colors['text'],size=10),
    legend=dict(x=0,y=1,bgcolor=colors['plotbg'],orientation='h')
    )

fig2d=go.Figure(data, layout=layout_d)
fig2d.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{'visible':[True, False]},
                          {'yaxis':{'type':'linear', 'title':'Total', 'ticks':'outside', 'fixedrange':True, 'automargin':True,
                                    'linewidth':2, 'mirror':True, 'linecolor':colors['text']}}],
                         # {'yaxis':{'visible':[True, False]}}],
                    label="linear",
                    method="update",
                
                    ),
                dict(
                    args=[{'visible':[False, True]},
                          {'yaxis':{'type':'log', 'title':'Total', 'tickvals':[0,10,100], 'ticks':'outside', 'fixedrange':True, 'automargin':True,
                                    'linewidth':2, 'mirror':True, 'linecolor':colors['text']}}],
                          #{'yaxis':{'visible':[False,True]}}],
                    label="log",
                    method="update"
                    )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            bgcolor='white',
            
            x=0.04,
            xanchor="left",
            y=0.95,
            yanchor="top"
            )
        ]
    )

###############HARRIS
trace1 = go.Scatter(x=houstoncases['Date'], y=houstoncases['Count'], name="Linear", mode = 'lines+markers')
trace2 = go.Scatter(x=houstoncases['Date'], y=houstoncases['Count'], name="Logarithmic",mode = 'lines+markers', visible=False)

data = [trace1, trace2]
layout_h = go.Layout(
    title={'text':'Total Cases in Harris County, TX',
           'x':0.5,'y':0.9,
           'xanchor':'center','yanchor':'top'},
    yaxis=dict(
        title='Total',
        linecolor=colors['text'],
        linewidth=2,
        mirror=True,
        showgrid=False,ticks='outside',fixedrange=True,automargin=True),
        #type='log'),
 
    xaxis=dict(linewidth=2,linecolor=colors['text'],mirror=True,showgrid=False,ticks='outside',automargin=True,fixedrange=True),
    xaxis_title='Date',
    autosize=True,
    #width=1000,
    #height=1000,
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['plotbg'],
    font=dict(color=colors['text'],size=10),
    legend=dict(x=0,y=1,bgcolor=colors['plotbg'],orientation='h')
    )

fig2h=go.Figure(data, layout=layout_h)
fig2h.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{'visible':[True, False]},
                          {'yaxis':{'type':'linear', 'title':'Total', 'ticks':'outside', 'fixedrange':True, 'automargin':True,
                                    'linewidth':2, 'mirror':True, 'linecolor':colors['text']}}],
                         # {'yaxis':{'visible':[True, False]}}],
                    label="linear",
                    method="update",
                
                    ),
                dict(
                    args=[{'visible':[False, True]},
                          {'yaxis':{'type':'log', 'title':'Total', 'tickvals':[0,10,100], 'ticks':'outside', 'fixedrange':True, 'automargin':True,
                                    'linewidth':2, 'mirror':True, 'linecolor':colors['text']}}],
                          #{'yaxis':{'visible':[False,True]}}],
                    label="log",
                    method="update"
                    )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            bgcolor='white',
            
            x=0.04,
            xanchor="left",
            y=0.95,
            yanchor="top"
            )
        ]
    )




trace1 = go.Scatter(x=x, y=y, name="Point1-Linear",mode = 'lines+markers')
trace1A = go.Scatter(x = x, y = y2, name="JHU-Linear", mode='lines+markers')
trace2 = go.Scatter(x=x, y=(y2+y)*0.5, name="Average-Logarithmic",mode = 'lines+markers', visible=False)

data2 = [trace1, trace1A, trace2]
layout2 = go.Layout(
    title={'text':'Total Cases in Texas',
           'x':0.5,'y':0.9,
           'xanchor':'center','yanchor':'top'},

    yaxis=dict(
        title='Total',
        linecolor=colors['text'],
        linewidth=2,
        mirror=True,
        showgrid=False,ticks='outside',automargin=True,fixedrange=True),
        #type='log'),

    xaxis=dict(linewidth=2,linecolor=colors['text'],mirror=True,showgrid=False,ticks='outside',automargin=True,fixedrange=True),
    xaxis_title='Date',
    #autosize=True,
    #width=1000,
    #height=500,
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['plotbg'],
    font=dict(color=colors['text'],size=10),
    legend=dict(x=0,y=1,bgcolor=colors['plotbg'],orientation='h')
    )

fig3=go.Figure(data2, layout=layout2)
fig3.update_yaxes(tick0=20)

fig3.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{'visible':[True, True, False]},
                          {'yaxis':{'type':'linear', 'title':'Total', 'ticks':'outside', 'fixedrange':True, 'automargin':True,
                                    'linewidth':2, 'mirror':True, 'linecolor':colors['text']}}],
                         # {'yaxis':{'visible':[True, False]}}],
                    label="linear",
                    method="update",
                
                    ),
                dict(
                    args=[{'visible':[False, False, True]},
                          {'yaxis':{'type':'log', 'title':'Total', 'tickvals':[0,10,100, 1000], 'ticks':'outside', 'fixedrange':True, 'automargin':True,
                                    'linewidth':2, 'mirror':True, 'linecolor':colors['text']}}],
                          #{'yaxis':{'visible':[False,True]}}],
                    label="log",
                    method="update"
                    )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            bgcolor='white',
            
            x=0.04,
            xanchor="left",
            y=0.85,
            yanchor="top"
            )
        ]
    )



#fig2.update_xaxes(automargin=True)
#fig2.show(config={'scrollZoom': True})
#y = austincases['Cumulative Cases'].to_numpy()
#fig2.add_trace(go.Scatter(x=austincases['Date'][1:], y=y))
#fig2.update_layout(yaxis_type='log')





external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

#external_scripts = [{'type':"text/javascript",'src':'https://www.statcounter.com/counter/counter.js'}]
app = dash.Dash(__name__, assets_external_path='http://assets/')#, external_scripts=external_scripts)
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.scripts.append_script({"external_url": ['https://www.statcounter.com/counter/counter.js',
app.title = 'Tracking COVID-19 cases in Austin and Texas'




#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})

#app.scripts.config.serve_locally = False
#app.css.append_css({'external_url':'/base.css'})



app.layout = html.Div(style={'backgroundColor':colors['background'],'textAlign':'center', 'max-width':'1200px',
                             'border':'thick solid black', 'margin-left':'auto', 'margin-right':'auto', 'id':'grid'},
            children=[
                html.H1(children='Keeping track of COVID19 in  Texas',
                        style={'textAlign':'center',
                               'color':colors['text']}),
                html.H5(style={'color':colors['text']},children='Austin data updated on 3/27/20. Texas data updated 3/27/20.'),
                html.Div([
                    html.Div([dcc.Graph(figure=fig3,
                        config={'scrollZoom':True,'responsive':True})], className="eight columns"),
                    html.Div([dcc.Graph(figure=fig2,
                        config={'scrollZoom':True,'responsive':True})], className="eight columns"),
                    html.Div([dcc.Graph(figure=fig2d,
                        config={'scrollZoom':True,'responsive':True})], className="eight columns"),
                    html.Div([dcc.Graph(figure=fig2h,
                           config={'scrollZoom':True,'responsive':True})], className="eight columns")],
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
        <meta property="og:description" content="Daily updates of cases in Austin and Texas.">
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
        </footer>
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
    

            
                            
