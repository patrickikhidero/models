import paramiko
from utils.logger import Logger

class SSHClient:
    def __init__(self, hostname, username, password=None, key_filename=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.client = None
        self.logger = Logger(__name__)

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                self.hostname,
                username=self.username,
                password=self.password,
                key_filename=self.key_filename
            )
            self.logger.info(f"Successfully connected to {self.hostname}")
        except paramiko.AuthenticationException:
            self.logger.error(f"Authentication failed for {self.hostname}")
            raise
        except paramiko.SSHException as ssh_exception:
            self.logger.error(f"SSH exception occurred: {str(ssh_exception)}")
            raise
        except Exception as e:
            self.logger.error(f"Error connecting to {self.hostname}: {str(e)}")
            raise

    def execute_command(self, command):
        if not self.client:
            self.logger.error("Not connected. Call connect() first.")
            return None

        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            
            if exit_status == 0:
                output = stdout.read().decode('utf-8').strip()
                self.logger.info(f"Command executed successfully: {command}")
                return output
            else:
                error = stderr.read().decode('utf-8').strip()
                self.logger.warning(f"Command failed: {command}. Error: {error}")
                return None
        except Exception as e:
            self.logger.error(f"Error executing command: {str(e)}")
            return None

    def close(self):
        if self.client:
            self.client.close()
            self.logger.info(f"Closed connection to {self.hostname}")