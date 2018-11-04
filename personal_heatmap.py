import os
import glob

import folium
import gpxpy
import tcxparser
import matplotlib.colors as clrs

import numpy as np
import pandas as pd
import matplotlib.cm as cm
from geopy.geocoders import Nominatim

#### CHANGES FOR MATT ####
'''
Imports
    - tcxparser
    - matplotlib.colors as clrs
    - matplotlib.cm as cm

Functions
    get_color(hr)

Plot points as planes and add heartrate as color value

    for i in range(np.min((len(points),len(hr)+1))-1):
        plane = [points[i]] + [points[i+1]]
        folium.PolyLine(plane, color=get_color(hr[i]), weight=2.5, opacity=1).add_to(m)

This made the code about threefold slower.

You're welcome.

'''
def get_color(hr):
    # min and max heart rates
    norm = clrs.Normalize(vmin=100, vmax=200) # Min/max heart rate
    m = cm.ScalarMappable(norm=norm, cmap='YlOrRd') # Choose colormap (from YeLlow to ReD)
    rgbs = m.to_rgba(hr)[:-1] # Remove opacity
    return clrs.rgb2hex(rgbs) # Turn into hex, because folium.Polyline doesn't take rgb

geolocator = Nominatim()
location = geolocator.geocode("Montreal Quebec")
lat_check = float(location.raw['lat'])
lon_check = float(location.raw['lon'])

data = glob.glob('gpxdata/*.gpx')
fitdata = glob.glob('*.fit')

if not len(fitdata) == 0:
    print('Converting Garmin FIT files')
    os.system('python fit_to_csv.py')
    os.system('mkdir fit_files')
    os.system('mv *.fit ./fit_files')

csvdata = glob.glob('*.csv')

all_lat = []
all_long = []

print('Loading data')

for activity in data:

    filename = activity[8:-4] #Remove foldername, remove extension
    
    gpx_file = open('gpxdata/'+filename+'.gpx', 'r')    
    gpx = gpxpy.parse(gpx_file)

    lat = []
    lon = []
    
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)

    check1 = np.any(np.isclose(lat, lat_check,atol=0.5))
    check2 = np.any(np.isclose(lon, lon_check,atol=0.5))

    if check1 and check2 :
        all_lat.append(lat)
        all_long.append(lon)

for activity in csvdata:
    csv_filename = activity
    csv_file = pd.read_csv(csv_filename)

    for i in range(len(csv_file)):
        lat.append(csv_file['position_lat'][i])
        lon.append(csv_file['position_long'][i])

    check1 =  np.any(np.isclose(lat,lat_check,atol=0.5))
    check2 = np.any(np.isclose(lon, lon_check,atol=0.5))

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
m = folium.Map(location=[central_lat,central_long],tiles="Stamen Toner",zoom_start=14.2)

print('Plotting gpx data')

for activity in data:
    gpx_filename = activity
    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    filename = activity[8:-4]

    print(filename)
    
    gpx_file = open('gpxdata/'+filename+'.gpx', 'r')    
    gpx = gpxpy.parse(gpx_file)

    tcx_file = open('tcxdata/'+filename+'.tcx', 'r')
    tcx = tcxparser.TCXParser(tcx_file)
    
    hr = tcx.hr_values()

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)

    points = zip(lat,lon)
    points = [item for item in zip(lat,lon)]

    print(len(points))
    print(len(hr))
    print('\n')

    for i in range(np.min((len(points),len(hr)+1))-1):
        plane = [points[i]] + [points[i+1]]
        folium.PolyLine(plane, color=get_color(hr[i]), weight=2.5, opacity=1).add_to(m)

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
