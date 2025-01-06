import mysql.connector
from configparser import ConfigParser
import logging

# Set up logging configuration
log_directory = "CODE_LOGS"
log_filename = "db_connection_test.log"
#  žurnalēšana
logging.basicConfig(
    filename=f"{log_directory}/{log_filename}",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

#automatizēti testi
def test_database_connection():
    """Test the database connection by executing a simple query."""
    #mainīg ielas
    config = ConfigParser()
    config.read('CONFIGURATION.ini')

    try:
        # Connect to the MySQL server
        connection = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database']
        )
        cursor = connection.cursor()

        # Run a simple query to test the connection
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        if result:
            logging.info("Database connection test successful. The database is responsive.")
            print("Connection test successful.")
        else:
            logging.error("Database connection test failed. No response from the database.")
            print("Connection test failed.")

    except mysql.connector.Error as e:
        logging.error(f"Error during database connection test: {e}")
        print(f"Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    test_database_connection()
