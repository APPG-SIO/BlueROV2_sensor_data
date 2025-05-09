# README_ping

### Useful links:
- [Blue Robotics - Access ping360 data for post processing](https://discuss.bluerobotics.com/t/access-ping360-data-for-post-processing-python/10416/2)
      

## Overview

This will walk you through how to parse .bin files from the Ping360 and Ping 1D (Echosounder/altimeter) into readable .csv files. You are going to need to make sure you are running a python system of atleast 3.11 (I think)

### Download the following files
Note that the first file is from Blue Robotic's ping-viewer repository, **not** in this ping folder
- [decode_sensor_binary_log.py](https://github.com/bluerobotics/ping-viewer/blob/master/examples/decode_sensor_binary_log.py)
- [decodePing1D_2csv.py](decodePing1D_2csv.py)
- [decodePing360_2csv.py](decodePing360_2csv.py)
- [folderLoop.py](folderLoop.py)


Make sure the files you just downloaded are all in the **same** folder, otherwise they will not be able to find each other with the existing code.
    
    

### ⚠️ If you have ping1D and ping360 files together in a folder, you can sort them using the following python script:
- [sortPingFiles.py](sortPingFiles.py)

Open it in your favorite text editor. *You’ll need to change the paths to the folders in the script after you download,* (it currently has my folder paths).
Run the code however you typically like to run python files
    

# Ping 360
### To process a single 360 .bin file into a .csv

1. In your terminal, navigate to the folder with the files you just downloaded
2. Enter the following into your terminal

```bash
python3 decodePing360_2csv.py path/to/binfile.bin -o path/to/csvfilename.csv
```

### To process multiple 360 .bin files into .csv’s

1. Navigate to the folder with the files you just downloaded
2. Enter the following into your terminal (It will put all of the csv’s into an adjacent folder to the bin folder, called csv)

```bash
cpython3 folderLoop.py path/to/folder/with/bin/files --script decodePing360_2csv.py
```

### You should get a CSV formatted like this:
<img width="1361" alt="Screenshot 2025-03-17 at 12 45 53 PM" src="https://github.com/user-attachments/assets/ddce93e7-889d-4001-b0fc-55b41d24e2d4" />


# Ping 1D
### To process a single ping1D .bin file into a .csv

1. In your terminal, navigate to the folder with the files you just downloaded
2. Enter the following into your terminal

```bash
python3 decodePing1D_2csv.py path/to/binfile.bin -o path/to/csvfilename.csv
```

### To process multiple ping .bin files into .csv’s

1. Navigate to the folder with the files you just downloaded
2. Enter the following into your terminal (It will put all of the csv’s into an adjacent folder to the bin folder, called csv)

```bash
python3 folderLoop.py path/to/folder/with/bin/files --script decodePing1D_2csv.py
```

### You should get a CSV formatted like this:
<img width="1029" alt="Screenshot 2025-03-21 at 3 41 27 PM" src="https://github.com/user-attachments/assets/e96b05ea-2e1e-4aab-b4f0-bfb85231e078" />

