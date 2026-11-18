from database import get_connection
from validation import validate_product_id, validate_restock_quantity


def increase_product_stock(product_id, quantity):
    """Add units to an existing product without creating a new product."""

    product_id = validate_product_id(product_id)
    quantity = validate_restock_quantity(quantity)

    connection = get_connection()
    cursor = None

    try:
        connection.start_transaction()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE Product
            SET StockQuantity = StockQuantity + %s
            WHERE ProductID = %s
            """,
            (quantity, product_id)
        )

        if cursor.rowcount != 1:
            raise ValueError("Product not found. Stock was not changed.")

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

