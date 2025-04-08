# IMU Data

**This page explains how to extract MAVLINK messages and data**

The IMU data we currently have is in .tlog file format, which are output from QGroundControl. The data is pulled by ArduSub, which is a branch of ArduPilot — firmware that runs on the onboard computer and helps with control of the ROV. 

https://www.ardusub.com/reference/data-logging.html

- Dataflash logs are in .bin format and can be downloaded from QGroundControl>Logs. They store higher frequency data, using GPS for time sync
- The .tlog files contain all of the MAVLink messages received in their binary format

## Set up *(if you need to decode the .tlog files)*

Go to command line and install pymavlink (make sure you have pip)

```bash
pip install pymavlink
```

Make sure you know where [mavlogdump.py](http://mavlogdump.py), which is installed with pymavlink, is in you computer. If you are unsure where it is, run the following:

```bash
find ~/.local -name "mavlogdump.py"
```

It should return the file path for [mavlogdump.py](http://mavlogdump.py). Add the file path, up to the folder that mavlogdump.py is in, to your path. To add it permanently to your path, you can run the following. NOTE: this works on my machine (macOS Sequoia 15) because it uses zsh. You might have bash if you have an older mac. Not sure how this works on windows but you can easily Google how. 

```bash
echo 'export PATH=/path/to/enclosing/folder:$PATH' >> ~/.zshrc # to put this in your terminal path file
source ~/.zshrc # to save changes
```

## Instructions to decode the .tlog file to .csv

To run the file, just type [mavlogdump.py](http://mavlogdump.py) with the appropriate flags, file paths, and options following it. Here are some relevant examples

```bash
mavlogdump.py -h # This will tell you more about the file's options
mavlogdump.py path/to/tlog/file --show-types  # Will tell you the data columns that the tlog file has
mavlogdump.py --format csv --types TIMESYNC,RAW_IMU,ATTITUDE,SCALED_IMU2,GPS_RAW_INT,GLOBAL_POSITION_INT  path/to/file.tlog > output/path/file.csv #This will put out these types into an output .csv file  
```

these are the data columns that the .tlog files are able to put out (that I’ve seen):

```
GIMBAL_DEVICE_ATTITUDE_STATUS
RAW_IMU
VIBRATION
COMMAND_LONG
BATTERY_STATUS
MISSION_ACK
AHRS
PARAM_VALUE
STATUSTEXT
MANUAL_CONTROL
NAMED_VALUE_FLOAT
HEARTBEAT
ATTITUDE
MEMINFO
AHRS2
MISSION_COUNT
AUTOPILOT_VERSION
SCALED_PRESSURE
TIMESYNC
SCALED_PRESSURE2
MISSION_REQUEST_LIST
VFR_HUD
NAV_CONTROLLER_OUTPUT
POWER_STATUS
SERVO_OUTPUT_RAW
SCALED_IMU2
COMMAND_ACK
SYSTEM_TIME
RANGEFINDER
REQUEST_DATA_STREAM
GPS_RAW_INT
GLOBAL_POSITION_INT
EKF_STATUS_REPORT
PARAM_REQUEST_LIST
RC_CHANNELS
DISTANCE_SENSOR
MISSION_CURRENT
SYS_STATUS
```

## Running multiple files

To run multiple files, you can run the following code, modifying the --types you want, and the input and output folders
```python
import os
import subprocess

# Set your input and output folder paths
INPUT_FOLDER = "path/to/tlog/files"
OUTPUT_FOLDER = "path/to/output/csv"

# Ensure the output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Find all .tlog files in the input directory
tlog_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".tlog")]

# Path to mavlogdump.py (if not in PATH, set the full path here)
MAVLOGDUMP_CMD = "mavlogdump.py"

# Process each .tlog file
for tlog_file in tlog_files:
    input_file_path = os.path.join(INPUT_FOLDER, tlog_file)
    output_file_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(tlog_file)[0]}.csv")

    # Run mavlogdump.py to convert the file
    command = [
        MAVLOGDUMP_CMD,
        "--format", "csv",
        "--types", "TIMESYNC,RAW_IMU,ATTITUDE,SCALED_IMU2",
        input_file_path
    ]

    try:
        with open(output_file_path, "w") as output_file:
            subprocess.run(command, stdout=output_file, check=True)
        print(f"Successfully converted: {tlog_file} -> {output_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {tlog_file}: {e}")
```

## Interpreting the files
[See this MAVLINK page](https://mavlink.io/en/messages/common.html)
