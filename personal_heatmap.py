from os import listdir
from os.path import isfile, join
import gpxpy
import os
import glob
import folium
import numpy as np
from geopy.geocoders import Nominatim
import fitparse


geolocator = Nominatim()
location = geolocator.geocode("Montreal Quebec")
lat_check = float(location.raw['lat'])
lon_check = float(location.raw['lon'])

data = glob.glob('*.gpx')

fitdata = glob.glob('*.fit')

if not len(fitdata) == 0:
    print('Converting Garmin FIT files')
    os.system('python fit_to_csv.py')
#    directory = os.path.dirname(os.path.abspath(__file__))
    #os.system('python process_all.py --subject-name="Matt" --fit-source-dir='+directory+' --fit-processed-csv-dir='+directory+' --fit-ignore-splits-and-pylaps --skip-gpx-conversion')
    #print('Garmin conversion done!')

#print('data = ',data)
lat = []
lon = []

all_lat = []
all_long = []

for activity in data:
    gpx_filename = activity
    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)

    check1 =  np.any(np.isclose(lat,lat_check,atol=0.5))
    check2 = np.any(np.isclose(lon, lon_check,atol=0.5))

    if check1 and check2 :
        all_lat.append(lat)
        all_long.append(lon)

    lon = []
    lat = []
#exit()
i = 1
all_lat = all_lat[0]
all_long = all_long[0]

min_lat = min(all_lat)
max_lat = max(all_lat)
min_long = max(all_long)
max_long = min(all_long)

central_long = sum(all_long)/float(len(all_long))
central_lat = sum(all_lat)/float(len(all_lat))

m = folium.Map(location=[central_lat,central_long],tiles="Stamen Toner",zoom_start=14.2)

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

m.save('heatmap.html')
