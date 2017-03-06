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

def get_all_trip_data(years=[2015, 2016]):
  months = np.arange(1,13, dtype='int')
  dfs = []
  for year in years:
    for month in months:
      df = get_trip_data(year, month)
      # Need to use '~' and 'isin' instead of != because != not defined 
      # for ints and 
      df = df[~df['end station id'].isin(['\\N'])]
      # df['end station id'] = df['end station id'].astype(int)
      df.loc[:, ('end station id')] = df['end station id'].astype(int)
      df = df[~df['end station id'].isin([153, 158])]
      df = df[~df['start station id'].isin([153, 158])]
      df.rename(index=str, columns={"start station latitude": 'lat', "start station longitude": 'lon'}, inplace=True)
      df['starttime'] = pd.to_datetime(df['starttime'])
      df['stoptime'] = pd.to_datetime(df['stoptime'])
      dfs.append(df)
  return pd.concat(dfs, ignore_index=True)

def get_stations_from_trips(trips):
  ''' Return a dataframe with the lat, lon, name, id fields fore each station.
  '''
  station_properties = ('start station name', 'start station id', 'lat', 'lon')
  stations = trips.copy()
  # Loc to make sure the actual values are accessed 
  stations = stations.loc[:, station_properties]
  # stations.rename(index=str, columns={"start station latitude": 'lat', "start station longitude": 'lon'}, inplace=True)
  # Take only unique instances - there appear to be some misspellings? 
  return stations.drop_duplicates()

def get_hubway_data(years=[2015,2016]):
  trips = get_all_trip_data(years)
  stations = get_stations_from_trips(trips)
  return trips, stations

if __name__=='__main__':

  stations_df = get_stations()
  print(stations_df.describe())