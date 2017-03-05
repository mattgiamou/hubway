#!/usr/bin/env python3

import numpy as np
import pandas as pd

data_path = '/drive1/Datasets/hubway/'
tripdata_path = data_path + 'tripdata/'
station_path = data_path + 'stations/2016_0429_Hubway_Stations.csv'

def get_stations(path=station_path):
  df = pd.read_csv(station_path)
  df.rename(index=str, columns={"Latitude": 'lat', "Longitude": 'lon'}, inplace=True)
  return df

def get_trip_data(year, month, path=tripdata_path):
  trip_path = tripdata_path + str(year) + str(month).zfill(2) + '-hubway-tripdata.csv'
  return pd.read_csv(trip_path)

def get_all_trip_data():
  years = [2015, 2016]
  months = np.arange(1,13, dtype='int')
  dfs = []
  for year in years:
    for month in months:
      df = get_trip_data(year, month)
      df = df[~df['end station id'].isin(['\\N'])]
      df['end station id'] = df['end station id'].astype(int)
      dfs.append(df)
  return pd.concat(dfs, ignore_index=True)

if __name__=='__main__':

  stations_df = get_stations()
  print(stations_df.describe())