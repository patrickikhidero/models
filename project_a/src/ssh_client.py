import paramiko
from .logger import logger

class SSHClient:
    def __init__(self, hostname, username, password=None, key_filename=None):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname, username=username, password=password, key_filename=key_filename)
        except paramiko.AuthenticationException:
            logger.error("Authentication failed")
            raise
        except Exception as e:
            logger.error(f"Could not SSH to {hostname}, error: {e}")
            raise

    def execute_command(self, command):
        """Execute a command on the SSH server."""
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to execute command {command}: {e}")
            return None, str(e)

    def close(self):
        self.client.close()

# Usage
ssh = SSHClient('hostname', 'username', password='password')
out, err = ssh.execute_command('ls -l')
ssh.close()