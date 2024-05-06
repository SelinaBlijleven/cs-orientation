"""
edit_dataframe.py

Launch a clunky interface to edit the domain file
"""
import dash
from dash import dcc, html, Input, Output, dash_table, State
from dash.exceptions import PreventUpdate

import pandas as pd

from config import DOMAIN_FILE
from tree_graph import treemap

# Read the domain file
df = pd.read_csv(DOMAIN_FILE)

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Editable DataFrame"),
    dash_table.DataTable(
        id='editable-table',
        columns=[{'name': col, 'id': col, 'editable': True} for col in df.columns],  # Make all columns editable
        data=df.to_dict('records'),
        editable=True,  # Allow editing
        row_deletable=True,  # Allow row deletion
        style_table={'overflowX': 'auto'}  # Enable horizontal scroll
    ),
    html.Button("Add Row", id="add-row-button", n_clicks=0),
    html.Div(id='output-container')
])


@app.callback(
    Output('editable-table', 'data'),
    [Input('add-row-button', 'n_clicks')],
    [State('editable-table', 'data')]
)
def add_row(n_clicks, rows):
    if n_clicks > 0:
        new_row = {col: '' for col in rows[0]}  # Corrected iteration over keys
        rows.append(new_row)  # Append the new row to the existing data
        return rows
    else:
        raise PreventUpdate  # Prevent callback execution if button hasn't been clicked


# Define callback to update the output container
@app.callback(
    Output('output-container', 'children'),
    [Input('editable-table', 'data')]
)
def update_output(data):
    # Convert the edited data back to DataFrame
    edited_df = pd.DataFrame(data)

    # Store to a CSV
    edited_df.to_csv(DOMAIN_FILE, index=False)

    #
    return html.Div([
        html.H3("Updated Graph"),
        dcc.Graph(
            id='interactive-plot',
            figure=treemap(edited_df)
        )
    ])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
