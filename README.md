# daily_masses_cdse
This code is to fetch daily SO2 maps of a given region and extract the long term cumulative SO2 signal from the data

## `fetch_time_series.py`
This script fetches the data cube for the region given over the required time interval. The region is defined within the `regions.yml` file.

This script takes the following arguments:
- `region_id`: the name of the region, as defined in the `regions.yml` file
- `start_date` : the analysis start date (YYYY-MM-DD)
- `end_date` : the analysis end date (YYYY-MM-DD)

This will automatically download the datacube to a local file.

## `extract_time_series.py`
This script extracts the SO2 time sereis from the downloaded datacube. It takes the same arguments as `fetch_time_series.py`, and will save the results as a `.csv` file

## `example_analysis.ipynb`
This is an example notebook with some basic analysis on the results of the two above scripts, including generating a map of the region and plotting the SO2 time series.

## `regions.yml`
This file (in yaml format) defines the regions to analyse. Each region is a seperate entry, with the following defined:
- `bounds`: a 4-element list giving the east, west, south and north limits of the region of interest
- `vent_location`: a tuple giving the location of the vent (latitude, longitude)
- `clear_locations`: a list of tuples giving the clear locations (latitude, longitude)
- `radius`: the radius, in meters, around the locations to sum the SO2 data over
