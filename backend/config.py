import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost/inventory_management')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for session management or JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

    # Additional configurations can be added here
    DEBUG = True

DATABASE_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'Pritam@123',
    'database': 'inventory_management'
}