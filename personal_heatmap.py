import argparse
import glob
import os
from zoneinfo import ZoneInfo

import folium
import gpxpy
import numpy as np
import pandas as pd

from fit_to_csv import collect_data


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

    gpx_files = glob.glob(args.dir + "/*.gpx")
    fit_files = glob.glob(args.dir + "/*.fit")

    fit_data = []
    if len(fit_files):
        print("Converting Garmin FIT files")
        for file in fit_files:
            activity_data = collect_data(file, tz=ZoneInfo(args.timezone))
            df_activity_data = pd.DataFrame(activity_data)
            fit_data.append(df_activity_data)

    all_lat = []
    all_long = []

    print("Loading data")

    for activity in gpx_files:
        lon = []
        lat = []

        with open(activity, "r") as gpx_file:
            gpx = gpxpy.parse(gpx_file)

            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        lat.append(point.latitude)
                        lon.append(point.longitude)

        all_lat.append(lat)
        all_long.append(lon)

    for activity in fit_data:
        lon = []
        lat = []
        for i in range(len(activity)):
            # TODO: use extend and .values.to_list() and avoid the loop entirely
            lat.append(float(activity["position_lat"][i]))
            lon.append(float(activity["position_long"][i]))

        all_lat.append(lat)
        all_long.append(lon)

    central_long = np.mean(np.array(all_long).flatten())
    central_lat = np.mean(np.array(all_lat).flatten())

    print("Initializing map")
    m = folium.Map(
        location=[central_lat, central_long], tiles="Cartodb Positron", zoom_start=14.2
    )

    print("Plotting activities")

    for i in range(len(all_lat)):
        lat = all_lat[i]
        lon = all_long[i]
        points = list(zip(lat, lon))

        folium.PolyLine(points, color="red", weight=2.5, opacity=0.5).add_to(m)

    m.save(args.output_path)


if __name__ == "__main__":
    main()
