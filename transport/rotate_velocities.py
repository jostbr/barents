#!/use/bin/env python
import scipy as sp
import numpy as np
import scipy.ndimage as nd
from netCDF4 import Dataset
import sys
#from get_latlon import *

def rotate_vectorfield(U,V,alpha):
    '''rotate wind vectors clockwise. alpha may be a scalar or an array
	alpha is in degrees
	returns u,v '''
    alpha = sp.array(alpha)*sp.pi/180
    alpha = alpha.flatten()
    R = sp.array([[sp.cos(alpha), -sp.sin(alpha)], [sp.sin(alpha), sp.cos(alpha)] ])
    shpe = U.shape
    origwind = sp.array((U.flatten(), V.flatten()))
    if len(R.shape)==2:
        rotwind = np.dot(R, origwind) # for constant rotation angle
    else:
        # for rotation angle given as array with same dimensions as U and V:
        # k-loop with rotwind(k) = dot(R(i,j,k), origwind(j,k)) (einstein summation indices)
        # i: points, j: y vector, k: x vector
        rotwind = sp.einsum("ijk,ik -> jk", R, origwind)  # einstein summation indices
    Urot ,Vrot = rotwind[0,:], rotwind[1,:]
    Urot = Urot.reshape(shpe)
    Vrot = Vrot.reshape(shpe)
    return Urot, Vrot

def append_section_referenced_velocities(sec_data_file, sec_mod_grid):
    '''rotate u,v velocities in a section data file from model grid to section grid
       and append rotated velocities to section data file

       new u velocities are along section and new
           v velocities are across section

       append_section_referenced_velocities(section_data_file, sec_mod_file) '''

    sdf = Dataset(sec_data_file, 'r+')
    u = sdf.variables['u'] 
    v = sdf.variables['v']

    smg = Dataset(sec_mod_file, 'r')
    # alpha is the angel from section x direction to model x direction, 
    # section x is defined as along-section and section y is perpendicular to the section
    alpha = smg.variables['alpha']

    u_sec, v_sec = rotate_vectorfield(u[:], v[:], -alpha[:]) # rotate from model x to section x

    u_sec_nc = sdf.createVariable('u_sec', u.datatype, u.dimensions)
    u_sec_nc.setncatts({k: u.getncattr(k) for k in u.ncattrs()})
    u_sec_nc.setncatts({'long_name' : 'along_section_velocity'})
    u_sec_nc.setncatts({'standard_name' : 'along_section_velocity'})

    v_sec_nc = sdf.createVariable('v_sec', v.datatype, v.dimensions)
    v_sec_nc.setncatts({k: v.getncattr(k) for k in v.ncattrs()})
    v_sec_nc.setncatts({'long_name' : 'cross_section_velocity'})
    v_sec_nc.setncatts({'standard_name' : 'cross_section_velocity'})

    sdf.close()
    smg.close()

if __name__ == "__main__":
    sec_data_file = sys.argv[1]
    sec_mod_grid = sys.argv[2]
    append_section_referenced_velocities(sec_data_file, sec_mod_grid)








