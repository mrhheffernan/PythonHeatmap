import argparse
import glob
import os

import gpxpy
import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    args = argparse.ArgumentParser(description="Create a simple heatmap")

    args.add_argument(
        "--dir",
        help="Path to directory containing files to parse to generate the heatmap",
        default=os.getcwd(),
    )
    args.add_argument(
        "--output_path",
        help="Path to output the simple heatmap",
        default="simple_heatmap.png",
    )

    return args.parse_args()


def main():
    args = parse_args()

    gpx_list = glob.glob(args.dir + "/*.gpx")

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
        with open(gpx_data, "r") as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        lat.append(point.latitude)
                        lon.append(point.longitude)
        plt.plot(lon, lat, color="deepskyblue", lw=0.8, alpha=0.8)
    plt.savefig(args.output_path)
    plt.show()


if __name__ == "__main__":
    main()
