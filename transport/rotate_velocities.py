import scipy as sp
import numpy as np
import scipy.ndimage as nd
from netCDF4 import Dataset
import sys
#from get_latlon import *

sectionfilename = sys.argv[1]
#alphafilename = sys.argv[2]


def rotate_vectorfield(U,V,alpha):
    '''rotate wind vectors clockwise. alpha may be a scalar or an array
	alpha is in degrees
	returns u,v '''
    alpha = sp.array(alpha)*sp.pi/180
    alpha = alpha.flatten()
    R = sp.array([[sp.cos(alpha), -sp.sin(alpha)], [sp.sin(alpha), sp.cos(alpha)] ])
    shpe = U.shape
    origwind = sp.array((U.flatten(), V.flatten()))
    #if len(R.shape)==2:
    #    rotwind = np.dot(R, origwind) # for constant rotation angle
    #else:
    # for rotation angle given as array with same dimensions as U and V:
    # k-loop with rotwind(k) = dot(R(i,j,k), origwind(j,k)) (einstein summation indices)
    rotwind = sp.einsum("ijk,ik -> jk", R, origwind)  # einstein summation indices

    Urot ,Vrot = rotwind[0,:], rotwind[1,:]
    Urot = Urot.reshape(shpe)
    Vrot = Vrot.reshape(shpe)
    return Urot, Vrot

def north_direction(lat):
    '''get the north direction relative to image positive y coordinate'''
    dlatdx = nd.filters.sobel(lat,axis=1,mode='constant',cval=sp.nan) #gradient in x-direction
    dlatdy = nd.filters.sobel(lat,axis=0,mode='constant',cval=sp.nan)
    ydir = lat[-1,0] -lat[0,0] # check if latitude is ascending or descending in y axis
    # same step might have to be done with x direction.
    return sp.arctan2(dlatdx,dlatdy*sp.sign(ydir) )*180/sp.pi


sf = Dataset(sectionfilename)
u = sf.variables['u'][:]
v = sf.variables['v'][:]
alpha = sf.variables['alpha'][:]

#lat_grid, lon_grid = get_latlon_from_topaz()

sec_northdir  = north_direction(sec_lat.T)



#alpha = sec_northdir - grid_northdir
