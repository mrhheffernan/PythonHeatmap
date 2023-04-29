import csv
import os

# to install fitparse, run
# sudo pip3 install -e git+https://github.com/dtcooper/python-fitparse#egg=python-fitparse
import fitparse
import pytz

allowed_fields = [
    "timestamp",
    "position_lat",
    "position_long",
    "distance",
    "enhanced_altitude",
    "altitude",
    "enhanced_speed",
    "speed",
    "heart_rate",
    "cadence",
    "fractional_cadence",
]
required_fields = ["timestamp", "position_lat", "position_long", "altitude"]

UTC = pytz.UTC
CST = pytz.timezone("US/Central")


def main():
    files = os.listdir()
    fit_files = [file for file in files if file[-4:].lower() == ".fit"]
    for file in fit_files:
        new_filename = file[:-4] + ".csv"
        if os.path.exists(new_filename):
            # print('%s already exists. skipping.' % new_filename)
            continue
        fitfile = fitparse.FitFile(
            file, data_processor=fitparse.StandardUnitsDataProcessor()
        )

        print("converting %s" % file)
        write_fitfile_to_csv(fitfile, new_filename)
    print("finished conversions")


def write_fitfile_to_csv(fitfile, output_file="test_output.csv"):
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
                    mdata[field.name] = UTC.localize(field.value).astimezone(CST)
                else:
                    mdata[field.name] = field.value
        for rf in required_fields:
            if rf not in mdata:
                skip = True
        if not skip:
            data.append(mdata)
    # write to csv
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(allowed_fields)
        for entry in data:
            writer.writerow([str(entry.get(k, "")) for k in allowed_fields])
    print("wrote %s" % output_file)


if __name__ == "__main__":
    main()
