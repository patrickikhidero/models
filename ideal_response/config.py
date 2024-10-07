import os

class Config:
    # Server Configuration
    SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))
    MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS', 10))
    USE_SSL = os.getenv('USE_SSL', 'False').lower() == 'true'

    # SSH Configuration
    SSH_HOST = os.getenv('SSH_HOST', 'example.com')
    SSH_USERNAME = os.getenv('SSH_USERNAME', 'user')
    SSH_PASSWORD = os.getenv('SSH_PASSWORD', 'password')

    # Network Configuration
    NETWORK_INTERFACE = os.getenv('NETWORK_INTERFACE', 'eth0')

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')

    # Security Configuration
    ENCRYPTION_KEY_FILE = os.getenv('ENCRYPTION_KEY_FILE', 'secret.key')