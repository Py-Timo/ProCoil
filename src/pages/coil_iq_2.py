
import os
import base64
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State, callback

# Register the page
dash.register_page(__name__)

# Layout for the Coil Hardware Parameters page
layout = html.Div(
    children=[
        # Title for the page
        html.H1(
            children='Coil Hardware Parameters',
            style={
                'textAlign': 'center',
                'fontSize': '36px',
                'color': '#2C3E50',
                'fontFamily': 'Arial, sans-serif',
                'marginBottom': '20px'
            }
        ),
        # File upload section
        dcc.Upload(
            id='upload-data',
            children=html.Div(
                [
                    'Drag and Drop or ',
                    html.A('Select Files', style={'color': '#3498DB', 'fontWeight': 'bold'})
                ]
            ),
            style={
                'width': '100%',
                'height': '80px',
                'lineHeight': '80px',
                'borderWidth': '2px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '20px 0',
                'backgroundColor': '#ECF0F1',
                'cursor': 'pointer',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'fontFamily': 'Arial, sans-serif',
                'color': '#34495E'
            },
            multiple=True  # Allow multiple files to be uploaded
        ),
        # File information and graphs container
        html.Div(id='file-info', style={'marginTop': '30px', 'fontSize': '18px', 'fontFamily': 'Arial, sans-serif'}),
        html.Div(id='graphs-container', style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fill, minmax(500px, 1fr))', 'gap': '20px', 'padding': '20px'})
    ],
    style={'backgroundColor': '#F5F5F5', 'padding': '30px', 'fontFamily': 'Arial, sans-serif'}
)

# Callback
@callback(
    [Output('file-info', 'children'), Output('graphs-container', 'children')],
    [Input('upload-data', 'contents')],
    [Input('upload-data', 'filename')]
)
def update_output(contents, filenames):
    if contents is None:
        return "No files uploaded yet.", []

    try:
        graphs = []
        file_info = []

        # Process each uploaded file
        for content, filename in zip(contents, filenames):
            # Skip files containing "_err" in the filename
            if "_err" in filename:
                continue

            # Decode the uploaded file contents
            content_type, content_string = content.split(',')
            decoded = base64.b64decode(content_string)

            # Save the uploaded file to a temporary location
            temp_file = f"uploaded_{filename}"
            with open(temp_file, 'wb') as f:
                f.write(decoded)

            # Load the CSV file into a DataFrame
            df = pd.read_csv(temp_file, skiprows=9, sep='\t', names=['date', 'time', 'value'])

            # Combine date and time into a single datetime column
            df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

            # Calculate basic statistics
            mean_value = df['value'].mean()
            min_value = df['value'].min()
            max_value = df['value'].max()

            # File information and statistics
            file_info.append(html.Div(
                [
                    html.H3(f"File: {filename}", style={'color': '#3498DB'}),
                    html.P(f"Mean Value: {mean_value:.6f}", style={'fontSize': '16px'}),
                    html.P(f"Minimum Value: {min_value:.6f}", style={'fontSize': '16px'}),
                    html.P(f"Maximum Value: {max_value:.6f}", style={'fontSize': '16px'}),
                    html.Hr(style={'borderColor': '#3498DB', 'borderWidth': '2px'}),
                ],
                style={'backgroundColor': '#ECF0F1', 'padding': '15px', 'borderRadius': '8px'}
            ))

            # Create a Plotly Express line graph
            fig = px.line(df, x='datetime', y='value', title=f'Data Plot: {filename}')
            graphs.append(dcc.Graph(figure=fig))

            # Clean up the temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)

        return file_info, graphs

    except Exception as e:
        return html.P(f"Error: {e}"), []
