# SRM Analysis Package

A Python package for Solar Radiation Modification (SRM) climate data analysis. This package implements mathematical operations and extreme climate event categorizations derived from the SRM impact studies on Southeast Asia and Eastern Africa.

## Features

- **Downscaling**: Bilinear interpolation for mapping simulation outputs to observation grid resolutions.
- **Bias Correction**: Delta Method (Linear Scaling) to align historical simulations with observations and adjust future projections.
- **SPEI Calculation**: Computes the Standardized Precipitation-Evapotranspiration Index (SPEI) and classifies extreme wet/dry events.
- **Dummy Data Generator**: Easily test functions using mock climate datasets containing synthetic temperature and precipitation variables.

## Requirements

- `python >= 3.8`
- `numpy`
- `pandas`
- `xarray`
- `scipy`
- `cftime`

## Installation

To install this package locally for development:

```bash
git clone https://github.com/naufal012/SRM.git
cd SRM/srm_analysis
pip install -e .
```

## How to Use

### Generating Dummy Data
You can generate `.nc` (NetCDF) datasets using the built-in generator to test out the functions:

```bash
python -m srm_analysis.dummy_data
```

This will produce `dummy_observed.nc` and `dummy_simulated.nc` in your current directory.

### Example Workflow in Python

```python
import xarray as xr
from srm_analysis import (
    bilinear_interpolation,
    delta_bias_correction,
    calculate_spei,
    categorize_spei
)

# 1. Load Data
obs = xr.open_dataset('dummy_observed.nc')
sim = xr.open_dataset('dummy_simulated.nc')

# 2. Downscale (Interpolate) simulated data to match observed grid
target_lons = obs['lon'].values
target_lats = obs['lat'].values
sim_interp = bilinear_interpolation(sim, target_lons, target_lats)

# 3. Apply Bias Correction
# (Using the same simulation as 'historical' and 'future' for this example)
future_corrected = delta_bias_correction(
    simulated_hist=sim_interp['temperature'], 
    observed=obs['temperature'], 
    simulated_future=sim_interp['temperature']
)

# 4. Calculate SPEI on bias-corrected data
# (Assuming future_corrected is temperature, using sim_interp for precipitation)
spei = calculate_spei(
    precip=sim_interp['precipitation'], 
    temp=future_corrected, 
    lat_arr=target_lats
)

# 5. Categorize Extreme Events
spei_categories = categorize_spei(spei)

print(spei_categories)
```
