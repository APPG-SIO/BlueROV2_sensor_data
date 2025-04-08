# README_omniscan450
**The following will walk through how to process the .svlog files which contain side scan sonar data.**

*Note: the existing documentation online for how to do this was poor, so extra time and care was spent getting this into a format so anyone who wants to process .svlogs can do so on their own, regardless of their technical prowess.*

### Relevant links:

- [Application Programming Interface | Cerulean Sonar Docs](https://docs.ceruleansonar.com/c/omniscan-450/application-programming-interface)
- [Cerulean Standard Packet Protocol | Cerulean Sonar Docs](https://docs.ceruleansonar.com/c/cerulean-ping-protocol)
- [Ping Protocol](https://docs.bluerobotics.com/ping-protocol/)

## Overview & explanation

All the hard work has been done for you here. If you want to, you could download the files below and follow the instructions and get your svlog turned into something readable in no time. However, if you want to do something else with the svlog files, or understand a bit better what is going on under the hood, you can take this adventure a little further and learn a bit more. Mostly, this page hopes to provide you with working tools and instructions to understand and decode svlog files. In other words: **SVLOG for dummies**. 

### Download the following files
- [csv_writer.py](csv_writer.py)
- [svlog_parser.py](svlog_parser.py)

## Using the files above is simple enough
In terminal, navigate to the folder containing the files you just downloaded and you can run csv_writer.py, which calls on svlog_parser.py with the following line of code

```bash
python3 csv_write.py -h #tells you the argument options, but for easiness' sake I'll tell you here
# If you want to constrain the parsing to only certain message types (2, 10, 2198 are the desirable ones it turns out) then you can do that with --included_IDs
# (and the opposite for IDs you don't want with --excluded_IDs)
# if you only want the first 10 messages, you can include that after --max_packets

# The following is a full example of what you might type
python3 csv_write.py --included_IDs 2,10,2198 --max_packets 100 path/to/input_file.svlog path/to/output_file.csv
```


# :construction: the rest of this page is under construction for now
