import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
from coil_functions import File

# Register the main page
dash.register_page(__name__)

# Layout
layout = html.Div([
    html.P("Welcome to Coil Analyzer"),
    dcc.Dropdown(
        id='coil-dropdown',
        options=[
            #{'label': 'BASE', 'value': 'BASE'},
            {'label': 'DCP', 'value': 'DCP'},
            {'label': 'KNEE16', 'value': 'KNEE_16'},
            {'label': 'ACI', 'value': 'ACI'},
            {'label': 'SHOULDER16', 'value': 'SHOULDER_16'},
            {'label': 'ANTERIOR', 'value': 'ANTERIOR'}
        ],
        placeholder="Select the coil",
        style={'width': '50%', 'margin': '0 auto'}
    ),
    html.Hr(style={'border': '3px solid green', 'margin': '10px auto', 'width': '60%'}),
    dcc.Dropdown(
        id='rxe-dropdown',
        options=[
            {'label': 'MSEQ0', 'value': 'MSEQ0'},
            {'label': 'MSEQ1', 'value': 'MSEQ1'},
            {'label': 'MSEQ2', 'value': 'MSEQ2'},
            {'label': 'MSEQ3', 'value': 'MSEQ3'}
        ],
        value=['MSEQ0','MSEQ1','MSEQ2','MSEQ3'],  # Default value is empty
        multi=True,
        placeholder="Select the RXE option",
        style={'width': '50%', 'margin': '0 auto', 'color': 'blue'}
    ),
    dcc.Dropdown(
        id='voltage-dropdown',
        options=[
            {'label': 'VDH', 'value': 'VDH'},
            {'label': 'VDL', 'value': 'VDL'},
            {'label': 'VLNA', 'value': 'VLNA'},
            {'label': 'VPIN', 'value': 'VPIN'}
        ],
        value=['VDH','VDL','VLNA','VPIN'],  # Default value is empty
        multi=True,
        placeholder="Select the voltage",
        style={'width': '50%', 'margin': '0 auto', 'color': 'blue'}
    ),
    html.Button('Graph', id='graph-button', n_clicks=0, style={'marginTop': '20px'}),
    html.Hr(style={'border': '3px solid blue', 'margin': '10px auto', 'width': '60%'}),
    dcc.Graph(id='voltage-graph3'),  # Graph for RXE = MSEQ0
    dcc.Graph(id='voltage-graph4'),  # Graph for RXE = MSEQ1
    dcc.Graph(id='voltage-graph5'),  # Graph for RXE = MSEQ2
    dcc.Graph(id='voltage-graph6'),  # Graph for RXE = MSEQ3
    html.Div(id='output-div_3', style={'marginTop': '20px'})
], style={'textAlign': 'center'})

# Callback
@callback(
    [Output('voltage-graph3', 'figure'),
     Output('voltage-graph4', 'figure'),
     Output('voltage-graph5', 'figure'),
     Output('voltage-graph6', 'figure'),
     Output('output-div_3', 'children')],
    [Input('graph-button', 'n_clicks')],
    [State('coil-dropdown', 'value'),
     State('rxe-dropdown', 'value'),
     State('voltage-dropdown', 'value')]
)
def update_output(n_clicks, selected_coil, selected_rxe, selected_voltage):
    if n_clicks == 0:
        # No action until button is clicked
        return px.line(), px.line(), px.line(), px.line(), "Click the 'Graph' button to start."

    if not selected_coil or not selected_rxe or not selected_voltage:
        return px.line(), px.line(), px.line(), px.line(), "Please make all selections."

    figures = [px.line(), px.line(), px.line(), px.line()]  # Initialize empty figures
    statistics_text = []  # List to hold html elements for the output
    error_messages = []  # List to hold error messages

    # Generate figures and handle errors
    for rxe in selected_rxe:
        for voltage in selected_voltage:
            try:
                df = File(selected_coil, rxe, voltage)
                if isinstance(df, str):  # If File function returns an error message
                    error_messages.append(html.P(f"Error: {df} for RXE = {rxe}, Voltage = {voltage}."))
                    continue

                # Map RXE to the corresponding figure index
                fig_index = int(rxe[-1])  # Extract 0, 1, 2, or 3 from MSEQ0, MSEQ1, etc.
                figures[fig_index].add_scatter(
                    x=df['datetime'], y=df['voltage'], mode='lines', name=f"{voltage} ({rxe})"
                )
                figures[fig_index].update_layout(
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

    return figures[0], figures[1], figures[2], figures[3], html.Div(output_content)
