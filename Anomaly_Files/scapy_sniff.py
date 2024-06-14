import os
import sys

current_dir = os.path.dirname(__file__)

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    
import pandas as pd
from scapy.all import sniff
from scapy.layers.inet import IP, TCP
from process_cap_df import process_packet_capture_data
import psutil

# Function to extract required fields from each packet
def extract_fields(packet):
    if IP in packet and TCP in packet:
        flags = packet.sprintf('%TCP.flags%')
        return {
            'frame.time_relative': packet.time,
            'ip.proto': packet[IP].proto,
            'tcp.flags': flags,
            'ip.len': len(packet[IP]),
            'tcp.srcport': packet[TCP].sport,
            'tcp.dstport': packet[TCP].dport,
            'tcp.flags.reset': 'R' in flags,  # RST flag
            'tcp.flags.syn': 'S' in flags,    # SYN flag
            'ip.frag_offset': packet[IP].frag,
            'tcp.urgent_pointer': packet[TCP].urgptr
        }
    else:
        return None

# Function to map tcp.flags to the provided textual representation
def map_flags(tcp_flags):
    flag_mapping = {
        'R': 'REJ',
        'SA': 'S2',
        'S': 'S0',
        'FA': 'SF',
        'RA': 'RSTR',
        'F': 'SH',
        'SAE': 'S3',  # Assuming SAE as S3
        'PA': 'OTH',  # Example: PA can be considered as OTH (not directly mapped)
        '': 'OTH'  # Any other combination
    }

    # Combine all possible flag combinations into their corresponding textual representation
    if 'R' in tcp_flags and 'S' in tcp_flags:
        return 'RSTOS0'
    if 'R' in tcp_flags and 'A' in tcp_flags:
        return 'RSTR'
    if 'R' in tcp_flags:
        return 'REJ'
    if 'S' in tcp_flags and 'F' in tcp_flags:
        return 'SH'
    if 'S' in tcp_flags and 'A' in tcp_flags:
        return 'S2'
    if 'S' in tcp_flags:
        return 'S0'
    if 'F' in tcp_flags and 'A' in tcp_flags:
        return 'SF'
    if 'F' in tcp_flags:
        return 'SH'
    if 'S' in tcp_flags and ('E' in tcp_flags or 'C' in tcp_flags):
        return 'S3'
    return flag_mapping.get(tcp_flags, 'OTH')

def get_interface_names():
    # Retrieve the network interface addresses
    net_if_addrs = psutil.net_if_addrs()
    
    # Extract the interface names
    interface_names = list(net_if_addrs.keys())
    
    return interface_names

# List to store packet data
packet_data = []

# Packet handler function
def packet_handler(packet):
    fields = extract_fields(packet)
    if fields:
        fields['tcp.flags.mapped'] = map_flags(fields['tcp.flags'])
        packet_data.append(fields)

# Capture packets (example capturing 50 packets)
sniff(iface='', prn=packet_handler, filter='ip', count=50)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(packet_data)

