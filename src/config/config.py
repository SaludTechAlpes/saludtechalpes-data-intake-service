import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        environment = os.getenv('FLASK_ENV')
        
        self.ENVIRONMENT = environment
        self.APP_NAME = os.getenv('APP_NAME', 'saludtech-data-intake')
        self.PULSAR_HOST = os.getenv('PULSAR_HOST', 'pulsar')
        self.BROKER_HOST = os.getenv('BROKER_HOST', 'broker')
        self.BROKER_PORT = os.getenv('BROKER_PORT', '6650')
        self.DB_HOST = os.getenv('DB_HOST', 'db')
        self.DB_PORT = os.getenv('DB_PORT', '5432')
        self.DB_USER = os.getenv('DB_USER', 'admin')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
        self.DB_NAME = os.getenv('DB_NAME', 'saludtechalpes')
