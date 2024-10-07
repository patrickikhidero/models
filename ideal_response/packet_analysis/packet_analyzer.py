from scapy.all import sniff, IP, TCP, UDP
from utils.logger import Logger
import subprocess

class PacketAnalyzer:
    def __init__(self, interface='en0'):
        self.interface = interface
        self.logger = Logger(__name__)

    def capture_packets(self, count=0, filter="tcp"):
        try:
            self.logger.info(f"Starting packet capture on interface {self.interface}")
            packets = sniff(iface=self.interface, count=count, filter=filter, prn=self._packet_callback)
            return packets
        except Exception as e:
            self.logger.error(f"Error during packet capture: {str(e)}")
            return None    
    
    def _packet_callback(self, packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto

            if TCP in packet:
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                self.logger.info(f"TCP: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
            elif UDP in packet:
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                self.logger.info(f"UDP: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
            else:
                self.logger.info(f"Other IP: {src_ip} -> {dst_ip}, Protocol: {protocol}")

    def analyze_packet(self, packet):
        analysis = {}
        if IP in packet:
            analysis['ip'] = {
                'src': packet[IP].src,
                'dst': packet[IP].dst,
                'proto': packet[IP].proto
            }
            if TCP in packet:
                analysis['tcp'] = {
                    'sport': packet[TCP].sport,
                    'dport': packet[TCP].dport,
                    'flags': packet[TCP].flags
                }
            elif UDP in packet:
                analysis['udp'] = {
                    'sport': packet[UDP].sport,
                    'dport': packet[UDP].dport
                }
        return analysis
    
    def detect_port_scan(self, packets, threshold=10):
        port_attempts = {}

        for packet in packets:
            if TCP in packet:
                src_ip = packet[IP].src
                dst_port = packet[TCP].dport
                # Use only src_ip to count unique destination ports
                if src_ip not in port_attempts:
                    port_attempts[src_ip] = set()  # Use a set to track unique ports
                port_attempts[src_ip].add(dst_port)

        potential_scans = [
            (ip, len(ports)) for ip, ports in port_attempts.items() if len(ports) >= threshold
        ]
        
        if potential_scans:
            self.logger.warning(f"Potential port scan detected from IPs: {potential_scans}")

        return potential_scans


        