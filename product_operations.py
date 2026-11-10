
from database import get_connection


def get_all_products():
    connection = get_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()

    for product in products:
        print(
            f"ID: {product[0]} | Name: {product[1]} | "
            f"Category: {product[2]} | Price: {product[3]} | "
            f"StockQuantity: {product[4]}"
        )

    cursor.close()
    connection.close()
    return products


def search_products(keyword):
    connection = get_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    query = """
        SELECT ProductID, Name, Category, Price, StockQuantity
        FROM Product
        WHERE Name LIKE %s OR Category LIKE %s
    """
    value = f"%{keyword}%"
    cursor.execute(query, (value, value))
    products = cursor.fetchall()

    for product in products:
        print(
            f"ID: {product[0]} | Name: {product[1]} | "
            f"Category: {product[2]} | Price: {product[3]} | "
            f"StockQuantity: {product[4]}"
        )

    cursor.close()
    connection.close()
    return products
