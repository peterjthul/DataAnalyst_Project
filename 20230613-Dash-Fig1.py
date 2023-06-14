import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df_NH3 = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NH3.csv')
df_NOX = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NOX.csv')
df_NMVOC = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NMVOC.csv')
df_PM10 = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/PM10.csv')

liste_laender = df_NH3.columns[2:].tolist()  # für die Checkliste

dataframes = {          # hier können alle Schadstoffe oder sonstiges eingefügt werden
    'NH3': df_NH3,
    'NMVOC': df_NMVOC,
    'NOX': df_NOX,
    'PM10': df_PM10
}


app = Dash(__name__)

app.layout = html.Div([
    html.H4('Luftschadstoffe'),
    dcc.Dropdown(
        options=[
            {'label': 'NH3', 'value': 'NH3'},
            {'label': 'NMVOC', 'value': 'NMVOC'},
            {'label': 'NOX', 'value': 'NOX'},
            {'label': 'PM10', 'value': 'PM10'}
        ],
        value='NH3',
        id='dropdown-selection'
            ),
    dcc.Graph(id='graph-schadstoff'),
    dcc.Checklist(id='checkliste', options=[{'label': land, 'value': land} for land in liste_laender], value=['Deutschland', 'EU27_2020'], inline=True),
    ])

@app.callback(
    Output('graph-schadstoff', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('checkliste', 'value')
)
def update_graph(value, selected_land):
    dataframe = dataframes.get(value)
    if dataframe is not None:
        fig = px.line()
        for land in selected_land:
            fig.add_scatter(x=dataframe['Jahr'], y=dataframe[land], mode='lines', name=land, showlegend=True)
        # fig.add_scatter(x=dataframe['Jahr'], y=dataframe['Deutschland'], mode='lines', name='Deutschland', line_color='red')
        # fig.add_scatter(x=dataframe['Jahr'], y=dataframe['EU27_2020'], mode='lines', name='EU27_2020', line_color='blue')
        fig.update_yaxes(title_text='in t')
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
