import argparse
import csv
import glob
import os
from datetime import timezone
from zoneinfo import ZoneInfo

import fitparse

allowed_fields = [
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
required_fields = ["timestamp", "position_lat", "position_long"]

UTC = timezone.utc
TZ = ZoneInfo("US/Central")


def write_fitfile_to_csv(fitfile, output_path: str, tz: ZoneInfo = TZ):
    messages = fitfile.messages
    data = []
    for m in messages:
        skip = False
        if not hasattr(m, "fields"):
            continue
        fields = m.fields
        # check for important data types
        mdata = {}
        for field in fields:
            if field.name in allowed_fields:
                if field.name == "timestamp":
                    ts_value = field.value
                    if ts_value.tzinfo is None:
                        ts_value = ts_value.replace(tzinfo=UTC)
                    mdata[field.name] = ts_value.astimezone(tz)
                else:
                    mdata[field.name] = field.value
        for rf in required_fields:
            if rf not in mdata:
                skip = True
        if not skip:
            data.append(mdata)
    # write to csv
    with open(output_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(allowed_fields)
        for entry in data:
            writer.writerow([str(entry.get(k, "")) for k in allowed_fields])
    print("wrote %s" % output_path)


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

    fit_files = glob.glob(args.dir + "/*.fit")
    for file in fit_files:
        base_filename = file.removesuffix(".fit")
        new_filename = base_filename + ".csv"
        if not args.overwrite and os.path.exists(new_filename):
            # print('%s already exists. skipping.' % new_filename)
            continue
        fitfile = fitparse.FitFile(
            file, data_processor=fitparse.StandardUnitsDataProcessor()
        )

        print("converting %s" % file)
        write_fitfile_to_csv(fitfile, new_filename, tz=ZoneInfo(args.timezone))
    print("finished conversions")


if __name__ == "__main__":
    main()
