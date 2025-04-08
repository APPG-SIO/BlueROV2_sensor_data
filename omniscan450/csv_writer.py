# csv_writer.py

import csv
from svlog_parser import parse_svlog_file
import json
import argparse


def write_packets_to_csv(packets, output_filename):
    """
    Writes the packet data to a CSV file.
    
    Args:
        packets (list): A list of Packet objects to be written to the CSV file.
        output_filename (str): The name of the output CSV file.
    """
    fieldnames = [
        "Packet Position", "Message ID", "Message Type", "Sender ID", "Receiver ID",
        "Payload Data"
    ]

    with open(output_filename, mode="w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for packet in packets:
            # Prepare the row data from the packet object
            row = {
                "Packet Position": packet.pos,
                "Message ID": packet.payload.message_id,
                "Message Type": packet.payload.message_type,
                "Sender ID": packet.header.sender_id,
                "Receiver ID": packet.header.receiver_id,
                "Payload Data": json.dumps(packet.payload.__dict__, skipkeys=True)
            }
            writer.writerow(row)

    print(f"Data successfully written to {output_filename}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Parse an svlog file and write packets to a CSV file.")
    parser.add_argument("input_file", help="Path to the input svlog file.")
    parser.add_argument("output_file", help="Path to the output CSV file.")
    parser.add_argument("--included_ids", nargs="*", type=int, default=[], help="List of included IDs.")
    parser.add_argument("--excluded_ids", nargs="*", type=int, default=[], help="List of excluded IDs.")
    parser.add_argument("--max_packets", type=int, default=None, help="Maximum number of packets to process.")

    args = parser.parse_args()

    packets = parse_svlog_file(
        args.input_file,
        included_ids=args.included_ids,
        excluded_ids=args.excluded_ids,
        max_packets=args.max_packets
    )
    write_packets_to_csv(packets, args.output_file)
