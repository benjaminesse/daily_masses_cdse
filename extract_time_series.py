import yaml
import argparse
import numpy as np
import pandas as pd
import xarray as xr
from functions import haversine

def extract_timeseries(name, start_date, end_date, vent_location,
                       clear_locations, radius):

    fname = f"{name}_{start_date}_{end_date}_so2_data.nc"
    with xr.open_dataset(fname) as ds:

        # Define the X and Y grid in 2D
        X, Y = np.meshgrid(ds.x, ds.y)

        # Calculate grid spacing
        dx = np.diff(ds.x)[0]
        dy = np.diff(ds.y)[0]

        # Calculate the region mask for the volcano
        vlat, vlon = vent_location
        region_mask = (
            haversine([vlat, vlon], [Y.ravel(), X.ravel()]) <= radius
        ).reshape(X.shape)

        # Add the clear regions to the mask
        for i, (clat, clon) in enumerate(clear_locations):
            region_mask = np.where(
                (haversine([clat, clon], [Y.ravel(), X.ravel()])).reshape(X.shape) <= radius,
                i+2, region_mask
            )

        # Initialise the output arrays in a dictionary
        output = {
            'volcano': np.full(len(ds.t), np.nan),
            **{
                f'clear_{i+1}': np.full(len(ds.t), np.nan)
                for i in range(len(clear_locations))
            }
        }

        # For each day, extract the region SO2 VCD and sum the values
        for ti in range(len(ds.t)):
            day_so2 = ds.SO2.isel(t=ti)
            output['volcano'][ti] = np.nansum(np.where(region_mask==1, day_so2, 0))
            for i in range(len(clear_locations)):
                output[f'clear_{i+1}'][ti] = np.nansum(np.where(region_mask==i+2, day_so2, 0))

    # Convert to a dataframe
    df = pd.DataFrame({'date': ds.t, **output})

    df.to_csv(f'{name}_SO2.csv')

if __name__ == '__main__':

    # Pull keyword arguments from the user
    parser = argparse.ArgumentParser(
        prog='extract_time_series.py',
        description='Extract long-term SO2 time series data'
    )
    parser.add_argument('region_id', help='Target region ID')
    parser.add_argument('start_date', help='Analysis start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='Analysis stop date (YYYY-MM-DD)')
    args = parser.parse_args()

    # Read in the region details
    with open('regions.yml', 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)[args.region_id]

    extract_timeseries(
        name=args.region_id,
        start_date=args.start_date,
        end_date=args.end_date,
        vent_location=config['vent_location'],
        clear_locations=config['clear_locations'],
        radius=config['radius']
    )