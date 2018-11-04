import os
import glob

import folium
import gpxpy

import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim()
location = geolocator.geocode("Montreal Quebec") # Change this to change location centering
lat_check = float(location.raw['lat'])
lon_check = float(location.raw['lon'])

data = glob.glob('*.gpx')
fitdata = glob.glob('*.fit')

if not len(fitdata) == 0:
    print('Converting Garmin FIT files')
    os.system('python fit_to_csv.py')
    os.system('mkdir fit_files')
    os.system('mv *.fit ./fit_files')

csvdata = glob.glob('*.csv')

lat = []
lon = []

all_lat = []
all_long = []

print('Loading data')

for activity in data:
    gpx_filename = activity
    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)

    check1 =  np.any(np.isclose(lat,lat_check,atol=0.5)) # Change the tolerance 'atol' to include a larger or smaller area around the centering point
    check2 = np.any(np.isclose(lon, lon_check,atol=0.5)) # Change the tolerance 'atol' to include a larger or smaller area around the centering point

    if check1 and check2 :
        all_lat.append(lat)
        all_long.append(lon)

    lon = []
    lat = []

for activity in csvdata:
    csv_filename = activity
    csv_file = pd.read_csv(csv_filename)

    for i in range(len(csv_file)):
        lat.append(csv_file['position_lat'][i])
        lon.append(csv_file['position_long'][i])

    check1 =  np.any(np.isclose(lat,lat_check,atol=0.5)) # Change the tolerance 'atol' to include a larger or smaller area around the centering point
    check2 = np.any(np.isclose(lon, lon_check,atol=0.5)) # Change the tolerance 'atol' to include a larger or smaller area around the centering point

    if check1 and check2 :
        all_lat.append(lat)
        all_long.append(lon)

    lon = []
    lat = []

all_lat = all_lat[0]
all_long = all_long[0]

min_lat = min(all_lat)
max_lat = max(all_lat)
min_long = max(all_long)
max_long = min(all_long)

central_long = sum(all_long)/float(len(all_long))
central_lat = sum(all_lat)/float(len(all_lat))

print('Initializing map')
m = folium.Map(location=[central_lat,central_long],tiles="Stamen Toner",zoom_start=14.2) # Recommended map styles are "Stamen Terrain", "Stamen Toner"

print('Plotting gpx data')

for activity in data:
    gpx_filename = activity
    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)

    points = zip(lat,lon)
    points = [item for item in zip(lat,lon)]

    folium.PolyLine(points, color="red", weight=2.5, opacity=0.5).add_to(m)
    lat = []
    lon = []

print('Plotting csv data')

for activity in csvdata:
    csv_filename = activity
    csv_file = pd.read_csv(csv_filename)
    for i in range(len(csv_file)):
        lat.append(csv_file['position_lat'][i])
        lon.append(csv_file['position_long'][i])

    points = zip(lat,lon)
    points = [item for item in zip(lat,lon)]

    folium.PolyLine(points, color="red", weight=2.5, opacity=0.5).add_to(m)
    lat = []
    lon = []

m.save('heatmap.html')
