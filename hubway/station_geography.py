#!/usr/bin/env python3

import numpy as np
from numpy import cos
import geoplotlib as gp

def meters_deglon(ang):
  ''' Takes latitude as argument ang in radians.
  '''
  return 111415.13*cos(ang) - 94.55*cos(3.0*ang) + (0.12 * cos(5.0*ang)) 

def meters_deglat(ang):
  ''' Takes latitude as argument ang in radians.
  '''
  return 111132.09 - 566.05*cos(2.0*ang) + 1.20*cos(4.0*ang) - 0.002*cos(6.0*ang)


def lat_lon_to_xy(lat, lon, x0=0.0, y0=0.0):
  ''' Assumes lat, lon are in radians already.
  x0, y0 are origin of coordinate frame - should add option so that this is 
  actual coordinates.
  '''

  # Note that latitude is used for both as the Earth is modelled as symmetric
  # about its rotational axis 
  dlon = lon - lon[0]
  dlat = lat - lat[0]
  x = dlon*meters_deglon(lat)*180.0/np.pi + x0
  y = dlat*meters_deglat(lat)*180.0/np.pi + y0
  return x, y


if __name__=='__main__':

  pass