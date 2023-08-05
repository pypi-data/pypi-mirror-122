import numpy as np
import pandas as pd

import asilib

earth_radius_km = 6371  # Earth radius


def equal_area(mission, station, time, lla, box_km=(5, 5), alt_thresh_km=3):
    """
    Given a square are in kilometers and a series of (latitude,
    longitude, altitude) coordinates, calculate the pixel box
    width and height.

    Parameters
    ----------
    mission: str
        The mission used to look up the skymap file.
    station: str
        The station used to look up the skymap file.
    time: datetime, or str
        Time is used to find the relevant skymap file: file created nearest to, and before, the time.
    lla: np.ndarray
        An array with (n_time, 3) dimensions with the columns
        representing the latitude, longitude, and altitude
        coordinates.
    box_size_km: iterable
        A length 2 iterable with the box dimensions in
        longitude and latitude in units of kilometers.

    Returns
    -------
    pixel_mask: np.ndarray
        An array with (n_time, n_x_pixels, n_y_pixels) dimensions with
        dimensions n_x_pixels and n_y_pixels dimensions the size of each
        image. Values inside the area are 1 and outside are np.nan.
    """
    assert len(box_km) == 2, 'The box_km parameter must have a length of 2.'

    skymap_dict = asilib.load_skymap(mission, station, time)

    # Get numpy array if pd.DataFrame passed
    if isinstance(lla, pd.DataFrame):
        lla = lla.to_numpy()
    elif isinstance(lla, list):
        lla = np.array(lla)

    initial_shape = lla.shape
    # I want to work with 2d arrays, even if 1d array was supplied. We will reduce the dimensions
    # at the end.
    if len(initial_shape) == 1:
        lla = np.array([lla])

    # Check that the altitude value is in the skymap.
    for alt in lla[:, -1]:
        assert (
            np.min(np.abs(skymap_dict['FULL_MAP_ALTITUDE'] / 1000 - alt)) < alt_thresh_km
        ), f'Got {alt} km altitude, but it must be one of these: {skymap_dict["FULL_MAP_ALTITUDE"]/1000}'
    alt_index = np.argmin(np.abs(skymap_dict['FULL_MAP_ALTITUDE'] / 1000 - alt))
    lat_map = skymap_dict['FULL_MAP_LATITUDE'][alt_index, :, :]
    lon_map = skymap_dict['FULL_MAP_LONGITUDE'][alt_index, :, :]

    # shape[X]-1 because the lat/lon maps define the vertices.
    pixel_mask = np.nan * np.zeros((lla.shape[0], lat_map.shape[0] - 1, lat_map.shape[1] - 1))

    dlat = _dlat(box_km[1], lla[:, -1])
    dlon = _dlon(box_km[0], lla[:, -1], lla[:, 0])

    for i, ((lat, lon, _), dlon_i, dlat_i) in enumerate(zip(lla, dlon, dlat)):
        # Find the indices of the box. If none were found (pixel smaller than
        # the box_size_km) then increase the box size until one pixel is found.
        masked_box_len = 0
        multiplier = 1
        step = 0.1

        while masked_box_len == 0:
            idx_box = np.where(
                (lat_map >= lat - multiplier * dlat_i / 2)
                & (lat_map <= lat + multiplier * dlat_i / 2)
                & (lon_map >= lon - multiplier * dlon_i / 2)
                & (lon_map <= lon + multiplier * dlon_i / 2)
            )

            masked_box_len = len(idx_box[0])
            if masked_box_len:
                pixel_mask[i, idx_box[0], idx_box[1]] = 1
            else:
                multiplier += step

    pixel_mask = pixel_mask[:, ::-1, ::-1]

    if len(initial_shape) == 1:
        return pixel_mask.reshape(lat_map.shape)
    else:
        return pixel_mask


def _dlat(d, alt):
    """
    Calculate the change in latitude that correpsponds to arc length distance d at
    alt altitude. Units are kilometers. Both d and alt must be the same length.

    Parameters
    ----------
    d: float or np.ndarray
        A float, 1d list, or 1d np.array of arc length.
    alt: float or np.ndarray
        A float, 1d list, or 1d np.array of satellite altitudes.

    Returns
    -------
    dlat: float or np.ndarray
        A float or an array of the corresponding latitude differences in degrees.
    """
    if isinstance(alt, list):  # Don't need to cast d since it is in np.divide().
        alt = np.array(alt)
    return np.rad2deg(np.divide(d, (earth_radius_km + alt)))


def _dlon(d, alt, lat):
    """
    Calculate the change in longitude that corresponds to arc length distance d at
    a lat latitude, and alt altitude.

    Parameters
    ----------
    d: float or np.ndarray
        A float or an array of arc length in kilometers.
    alt: float or np.ndarray
        A float or an array of satellite altitudes in kilometers.
    lat: float
        The latitude to evaluate the change in longitude in degrees.

    Returns
    -------
    dlon: float or np.ndarray
        A float or an array of the corresponding longitude differences in degrees.
    """
    if isinstance(alt, list):  # Don't need to cast other variables.
        alt = np.array(alt)

    numerator = np.sin(d / (2 * (earth_radius_km + alt)))
    denominator = np.cos(np.deg2rad(lat))
    dlon_rads = 2 * np.arcsin(numerator / denominator)
    return np.rad2deg(dlon_rads)
