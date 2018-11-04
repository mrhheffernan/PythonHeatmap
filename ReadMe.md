# PythonHeatmap

This is a simple way to visualize GPS data from Strava/Garmin/Polar in either the csv, fit, and/or gpx formats on an attractive and interactive interface.
This was a side-project while I helped organize the McGill Physics Hackathon.

If you are interested in physics or programming, hackathons are a great idea. If you're curious about more of my work, the linked pages at mrhheffernan.github.io provide links to more information.

## Getting Started

Download your data as a gpx, csv, or fit file from your provider of choice. Note that extra python packages may be required if you have fit files, as the binary files are not easily readable on all systems. Just download the python files here and run them! This is also written in to be compatible with Python 3.7, certain rewrites will be necessary if using Python2.


### Prerequisites

Certain Python modules are required. They are: numpy, pandas, geopy, folium, gpxpy, fitparse, and pytz. To download any and all of these in one fell swoop, the below code is provided.

```
pip install numpy pandas geopy folium gpxpy fitparse pytz
```

Also required prerequisites are GPS tracks. On Strava, these are available for bulk download under settings. If files have been uploaded via Garmin Connect, there may be compressed .fit files in .fit.gz format. To unzip these (at least in linux/unix-based systems):
```
gunzip *.fit.gz
```

## Running the tests

The heatmap will be output in a html file, which is viewable in a web browser. Currently, there is no native folium support for image exports, so screenshots of relevant areas is the recommended strategy.

The Python is designed to run in the same directory as the GPS files, so make sure this is the case.

## License

Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.

Original Python Copyright 2018 Matthew Heffernan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This code is by Matthew Heffernan.  As long as you retain this notice you
can do whatever you want with this stuff, subject to the conditions above.
If we meet some day, and you think this stuff is worth it, you can buy me a beer
in return.   - Matthew Heffernan

## Acknowledgements
This code is built with a combination of original and unlicensed code. Special thanks are due to the developers working to make the FIT file format more accessible, especially Max Candocia whose fit_to_csv code is instrumental and included here. Source: https://maxcandocia.com/article/2017/Sep/22/converting-garmin-fit-to-csv/

Additional thanks are due to the McGill Physics Hackathon 2018, during which I wrote this code while assisting many capable hackers visualize physics concepts. Their dedication and the unlimited coffee were inspirational to the development of this project.
