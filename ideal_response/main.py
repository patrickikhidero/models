import sys
from server.tcp_server import TCPServer
from ssh.ssh_client import SSHClient
from packet_analysis.packet_analyzer import PacketAnalyzer
from utils.logger import Logger
from config import Config
import threading

def main():
    logger = Logger(__name__)
    config = Config()

    try:
        # Start TCP Server
        server = TCPServer(config.SERVER_HOST, config.SERVER_PORT, config.MAX_CONNECTIONS, config.USE_SSL)
        server_thread = threading.Thread(target=server.start)
        server_thread.start()

        # SSH Client example
        ssh_client = SSHClient(config.SSH_HOST, config.SSH_USERNAME, config.SSH_PASSWORD)
        ssh_client.connect()
        result = ssh_client.execute_command('ls -l')
        logger.info(f"SSH Command Result: {result}")
        ssh_client.close()

        # Packet Analyzer example
        analyzer = PacketAnalyzer(config.NETWORK_INTERFACE)
        packets = analyzer.capture_packets(count=10, filter="tcp")
        for packet in packets:
            analysis = analyzer.analyze_packet(packet)
            logger.info(f"Packet Analysis: {analysis}")

        potential_scans = analyzer.detect_port_scan(packets)
        if potential_scans:
            logger.warning(f"Potential port scans detected: {potential_scans}")

        # Keep the main thread running
        server_thread.join()

    except KeyboardInterrupt:
        logger.info("Shutting down...")
        server.stop()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()