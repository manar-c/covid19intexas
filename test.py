import dash
import dash_html_components as html
import dash_core_components as dcc


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
#app = dash.Dash(__name__, assets_external_path='http://assets/')#, external_scripts=external_scripts)
app = dash.Dash(__name__, assets_external_path='http://assets/')
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#app = dash.Dash()
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Column 1'),
            dcc.Graph(id='g1', figure={'data': [{'y': [1, 2, 3]}]})
        ], className="four columns"),

        html.Div([
            html.H3('Column 2'),
            dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}]})
        ], className="four columns"),
    ], className="row", style={'text-align':'center', 'margin-left':'auto', 'margin-right':'auto'})
])


if __name__ == '__main__':
    app.run_server(debug=True)
