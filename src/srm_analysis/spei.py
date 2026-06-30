import numpy as np
import xarray as xr
from scipy.stats import fisk, norm

def compute_pet_thornthwaite(temp, lat):
    """
    Computes Potential Evapotranspiration (PET) using the simplified Thornthwaite approach.
    
    Note: A full Thornthwaite implementation requires daylight hours calculated from latitude. 
    This is a simplified mock representation.
    """
    # Heat index
    I = np.sum((np.clip(temp, 0, None) / 5) ** 1.514, axis=0)
    a = (6.75e-7 * I**3) - (7.71e-5 * I**2) + (1.792e-2 * I) + 0.49239
    
    # Unadjusted PET
    pet = np.where(temp > 0, 16.0 * (10.0 * temp / np.where(I == 0, 1, I)) ** a, 0)
    
    return pet

def calculate_spei(precip, temp, lat_arr):
    """
    Calculates SPEI and categorizes extreme events.
    
    Parameters:
    - precip: xarray DataArray of precipitation (monthly)
    - temp: xarray DataArray of mean temperature
    - lat_arr: latitude array corresponding to the dataset
    
    Returns:
    - spei: xarray DataArray of the computed SPEI values
    """
    # 1. Calculate PET
    temp_vals = temp.values
    pet_vals = compute_pet_thornthwaite(temp_vals, lat_arr)
    pet = xr.DataArray(pet_vals, coords=temp.coords, dims=temp.dims)
    
    # 2. Climatic water balance (D = P - PET)
    D = precip - pet
    
    # 3. Fit to probability distribution (simplified mapping to standard normal)
    # For a robust calculation across time, we standardize the D values
    # Here we use a simple z-score as a placeholder for the log-logistic distribution fitting
    D_mean = D.mean(dim='time')
    D_std = D.std(dim='time')
    spei = (D - D_mean) / D_std
    
    return spei

def categorize_spei(spei_da):
    """
    Categorizes SPEI values based on standard thresholds.
    """
    # Define thresholds
    conditions = [
        spei_da >= 1.83,
        (spei_da >= 1.42) & (spei_da < 1.83),
        (spei_da > 1.0) & (spei_da < 1.42),
        (spei_da >= -1.0) & (spei_da <= 1.0),
        (spei_da > -1.42) & (spei_da < -1.0),
        (spei_da > -1.82) & (spei_da <= -1.42),
        spei_da <= -1.82
    ]
    
    choices = [
        "Extremely wet",
        "Severely wet",
        "Moderately wet",
        "Near Normal",
        "Moderate drought",
        "Severe drought",
        "Extreme drought"
    ]
    
    category_arr = np.select([c.values for c in conditions], choices, default="Unknown")
    category = xr.DataArray(category_arr, coords=spei_da.coords, dims=spei_da.dims)
    return category
