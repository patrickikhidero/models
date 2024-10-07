import unittest
import paramiko
from ssh.ssh_client import SSHClient

class TestSSHClient(unittest.TestCase):
    def setUp(self):
        # Initialize SSHClient with a public test server
        self.ssh_client = SSHClient('test.rebex.net', 'demo', 'password')  # Using demo credentials

    def test_connect_success(self):
        try:
            self.ssh_client.connect()
            self.assertTrue(True)  # If it connects, the test passes
        except paramiko.AuthenticationException:
            self.fail("Authentication failed unexpectedly.")

    def test_connect_auth_failure(self):
        # Set incorrect credentials to trigger an authentication failure
        self.ssh_client = SSHClient('test.rebex.net', 'demo', 'wrongpassword')
        with self.assertRaises(paramiko.AuthenticationException):
            self.ssh_client.connect()

    def test_execute_command_success(self):
        self.ssh_client.connect()
        result = self.ssh_client.execute_command('echo Hello, World!')
        self.assertEqual(result, 'Hello, World!')

    def test_execute_command_failure(self):
        self.ssh_client.connect()
        result = self.ssh_client.execute_command('invalid_command')
        self.assertIsNone(result)  # Expect None on failure

if __name__ == '__main__':
    unittest.main()
