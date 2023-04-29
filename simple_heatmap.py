import gpxpy
import matplotlib.pyplot as plt
import glob

gpx_list = glob.glob("*.gpx")


fig = plt.figure(facecolor="0.05")
ax = plt.Axes(
    fig,
    [0.0, 0.0, 1.0, 1.0],
)
ax.set_aspect("equal")
ax.set_axis_off()
fig.add_axes(ax)

for gpx_data in gpx_list:
    lat = []
    lon = []
    gpx_file = open(gpx_data, "r")
    gpx = gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
    plt.plot(lon, lat, color="deepskyblue", lw=0.8, alpha=0.8)
# plt.savefig('simple_heatmap.png')
plt.show()
