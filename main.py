import os

from connectors.database import DBConnection
from connectors.storage import StorageConnection

FILE_TO_PROC = 'taxi_bi.csv'
BUCKET = 'brytlyt'
KEY = 'MG/taxi_bi.csv'
DB_CONFIG = 'config/database.ini'
TABLE_CREATE = 'plpgsql/create_taxi_table.sql'
TABLE_NAME = 'taxi_table'

if __name__ == "__main__":

    if not os.path.isfile(FILE_TO_PROC):
        print('Downloading the file from the s3 in progress')
        StorageConnection.download_file(BUCKET, KEY, FILE_TO_PROC)
    else:
        print(f"{FILE_TO_PROC} exists!")

    DBConnection.connect(DB_CONFIG)

    DBConnection.execute_query(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    
    with open(TABLE_CREATE, 'r') as file_:
        query = file_.read().replace('{table}', TABLE_NAME)
        DBConnection.execute_query(query)

    DBConnection.load_from_file(FILE_TO_PROC, TABLE_NAME)