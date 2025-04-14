import re
import struct

# ================================================================
# Section: Defining struct format codes for unpacking binary data
# ================================================================

U8 = "B"  # Unsigned 8-bit integer
U16 = "H"  # Unsigned 16-bit integer
U32 = "I"  # Unsigned 32-bit integer
FLOAT = "f"  # 4-byte float
CHAR = "s"  # 1-byte character

"""
    Important notes:

        1.  To represent an array, place the code between brackets:

                [U16].......indicates an array of unsigned 16-bit integers
                [CHAR]......indicates an array of characters (i.e a string).

            If you know the length of the array, you can specify it as well:

                [U16]*2.....indicates an array of exactly two unsigned 16-bit integers

            Otherwise the length will be dynamically determined based on the amount of available data 
            remaining in the payload. Note that this means that the array must come at the end of the payload.
            Note too that you cannot pre-indicate an array of only one element.  If you want one,
            include it as a single element (e.g. U16) instead of an array (e.g. [U16] or [U16]*1).
        
        2.  A string is represented as [CHAR] in the format dictionary 
            (but don't worry, it will be unpacked as a normal string).
"""

# ===================================================================
# Section: Defining function to unpack binary data of a given format
# ===================================================================

def unpack_from_format(format_dict, data):
    """
    Unpack binary data into usable form based on the provided format dictionary.

    Args:
        format_dict: A dictionary mapping attribute names to struct format codes or arrays thereof.
        data: The binary data to unpack.

    Returns:
        dict: The unpacked data, in {attribute_name : extracted_value} pairs
    """
    unpacked_data = {}
    pos = 0
    for attribute_name, format_code in format_dict.items():

        if isinstance(format_code, list):
            data_type = format_code[0]  # Assume all elements are the same type
            # If the array only has one value, assume you're supposed to fill it with the rest of the data 
            if len(format_code) == 1:
                length = (len(data) - pos) // struct.calcsize(data_type)
            # Otherwise, assume the correct length has been specified
            else:
                length = len(format_code)
            
            fmt = '<' + f"{length}{data_type}"
            size = struct.calcsize(fmt)
            try:
                # Attempt to unpack the data
                value = struct.unpack(fmt, data[pos:pos+size])
            except struct.error as e:
                raise ValueError(f"Error unpacking data with length {len(data[pos:pos+size])} at position {pos}: {e}")
            if data_type == CHAR:
                # The value is a string
                value = value[0].decode('ascii').rstrip("\x00")
            else:
                # The value is a true array 
                value = list(value)
        else:
            fmt = '<' + format_code
            size = struct.calcsize(fmt)
            value = struct.unpack(fmt, data[pos:pos+size])[0]

        unpacked_data[attribute_name] = value
        pos += size
    
    if pos != len(data) or len(unpacked_data) != len(format_dict):
        raise ValueError(f"Format does not match data size: {len(data)} bytes")
    return unpacked_data


# ===============================================================
# Section: Defining classes to represent Ping Protocol messages
# ===============================================================

class Header:
    """
    Class to represent a packet header (including initial 'BR').
    
    Args:
        header_data: The 8-byte binary data that will be translated into usable form
            and loaded into the attributes defined in FORMAT.  For details on the 
            Ping Protocol header format, see https://docs.bluerobotics.com/ping-protocol/ 
    """

    FORMAT = {
        "br": [CHAR]*2,
        "payload_length": U16,  # Two bytes for an integer representing the payload length (in bytes)
        "message_id": U16,      # Two bytes for an integer representing the message ID (the message type)
        "sender_id": U8,        # One byte for an integer representing the sender ID (typically 1 or 2 for the sidescan sonars)
        "receiver_id": U8,      # One byte for an integer representing the receiver ID (typically 0 for the topside computer)
    }
    
    def __init__(self, header_data):
        # Translate the binary data into usable form, and load it into this object's attributes
        unpacked_data = unpack_from_format(self.FORMAT, header_data)
        for attribute, value in unpacked_data.items():
            setattr(self, attribute, value)

        # Make sure the first two bytes are 'BR'
        if self.br != 'BR':
            raise ValueError(f"Invalid header signature: {self.br}")
    
    def __repr__(self):
        return f"Header(br='{self.br}', payload_length={self.payload_length}, message_id={self.message_id}, sender_id={self.sender_id}, receiver_id={self.receiver_id})"


class Payload:
    """
    Base class for all payload messages.
    
    To instantiate, use Payload.create(message_id, payload_data) instead of Payload().
    These will return an object from the appropriate message subclass (e.g. NackMessage 
    or OsMonoProfileMessage), with all of the attributes automatically unpacked from the
    binary data and saved in the object.

    Example usage:
        payload = Payload.create(message_id=2198, payload_data)
        print("Ping number is", payload.ping_number)
        print("Ping frequency is", payload.ping_hz)

    To recap: any attribute included in the format dictionary of the relevant subclass
    will be saved in the Payload object as an attribute of the SAME NAME.
    """

    @staticmethod
    def create(message_id, payload_data):
        """Factory method to instantiate the correct subclass."""
        # Check if the message ID exists in the registry
        if message_id in MESSAGE_REGISTRY:
            # Create an instance of the appropriate message type
            return MESSAGE_REGISTRY[message_id](payload_data)
        else:
            return Payload(payload_data, message_id)  # Default to base class
            
    def __init__(self, payload_data, message_id, message_type="Unknown message type", format=None):
        self.length = len(payload_data)  # In bytes
        self.message_id = message_id 
        self.message_type = message_type
        if format is not None:
            # Translate the binary data into usable form, and load it into this object's attributes
            unpacked_data = unpack_from_format(format, payload_data)
            for attribute, value in unpacked_data.items():
                setattr(self, attribute, value)
    
    def __repr__(self):
        attrs = ", ".join(
            f"{key}='{value}'" if isinstance(value, str) else
            f"{key}=[{len(value)} values]" if isinstance(value, (list, tuple, dict)) else
            f"{key}={value}"
            for key, value in vars(self).items()
        )
        return f"{self.__class__.__name__}({attrs})"


class Packet:
    """
    Class to represent a packet (header + payload + checksum).
    
    Args:
        pos: The header start index within the provided data.
        data: The data that contains the packet.
    """

    def __init__(self, pos, data):
        self.pos = pos
        self.header = Header(data[pos:pos + 8])

        if len(data) - pos < 8 + self.header.payload_length + 2:
            raise ValueError(f"Not enough data for full packet at position {pos} with header {self.header}")
        
        self.checksum = struct.unpack("<H", data[pos + 8 + self.header.payload_length : pos + 8 + self.header.payload_length + 2])[0]
        self.corrupted = self.checksum != self.compute_checksum(data, pos, self.header.payload_length)
        
        if not self.corrupted:
            try:
                self.payload = Payload.create(self.header.message_id, data[pos + 8 : pos + 8 + self.header.payload_length])
            except struct.error as e:
                raise ValueError(f"Error unpacking payload for message with header {self.header}: {e}")
        else:
            self.payload = None

    def compute_checksum(self, data, pos, payload_length):
        """Compute checksum by summing header + payload (excluding checksum)."""
        packet_data = data[pos:pos + 8 + payload_length]  # Header + Payload
        return sum(packet_data) & 0xFFFF  # Truncate to 16 bits
    
    @classmethod
    def from_bytes(cls, pos, data):
        header = Header(data[pos:pos + 8])
        if header.message_id not in MESSAGE_REGISTRY:
            return None
        return cls(pos, data)

    def __repr__(self):
        return f"Packet(header={self.header}, payload={self.payload}, checksum={self.checksum})"
    

# ================================================
# Section: Defining Ping Protocol message types
# ================================================

MESSAGE_REGISTRY = {}

def register(cls):
    MESSAGE_REGISTRY[cls.MESSAGE_ID] = cls
    return cls

@register
class NackMessage(Payload):
    """Subclass for message ID 2, representing a NACK (not acknowledged) message."""

    MESSAGE_ID = 2
    MESSAGE_TYPE = "Not acknowledged"
    FORMAT = {
        "nacked_id": U16,  # Two bytes for the message ID that was not acknowledged
        "nack_message": [CHAR]  # Remaining bytes as ASCII text indicating NACK condition
    }
    
    def __init__(self, payload_data):
        super().__init__(payload_data, message_id=self.MESSAGE_ID, 
                         message_type=self.MESSAGE_TYPE, format=self.FORMAT)
    

@register
class JSONMessage(Payload):
    """Subclass for message ID 10, representing a JSON header message."""
    
    MESSAGE_ID = 10
    MESSAGE_TYPE = "JSON header"
    FORMAT = {
        "JSON_message": [CHAR]  # Remaining bytes as ASCII text giving JSON header message
    }
    
    def __init__(self, payload_data):
        super().__init__(payload_data, message_id=self.MESSAGE_ID, 
                         message_type=self.MESSAGE_TYPE, format=self.FORMAT)
    

@register
class OsMonoProfileMessage(Payload):
    """Subclass for message ID 2198, representing an os_mono_profile message for the Omniscan 450."""
    
    MESSAGE_ID = 2198
    MESSAGE_TYPE = "Omniscan 450 Mono Profile"
    FORMAT = {
        "ping_number": U32,         # Sequentially assigned from 0 at power up
        "start_mm": U32,            # The beginning of the scan region in mm from the transducer
        "length_mm": U32,           # The length of the scan region in mm
        "timestamp_ms": U32,        # Timestamp in milliseconds since power-up
        "ping_hz": U32,             # Frequency of the acoustic signal in Hz
        "gain_index": U16,          # Gain index (0-7)
        "num_results": U16,         # Length of pwr_results array
        "sos_dmps": U16,            # Speed of sound, decimeters/sec	
        "channel_number": U8,
        "reserved": U8,
        "pulse_duration_sec": FLOAT,
        "analog_gain": FLOAT,
        "max_pwr_db": FLOAT,
        "min_pwr_db": FLOAT,
        "transducer_heading_deg": FLOAT,
        "vehicle_heading_deg": FLOAT,	
        "pwr_results": [U16]     # An array of return strength measurements taken 
                                    # at regular intervals across the scan region. 
                                    # The first element is the closest measurement to the sensor, 
                                    # and the last element is the farthest measurement in the scanned range. 
                                    # Power results scaled from min_pwr_db to max_pwr_db.
                                    # Length is derived from payload_length in the header.	
    }
    
    def __init__(self, payload_data):
        super().__init__(payload_data, message_id=self.MESSAGE_ID, 
                         message_type=self.MESSAGE_TYPE, format=self.FORMAT)


@register
class ImplementYourOwnMessage(Payload):
    """Subclass for your custom message ID, representing a custom message."""
    # Note: you must also include @register above this class definition to place it in the MESSAGE_REGISTRY.

    MESSAGE_ID = 99999  # Replace with your custom message ID
    MESSAGE_TYPE = "Your custom message type"
    FORMAT = {
        "your_field1": U16,  # e.g. Two bytes for your custom field 1
        "your_field2": U8,   # e.g. One byte for your custom field 2
        "your_message": [CHAR]  # e.g. Remaining bytes as ASCII text giving your custom message data
    }
    
    # No need to change __init__ at all!
    def __init__(self, payload_data):
        super().__init__(payload_data, message_id=self.MESSAGE_ID, 
                         message_type=self.MESSAGE_TYPE, format=self.FORMAT)
        
    
# ==========================================================================
# Section: Defining function to extract message packets from a .svlog file!
# ==========================================================================

def parse_svlog_file(filename, included_ids=None, excluded_ids=None, max_packets=None):
    """
    Parse a .svlog file and extract message packets.
    Note: this function will only extract packets of known message types.
    """
    with open(filename, "rb") as f:
        data = f.read()  # Read the entire binary file

    pattern = re.compile(rb"\x42\x52")  # Match "BR"
    positions = [match.start() for match in pattern.finditer(data)]

    packets = []
    for pos in positions:  
        try:
            packet = Packet.from_bytes(pos, data)
            if packet is None:
                continue
            if included_ids is not None and packet.header.message_id not in included_ids:  # Only include wanted message IDs
                continue
            if excluded_ids is not None and packet.header.message_id in excluded_ids:  # Don't include unwanted message IDs
                continue
            if packet.corrupted:
                print(f"Invalid checksum for packet at byte {pos}")
                continue
            packets.append(packet)
            if max_packets is not None and len(packets) == max_packets:  # Cap the number of packets included in the output
                break
        except ValueError as e:
            print(f"Error parsing packet at byte {pos}: {e}")
    
    return packets



if __name__ == "__main__":
    # Example usage
    filename = "2025-03-24-12-14.svlog"  # Replace with your binary file
    packets = parse_svlog_file(filename)
    
    output_filename  = "message_log.txt"  # Output file name 
    with open(output_filename, "w") as output_file:
        output_file.truncate(0)  # Erase the file content before writing
        output_file.write(f"Message logs:\n\n")
        for packet in packets:
            output_file.write(f"Packet at byte {packet.pos}:\n")
            output_file.write(f"  Header: {packet.header}\n")
            output_file.write(f"  Payload: {packet.payload}\n")
            output_file.write(f"  Checksum: {packet.checksum}\n")
            output_file.write(f"  Corrupted: {packet.corrupted}\n\n")
