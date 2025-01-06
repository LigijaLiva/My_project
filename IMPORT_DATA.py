import os
import mysql.connector
from configparser import ConfigParser
import logging

# Create 'CODE_LOGS' directory if it doesn't exist
log_directory = "CODE_LOGS"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging configuration
log_filename = os.path.join(log_directory, "import_sql.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def import_sql_file():
    """Reads the SQL file from the TRANSFER folder and imports it into the database."""
    config = ConfigParser()
    config.read('CONFIGURATION.ini')

    transfer_folder = "TRANSFER"
    dump_file = "testdb_books.sql"
    dump_path = os.path.join(transfer_folder, dump_file)

    if not os.path.exists(dump_path):
        logging.error(f"SQL dump file '{dump_file}' not found in the TRANSFER folder!")
        return

    try:
        # Connect to the MySQL server (not specifying a database yet)
        connection = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password']
        )
        cursor = connection.cursor()

        # Check if the database exists
        database_name = config['database']['database']
        #datu lasīš/rakst
        cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
        db_exists = cursor.fetchone()

        if not db_exists:
            logging.info(f"Database '{database_name}' does not exist. Creating it...")
            cursor.execute(f"CREATE DATABASE {database_name}")
            logging.info(f"Database '{database_name}' created successfully!")

        # Now connect to the database
        connection.database = database_name

        # Read and execute the SQL file
        logging.info(f"Importing {dump_path}...")
        with open(dump_path, 'r') as file:
            sql = file.read()
            for statement in sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            connection.commit()
        logging.info(f"Successfully imported '{dump_file}'!")

    except mysql.connector.Error as e:
        logging.error(f"Error importing SQL file: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    import_sql_file()
