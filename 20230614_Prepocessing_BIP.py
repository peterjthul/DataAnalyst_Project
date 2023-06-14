'''BIP und Hauptkomponenten (Produktionswert, Ausgaben und Einkommen)
Online Datencode NAMA_10_GDP__custom_6543219
Letzte Aktualisierung: 13/06/2023 23:00  '''

import pandas as pd

# Einladen der Datei von github in pandas dataframe
df_BIP_raw = pd.read_csv(
    'https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/nama_10_gdp__custom_6543219_tabular.tsv', sep='\t')
# print(df_BIP_raw)

# Ersetze Buchstaben und Leerzeichen in allen Spalten außer der ersten
df_BIP = df_BIP_raw
df_BIP.iloc[:, 1:] = df_BIP.iloc[:, 1:].astype(str).apply(
    lambda x: x.str.replace(r'[a-zA-Z\s]', '', regex=True))
# print(df_BIP)

### Transponieren
# # # Setze die Spalte 'freq,unit,age,sex,geo\TIME_PERIOD' als Index
df_BIP.set_index('freq,unit,na_item,geo\\TIME_PERIOD', inplace=True)

# # Transponiere den DataFrame
df_BIP = df_BIP.transpose()

# Zurücksetzen des Indexes und umbenennen
df_BIP.reset_index(inplace=True)
df_BIP = df_BIP.rename(columns={'index': 'Jahr'})
# print(df_BIP)
# print(df_BIP.dtypes)

# Werte in float umwandeln und das Jahr als datetime
# Schleife über die Spalten ab der zweiten Spalte
for col in df_BIP.columns[1:]:
    df_BIP[col] = pd.to_numeric(df_BIP[col], errors='coerce') #pd.to_numeric() mit errors='coerce': Werte, die nicht in Float umgewandelt werden, werden NaN
df_BIP['Jahr'] = pd.to_datetime(df_BIP['Jahr'])
# print(df_BIP, df_BIP.dtypes)

# # # Teil-String aus den Spaltenüberschriften entfernen, damit nur das Länderkürzel bleibt
df_BIP.columns = df_BIP.columns.str.replace('A,CP_MEUR,B1GQ,', '')
# print(df_BIP)

# # # Nur Länder nehmen, die auch in anderen Datensätzen vorhanden sind
selected_laender = ['AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'EU27_2020', 'FI', 'FR', 'HR',
                    'HU', 'IE', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 'SI',
                    'SK', 'TR']

# Filtern nach den Ländern und das Jahr
spalten = ['Jahr'] + selected_laender
df_BIP = df_BIP.filter(items=spalten)
# print(df_BIP)


# # Spaltenüberschriften austauschen
land = {
    'Jahr': 'Jahr',
    'AT': 'Österreich',
    'BE': 'Belgien',
    'BG': 'Bulgarien',
    'CH': 'Schweiz',
    'CY': 'Zypern',
    'CZ': 'Tschechien',
    'DE': 'Deutschland',
    'DK': 'Dänemark',
    'EE': 'Estland',
    'EL': 'Griechenland',
    'ES': 'Spanien',
    'EU27_2020': 'EU27_2020',
    'FI': 'Finnland',
    'FR': 'Frankreich',
    'HR': 'Kroatien',
    'HU': 'Ungarn',
    'IE': 'Irland',
    'IS': 'Island',
    'IT': 'Italien',
    'LI': 'Lichtenstein',
    'LT': 'Litauen',
    'LU': 'Luxemburg',
    'LV': 'Lettland',
    'MT': 'Malta',
    'NL': 'Niederlande',
    'NO': 'Norwegen',
    'PL': 'Polen',
    'PT': 'Portugal',
    'RO': 'Rumänien',
    'SE': 'Schweden',
    'SI': 'Slowenien',
    'SK': 'Slowakei',
    'TR': 'Türkei'}
# Spaltenüberschriften austauschen
df_BIP = df_BIP.rename(columns=land)

# Spaltenüberschriften alphabetisch sortieren
sorted_columns = sorted(df_BIP.columns)
sorted_columns.remove('Jahr')
sorted_columns.insert(0, 'Jahr')
df_BIP = df_BIP.reindex(columns=sorted_columns)
# print(df_BIP)

# letzten beiden Zeilen Entfernen, weil die Schadstoffdaten nur bis 2020 gehen
df_BIP = df_BIP.iloc[:-2]
# print(df_BIP)

# # # in csv-Dateien schreiben
df_BIP.to_csv('BIP.csv', index=True)
