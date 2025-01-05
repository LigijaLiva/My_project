import mysql.connector
from configparser import ConfigParser
import logging
import os

# Create 'CODE_LOGS' directory if it doesn't exist
log_directory = "CODE_LOGS"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging configuration
log_filename = os.path.join(log_directory, "db_connection.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def check_database_connection():
    config = ConfigParser()
    config.read('CONFIGURATION.ini')

    try:
        # Attempt to connect to MySQL without specifying a database
        connection = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password']
        )
        logging.info("Connection established with MySQL!")
        
        # Now try connecting with the database
        connection.database = config['database']['database']
        logging.info("Connection established! Everything is working!")

    except mysql.connector.Error as e:
        if "Unknown database" in str(e):
            logging.warning("Connection established with MySQL! Failure to load database! Possibly does not exist, please launch IMPORT_DATA.py!")
        else:
            logging.error("Failure! Could not connect to the MySQL!")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    check_database_connection()
