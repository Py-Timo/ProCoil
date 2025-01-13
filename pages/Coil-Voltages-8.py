import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
from coil_functions import File

# Register the page
dash.register_page(__name__ , path= '/')

# Layout
layout = html.Div([
    html.P("Welcome to Coil Analyzer - "),
    dcc.Dropdown(
        id='coil-dropdown-p2',
        options=[
            {'label': 'BASE', 'value': 'BASE'},
            {'label': 'HEAD_NECK', 'value': 'HEAD_NECK'},
            #{'label': 'HEAD', 'value': 'HEAD_E'},
            {'label': 'KNEE8', 'value': 'KNEE8'},
            {'label': 'POSTERIOR', 'value': 'POSTERIOR'},
            {'label': 'SHOULDER8', 'value': 'SHOULDER8'},
            #{'label': 'ANTERIOR', 'value': 'ANTERIOR'}
        ],
        placeholder="Select the coil",
        style={'width': '50%', 'margin': '0 auto'}
    ),
    html.Hr(style={'border': '3px solid green', 'margin': '10px auto', 'width': '60%'}),
    dcc.Dropdown(
        id='rxe-dropdown-p2',
        options=[
            {'label': 'MSEQ0', 'value': 'MSEQ0'},
            {'label': 'MSEQ1', 'value': 'MSEQ1'},
            #{'label': 'MSEQ2', 'value': 'MSEQ2'},
            #{'label': 'MSEQ3', 'value': 'MSEQ3'}
        ],
        value=[ 'MSEQ0','MSEQ1'],  # Default value is empty
        multi=True,
        placeholder="Select the RXE option",
        style={'width': '50%', 'margin': '0 auto', 'color': 'blue'}
    ),
    dcc.Dropdown(
        id='voltage-dropdown-p2',
        options=[
            {'label': 'VDH', 'value': 'VDH'},
            {'label': 'VDL', 'value': 'VDL'},
            {'label': 'VLNA', 'value': 'VLNA'},
            {'label': 'VPIN', 'value': 'VPIN'}
        ],
        value=[ 'VDH' , 'VDL' , 'VLNA' , 'VPIN'],  # Default value is empty
        multi=True,
        placeholder="Select the voltage",
        style={'width': '50%', 'margin': '0 auto', 'color': 'blue'}
    ),
    html.Button('Graph', id='graph-button-p2', n_clicks=0, style={'marginTop': '20px'}),
    html.Hr(style={'border': '3px solid blue', 'margin': '10px auto', 'width': '60%'}),
    dcc.Graph(id='voltage-graph1-p2'),  # First Graph
    dcc.Graph(id='voltage-graph2-p2'),  # Second Graph
    html.Div(id='output-div-p2', style={'marginTop': '20px'})
], style={'textAlign': 'center'})

# Callback
@callback(
    [Output('voltage-graph1-p2', 'figure'),
     Output('voltage-graph2-p2', 'figure'),
     Output('output-div-p2', 'children')],
    [Input('graph-button-p2', 'n_clicks')],
    [State('coil-dropdown-p2', 'value'),
     State('rxe-dropdown-p2', 'value'),
     State('voltage-dropdown-p2', 'value')]
)
def update_output_p2(n_clicks, selected_coil, selected_rxe, selected_voltage):
    if n_clicks == 0:
        # No action until button is clicked
        return px.line(), px.line(), "Click the 'Graph' button to start."

    if not selected_coil or not selected_rxe or not selected_voltage:
        return px.line(), px.line(), "Please make all selections."

    figures = [px.line(), px.line()]  # Initialize empty figures
    statistics_text = []  # List to hold HTML elements for the output
    error_messages = []  # List to hold error messages

    # Generate figures and handle errors
    for idx, rxe in enumerate(selected_rxe):
        if idx >= 2:  # Limit to two RXE options
            break

        for voltage in selected_voltage:
            try:
                df = File(selected_coil, rxe, voltage)
                if isinstance(df, str):  # If File function returns an error message
                    error_messages.append(html.P(f"Error: {df} for RXE = {rxe}, Voltage = {voltage}."))
                    continue

                # Add data to the corresponding graph
                figures[idx].add_scatter(
                    x=df['datetime'], y=df['voltage'], mode='lines', name=f"{voltage} ({rxe})"
                )
                figures[idx].update_layout(
                    title=f"Voltage Graph: Coil = {selected_coil}, RXE = {rxe}",
                    xaxis_title="Time", yaxis_title="Voltage", legend_title="Voltage Types"
                )

                # Collect statistics in HTML format
                statistics_text.extend([
                    html.P(f"Statistics for RXE = {rxe}, Voltage = {voltage}:"),
                    html.P(f"Mean: {df['voltage'].mean():.2f}"),
                    html.P(f"Min: {df['voltage'].min():.2f}"),
                    html.P(f"Max: {df['voltage'].max():.2f}"),
                    html.Hr(style={'border': '1px solid gray'})
                ])
            except Exception as e:
                error_messages.append(html.P(f"Unexpected error for RXE = {rxe}, Voltage = {voltage}: {e}."))

    # Combine statistics and error messages
    output_content = statistics_text + error_messages
    if not output_content:  # If no content, show a default message
        output_content = [html.P("No data available for the selected options.")]

    return figures[0], figures[1], html.Div(output_content)
