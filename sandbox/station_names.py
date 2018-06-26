import numpy as np
import os
from ftplib import FTP
import pickle
import pandas as pd

def get_station_names():
    """ Return a dictonary containing the station ID's
    as keys and the list [Stations_id, von_datum, bis_datum, Stationshoehe,
    geoBreite, geoLaenge, Stationsname, Bundesland] and these column names in a list as value.
    """

    class Station:
        def __init__(self, Stations_id, von_datum, bis_datum, Stationshoehe,
        geoBreite, geoLaenge, Stationsname, Bundesland):
            self.Stations_id = Stations_id
            self.von_datum = von_datum
            self.bis_datum = bis_datum
            self.Stationshoehe = Stationshoehe
            self.geoBreite = geoBreite
            self.geoLaenge = geoLaenge
            self.Stationsname = Stationsname
            self.Bundesland = Bundesland


    # Download the file from the internet
    server = "ftp-cdc.dwd.de"
    ftp = FTP(server)
    ftp.login()

    # Create a file stations.txt with all the station information
    filename = "pub/CDC/observations_germany/climate/daily/kl/historical/KL_Tageswerte_Beschreibung_Stationen.txt"
    file = open("stations.txt", 'wb')
    ftp.retrbinary('RETR '+ filename, file.write)
    file.close()

    fileorigin = open("stations.txt", 'r', encoding = "cp1250")
    partial_read_in = False
    Stations = {}
    stations_dict = {}

    for lineid, line in enumerate(fileorigin):
        if lineid > 1:
            line_vec = list(filter(None, line.split(' ')))
            Stations[line_vec[0]] = Station(line_vec[0],line_vec[1], line_vec[2], line_vec[3],
                                line_vec[4], line_vec[5], line_vec[6:-1], line_vec[-1])
            stations_dict[Stations[line_vec[0]].Stations_id] = [Stations[line_vec[0]].von_datum,
            Stations[line_vec[0]].bis_datum, Stations[line_vec[0]].Stationshoehe,
            Stations[line_vec[0]].geoBreite, Stations[line_vec[0]].geoLaenge,
            Stations[line_vec[0]].Stationsname, Stations[line_vec[0]].Bundesland]

        elif lineid == 0:
            column_names = list(filter(None, line.split(' ')))
            column_names = [c.strip().lower() for c in column_names]

    print("number of stations loaded: ", len(Stations))
    fileorigin.close()

    # Join town names that are made up of multiple strings
    for key in stations_dict:
        if len(stations_dict[key][5]) > 2:
            town_name = stations_dict[key][5][0:-1]
            land_name = stations_dict[key][5][-1]
            joint_name = " ".join(town_name)
            stations_dict[key][5] = joint_name
            stations_dict[key][6] = land_name
        else:
            stations_dict[key][6] = stations_dict[key][5][1]
            stations_dict[key][5] = stations_dict[key][5][0]

    return stations_dict, column_names

def get_stations_dataframe():
    'Return stations in a pandas DataFrame'

    stations_dict, column_names = get_station_names()

    stations_pd = pd.DataFrame.from_dict(stations_dict, orient = 'index')
    stations_pd = stations_pd.reset_index()
    stations_pd.set_axis(column_names, axis = 'columns', inplace = True)
    stations_pd['stations_id'] = stations_pd['stations_id'].apply(int)
    stations_pd = stations_pd.set_index('stations_id')
    stations_pd['von_datum'] = pd.to_datetime(stations_pd['von_datum'])
    stations_pd['bis_datum'] = pd.to_datetime(stations_pd['bis_datum'])

    return stations_pd

if __name__ == '__main__':
    stations_dict = get_station_names()
    pickle.dump(stations_dict, open("stations.p", "wb"))
