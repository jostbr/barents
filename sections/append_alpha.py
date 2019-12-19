import scipy as sp
import numpy as np
import scipy.ndimage as nd
import netCDF4 
import sys

import matplotlib.pyplot as plt


def north_direction(lat):
    '''get the north direction relative to image positive y coordinate'''
    dlatdx = nd.filters.sobel(lat,axis=1,mode='constant',cval=sp.nan) #gradient in x-direction
    dlatdy = nd.filters.sobel(lat,axis=0,mode='constant',cval=sp.nan)
    ydir = -np.ones_like(lat)
    ydir[0:-1,:] = np.diff(lat, axis=0)  # check if latitude is ascending or descending in y axis

    # same step might have to be done with x direction.
    return sp.arctan2(dlatdx,dlatdy*sp.sign(ydir) )*180/sp.pi


filename = sys.argv[1]

ds = netCDF4.Dataset(filename, mode="r+")
a = ds.createVariable('alpha', np.float, dimensions=('y','x') )
lats = ds.variables["latitude"][:,:]
#lons = ds.variables["longitude"][:,:]

alpha = north_direction(lats)

a[:] = alpha

ds.close()


