import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Daten einlesen
data = pd.read_csv('46131-0003_Güterverkehr_Straße_bearbeitete_daten.csv')

# Dash-App initialisieren
app = Dash(__name__)

# Layout der Dash-App definieren
app.layout = html.Div([
    html.H4('Interactive data scaling using the secondary axis'),
    html.P("Select columns to plot:"),
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in data.columns[1:]],
        value=[],
        multi=True,
    ),
    dcc.Graph(id="graph"),
])

# Callback-Funktion für die Aktualisierung des Graphen
@app.callback(
    Output("graph", "figure"),
    Input("column-dropdown", "value")
)
def update_graph(selected_columns):
    # Figure-Objekt erstellen mit einer sekundären Y-Achse
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Schleife über ausgewählte Spalten
    for column in selected_columns:
        if column in data.columns[1:12:2]:
            # Falls die Spalte eine ungerade Zahl hat, wird sie auf der primären Y-Achse dargestellt
            fig.add_trace(
                go.Scatter(x=data['Jahr'], y=data[column], name=column),
                secondary_y=False,
            )
        elif column in data.columns[2:13:2]:
            # Falls die Spalte eine gerade Zahl hat, wird sie auf der sekundären Y-Achse dargestellt
            fig.add_trace(
                go.Scatter(x=data['Jahr'], y=data[column], name=column),
                secondary_y=True,
            )

    # Layout des Graphen aktualisieren
    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
    
    
    fig.update_layout(title_text="Güterverkehr")
    fig.update_xaxes(title_text="Jahr")
    fig.update_yaxes(title_text="Beförderte Gütermenge in 1000 t", secondary_y=False)
    fig.update_yaxes(title_text="Beförderungsleistung in Mill. TKm", secondary_y=True)

    return fig

# Starten der Dash-App
if __name__ == '__main__':
    app.run_server(port=8050)