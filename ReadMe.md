# PythonHeatmap

PythonHeatmap is a tool for visualizing GPS data from Strava, Garmin, Polar, and other fitness platforms in CSV, FIT, and/or GPX formats as interactive heatmaps.

## Features

- Supports GPX, and FIT file formats
- Interactive HTML heatmaps using Folium
- CLI arguments for customization
- Configurable timezone handling

## Getting Started

### Prerequisites

Python 3.13 or higher is required. Dependencies are managed automatically by uv - no installation required.

### Obtaining Data

Download GPS data from your fitness platform. For Strava, bulk exports are available under account settings. For Garmin Connect, compressed `.fit.gz` files may need to be extracted:

```bash
gunzip *.fit.gz
```

For automated downloading, `selenium_downloader.py` is provided. This requires:
- Selenium and Chromium configured
- A `login_info.secret` file containing `username,password,athlete_id`

Note: The selenium downloader may not export all historical data and is best suited for the most recent 12 months of activities. This script is not maintained or tested with updates to Strava's UI and may require adjustments to work with current Strava versions.

### Running

Run from the directory containing your GPS files:

```bash
uv run personal_heatmap.py
```

#### CLI Options

- `--dir`: Directory containing .fit and .gpx files (default: current directory)
- `--timezone`: Timezone for timestamps, e.g., 'US/Pacific' (default: 'US/Pacific')
- `--output_path`: Path for the output heatmap HTML file (default: 'heatmap.html')

For FIT to CSV conversion:

```bash
uv run fit_to_csv.py --dir /path/to/files --timezone US/Pacific
```

- `--overwrite`: Overwrite existing CSV files

For the simple matplotlib-based heatmap:

```bash
uv run simple_heatmap.py --dir /path/to/files --output_path output.png
```

## Output

The heatmap is generated as an HTML file viewable in any web browser. Use the interactive map controls to navigate and zoom to desired areas.

## License
Original Python Copyright 2018 Matthew Heffernan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgements

This code builds upon original work and tools for making the FIT file format more accessible. Special thanks to Max Candocia, whose fit_to_csv code is instrumental to this project. Source: https://maxcandocia.com/article/2017/Sep/22/converting-garmin-fit-to-csv/

Additional thanks to the McGill Physics Hackathon 2018, during which this project was developed while assisting participants with visualizing physics concepts.