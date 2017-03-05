#!/usr/bin/env python3

import pandas as pd

data_path = '/drive1/Datasets/hubway/'
tripdata_path = data_path + 'tripdata/'
station_path = data_path + 'stations/2016_0429_Hubway_Stations.csv'

def get_stations(path=station_path):
  df = pd.read_csv(station_path)
  df.rename(index=str, columns={"Latitude": 'lat', "Longitude": 'lon'}, inplace=True)
  return df

def get_trip_data(year, month, path=tripdata_path):
  pass

if __name__=='__main__':

  stations_df = get_stations()
  print(stations_df.describe())