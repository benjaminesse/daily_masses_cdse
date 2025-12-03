import numpy as np

def haversine(start_coords, end_coords, radius=6371000):
    """Calculate the distance between two points.

    Parameters
    ----------
    start_coords : tuple
        Start coordinates (lat, lon) in decimal degrees (+ve = north/east).
    end_coords : tuple
        End coordinates (lat, lon) in decimal degrees (+ve = north/east).
    radius: float, optional
        Radius of the body in meters. Default is set to the Earth radius
        (6731km).

    Returns
    -------
    distance : float
        The linear distance between the two points in meters.
    """
    # Unpack the coordinates and convert to radians
    lat1, lon1 = np.radians(start_coords)
    lat2, lon2 = np.radians(end_coords)

    # Calculate the change in lat and lon
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate the square of the half chord length
    a = np.add(
        (np.sin(dlat/2))**2,
        np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/2))**2
    )

    # Calculate the angular distance
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    # Find distance moved
    distance = radius * c

    return distance