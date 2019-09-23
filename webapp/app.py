import collections
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash.dash import no_update

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

url = 'https://raw.githubusercontent.com/jhaseon/Exploring-WebMD-WellRX/master/data/dash_data.csv'
df = pd.read_csv(url,sep=",")
drug = df.groupby(['drug']).mean().round(2).reset_index()
dfToList = drug['drug'].tolist()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = False

option_species = dict(zip(dfToList, dfToList))

navbar = dbc.NavbarSimple(
  children = [
  dbc.NavItem(dbc.NavLink("GitHub Link", href = "https://github.com/jhaseon/Exploring-WebMD-WellRX")),
  dbc.DropdownMenu(
    nav = True,
    in_navbar = True,
    label = "Menu",
    children = [
      dbc.DropdownMenuItem('WedMD', href = 'https://www.webmd.com/drugs/2/index'),
      dbc.DropdownMenuItem('WellRX'),
      dbc.DropdownMenuItem("Blog Post"),

      ],
  ),
  ],
  brand = "Average Ratings for WebMD's Most Common Drugs and Prices",
  brand_href = "#",
  sticky = "top",
)

body = dbc.Container(
  [
    dbc.Row(
      [
        dbc.Col(
            [
              html.H2("Description"),
              html.P(
                '''
                A simple web application created to visualize the average rating and price for WebMD's most common drugs, and paired with
                their respective prices based on WellRX.  
                '''

                ),
              ],
            md=4,
          ),
          dbc.Col(
            [
              html.H2('Bar Graph'),

              dcc.Dropdown(
                id='memory-dropdown',
                options=[{"label": key, "value": value} for key, value in option_species.items()]),
               
              dcc.Graph(id='memory-indicator-graphic'),
                
              ]
            ),
          ]
        )
      ],
    className = "mt-4",
)

app.layout = html.Div([navbar, body])
# app.layout = html.Div([
#     dcc.Store(id='memory-output'),
#     html.Div([

#         html.Div([
#             dcc.Dropdown(
#                 id='memory-dropdown',
#                 options=[{"label": key, "value": value} for key, value in option_species.items()]),
#             dcc.Graph(id='memory-indicator-graphic'),


#         ])])
#     ])


@app.callback(
    output=Output('memory-indicator-graphic', 'figure'),
    inputs=[Input('memory-dropdown', 'value')])
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
