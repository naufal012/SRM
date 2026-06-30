import numpy as np
import pandas as pd
import xarray as xr

def generate_dummy_climate_data(start_year="1995", end_year="2014", n_lat=10, n_lon=10):
    """
    Generates dummy climate data (temperature and precipitation) as xarray Datasets.
    Useful for testing the downscaling, bias correction, and SPEI functions.
    """
    dates = pd.date_range(start=f"{start_year}-01-01", end=f"{end_year}-12-31", freq="ME")
    lats = np.linspace(-10, 10, n_lat)
    lons = np.linspace(30, 50, n_lon)
    
    time_idx = np.arange(len(dates))
    
    # Temperature: seasonal variation + noise
    seasonal_temp = 5 * np.sin(2 * np.pi * time_idx / 12)
    base_temp = 25 + seasonal_temp[:, None, None] + np.random.normal(0, 2, size=(len(dates), n_lat, n_lon))
    
    # Precipitation: seasonal variation + noise, clipped to be non-negative
    seasonal_precip = 50 * np.sin(2 * np.pi * time_idx / 12) + 50
    base_precip = np.clip(seasonal_precip[:, None, None] + np.random.normal(0, 20, size=(len(dates), n_lat, n_lon)), 0, None)
    
    observed = xr.Dataset({
        "temperature": (["time", "lat", "lon"], base_temp),
        "precipitation": (["time", "lat", "lon"], base_precip)
    }, coords={
        "time": dates,
        "lat": lats,
        "lon": lons
    })
    
    # Create simulated dataset (with a bias)
    simulated = xr.Dataset({
        "temperature": (["time", "lat", "lon"], base_temp + 2.0), # +2C bias
        "precipitation": (["time", "lat", "lon"], base_precip * 0.8) # 20% dry bias
    }, coords={
        "time": dates,
        "lat": lats,
        "lon": lons
    })
    
    return observed, simulated

if __name__ == "__main__":
    print("Generating dummy data...")
    obs, sim = generate_dummy_climate_data()
    obs.to_netcdf("dummy_observed.nc")
    sim.to_netcdf("dummy_simulated.nc")
    print("Data saved to dummy_observed.nc and dummy_simulated.nc")
