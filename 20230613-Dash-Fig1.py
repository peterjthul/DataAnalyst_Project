import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df_treib = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/treibhausgase_abs.csv')
df_NH3 = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NH3.csv')
df_NOX = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NOX.csv')
df_NMVOC = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NMVOC.csv')
df_PM10 = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/PM10.csv')
df_BIP = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/BIP.csv')
df_demo = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/demo.csv')

df_BIP['Jahr'] = pd.to_datetime(df_BIP['Jahr'])  # Nach dem Exportieren war "Jahr" nicht mehr im datetime-Format
df_demo['Jahr'] = pd.to_datetime(df_demo['Jahr'])
# print(df_demo.dtypes)
# print(df_demo)

liste_laender = df_NH3.columns[2:].tolist()  # für die Checkliste

dataframes = {          # hier können alle Schadstoffe oder sonstiges eingefügt werden
    'Treibhausgase': df_treib,
    'NH3': df_NH3,
    'NMVOC': df_NMVOC,
    'NOX': df_NOX,
    'PM10': df_PM10
}


app = Dash(__name__)

app.layout = html.Div([
    html.H4('Luftschadstoffe Linien'),
    dcc.Dropdown(
        options=[
            {'label': 'Treibhausgase', 'value': 'Treibhausgase'},
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

    html.Div([
    html.H4('Luftschadstoffe Scatter'),
    dcc.Dropdown(
            options=[
                {'label': 'NH3', 'value': 'NH3'},
                {'label': 'NMVOC', 'value': 'NMVOC'},
                {'label': 'NOX', 'value': 'NOX'},
                {'label': 'PM10', 'value': 'PM10'},
                {'label': 'Treibhausgase', 'value': 'Treibhausgase'},
            ],
            value='NH3',
            id='dropdown-selection2'
                ),
        dcc.RadioItems(
            options=[
                {'label': 'Bevölkerung', 'value': 'demo'},
                {'label': 'BIP', 'value': 'BIP'}
            ],
            value='demo',
            id='yaxis-type'
                ),
    dcc.Graph(id='graph-scatter'),
    dcc.Slider(
        step=None,
        id='year--slider',
        value=df_demo['Jahr'].dt.year.max(),
        marks={str(year): str(year) for year in df_demo['Jahr'].dt.year.unique()}
        )
    ]
    )]
)

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
        fig.update_yaxes(title_text='in t')
        return fig


@app.callback(
    Output('graph-scatter', 'figure'),
    Input('dropdown-selection2', 'value'),
    Input('yaxis-type', 'value'),
    Input('year--slider', 'value')
)
def update_graph(value, yaxis_type, year_value):
    x_dataframe = dataframes.get(value)
    year_value = pd.to_datetime(year_value, format='%Y')  # Konvertiere das Jahr in den richtigen Datumsformat
    if yaxis_type == 'demo':
        y_dataframe = df_demo[df_demo['Jahr'] == year_value]
    else:
        y_dataframe = df_BIP[df_BIP['Jahr'] == year_value]
    if x_dataframe is not None and not y_dataframe.empty:  # Überprüfe, ob y_dataframe nicht leer ist
        fig = px.scatter()
        for land in x_dataframe.columns[2:]:
            marker_color = 'red' if land == 'Deutschland' else 'lightblue'
            fig.add_scatter(x=x_dataframe[land], y=y_dataframe[land], mode='markers', name=land,
                            marker_color=marker_color)
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
