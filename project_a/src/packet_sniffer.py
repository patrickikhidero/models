from scapy.all import sniff, IP
from .logger import logger

def packet_callback(packet):
    """Callback function for each captured packet."""
    if IP in packet:
        logger.info(f"Source IP: {packet[IP].src}, Destination IP: {packet[IP].dst}")

def start_sniffing(interface='eth0', count=0):
    """Start capturing packets."""
    try:
        logger.info(f"Starting sniff on {interface}")
        sniff(iface=interface, store=0, prn=packet_callback, count=count)
    except PermissionError:
        logger.error("Sniffing requires root privileges.")
    except Exception as e:
        logger.error(f"Sniffing error: {e}")

# Usage
# start_sniffing()