# README_omniscan450
**The following will walk through how to process the .svlog files which contain side scan sonar data.**

*Note: the existing documentation online for how to do this was poor, so extra time and care was spent getting this into a format so anyone who wants to process .svlogs can do so on their own, regardless of their technical prowess.*

### Relevant links:

- [Application Programming Interface | Cerulean Sonar Docs](https://docs.ceruleansonar.com/c/omniscan-450/application-programming-interface)
- [Cerulean Standard Packet Protocol | Cerulean Sonar Docs](https://docs.ceruleansonar.com/c/cerulean-ping-protocol)
- [Ping Protocol](https://docs.bluerobotics.com/ping-protocol/)

## Overview & explanation

All the hard work has been done for you here. If you want to, you could download the files below and follow the instructions and get your svlog turned into something readable in no time. However, if you want to do something else with the svlog files, or understand a bit better what is going on under the hood, you can take this adventure a little further and learn a bit more. Mostly, this page hopes to provide you with working tools and instructions to understand and decode svlog files. In other words: **SVLOG for dummies**. 

### What is an .svlog?
It is a binary file in a format created by Cerulean Sonar, which is similar to (but not the same as) the Ping Protocol format developed by Blue Robotics. It is simply a record of all of the messages that the Omniscan450s and computer send to eachother during the recorded data session. There are tons of message types; the messages are not just data. So, you have to do some sifting. 

### Download the following files
- [csv_writer.py](csv_writer.py)
- [svlog_parser.py](svlog_parser.py)
- [decode_payload_csv.py](decode_payload_csv.py)

## Using the files above is simple enough

[svlog_parser.py](svlog_parser.py) is doing the heavy lifting here. It takes the binary svlog files and outputs all the instances of a message type (or types) that you ask it to between the omniscan450(s) and the computer to a text file. If you would like a text file, you can run this code directly in something like Visual Studio code and change the input file name at the very bottom of the script under main to the script you would like it to parse. The script is currently configured to output the text file to message_logs.txt. You can change this too.

If you would like a csv of the messages, you can run [csv_writer.py](csv_writer.py) from the terminal, which calls on svlog_parser.py with the following line of code

```bash
python3 csv_write.py -h #tells you the argument options, but for easiness' sake I'll tell you here
# If you want to constrain the parsing to only certain message types (2, 10, 2198 are the desirable ones it turns out) then you can do that with --included_IDs
# (and the opposite for IDs you don't want with --excluded_IDs)
# if you only want the first 10 messages, you can include that after --max_packets

# The following is a full example of what you might type. This gives all the informational header (message 10) and SSS data (message 2198) for your entire svlog file into a large csv
python3 csv_write.py path/to/input_file.svlog path/to/output_file.csv --included_IDs 10 2198
```

Now, this might be all you need to do! If so, congrats. You may read no further. *However,* if you would like to either decode further and/or understand what the code is doing better, stay the course.

## Decoding further
The file that you should have now is pretty good. It tells you...
- Packet Position: tells you what byte number the packet (message) was found at
- Message ID: tells you what type of message it is. The ones we mostly care about are 10 and 2198.
- Message Type: tells you what type of information the payload contains
- Sender ID: tells you which device sent the message (if you have more than one sonar device hooked up, this will be relevant)
- Receiver ID: tells you which device recieves the message (should be 0, which means the computer is recieving it)
- Payload Data: is the raw message, contains relevant data and time stamps etc.

It is likely you want to decode the payload even more. *If you care about 2198 (data) messages, then you can continue with the following code:*


You can use [decode_payload_csv.py](decode_payload_csv.py) to extract the data messages further. Open the file in your favorite text editor (I use Visual Studio Code) and edit the code to suit your needs. Right now it is configured to only look and decode the payload for rows in which the Message_ID is 2198 and Sender_ID is 2. *It is likely you will need to change these parameters!* If you have just one Omniscan450, then you will likely only have Sender_ID = 1. To use this file go to your terminal and type something like the following:

```bash
python3 decode_payload_csv.py path/to/input.csv path/to/output_csv_payload_extracted.csv
```



## :construction: the rest of this page is under construction for now
