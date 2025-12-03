import yaml
import openeo
import argparse

def fetch_tropomi_data(name, bounds, start_date, end_date):

    # Establish the connetion to openeo
    connection = openeo.connect(url="openeo.dataspace.copernicus.eu")
    connection.authenticate_oidc()

    # Unpack the bounds
    lonW, lonE, latS, latN = bounds

    # Define the datacube to acquire
    so2_cube = connection.load_collection(
        "SENTINEL_5P_L2",
        temporal_extent=(start_date, end_date),
        spatial_extent={
            "west": lonW, "south": latS, "east": lonE, "north": latN,
            "crs": "EPSG:4326"
        },
        bands=["SO2"]
    )

    # Now aggregate by day to avoid having multiple data per day
    so2_cube = so2_cube.aggregate_temporal_period(reducer="mean", period="day")

    so2_cube.execute_batch(
        title=f"SO2 from {name}",
        outputfile=f"{name}_{start_date}_{end_date}_so2_data.nc"
    )

if __name__ == '__main__':

    # Pull keyword arguments from the user
    parser = argparse.ArgumentParser(
        prog='fetch_time_series.py',
        description='Fetch long-term SO2 time series data'
    )
    parser.add_argument('region_id', help='Target region ID')
    parser.add_argument('start_date', help='Analysis start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='Analysis stop date (YYYY-MM-DD)')
    args = parser.parse_args()

    # Read in the region details
    with open('regions.yml', 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)[args.region_id]

    fetch_tropomi_data(
        name=args.region_id,
        bounds=config['bounds'],
        start_date=args.start_date,
        end_date=args.end_date
    )