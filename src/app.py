import dash  # pip install dash
from dash import Dash, html
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
from datetime import datetime as dt
import sys  # Needed for sys.exit()

# Initialize the Dash app
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True
)

# Define the expiry date
expiry_date = dt(2025, 4, 25)  # Set the expiry date (Year, Month, Day)

# Check if the current date matches or exceeds the expiry date
current_date = dt.now()
if current_date >= expiry_date:
    print("This application has expired.")
    sys.exit()  # Exit the script if the date is expired

# Custom Navbar with Two Rows
navbar = dbc.Navbar(
    dbc.Container([
        # Column with two rows stacked
        dbc.Col(
            [
                html.Div("MRI Coil Data Analyzer", style={"fontSize": "20px", "fontWeight": "bold", "color": "white"}),
                html.Div("For help: tamer.dabour@philips.com", style={"fontSize": "15px", "color": "lightgray"}),
            ],
            width="auto",
        ),
        # Spacer to push the dropdown to the right
        dbc.Nav(
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem(page["name"], href=page["path"])
                    for page in dash.page_registry.values()
                    if page["module"] != "pages.not_found_404"
                ],
                nav=True,
                label="More Pages",
                in_navbar=True,
            ),
            className="ms-auto",  # Push to the right
            navbar=True,
        ),
    ]),
    color="primary",
    dark=True,
    className="mb-4",
)

# Layout with the Custom Navbar
app.layout = dbc.Container(
    html.Div([
        navbar,  # Custom Navbar
        dash.page_container,  # Page content container
        html.P(
            "For help: tamer.dabour@philips.com",
            style={'textAlign': 'left', 'color': 'green', 'fontSize': '15px'}
        )
    ]),
    fluid=True
)

if __name__ == "__main__":
    app.run(port=8080)
