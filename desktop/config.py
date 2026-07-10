import os

# Database Configuration
# This is the single source of truth for the database path across all Python apps.
# Use absolute path to ensure scripts can run from anywhere.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'attendance.db')

# Hardware Configuration
SERIAL_PORT = "COM3"
BAUD_RATE = 9600

# Application Configuration
LATE_CUTOFF = "08:00:00"
