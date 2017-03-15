#!/usr/bin/env python3

import numpy as np
import pandas as pd
from station_geography import lat_lon_to_xy

data_path = '/drive1/Datasets/hubway/'
tripdata_path = data_path + 'tripdata/'
station_path = data_path + 'stations/2016_0429_Hubway_Stations.csv'

null_char = '\\N'

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
      df = df[~df['end station id'].isin([null_char])]
      # df['end station id'] = df['end station id'].astype(int)
      df.loc[:, ('end station id')] = df['end station id'].astype(int)
      df = df[~df['end station id'].isin([153, 158])]
      df = df[~df['start station id'].isin([153, 158])]
      df.rename(index=str, columns={"start station latitude": 'lat', "start station longitude": 'lon'}, inplace=True)
      df['starttime'] = pd.to_datetime(df['starttime'])
      df['stoptime'] = pd.to_datetime(df['stoptime'])
      # Placeholder for unavailable birth year is same year 
      df.ix[df['birth year'].isin([null_char]), 'birth year'] = year
      df['birth year'] = df['birth year'].astype(int)
      df['age'] = year - df['birth year']

      dfs.append(df)
  return pd.concat(dfs, ignore_index=True)

def get_stations_from_trips(trips):
  ''' Return a dataframe with the lat, lon, name, id fields fore each station.
  '''
  station_properties = ('start station name', 'start station id', 'lat', 'lon')
  stations = trips.copy()
  # Loc to make sure the actual values are accessed 
  stations = stations.loc[:, station_properties]
  # Take only unique instances - there appear to be some misspellings? 
  stations = stations.drop_duplicates()
  x, y = lat_lon_to_xy(stations['lat']*np.pi/180.0, stations['lon']*np.pi/180.0)
  stations['x'] = x
  stations['y'] = y
  return stations

def get_hubway_data(years=[2015,2016]):
  trips = get_all_trip_data(years)
  stations = get_stations_from_trips(trips)
  return trips, stations

if __name__=='__main__':

  stations_df = get_stations()
  print(stations_df.describe())