# -*- coding: utf-8 -*-
"""
[add header]
"""
import os
import sys
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import numpy as np
import webbrowser

# =============================================================================
# Initializing Everything
# =============================================================================

# Getting the current path to this script, which is assumed to be in the same
# folder as the results
results_path = sys.argv[0][:-11]

# Format of results filenames
results_filename = 'results_model_test-clean'

# URL for app -- change if needed
app_url = 'http://127.0.0.1:8050/'

data_store = {}

# Loading data into data_store dictionary
for results_file in os.listdir(results_path):
    if results_filename in results_file:
        data_store[results_file[:-4]] = pd.read_table(results_path + results_file, sep=',')

# =============================================================================
# Begin App
# =============================================================================

app = dash.Dash(__name__)

colors = {'background': 'rgb(50, 50, 50)',
          'text': 'white'}

# Defining the app layout
app.layout = html.Div(style={'backgroundColor':colors['background'],
                             # 'columnCount': 2,
                             'height': '2000px'},
                    children=[
                    html.Div(style={'width': '100%'}, children=[
                        html.H2('   COMP 5630/6630/6636 8-Bit Brain Final Project Results',
                                style={'color': colors['text'],
                                       'font-family':'Arial',
                                       'float': 'left',
                                       'width': '100%'})
                        ]),
                    html.Div(style={'height': '100px', 'width': '100%'}, children=[
                        html.P('Authors: Dennis Brown (dgb0028@auburn.edu), '
                               'Shannon McDade (slm0035@auburn.edu), and Jacob Parmer '
                               '(jacob.parmer@auburn.edu)',
                               style={'color': colors['text'],
                                      'font-family':'Arial',
                                       'float': 'left',
                                       'width': '100%'})]),
                    html.Br(),
                    html.Div([
                        dcc.Dropdown(options=[{'label': i, 'value': i} for i in list(data_store.keys())],
                                     multi=True,
                                     value=list(data_store.keys()),
                                     id='dropdown-selection')
                        ]),
                    dcc.Graph( id='box-plot')
                    ])

@app.callback(Output('box-plot','figure'),
              [Input('dropdown-selection', 'value')])
def render_content(selections):
    fig = go.Figure()

    for selected in selections:
        select_data = data_store[selected]
        fig.add_trace(go.Bar(x=np.array([selected] * len(select_data.iloc[:,-1:])),
                             y=select_data.iloc[:,-1:].mean()))

    fig.update_layout(
        autosize=False,
        width=2000,
        height=2000,
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        showlegend=False
        )
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)

webbrowser.open(app_url)