
import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()


def get_connection():
    """Create and return a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("MYSQL_PASSWORD"),
            database="ecommerce_storedb"
        )
        return connection

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
