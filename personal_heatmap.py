import glob
import os

import folium
import gpxpy
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="heatmap_app")
location = geolocator.geocode("Montreal Quebec")
lat_check = float(location.raw["lat"])
lon_check = float(location.raw["lon"])

data = glob.glob("*.gpx")
fitdata = glob.glob("*.fit")

if len(fitdata) != 0:
    print("Converting Garmin FIT files")
    os.system("python fit_to_csv.py")
    os.system("mkdir fit_files")
    os.system("mv *.fit ./fit_files")

csvdata = glob.glob("*.csv")

lat = []
lon = []

all_lat = []
all_long = []

print("Loading data")

for activity in data:
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

for activity in csvdata:
    csv_filename = activity
    csv_file = pd.read_csv(csv_filename)

    for i in range(len(csv_file)):
        lat.append(csv_file["position_lat"][i])
        lon.append(csv_file["position_long"][i])

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

for activity in data:
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
for activity in csvdata:
    csv_filename = activity
    csv_file = pd.read_csv(csv_filename)
    for i in range(len(csv_file)):
        lat.append(csv_file["position_lat"][i])
        lon.append(csv_file["position_long"][i])
        if "heart_rate" in csv_file.columns:
            hr.append(csv_file["heart_rate"][i])
    points = list(zip(lat, lon))

    folium.PolyLine(points, color=color, weight=2.5, opacity=0.5).add_to(m)
    lat = []
    lon = []
    hr = []

m.save("heatmap.html")
