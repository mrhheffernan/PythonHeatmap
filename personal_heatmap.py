import argparse
import glob
import os
from zoneinfo import ZoneInfo

import folium
import gpxpy
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim

from fit_to_csv import collect_data

geolocator = Nominatim(user_agent="heatmap_app")


def parse_args() -> argparse.Namespace:
    args = argparse.ArgumentParser()
    args.add_argument(
        "--dir",
        help="Path to direcotry with .fit, .gpx files to process for the heatmap",
        default=os.getcwd(),
    )
    args.add_argument(
        "--timezone",
        help="Timezone for timestamps, e.g. 'US/Pacific'",
        default="US/Pacific",
    )
    args.add_argument(
        "--output_path",
        help="Path to write the heatmap .html to",
        default="heatmap.html",
    )

    return args.parse_args()


def main():
    args = parse_args()
    location = geolocator.geocode("Montreal Quebec")
    lat_check = float(location.raw["lat"])
    lon_check = float(location.raw["lon"])

    gpx_files = glob.glob(args.dir + "/*.gpx")
    fit_files = glob.glob(args.dir + "/*.fit")

    fit_data = []
    if len(fit_files):
        print("Converting Garmin FIT files")
        for file in fit_files:
            activity_data = collect_data(file, tz=ZoneInfo(args.timezone))
            df_activity_data = pd.DataFrame(activity_data)
            fit_data.append(df_activity_data)

    lat = []
    lon = []

    all_lat = []
    all_long = []

    print("Loading data")

    for activity in gpx_files:
        gpx_filename = activity
        with open(gpx_filename, "r") as gpx_file:
            gpx = gpxpy.parse(gpx_file)

            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        lat.append(point.latitude)
                        lon.append(point.longitude)

        check1 = np.any(np.isclose(lat, lat_check, atol=0.5))
        check2 = np.any(np.isclose(lon, lon_check, atol=0.5))

        if check1 and check2:
            all_lat.append(lat)
            all_long.append(lon)

        lon = []
        lat = []

    for activity in fit_data:
        for i in range(len(activity)):
            # TODO: use extend and .values.to_list() and avoid the loop entirely
            lat.append(activity["position_lat"][i])
            lon.append(activity["position_long"][i])

        check1 = np.any(np.isclose(lat, lat_check, atol=0.5))
        check2 = np.any(np.isclose(lon, lon_check, atol=0.5))

        if check1 and check2:
            all_lat.append(lat)
            all_long.append(lon)

        lon = []
        lat = []

    if not all_lat or not all_long:
        raise ValueError(
            "No activities found within the specified location. Check lat_check/lon_check."
        )

    all_lat = all_lat[0]
    all_long = all_long[0]

    central_long = sum(all_long) / len(all_long)
    central_lat = sum(all_lat) / len(all_lat)

    print("Initializing map")
    m = folium.Map(
        location=[central_lat, central_long], tiles="Stamen Toner", zoom_start=14.2
    )

    print("Plotting gpx data")

    for activity in gpx_files:
        gpx_filename = activity
        with open(gpx_filename, "r") as gpx_file:
            gpx = gpxpy.parse(gpx_file)

            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        lat.append(point.latitude)
                        lon.append(point.longitude)

        points = list(zip(lat, lon))

        folium.PolyLine(points, color="red", weight=2.5, opacity=0.5).add_to(m)
        lat = []
        lon = []

    print("Plotting csv data")
    color = "red"
    hr = []
    for activity in fit_data:
        for i in range(len(activity)):
            lat.append(activity["position_lat"][i])
            lon.append(activity["position_long"][i])
            if "heart_rate" in activity.columns:
                hr.append(activity["heart_rate"][i])
        points = list(zip(lat, lon))

        folium.PolyLine(points, color=color, weight=2.5, opacity=0.5).add_to(m)
        lat = []
        lon = []
        hr = []

    m.save(args.output_path)


if __name__ == "__main__":
    main()
