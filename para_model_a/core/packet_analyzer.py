from scapy.all import sniff, IP, TCP, UDP
import logging
from utils.logger import setup_logger

logger = setup_logger('packet_analyzer')

def analyze_packet(packet):
    if packet.haslayer(TCP):
        logger.info(f"TCP Packet from {packet[IP].src} to {packet[IP].dst}")
    elif packet.haslayer(UDP):
        logger.info(f"UDP Packet from {packet[IP].src} to {packet[IP].dst}")
    else:
        logger.debug(f"Other type of packet: {packet.summary()}")

def capture_packets(interface, count=10):
    logger.info(f"Starting packet capture on {interface}")
    try:
        sniff(iface=interface, store=False, prn=analyze_packet, count=count)
    except PermissionError:
        logger.error("Packet sniffing requires root privileges.")
    except Exception as e:
        logger.error(f"An error occurred during packet capture: {e}", exc_info=True)

# Usage would involve calling capture_packets with the desired interface and packet count.