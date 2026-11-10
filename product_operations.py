
from database import get_connection


def get_all_products():
    connection = get_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Product")
        products = cursor.fetchall()

        for product in products:
            print(
                f"ID: {product[0]} | Name: {product[1]} | "
                f"Category: {product[2]} | Price: {product[3]} | "
                f"StockQuantity: {product[4]}"
            )
            print()

        cursor.close()
        return products

    finally:
        connection.close()


def search_products(keyword):
    connection = get_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()

        query = """
            SELECT ProductID, Name, Category, Price, StockQuantity
            FROM Product
            WHERE Name LIKE %s OR Category LIKE %s
        """

        value = f"%{keyword}%"
        cursor.execute(query, (value, value))
        products = cursor.fetchall()

        if products:
            for product in products:
                print(
                    f"ID: {product[0]} | Name: {product[1]} | "
                    f"Category: {product[2]} | Price: {product[3]} | "
                    f"StockQuantity: {product[4]}"
                )
                print()
        else:
            print("No products found.")

        cursor.close()
        return products

    finally:
        connection.close()


def get_product_by_id(product_id):
    connection = get_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM Product WHERE ProductID = %s",
            (product_id,)
        )
        product = cursor.fetchone()

        if product:
            print(
                f"ID: {product[0]} | Name: {product[1]} | "
                f"Category: {product[2]} | Price: {product[3]} | "
                f"StockQuantity: {product[4]}"
            )
        else:
            print("Product not found.")

        cursor.close()
        return product

    finally:
        connection.close()


def add_products(name, category, price, stock):
    connection = get_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        sql = """
            INSERT INTO Product (Name, Category, Price, StockQuantity)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (name, category, price, stock))
        connection.commit()

        cursor.close()
        print("Product added successfully.")
        return True

    finally:
        connection.close()


def delete_product(product_id):
    connection = get_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM Product WHERE ProductID = %s",
            (product_id,)
        )

        connection.commit()
        deleted = cursor.rowcount > 0

        cursor.close()

        if deleted:
            print("Product deleted successfully.")
        else:
            print("Product not found.")

        return deleted

    finally:
        connection.close()
