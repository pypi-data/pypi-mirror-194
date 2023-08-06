import time
import numpy as np
from numba import njit, prange
from spins2cpu import functions

def iteration3(latt, X_s, Y_s, Ja, J0, J1, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 8))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        randvals = np.random.rand(2, 4, Y_s, X_s)
        E0 = update3(latt, randvals, X_s, Y_s, Ja, J0, J1, val)
    for i in range(nworks):
        randvals = np.random.rand(2, 4, Y_s, X_s)
        E0 = update3(latt, randvals, X_s, Y_s, Ja, J0, J1, val)
        Ew[i] = E0 / 2
        Nw[i] = functions.Average(latt[0,0]), functions.Average(latt[0,1]), functions.Average(latt[0,2]), functions.Average(latt[0,3]),\
                functions.Average(latt[1,0]), functions.Average(latt[1,1]), functions.Average(latt[1,2]), functions.Average(latt[1,3])
    t = time.time() - t0
    return t, Nw, Ew

@njit(cache=True, parallel=True)
def update3(latt, randvals, X_s, Y_s, Ja, J0, J1, val):
    nn_sum = 0
    for l in range(2):
        for k in prange(4):
            for j in range(Y_s):
                for i in range(X_s):
                    lo  = 1 - l
                    k1  = 3 - k
                    k2  = (5 - k) if k > 1 else (1 - k)
                    k3  = (2 - k) if k%2 == 0 else (4 - k)
                    ipp = (i + 1) if (i + 1) < X_s else 0
                    inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
                    jpp = (j + 1) if (j + 1) < Y_s else 0
                    jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
                    if k == 0:
                        x_inn = i
                        x_ipp = ipp
                        y_jnn = j
                        y_jpp = jpp
                    elif k == 1:
                        x_inn = i
                        x_ipp = ipp
                        y_jnn = jnn
                        y_jpp = j
                    elif k == 2:
                        x_inn = inn
                        x_ipp = i
                        y_jnn = jnn
                        y_jpp = j
                    else:
                        x_inn = inn
                        x_ipp = i
                        y_jnn = j
                        y_jpp = jpp

                    energy = ( latt[l,k,j,i] * ( -Ja * ( latt[l ,k1,j    ,x_ipp] + latt[l ,k1,j    ,x_inn] +
                                                         latt[l ,k2,y_jpp,i    ] + latt[l ,k2,y_jnn,i    ] +
                                                         latt[l ,k3,y_jnn,x_inn] + latt[l ,k3,y_jpp,x_ipp] ) -
                                                  J0 *   latt[lo,k ,j    ,i    ] -
                                                  J1 * ( latt[lo,k1,j    ,x_ipp] + latt[lo,k1,j    ,x_inn] +
                                                         latt[lo,k2,y_jpp,i    ] + latt[lo,k2,y_jnn,i    ] +
                                                         latt[lo,k3,y_jnn,x_inn] + latt[lo,k3,y_jpp,x_ipp] ) ) )

                    if val == 0:
                        if energy < 0:
                            pass
                        else:
                            latt[l,k,j,i] *= -1
                    else:
                        if energy < 0:
                            if randvals[l,k,j,i] < np.exp( 2.0 * val * energy ):
                                latt[l,k,j,i] *= -1
                        else:
                            latt[l,k,j,i] *= -1

                    nn_sum += energy
    return nn_sum
