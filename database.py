
import mysql.connector
from getpass import getpass
from mysql.connector import Error


def get_connection():
    """Creating and returning a connection to the MySQL database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=getpass("Enter password: "),
            database="ecommerce_storedb"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# Adding Product Functions

def get_all_products():
    """Getting all the products from the database"""
    connection = get_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    for product in products:
        print(
            f"ID: {product[0]} | Name: {product[1]} | Category: {product[2]} | Price: {product[3]} | StockQuantity: {product[4]}")
    cursor.close()
    connection.close()
    return products


def get_product_by_id(product_id):
    """Getting only one product"""
    connection = get_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Product where Productid = %s", (product_id,))
    product = cursor.fetchone()
    print(
        f"ID: {product[0]} | Name: {product[1]} | Category: {product[2]} | Price: {product[3]} | StockQuantity: {product[4]}")
    cursor.close()
    connection.close()
    return product


def search_products(keyword):
    """Search products by name or category"""
    connection = get_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    query = """SELECT ProductID, Name, Category, Price, StockQuantity
            FROM Product Where Name Like %s OR Category Like %s"""
    value = f"%{keyword}%"
    cursor.execute(query, (value, value))
    products = cursor.fetchall()
    for product in products:
        print(
            f"ID: {product[0]} | Name: {product[1]} | Category: {product[2]} | Price: {product[3]} | StockQuantity: {product[4]}")
    cursor.close()
    connection.close()
    return products


def add_products(name, category, price, stock):
    """Adding a new product"""
    connection = get_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    sql = "INSERT INTO Product (Name, Category, Price, StockQuantity) VALUES (%s,%s, %s, %s)"
    cursor.execute(sql, (name, category, price, stock))
    connection.commit()
    cursor.close()
    connection.close()
    return True


def delete_product(product_id):
    """Delete a product by ProductID"""
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    sql = "DELETE FROM Product WHERE ProductID = %s"
    values = (product_id,)
    cursor.execute(sql, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    connection.close()
    return affected_rows > 0


if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Connection was successful")
        search_products("Home")
        conn.close()
    else:
        print("Connection was failed")
