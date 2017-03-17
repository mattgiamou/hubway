#!/usr/bin/env python3

import numpy as np
from scipy import optimize
# import cvxopt

# Try optimize.basinhopping (simulated annealing alternative) if a normal gradient
# descent doesn't work

def optimize_station_position(X, M, S, alpha = 1.0):
  """ X is prior positions (actual geographic positions), 
  D is matrix of 'prior' (actual geographic distances),
  M is matrix of mean distances as measured by trip durations from station i to j,
  S is matrix of distance variances as measured by trip durations from station i to j. 
  """
  x = X[:,0]
  y = X[:,1]

  def J(x):
    x_col = np.reshape(x, (-1, 2))
    cost = 0.0
    N = x_col.shape[0]
    for idx in range(0, N):

      cost += np.linalg.norm(x_col[idx,:] - X[idx,:])**2
      for jdx in range(0, N):

        if M[idx, jdx] > 0.0:
          s_ij = max(S[idx, jdx], 1.0)

          cost += alpha*(np.linalg.norm(x_col[idx,:] - x_col[jdx,:]) - M[idx, jdx])**2/s_ij

    return cost

  x0 = X.reshape((1, -1)).flatten()
  res = optimize.minimize(J, x0, method='BFGS')

  return res

if __name__=='__main__':
  pass
