import logging
import os
import hashlib
from pymongo import MongoClient
from datetime import datetime

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['cityserve']
log_collection = db['logs']

class SecureLogger:
    def __init__(self, log_file='system.log'):
        self.logger = logging.getLogger('CityServeLogger')
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log_event(self, event_type, message, severity='INFO', user_id=None, component=None):
        timestamp = datetime.utcnow()
        log_entry = {
            'timestamp': timestamp.isoformat(),
            'event_type': event_type,
            'message': message,
            'severity': severity,
            'user_id': user_id,
            'component': component,
            'hash': self.generate_hash(event_type, message, timestamp)
        }

        # Log to file
        self.logger.log(self.get_log_level(severity), f"{event_type} - {message} - User: {user_id}")

        # Save to MongoDB
        log_collection.insert_one(log_entry)

    @staticmethod
    def generate_hash(event_type, message, timestamp):
        hash_input = f"{event_type}{message}{timestamp}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()

    @staticmethod
    def get_log_level(severity):
        levels = {'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
        return levels.get(severity, logging.INFO)

# Singleton Logger
secure_logger = SecureLogger()
