import paramiko
import logging
from utils.logger import setup_logger

logger = setup_logger('ssh_client')

class SSHClient:
    def __init__(self, hostname, username, password=None, key_filename=None):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname, username=username, password=password, key_filename=key_filename)
        except Exception as e:
            logger.error(f"SSH Connection failed: {e}")
            raise

    def execute_command(self, command):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout = stdout.read().decode('utf-8')
            stderr = stderr.read().decode('utf-8')
            if stdout:
                logger.info(f"Command output: {stdout}")
            if stderr:
                logger.warning(f"Command error: {stderr}")
            return stdout, stderr
        except Exception as e:
            logger.error(f"Command execution failed: {e}", exc_info=True)
            return None, str(e)

    def __del__(self):
        self.client.close()

# Usage would require creating an instance and calling execute_command with dynamic commands.