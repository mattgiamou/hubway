#!/usr/bin/env python3

import numpy as np
from scipy import optimize
# import cvxopt

# Try optimize.basinhopping (simulated annealing alternative) if a normal gradient
# descent doesn't work

def optimize_station_position(X, M, S):
  ''' Prior estimate of station positions in X (x, y coordinates). 
  M is matrix of mean time from station i to j

if __name__=='__main__':
  pass
