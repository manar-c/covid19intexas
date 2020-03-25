#Creating dashboard of covid cases

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
#x = texascases[casestart].index.values
#y = texascases[casestart]

#x = texascases.index.values
#y = texascases

#print(x)

#x = sdfsfdsfs


austincases = pd.read_excel('AustinCases.xlsx', sheet_name='Austin')
#print(austincases.head())

colors = {
    'background': '#F5F5F5',
    'text': '#484848',
    'plotbg': '#FDFDFD'
    }



trace1 = go.Scatter(x=austincases['Date'], y=austincases['Cumulative Cases'], name="Linear")
trace2 = go.Scatter(x=austincases['Date'], y=austincases['Cumulative Cases'], yaxis='y2', name="Logarithmic")

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
        showgrid=False,ticks='outside'),
        #type='log'),
    yaxis2=dict(
        title='Log',
        overlaying='y',
        side='right',
        type='log',
        showgrid=False,ticks='outside'
        ),
    xaxis=dict(linewidth=2,linecolor=colors['text'],mirror=True,showgrid=False,ticks='outside'),
    xaxis_title='Date',
    #autosize=True,
    #width=1000,
    #height=500,
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['plotbg'],
    font=dict(color=colors['text']),
    legend=dict(x=0,y=1,bgcolor=colors['plotbg'])
    )

fig2=go.Figure(data, layout=layout)



trace1 = go.Scatter(x=x, y=y, name="Linear")
trace2 = go.Scatter(x=x, y=y, yaxis='y2', name="Logarithmic")

data2 = [trace1, trace2]
layout2 = go.Layout(
    title={'text':'Total Cases in Texas',
           'x':0.5,'y':0.9,
           'xanchor':'center','yanchor':'top'},
    yaxis=dict(
        title='Total',
        linecolor=colors['text'],
        linewidth=2,
        mirror=True,
        showgrid=False,ticks='outside'),
        #type='log'),
    yaxis2=dict(
        title='Log',
        overlaying='y',
        side='right',
        type='log',
        showgrid=False,ticks='outside'
        ),
    xaxis=dict(linewidth=2,linecolor=colors['text'],mirror=True,showgrid=False,ticks='outside'),
    xaxis_title='Date',
    #autosize=True,
    #width=1000,
    #height=500,
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['plotbg'],
    font=dict(color=colors['text']),
    legend=dict(x=0,y=1,bgcolor=colors['plotbg'])
    )

fig3=go.Figure(data2, layout=layout2)


#fig2.update_xaxes(automargin=True)
#fig2.show(config={'scrollZoom': True})
#y = austincases['Cumulative Cases'].to_numpy()
#fig2.add_trace(go.Scatter(x=austincases['Date'][1:], y=y))
#fig2.update_layout(yaxis_type='log')

app = dash.Dash(__name__, assets_external_path='http://assets/')
app.title = 'Tracking COVID-19 cases in Austin and Texas'
#app.scripts.config.serve_locally = False
#app.css.append_css({'external_url':'/base.css'})



app.layout = html.Div(style={'backgroundColor':colors['background'],'textAlign':'center', 'max-width':'1000px',
                             'align':'right','border':'thick solid black', 'margin-left':'auto', 'margin-right':'auto'},
                      children=[
    html.H1(children='Keeping track of COVID19 in Austin and Texas',
    style={'textAlign':'center',
           'color':colors['text']}),
                          html.H3(style={'color':colors['text']},children='Austin data updated on 3/24/20.'),
                          
    #dcc.Graph(figure=fig1),
    html.Div([dcc.Graph(figure=fig2,
                        config={'scrollZoom':True,'responsive':True})]),
    html.Div([dcc.Graph(figure=fig3,
                        config={'scrollZoom':True,'responsive':True})]),
                          html.H3(style={'color':colors['text']},children='Data sources:  Texas data obtained from John Hopkins data set (https://github.com/CSSEGISandData).  They are currently changing the format of this data set, and data from March 23 onwards currently is not valid.  Austin data obtained from KUT and Travis County.')
              ])


#This is new
server = app.server

              
        
              
if __name__ == '__main__':
    app.run_server(debug=True)

 #   dcc.
    

            
                            
