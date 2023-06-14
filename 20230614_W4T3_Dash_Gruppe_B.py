import numpy as np
import pandas as pd
import dash
from dash import html, Input, Output, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px


# ---------------------------------------------------------------------------------------------

def fig_bevoelk(val_years):
    raw_data = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/12411-0005.csv',
                           skiprows=6, nrows=87, encoding='ISO-8859-1', sep=';')
    data = raw_data.copy()
    data.columns = ['Altersjahre', '31.12.2017', '31.12.2018', '31.12.2019', '31.12.2020', '31.12.2021']
    data = data[data['Altersjahre'] != 'Insgesamt']

    if val_years == []:
        indx_years = [1, 3]
    else:
        indx_years = []
        for i in range(0, len(data.columns)):
            if data.columns[i][-2:] == str(val_years[0]) or data.columns[i][-2:] == str(val_years[-1]):
                indx_years.append(i)

    # Datenvisualisierung
    if len(indx_years) > 1:
        fig_bev02 = px.line(data, x='Altersjahre', y=data.columns[indx_years[0]:indx_years[1] + 1], markers=True)
    else:
        fig_bev02 = px.line(data, x='Altersjahre', y=data.columns[indx_years[0]], markers=True)

    fig_bev02.update_layout(title="Altersverteilung der deutschen Bevölkerung",
                            xaxis_title='Altersjahre',
                            yaxis_title='Bevölkerung',
                            showlegend=True)

    return [data, fig_bev02]


# ---------------------------------------------------------------------------------------------

def fig_gebsterb(vals):
    raw_data_sterbene = pd.read_csv(
        'https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/12613-0002.csv', skiprows=5,
        nrows=73, encoding='ISO-8859-1', delimiter=';')
    raw_data_geborene = pd.read_csv(
        'https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/Geboren_12612-0001.csv',
        skiprows=5, nrows=73, encoding='ISO-8859-1',
        delimiter=';')

    data_geborene = raw_data_geborene.dropna()
    data_sterbene = raw_data_sterbene.dropna()

    data_geborene.rename(columns={'Unnamed: 0': 'Jahr'}, inplace=True)
    data_sterbene.rename(columns={'Unnamed: 0': 'Jahr'}, inplace=True)

    years = data_geborene['Jahr']
    births = data_geborene['Insgesamt']
    deaths = data_sterbene['Insgesamt']
    excess = births - deaths

    fig = px.line(title='Geborene, Gestorbene und Geburtenüberschuss über die Jahre')
    if vals == []:
        vals = ["Geburtenzahl", "Sterbezahl"]
    if len(vals) == 1 and vals[0] == "Geburtenzahl":
        fig.add_scatter(x=years, y=births, mode='lines', name='Geborene')
    elif len(vals) == 1 and vals[0] == "Sterbezahl":
        fig.add_scatter(x=years, y=deaths, mode='lines', name='Gestorbene')
    else:
        fig.add_scatter(x=years, y=births, mode='lines', name='Geborene')
        fig.add_scatter(x=years, y=deaths, mode='lines', name='Gestorbene')
        fig.add_bar(x=years, y=excess, name='Geburtenüberschuss')

    fig.update_layout(
        xaxis_title='Jahr',
        yaxis_title='Anzahl',
        legend_title='Kategorie',
        showlegend=True
    )
    return [data_geborene, data_sterbene, fig]


# ---------------------------------------------------------------------------------------------

def fig_gebmon(vals):
    # Daten einlesen
    data = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/12612-0002.csv',
                       skiprows=5, nrows=50, encoding='ISO-8859-1', delimiter=';')
    data.rename(columns={'Unnamed: 0': 'Jahr', 'Unnamed: 1': 'Monat'}, inplace=True)

    # Reihenfolge der Monate festlegen
    month_order = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober',
                   'November', 'Dezember']

    # Monat als kategorische Variable mit der gewünschten Reihenfolge festlegen
    data['Monat'] = pd.Categorical(data['Monat'], categories=month_order, ordered=True)

    # Datenvisualisierung mit Plotly Express
    fig = px.line(data_frame=data, x='Monat', y='Insgesamt', color='Jahr',
                  labels={'Monat': 'Monat', 'Insgesamt': 'Anzahl Lebendgeborene', 'Jahr': 'Jahr'},
                  title='Lebendgeborene nach ausgewählten Monaten (pro Jahr)')

    fig.update_traces(mode='lines+markers', marker=dict(size=5))

    fig.update_layout(
        yaxis=dict(range=[30000, 90000]),  # Y-Achse auf Bereich 0-75000 begrenzen
        legend_title_text=None,
        showlegend=True
    )

    return [data, fig]


# ---------------------------------------------------------------------------------------------

def fig_erwquo():
    # Daten einlesen
    raw_data = pd.read_csv(
        'https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/erwerbstaetigkeit-eltern.csv',
        encoding='ISO-8859-1', delimiter=';', skiprows=1,
        names=['Jahr', 'Mütter', 'Väter'])

    # Umwandlung der Spalten in numerische Werte
    raw_data['Mütter'] = raw_data['Mütter'].str.replace(',', '.').astype(float)
    raw_data['Väter'] = raw_data['Väter'].str.replace(',', '.').astype(float)

    fig = px.line(raw_data, x='Jahr', y=['Mütter', 'Väter'], title='Erwerbstätigenquote von Müttern und Vätern')
    fig.update_layout(
        xaxis_title='Jahr',
        yaxis_title='Erwerbstätigenquote',
        legend_title='Geschlecht'
    )
    return fig


# ---------------------------------------------------------------------------------------------

def figure_01_ea():
    # Datenimport
    # pfad = "file://localhost/D:/alexc/Documents/2023_Alfatraining/Modul_5_DataAnalyst/Tag 9/4364_Autoverkaufsdaten_dataPreprocessing_cleaning.csv"
    # raw_data = pd.read_csv(pfad)

    data_fig1 = np.linspace(0, 10, 100)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=data_fig1, y=np.sin(data_fig1), mode='lines', name='Sinus'))
    fig1.add_trace(go.Scatter(x=data_fig1, y=np.cos(data_fig1), mode='lines', name='Kosinus'))

    return (fig1)


# ---------------------------------------------------------------------------------------------

def dashboard():
    ######## Daten Umwelt ################
    df_treib = pd.read_csv(
        'https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/treibhausgase_abs.csv')
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

    dataframes = {  # hier können alle Schadstoffe oder sonstiges eingefügt werden
        'Treibhausgase': df_treib,
        'NH3': df_NH3,
        'NMVOC': df_NMVOC,
        'NOX': df_NOX,
        'PM10': df_PM10
    }

    ################ Beginn Dash ####################################
    app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True)

    ### Bevölkerungszusammensetzung Subthema Auswahl ###
    dropdown_b01 = dcc.Dropdown(
        ["Geburtenverteilung über das Jahr",
         "Erwerbstätigkeit Eltern",
         "Migration",
         "Gleichgeschlechtliche Ehen",
         "Altersverteilung der deutschen Bevölkerung"],
        value="Geburtenverteilung über das Jahr",
        id='subthema_bevoelk')

    z_c03 = dbc.Row(dbc.Col(children=dropdown_b01, width={"size": 10, "offset": 1}))

    z_c04 = dbc.Row(children=[], id="inhalt_geburten")

    s_b02 = dbc.Col(children=[z_c03, html.Br(), z_c04])

    ### Bevölkerungszusammensetzung Hauptthema ###

    datfig = fig_gebsterb([])
    fig_gebstr = datfig[2]
    s_d01 = dbc.Col(dcc.Graph(id="id_fig_bev01", figure=fig_gebstr), md=9)  # , md=4 ### Alterszusammensetzung
    s_d02 = dbc.Col(dcc.Checklist(options=['Geburtenzahl', 'Sterbezahl'],
                                  value=['Geburtenzahl', 'Sterbezahl'],
                                  inline=False,
                                  id="chklst_geburten"), md=3)
    z_c01 = dbc.Row([s_d01, s_d02])

    s_b01 = dbc.Col([z_c01])
    z_a03 = dbc.Row([s_b01, s_b02])

    ### Umwelt Hauptthema ###
    z_e03 = dbc.Row([dcc.Slider(step=None,
                                id='year--slider',
                                value=df_demo['Jahr'].dt.year.max(),
                                marks={str(year): str(year) for year in df_demo['Jahr'].dt.year.unique()}
                                )])  # Slider
    # Graph scatter
    z_e02 = dbc.Row([dcc.Graph(id='graph-scatter')])  # Graph
    z_e01 = dbc.Row([html.H4('Luftschadstoffe Scatter')])  # Header
    s_d04 = dbc.Col(
        [dcc.RadioItems(options=[{'label': 'Bevölkerung', 'value': 'demo'},
                                 {'label': 'BIP', 'value': 'BIP'}],
                        value='demo',
                        id='yaxis-type')],
        md=1,
        width={"size": 3, "offset": -1})

    s_d03 = dbc.Col([z_e01, z_e02, z_e03])

    z_d01 = dbc.Row([html.H4('Luftschadstoffe Linien')])

    s_d06 = dbc.Col([dcc.Checklist(id='checkliste',
                                   options=[{'label': land, 'value': land} for land in liste_laender],
                                   value=['Deutschland', 'EU27_2020'],
                                   inline=False)],
                    md=1,
                    width={"size": 3, "offset": -1})
    # Graph schadstoff
    s_d05 = dbc.Col([z_d01, dcc.Graph(id='graph-schadstoff')])
    z_c06 = dbc.Row([s_d05, s_d06])

    z_c05 = dbc.Row([s_d03, s_d04])
    s_b04 = dbc.Col([z_c05, html.Br(), z_c06], width={"size": 9})

    s_b03 = dbc.Col(
        [dcc.Dropdown(options=[{'label': 'Treibhausgase', 'value': 'Treibhausgase'},
                               {'label': 'NH3', 'value': 'NH3'},
                               {'label': 'NMVOC', 'value': 'NMVOC'},
                               {'label': 'NOX', 'value': 'NOX'},
                               {'label': 'PM10', 'value': 'PM10'}],
                      value='NH3',
                      id='dropdown-selection')],
        # md=1,
        width={"size": 1, "offset": 1})

    z_a04 = dbc.Row([s_b03, s_b04])

    ### Mobilität ###
    z_a05 = []

    ### Hauptfenster ###

    tab1_content = [html.Br(), z_a03]  # Bevölkerungszusammensetzung
    tab2_content = [html.Br(), z_a04]  # Umwelt
    tab3_content = [html.Br(), z_a05]  # Mobilität

    tabs = dbc.Tabs(
        [dbc.Tab("", label="Themen:", disabled=True),
         dbc.Tab(tab1_content, label="Bevölkerungszusammensetzung", tab_id="tab_a01"),
         dbc.Tab(tab2_content, label="Umwelt und Luftemissionen"),  ###### Noch zu ändern
         dbc.Tab(tab3_content, label="Mobilität"),  ###### Noch zu ändern
         ], active_tab="tab_a01")

    z_a02 = dbc.Row(dbc.Col([tabs], width={"size": 12, "offset": 0}))

    # Hauptfenster Zeile 1
    z_a01 = dbc.NavbarSimple(children=
                             [dbc.DropdownMenu(children=
                                               [dbc.DropdownMenuItem("Authors", header=True),
                                                dbc.DropdownMenuItem(divider=True),
                                                dbc.DropdownMenuItem("Esra Aciksöz Werner",
                                                                     href="https://www.linkedin.com/in/esra-aciks%C3%B6z-werner-18a131268/"),
                                                dbc.DropdownMenuItem("Kapila Kasam",
                                                                     href="https://www.linkedin.com/in/kapila-kasam-019181156/"),
                                                dbc.DropdownMenuItem("Marcus Köbe",
                                                                     href="https://www.linkedin.com/in/marcus-koebe/"),
                                                dbc.DropdownMenuItem("Nour-Eddine Kzaiber", href="#"),
                                                dbc.DropdownMenuItem("Peter Thul",
                                                                     href="https://www.linkedin.com/in/peter-thul-659151195/"),
                                                dbc.DropdownMenuItem("Alexander Warmbold",
                                                                     href="https://www.xing.com/profile/Alexander_Warmbold2/portfolio")
                                                ], nav=True, in_navbar=True, label="Team", )
                              ], brand="Dashboard Gruppe B",
                             brand_href="https://www.alfatraining.de")  # , color="primary", dark=True)

    layout_proj = html.Div(children=[z_a01, html.Br(), z_a02], id="GesamtAppLayout")  # Hauptcontainer/Fenster
    app.layout = layout_proj

    ### Callback zu den Subthemen Bevölkerung #### ---------------------------------------------------------------------------------------------

    @app.callback(
        Output("inhalt_geburten", "children"),
        Input("subthema_bevoelk", "value"))
    def count_clicks(n):
        if n == "Geburtenverteilung über das Jahr":
            ### Bevölkerungszusammensetzung Subthema Geburten/Jahr ###
            datafig_b03 = fig_gebmon([])
            fig1 = datafig_b03[1]
            s_d02 = dbc.Col(dcc.Graph(figure=fig1))  # , md=4 ### Alterszusammensetzung

            return [s_d02]

        elif n == "Erwerbstätigkeit Eltern":
            ### Erwerbstätigkeit Eltern ###
            fig1 = fig_erwquo()
            s_d01 = dbc.Col(dcc.Graph(figure=fig1), md=9)  # , md=4 ### Alterszusammensetzung

            return [s_d01]

        elif n == "Migration":
            ### Migration ###
            fig1 = figure_01_ea()
            s_d03 = dbc.Col(dcc.Graph(figure=fig1), md=9)  # , md=4 ### Migration

            # s_d04 = dbc.Col(dcc.RadioItems(['Mütter', 'Väter'], 'Geburtenzahl', inline=False), md=2)

            return [s_d03]  # , s_d04]

        elif n == "Gleichgeschlechtliche Ehen":
            ### Ehe Gleichgeschlechtlich ###
            fig1 = figure_01_ea()
            s_d05 = dbc.Col(dcc.Graph(figure=fig1), md=9)  # , md=4 ### Ehe Gleichgeschlechtlich

            # s_d06 = dbc.Col(dcc.RadioItems(['Mütter', 'Väter'], 'Geburtenzahl', inline=False), md=2)

            return [s_d05]  # , s_d06]

        elif n == "Altersverteilung der deutschen Bevölkerung":
            ### Altersverteilung der deutschen Bevölkerung ###
            datenfig_ea01 = fig_bevoelk([])  # Daten Esra A. 01 Bevölkerungszusammensetzung (Figure und Datensatz)
            fig_bev02 = datenfig_ea01[1]
            daten_bev02 = datenfig_ea01[0]

            z_d08 = dbc.Row([dcc.RangeSlider(min=int(daten_bev02.columns[1][-2:]),
                                             max=int(daten_bev02.columns[-1][-2:]),
                                             step=1,
                                             value=[int(daten_bev02.columns[2][-2:]),
                                                    int(daten_bev02.columns[-2][-2:])],
                                             id='my-range-slider01',
                                             tooltip={"placement": "bottom",
                                                      "always_visible": True})])  ###Slider Werte durch echte Daten erstezen

            z_d07 = dbc.Col(dcc.Graph(id="id_fig_bev02", figure=fig_bev02), md=9)  # , md=4 ### Alterszusammensetzung

            return [z_d07, z_d08]

        return

    ### Callback zum Hauptthema Bevölkerung (Geboren/Sterben) #### ---------------------------------------------------------------------------------------------

    @app.callback(Output("id_fig_bev01", "figure"),
                  Input("chklst_geburten", "value"))
    def fig_bevoelk01_update(vals):
        datfig = fig_gebsterb(vals)
        fig_gebstr = datfig[2]
        return fig_gebstr

    ### Callback zum Subthema Bevölkerung, Alterszusammenstellung #### ---------------------------------------------------------------------------------------------

    @app.callback(Output("id_fig_bev02", "figure"),
                  Input("my-range-slider01", "value"))
    def fig_bevoelk02_update(slider_values):
        datenfig_ea01 = fig_bevoelk(
            slider_values)  # Daten Esra A. 01 Bevölkerungszusammensetzung (Figure und Datensatz)
        fig = datenfig_ea01[1]
        return fig

    ### Callback zum Hauptthema Umwelt, Linienplot #### ---------------------------------------------------------------------------------------------
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
        Input('dropdown-selection', 'value'),
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

    #################################################### ---------------------------------------------------------------------------------------------

    app.run_server(debug=True)


# ---------------------------------------------------------------------------------------------


def main():
    dashboard()


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
