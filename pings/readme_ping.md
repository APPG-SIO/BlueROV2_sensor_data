# readme_ping

### Useful links:
- [Blue Robotics - Access ping360 data for post processing](https://discuss.bluerobotics.com/t/access-ping360-data-for-post-processing-python/10416/2)
- 

## Overview

This will walk you through how to parse .bin files from the Ping360 and Ping 1D (Echosounder/altimeter) into readable .csv files. You are going to need to make sure you are running a python system of atleast 3.11 (I think)

### Download the following files


Make sure the files you just downloaded are all in the **same** folder, otherwise they will not be able to find each other with the existing code.

⚠️ **if you have ping1D and ping360 files together in a folder, you can sort them using the following python script.**

- You’ll need to change the paths to the folders in the script after you download, it currently has my folder paths
- Run the code however you typically like to run python files

# Ping 360
### To process a single 360 .bin file into a .csv

1. In your terminal, navigate to the folder with the files you just downloaded
2. Enter the following into your terminal

```bash
python3 decodePing360_2csv.py path/to/binfile.bin -o path/to/csvfilename.csv
```

### To process multiple 360 .bin files into .csv’s

1. Navigate to the folder with the files you just downloaded
2. Enter the following into your terminal
    1. It will put all of the csv’s into an adjacent folder to the bin folder, called csv

```bash
cpython3 folderLoop.py path/to/folder/with/bin/files --script decodePing360_2csv.py
```

### You should get a CSV formatted like this:
<img width="1361" alt="Screenshot 2025-03-17 at 12 45 53 PM" src="https://github.com/user-attachments/assets/ddce93e7-889d-4001-b0fc-55b41d24e2d4" />


# Ping 1D
