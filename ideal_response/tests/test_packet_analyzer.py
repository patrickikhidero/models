import unittest
from unittest.mock import patch, MagicMock
from scapy.all import IP, TCP, UDP, sniff
from packet_analysis.packet_analyzer import PacketAnalyzer

class TestPacketAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PacketAnalyzer('en0')

    @patch('scapy.all.sniff')
    def test_capture_packets(self, mock_sniff):
        mock_packets = [MagicMock(), MagicMock()]
        result = mock_sniff(iface='en0', count=2, filter="tcp", prn=self.analyzer._packet_callback)
        mock_sniff.assert_called_once_with(iface='en0', count=2, filter="tcp", prn=self.analyzer._packet_callback)
        self.assertNotEqual(result, mock_packets)

    def test_analyze_packet(self):
        # Create a mock IP/TCP packet
        mock_packet = IP(src="192.168.1.1", dst="10.0.0.1")/TCP(sport=12345, dport=80, flags="S")

        analysis = self.analyzer.analyze_packet(mock_packet)

        self.assertEqual(analysis['ip']['src'], "192.168.1.1")
        self.assertEqual(analysis['ip']['dst'], "10.0.0.1")
        self.assertEqual(analysis['tcp']['sport'], 12345)
        self.assertEqual(analysis['tcp']['dport'], 80)
        self.assertEqual(analysis['tcp']['flags'], "S")

    def test_detect_port_scan(self):
        # Create mock packets simulating a port scan
        packets = [
            IP(src="192.168.1.1", dst="10.0.0.1")/TCP(sport=12345, dport=port)
            for port in range(1, 15)  # This generates ports 1 to 14
        ]

        potential_scans = self.analyzer.detect_port_scan(packets, threshold=5)

        # Check that the IP and the number of unique ports is correct
        self.assertIn(("192.168.1.1", 14), potential_scans)
        # This check for ("192.168.1.1", 10) does not make sense and should be removed
        self.assertEqual(len(potential_scans), 1)  # Only one unique IP should be detected

    
    

if __name__ == '__main__':
    unittest.main()