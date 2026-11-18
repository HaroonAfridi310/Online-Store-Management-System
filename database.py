import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Create and return a connection to the MySQL database."""

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="ecommerce_storedb"
    )

    return connection