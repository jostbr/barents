
# Miscellaneous math tools to be called from elsewhere.

import math
import numpy as np
import scipy as sp

def get_path_length(lat1,lng1,lat2,lng2):
    """calculates the distance between two lat, long coordinate pairs"""
    R = 6371000 # radius of earth in m
    lat1rads = math.radians(lat1)
    lat2rads = math.radians(lat2)
    deltaLat = math.radians((lat2-lat1))
    deltaLng = math.radians((lng2-lng1))
    a = math.sin(deltaLat/2) * math.sin(deltaLat/2) + math.cos(lat1rads) * math.cos(lat2rads) * math.sin(deltaLng/2) * math.sin(deltaLng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def get_destination_latlon(lat,lng,azimuth,distance):
    """returns the lat an long of destination point
    given the start lat, long, aziuth, and distance"""
    R = 6378.1 #Radius of the Earth in km
    brng = math.radians(azimuth) #Bearing is degrees converted to radians.
    d = distance/1000 #Distance m converted to km
    lat1 = math.radians(lat) #Current dd lat point converted to radians
    lon1 = math.radians(lng) #Current dd long point converted to radians
    lat2 = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1)* math.sin(d/R)* math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d/R)* math.cos(lat1), math.cos(d/R)- math.sin(lat1)* math.sin(lat2))
    #convert back to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return[lat2, lon2]

def calculate_bearing(lat1,lng1,lat2,lng2):
    """calculates the azimuth in degrees from start point to end point"""
    startLat = math.radians(lat1)
    startLong = math.radians(lng1)
    endLat = math.radians(lat2)
    endLong = math.radians(lng2)
    dLong = endLong - startLong
    dPhi = math.log(math.tan(endLat/2.0+math.pi/4.0)/math.tan(startLat/2.0+math.pi/4.0))

    if abs(dLong) > math.pi:
         if dLong > 0.0:
             dLong = -(2.0 * math.pi - dLong)
         else:
             dLong = (2.0 * math.pi + dLong)

    bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0;
    return bearing

def get_coordinates(interval,azimuth,lat1,lng1,lat2,lng2):
    """returns every coordinate pair inbetween two coordinate
    pairs given the desired interval"""

    d = get_path_length(lat1,lng1,lat2,lng2)
    remainder, dist = math.modf((d / interval))
    counter = float(interval)
    coords = []
    coords.append([lat1,lng1])

    for distance in range(0,int(dist)):
        coord = get_destination_latlon(lat1,lng1,azimuth,counter)
        counter = counter + float(interval)
        coords.append(coord)

    coords.append([lat2,lng2])
    return coords

def meshgrid(x, y):
    """Wrapper for numpy.meshgrid."""
    return np.meshgrid(x, y)

def angle_from_dydx(x, y, unit="radians"):
    """Function to compute the angle array through atan(dy/dx)
    given arrays of y and x values."""
    x_grad = np.gradient(x)
    y_grad = np.gradient(y)

    angle = np.arctan2(y_grad, x_grad)  # arctan to find angle

    if unit == "radians":
        return angle
    elif unit == "degrees":
        return angle*360.0/(2*np.pi)
    else:
        raise ValueError("Invalid choice {} for angle unit!".format(unit))

def rotate_vectorfield(U, V, alpha):
    """Rotate wind vectors clockwise. alpha may be a scalar or an array
	alpha is in degrees. Returns u,v"""
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

def interp_midpoint(x, axis=()):
    """
    Function that interpolates an array along a given set of axes to midpoint
    values between existing data, i.e. takes the mean of two adjacent values to
    get the midpoint. The interpolated array has one less element along the interp
    axes.

    Args:
        x (ndarray)  : Array to be interpolated
        axis (tuple) : Tuple of which axes to interpolate along (subsequently)
    Returns:
        x_interp (ndarray) : Interpolated array
    """
    if type(axis) is int:
        axis = tuple(axis)

    for a in axis:
        slice_left = tuple(slice(None) if i != a else slice(0, x.shape[i]-1) for i in range(len(x.shape)))
        slice_right = tuple(slice(None) if i != a else slice(1, None) for i in range(len(x.shape)))
        x = (x[slice_left] + x[slice_right])/2.0

    return x

def compute_dz(depth, model_depth):
    """
    Function that computes the height of each cell given the vertical
    depths and the bottom topography

    Args:
        depth (ndarray) : Either 1d or 2d array of vertical levels in the section
        model_depth (ndarray) : 1d array of model topography at each point along section
    Returns:
        dz (ndarray) : 2d array of shape (depth.shape[0], model_depth.shape[0])
    """
    if len(depth.shape) == 1:
        depth = np.column_stack([depth for _ in range(len(model_depth))])

    dz = np.zeros(depth.shape)
    dz[0] = ((depth[1] - depth[0])/2.0 + depth[0])*np.where(model_depth.mask, float("nan"), 1.0)

    for i in range(len(model_depth)):
        for j in range(1, depth.shape[0]):
            if not type(model_depth[i]) is np.ma.core.MaskedConstant and depth[j,i] < model_depth[i]:
                if j == depth.shape[0] - 1 or depth[j+1,i] > model_depth[i]:
                    dz[j,i] = model_depth[i] - depth[j,i] + (depth[j,i] - depth[j-1,i])/2.0  # bottom cell
                else:
                    dz[j,i] = (depth[j+1,i] - depth[j-1,i])/2.0  # general cell
            else:
                dz[j,i] = float("nan")

    return dz
