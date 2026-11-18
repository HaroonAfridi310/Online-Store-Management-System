
from database import get_connection
from validation import (
    validate_product,
    validate_product_id,
    validate_search_keyword
)


def get_all_products():
    """Return all products from the database."""

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT ProductID, Name, Category, Price, StockQuantity
            FROM Product
            ORDER BY ProductID
            """
        )

        products = cursor.fetchall()

        return products

    finally:
        if cursor:
            cursor.close()

        connection.close()


def search_products(keyword):
    """Search products by name or category."""

    keyword = validate_search_keyword(keyword)

    connection = get_connection()
    cursor = None

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

        return products

    finally:
        if cursor:
            cursor.close()

        connection.close()


def get_product_by_id(product_id):
    """Return one product using its ID."""

    product_id = validate_product_id(product_id)

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT ProductID, Name, Category, Price, StockQuantity
            FROM Product
            WHERE ProductID = %s
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        return product

    finally:
        if cursor:
            cursor.close()

        connection.close()


def add_products(name, category, price, stock):
    """Validate and add a new product."""

    # Validate before opening the database connection.
    name, category, price, stock = validate_product(
        name,
        category,
        price,
        stock
    )

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        sql = """
            INSERT INTO Product
            (Name, Category, Price, StockQuantity)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (name, category, price, stock))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    else:
        return True

    finally:
        if cursor:
            cursor.close()

        connection.close()


def delete_product(product_id):
    """Delete a product using its ID."""

    product_id = validate_product_id(product_id)

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM Product
            WHERE ProductID = %s
            """,
            (product_id,)
        )

        deleted = cursor.rowcount > 0

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    else:
        return deleted

    finally:
        if cursor:
            cursor.close()

        connection.close()
