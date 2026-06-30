import xarray as xr
import numpy as np

def bilinear_interpolation(ds, target_lon, target_lat):
    """
    Interpolates an xarray Dataset to a new grid using bilinear interpolation.
    
    Parameters:
    - ds: xarray Dataset or DataArray to interpolate
    - target_lon: 1D array-like of target longitudes
    - target_lat: 1D array-like of target latitudes
    
    Returns:
    - Interpolated xarray Dataset/DataArray
    """
    return ds.interp(lon=target_lon, lat=target_lat, method="linear")

def delta_bias_correction(simulated_hist, observed, simulated_future):
    """
    Applies bias correction to future simulations using the Delta Method (Linear Scaling).
    
    Parameters:
    - simulated_hist: xarray DataArray of historical simulations (climatology)
    - observed: xarray DataArray of observations (climatology)
    - simulated_future: xarray DataArray of future simulations
    
    Returns:
    - bias_corrected_future: xarray DataArray of bias-corrected future simulations
    """
    # Calculate climatological mean for observed and simulated historical data
    # Assuming the input arrays are already aligned in space and represent the same time period
    obs_mean = observed.mean(dim='time')
    sim_mean = simulated_hist.mean(dim='time')
    
    # Calculate the adjustment factor A = Obs_mean - Sim_mean
    adjustment_factor = obs_mean - sim_mean
    
    # Apply bias correction
    bias_corrected_future = simulated_future + adjustment_factor
    
    return bias_corrected_future
