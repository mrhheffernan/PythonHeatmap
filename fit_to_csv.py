import argparse
import csv
import glob
import os
from datetime import timezone
from typing import Any
from zoneinfo import ZoneInfo

import fitparse

FIELDS_ALLOWED = [
    "timestamp",
    "position_lat",
    "position_long",
    "distance",
    "enhanced_altitude",
    "altitude",
    "enhanced_speed",
    "speed",
    "avg_heart_rate",
    "heart_rate",
    "cadence",
    "fractional_cadence",
]
FIELDS_REQUIRED = ["timestamp", "position_lat", "position_long"]

UTC = timezone.utc
TZ = ZoneInfo("US/Pacific")


def write_to_csv(data: list[dict[str, Any]], output_path: str) -> None:
    """Write extracted data fields from the .fit messages to file

    Args:
        data (list[dict[str, Any]]): Data from messages
        output_path (str): Output path
    """
    # write to csv
    with open(output_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDS_ALLOWED)
        for entry in data:
            writer.writerow([str(entry.get(k, "")) for k in FIELDS_ALLOWED])
    print("wrote %s" % output_path)


def collect_data(filepath: str, tz: ZoneInfo = TZ) -> list[dict[str, Any]]:
    """Collects data from the .fit file at filepath

    Args:
        filepath (str): Path to .fit file
        tz (ZoneInfo, optional): Timezone identifier. Defaults to TZ.

    Returns:
        list[dict[str, Any]]: List of dicts containing relevant data from each message in the .fit
    """
    # Parse the .fit file
    fitfile = fitparse.FitFile(
        filepath, data_processor=fitparse.StandardUnitsDataProcessor()
    )

    data = []
    messages = fitfile.messages

    for m in messages:
        skip = False
        if not hasattr(m, "fields"):
            continue
        fields = m.fields

        # check for desired data and collect it
        mdata = {}
        for field in fields:
            if field.name in FIELDS_ALLOWED:
                if field.name == "timestamp":
                    timestamp_value = field.value
                    if timestamp_value.tzinfo is None:
                        timestamp_value = timestamp_value.replace(tzinfo=UTC)
                    mdata[field.name] = timestamp_value.astimezone(tz)
                else:
                    mdata[field.name] = field.value

        for required_field in FIELDS_REQUIRED:
            if required_field not in mdata:
                skip = True

        if not skip:
            data.append(mdata)

    return data


def parse_args() -> argparse.Namespace:
    args = argparse.ArgumentParser(description="Convert .fit to .csv")

    args.add_argument(
        "--dir",
        help="Path to directory containing .fit files",
        type=str,
        default=os.getcwd(),
    )
    args.add_argument(
        "--timezone",
        help="Timezone for timestamps, e.g. 'US/Pacific'",
        default="US/Pacific",
    )
    args.add_argument(
        "--overwrite",
        help="Overwrite any .csv files already converted from .fit",
        action="store_true",
    )

    return args.parse_args()


def main():
    args = parse_args()

    # Identify .fit files
    fit_files = glob.glob(args.dir + "/*.fit")

    for file in fit_files:
        # Use the same filename, just change extension to .csv
        base_filename = file.removesuffix(".fit")
        new_filename = base_filename + ".csv"
        if not args.overwrite and os.path.exists(new_filename):
            continue

        print("converting %s" % file)
        data = collect_data(file, tz=ZoneInfo(args.timezone))
        write_to_csv(data, new_filename)

    print("finished conversions")


if __name__ == "__main__":
    main()
