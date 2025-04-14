import csv
import json
import argparse

def process_payload_data(input_csv, output_csv):
    decoded_data = []

    # Open and read the large CSV file.
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Convert the Message ID and Sender ID to integers for comparison.
                message_id = int(row.get("Message ID", -1))
                sender_id = int(row.get("Sender ID", -1))
            except ValueError:
                # If conversion fails, skip the row.
                continue

            # Filter on Message ID = 2198 and Sender ID = 2.
            if message_id == 2198 and sender_id == 1:
                payload_text = row.get("Payload Data", "").strip()
                if payload_text:
                    try:
                        # Decode the payload JSON text.
                        payload_dict = json.loads(payload_text)
                        decoded_data.append(payload_dict)
                    except json.JSONDecodeError as e:
                        print(f"Skipping row with invalid JSON payload: {payload_text}\nError: {e}")

    if not decoded_data:
        print("No matching rows with valid JSON payload were found.")
        return

    # Gather all column headers from all decoded payloads.
    headers = set()
    for entry in decoded_data:
        headers.update(entry.keys())
    headers = sorted(list(headers))  # Sorted for consistency

    # Write out the new CSV file with decoded payload data.
    with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers)
        writer.writeheader()
        for entry in decoded_data:
            row_to_write = {}
            for key in headers:
                value = entry.get(key, "")
                # If the value is a list (or any non-primitive), convert it to a JSON string.
                if isinstance(value, list):
                    row_to_write[key] = json.dumps(value)
                else:
                    row_to_write[key] = value
            writer.writerow(row_to_write)

    print(f"New CSV with decoded payload data has been written to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract and decode the 'Payload Data' JSON from rows with Message ID 2198 and Sender ID 1 into a new CSV."
    )
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to the output CSV file where decoded payloads will be written")
    args = parser.parse_args()
    process_payload_data(args.input_csv, args.output_csv)
