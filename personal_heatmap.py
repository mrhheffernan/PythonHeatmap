from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import gpxpy
import os
import glob
#import plotly.plotly as py
#import plotly.io as pio

#data_path = os.path.dirname(os.path.realpath(__file__))
#data = [f for f in listdir(data_path) if isfile(join(data_path,f))]

data = glob.glob('*.gpx')

print('data = ',data)
lat = []
lon = []

fig = plt.figure(facecolor = '0.05')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

all_lat = []
all_long = []

for activity in data:
    gpx_filename = activity#join(data_path,activity)
    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
    #plt.plot(lon, lat, color = 'deepskyblue', lw = 0.2, alpha = 0.8)
    all_lat.append(lat)
    all_long.append(lon)
    lat = []
    lon = []
all_lat = all_lat[0]
all_long = all_long[0]

min_lat = min(all_lat)
max_lat = max(all_lat)
min_long = max(all_long)
max_long = min(all_long)

#print('all_lat',all_lat[0])
print('max lat',max(all_lat))
print('min lat',min(all_lat))
print('max lat',min(all_long))
print('min lat',max(all_long))
#plt.show()
#filename = data_path + '.png'
#plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=300)



# nyc_london = [ dict(
#     type = 'scattergeo',
#     lat = all_lat,
#     lon = all_long,
#     mode = 'lines',
#     line = dict(
#         width = 2,
#         color = 'blue',
#     ),
# ) ]
#
# layout = dict(
#         title = 'London to NYC Great Circle',
#         showlegend = False,
#         geo = dict(
#             resolution = 50,
#             showland = True,
#             showlakes = True,
#             landcolor = 'rgb(204, 204, 204)',
#             countrycolor = 'rgb(204, 204, 204)',
#             lakecolor = 'rgb(255, 255, 255)',
#             projection = dict( type="equirectangular" ),
#             coastlinewidth = 2,
#             lataxis = dict(
#                 range = [ min_lat, max_lat ],
#                 showgrid = True,
#                 tickmode = "linear",
#                 dtick = 10
#             ),
#             lonaxis = dict(
#                 range = [min_long, max_long],
#                 showgrid = True,
#                 tickmode = "linear",
#                 dtick = 20
#             ),
#         )
#     )
#
# fig = dict( data=nyc_london, layout=layout )
# py.iplot( fig, validate=False, filename='d3-great-circle' )

#pio.write_image(fig, 'images/fig1.png')


# Now let's do this in folium

import folium

central_long = sum(all_long)/float(len(all_long))
central_lat = sum(all_lat)/float(len(all_lat))

m = folium.Map(location=[central_lat,central_long],tiles="Stamen Toner",zoom_start=15)
m.save('heatmap.html')
