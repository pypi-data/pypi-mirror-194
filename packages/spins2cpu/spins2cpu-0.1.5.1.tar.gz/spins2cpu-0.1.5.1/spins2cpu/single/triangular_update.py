import time
import numpy as np
from numba import njit, prange
from spins2cpu import functions

def iteration3(latt, X_s, Y_s, Ja, Jb, Jc, Aa, val, nequilibrium, nworks):
    t0 = time.time()
    ju = abs(Ja) * val
    Nw = np.zeros((nworks, 8))
    Ew = np.zeros(nworks)
    if ju > 3:
        sigma = 0.08 * np.power(val, 0.2)
        for i in range(nequilibrium):
            laRn = functions.sigmaNN(2, 4, Y_s, X_s, sigma, latt)
            randvals = np.random.rand(2, 4, Y_s, X_s)
            latZ = energy_A(latt, Aa)
            laRZ = energy_A(laRn, Aa)
            Etot = update3(latt, latZ, laRn, laRZ, randvals, X_s, Y_s, Ja, Jb, Jc, val)
        for i in range(nworks):
            laRn = functions.sigmaNN(2, 4, Y_s, X_s, sigma, latt)
            randvals = np.random.rand(2, 4, Y_s, X_s)
            latZ = energy_A(latt, Aa)
            laRZ = energy_A(laRn, Aa)
            Etot = update3(latt, latZ, laRn, laRZ, randvals, X_s, Y_s, Ja, Jb, Jc, val)
            Ew[i] = Etot
            Nw[i] = functions.Average(latt[0,0,:,:,2]), functions.Average(latt[0,1,:,:,2]), functions.Average(latt[0,2,:,:,2]), functions.Average(latt[0,3,:,:,2]),\
                    functions.Average(latt[1,0,:,:,2]), functions.Average(latt[1,1,:,:,2]), functions.Average(latt[1,2,:,:,2]), functions.Average(latt[1,3,:,:,2])
    else:
        for i in range(nequilibrium):
            laRn = functions.NormalrandNN(2, 4, Y_s, X_s)
            randvals = np.random.rand(2, 4, Y_s, X_s)
            latZ = energy_A(latt, Aa)
            laRZ = energy_A(laRn, Aa)
            Etot = update3(latt, latZ, laRn, laRZ, randvals, X_s, Y_s, Ja, Jb, Jc, val)
        for i in range(nworks):
            laRn = functions.NormalrandNN(2, 4, Y_s, X_s)
            randvals = np.random.rand(2, 4, Y_s, X_s)
            latZ = energy_A(latt, Aa)
            laRZ = energy_A(laRn, Aa)
            Etot = update3(latt, latZ, laRn, laRZ, randvals, X_s, Y_s, Ja, Jb, Jc, val)
            Ew[i] = Etot
            Nw[i] = functions.Average(latt[0,0,:,:,2]), functions.Average(latt[0,1,:,:,2]), functions.Average(latt[0,2,:,:,2]), functions.Average(latt[0,3,:,:,2]),\
                    functions.Average(latt[1,0,:,:,2]), functions.Average(latt[1,1,:,:,2]), functions.Average(latt[1,2,:,:,2]), functions.Average(latt[1,3,:,:,2])
    t = time.time() - t0
    return t, Nw, Ew

def energy_A(latt, Aa):
    latt_2 = latt ** 2
    if Aa > 0:
        L_z_2 = latt_2[:,:,:,:,2]
        return ( -Aa * L_z_2 )
    else:
        L_y_2 = latt_2[:,:,:,:,1]
        return ( -Aa * L_y_2 )

@njit(cache=True, parallel=True)
def update3(latt, latZ, laRn, laRZ, randvals, X_s, Y_s, Ja, Jb, Jc, val):
    nn_sum = 0
    nn_p = 0
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
                        i_c = ipp
                        j_c = jpp
                    elif k == 1:
                        x_inn = i
                        x_ipp = ipp
                        y_jnn = jnn
                        y_jpp = j
                        i_c = ipp
                        j_c = jnn
                    elif k == 2:
                        x_inn = inn
                        x_ipp = i
                        y_jnn = jnn
                        y_jpp = j
                        i_c = inn
                        j_c = jnn
                    else:
                        x_inn = inn
                        x_ipp = i
                        y_jnn = j
                        y_jpp = jpp
                        i_c = inn
                        j_c = jpp

                    if l == 0:
                        i_1 = x_inn
                        j_2 = y_jpp
                        ib0 = inn
                        ib1 = x_ipp
                    else:
                        i_1 = x_ipp
                        j_2 = y_jnn
                        ib0 = ipp
                        ib1 = x_inn

                    energy = ( latt[l,k,j,i,0] * ( -Ja * ( latt[lo,k ,j    ,i    ,0] + latt[lo,k1,j    ,i_1  ,0] + latt[lo,k2,j_2  ,i    ,0] + latt[lo,k3,j_2  ,i_1  ,0] +
                                                           latt[l ,k1,j    ,x_ipp,0] + latt[l ,k1,j    ,x_inn,0] ) -
                                                    Jb * ( latt[lo,k ,j    ,ib0  ,0] + latt[lo,k1,j    ,ib1  ,0] + latt[lo,k2,j_2  ,ib0  ,0] + latt[lo,k3,j_2  ,ib1  ,0] +
                                                           latt[l ,k2,y_jpp,i    ,0] + latt[l ,k2,y_jnn,i    ,0] ) -
                                                    Jc * ( latt[l ,k3,j    ,i    ,0] + latt[l ,k3,j    ,i_c  ,0] + latt[l ,k3,j_c  ,i    ,0] + latt[l ,k3,j_c  ,i_c  ,0] +
                                                           latt[l ,k ,j    ,ipp  ,0] + latt[l ,k ,j    ,inn  ,0] ) ) +
                               latt[l,k,j,i,1] * ( -Ja * ( latt[lo,k ,j    ,i    ,1] + latt[lo,k1,j    ,i_1  ,1] + latt[lo,k2,j_2  ,i    ,1] + latt[lo,k3,j_2  ,i_1  ,1] +
                                                           latt[l ,k1,j    ,x_ipp,1] + latt[l ,k1,j    ,x_inn,1] ) -
                                                    Jb * ( latt[lo,k ,j    ,ib0  ,1] + latt[lo,k1,j    ,ib1  ,1] + latt[lo,k2,j_2  ,ib0  ,1] + latt[lo,k3,j_2  ,ib1  ,1] +
                                                           latt[l ,k2,y_jpp,i    ,1] + latt[l ,k2,y_jnn,i    ,1] ) -
                                                    Jc * ( latt[l ,k3,j    ,i    ,1] + latt[l ,k3,j    ,i_c  ,1] + latt[l ,k3,j_c  ,i    ,1] + latt[l ,k3,j_c  ,i_c  ,1] +
                                                           latt[l ,k ,j    ,ipp  ,1] + latt[l ,k ,j    ,inn  ,1] ) ) +
                               latt[l,k,j,i,2] * ( -Ja * ( latt[lo,k ,j    ,i    ,2] + latt[lo,k1,j    ,i_1  ,2] + latt[lo,k2,j_2  ,i    ,2] + latt[lo,k3,j_2  ,i_1  ,2] +
                                                           latt[l ,k1,j    ,x_ipp,2] + latt[l ,k1,j    ,x_inn,2] ) -
                                                    Jb * ( latt[lo,k ,j    ,ib0  ,2] + latt[lo,k1,j    ,ib1  ,2] + latt[lo,k2,j_2  ,ib0  ,2] + latt[lo,k3,j_2  ,ib1  ,2] +
                                                           latt[l ,k2,y_jpp,i    ,2] + latt[l ,k2,y_jnn,i    ,2] ) -
                                                    Jc * ( latt[l ,k3,j    ,i    ,2] + latt[l ,k3,j    ,i_c  ,2] + latt[l ,k3,j_c  ,i    ,2] + latt[l ,k3,j_c  ,i_c  ,2] +
                                                           latt[l ,k ,j    ,ipp  ,2] + latt[l ,k ,j    ,inn  ,2] ) ) )
                    Erandn = ( laRn[l,k,j,i,0] * ( -Ja * ( latt[lo,k ,j    ,i    ,0] + latt[lo,k1,j    ,i_1  ,0] + latt[lo,k2,j_2  ,i    ,0] + latt[lo,k3,j_2  ,i_1  ,0] +
                                                           latt[l ,k1,j    ,x_ipp,0] + latt[l ,k1,j    ,x_inn,0] ) -
                                                    Jb * ( latt[lo,k ,j    ,ib0  ,0] + latt[lo,k1,j    ,ib1  ,0] + latt[lo,k2,j_2  ,ib0  ,0] + latt[lo,k3,j_2  ,ib1  ,0] +
                                                           latt[l ,k2,y_jpp,i    ,0] + latt[l ,k2,y_jnn,i    ,0] ) -
                                                    Jc * ( latt[l ,k3,j    ,i    ,0] + latt[l ,k3,j    ,i_c  ,0] + latt[l ,k3,j_c  ,i    ,0] + latt[l ,k3,j_c  ,i_c  ,0] +
                                                           latt[l ,k ,j    ,ipp  ,0] + latt[l ,k ,j    ,inn  ,0] ) ) +
                               laRn[l,k,j,i,1] * ( -Ja * ( latt[lo,k ,j    ,i    ,1] + latt[lo,k1,j    ,i_1  ,1] + latt[lo,k2,j_2  ,i    ,1] + latt[lo,k3,j_2  ,i_1  ,1] +
                                                           latt[l ,k1,j    ,x_ipp,1] + latt[l ,k1,j    ,x_inn,1] ) -
                                                    Jb * ( latt[lo,k ,j    ,ib0  ,1] + latt[lo,k1,j    ,ib1  ,1] + latt[lo,k2,j_2  ,ib0  ,1] + latt[lo,k3,j_2  ,ib1  ,1] +
                                                           latt[l ,k2,y_jpp,i    ,1] + latt[l ,k2,y_jnn,i    ,1] ) -
                                                    Jc * ( latt[l ,k3,j    ,i    ,1] + latt[l ,k3,j    ,i_c  ,1] + latt[l ,k3,j_c  ,i    ,1] + latt[l ,k3,j_c  ,i_c  ,1] +
                                                           latt[l ,k ,j    ,ipp  ,1] + latt[l ,k ,j    ,inn  ,1] ) ) +
                               laRn[l,k,j,i,2] * ( -Ja * ( latt[lo,k ,j    ,i    ,2] + latt[lo,k1,j    ,i_1  ,2] + latt[lo,k2,j_2  ,i    ,2] + latt[lo,k3,j_2  ,i_1  ,2] +
                                                           latt[l ,k1,j    ,x_ipp,2] + latt[l ,k1,j    ,x_inn,2] ) -
                                                    Jb * ( latt[lo,k ,j    ,ib0  ,2] + latt[lo,k1,j    ,ib1  ,2] + latt[lo,k2,j_2  ,ib0  ,2] + latt[lo,k3,j_2  ,ib1  ,2] +
                                                           latt[l ,k2,y_jpp,i    ,2] + latt[l ,k2,y_jnn,i    ,2] ) -
                                                    Jc * ( latt[l ,k3,j    ,i    ,2] + latt[l ,k3,j    ,i_c  ,2] + latt[l ,k3,j_c  ,i    ,2] + latt[l ,k3,j_c  ,i_c  ,2] +
                                                           latt[l ,k ,j    ,ipp  ,2] + latt[l ,k ,j    ,inn  ,2] ) ) )
                    ez = latZ[l,k,j,i]
                    Ez = laRZ[l,k,j,i]
                    if val == 0:
                        if energy < 0:
                            pass
                            DeltaE = ez + energy - Ez - Erandn
                        else:
                            latt[l,k,j,i] *= -1
                            DeltaE = ez - energy - Ez - Erandn
                        if DeltaE < 0:
                            pass
                        else:
                            latt[l,k,j,i] = laRn[l,k,j,i]
                    else:
                        if energy < 0:
                            if randvals[l,k,j,i] < np.exp( 2.0 * val * energy ):
                                latt[l,k,j,i] *= -1
                                DeltaE = ez - energy - Ez - Erandn
                            else:
                                DeltaE = ez + energy - Ez - Erandn
                        else:
                            latt[l,k,j,i] *= -1
                            DeltaE = ez - energy - Ez - Erandn
                        if DeltaE < 0:
                            if randvals[l,k,j,i] < np.exp( val * DeltaE ):
                                latt[l,k,j,i] = laRn[l,k,j,i]
                        else:
                            latt[l,k,j,i] = laRn[l,k,j,i]

                    nn_sum += energy
                    nn_p += ez
    return ( nn_p + nn_sum / 2.0 )
