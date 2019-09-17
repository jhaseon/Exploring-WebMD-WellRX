import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash.dash import no_update

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

url = 'https://raw.githubusercontent.com/jhaseon/WebMD-Scraping-project-/master/dash.csv'
df = pd.read_csv(url,sep=",")
drug = df.groupby(['drug']).mean().round(2).reset_index()
dfToList = drug['drug'].tolist()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = False

option_species = dict(zip(dfToList, dfToList))

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='dropdown',
                options=[{"label": key, "value": value} for key, value in option_species.items()]),
            dcc.Graph(id='indicator-graphic'),


        ])])])


@app.callback(
    output=Output('indicator-graphic', 'figure'),
    inputs=[Input('dropdown', 'value')])
def update_graph(dropdown):
  ctx = dash.callback_context
  # Check if triggered or dropdown value is None
  if not ctx.triggered or dropdown is None:
    return no_update

  # set_index requires an input that is a column name
  a = df.set_index(['drug'])
  name = dropdown
  a1 = a.loc[[name]].mean().to_frame().reset_index()
  return {'data': [go.Bar(
        x=a1['index'][:-1],
        y=a1[0]
        )]
        }

if __name__ == '__main__':
    app.run_server(debug=True)