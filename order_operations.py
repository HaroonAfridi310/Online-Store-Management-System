
from database import get_connection
from validation import (
    validate_order,
    validate_order_status,
    validate_payment
)
from decimal import Decimal


# Allowed order status progression.
ALLOWED_STATUS_TRANSITIONS = {
    "Pending": "Processing",
    "Processing": "Shipped",
    "Shipped": "Delivered",
    "Delivered": None
}


def create_order(customer_id, items):
    """Create an order only when all requested products are available."""

    customer_id, items = validate_order(customer_id, items)

    combined_items = {}

    for product_id, quantity in items:
        combined_items[product_id] = (
            combined_items.get(product_id, 0) + quantity
        )

    connection = get_connection()
    cursor = None

    try:
        connection.start_transaction()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT CustomerID
            FROM customer
            WHERE CustomerID = %s
            """,
            (customer_id,)
        )

        if cursor.fetchone() is None:
            raise ValueError("Customer not found.")

        product_details = {}

        for product_id, quantity in sorted(combined_items.items()):

            cursor.execute(
                """
                SELECT Price, StockQuantity
                FROM Product
                WHERE ProductID = %s
                FOR UPDATE
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if product is None:
                raise ValueError(
                    f"Product ID {product_id} was not found."
                )

            price = Decimal(str(product[0]))
            available_stock = product[1]

            if quantity > available_stock:
                raise ValueError(
                    f"Insufficient stock for product ID {product_id}. "
                    f"Requested: {quantity}. "
                    f"Available: {available_stock}."
                )

            product_details[product_id] = {
                "price": price,
                "quantity": quantity
            }

        cursor.execute(
            """
            INSERT INTO orders
            (CustomerID, OrderStatus, TotalAmount)
            VALUES (%s, %s, %s)
            """,
            (customer_id, "Pending", Decimal("0.00"))
        )

        order_id = cursor.lastrowid
        total_amount = Decimal("0.00")

        for product_id, details in product_details.items():

            price = details["price"]
            quantity = details["quantity"]

            cursor.execute(
                """
                INSERT INTO orderitem
                (OrderID, ProductID, Quantity, UnitPrice)
                VALUES (%s, %s, %s, %s)
                """,
                (order_id, product_id, quantity, price)
            )

            cursor.execute(
                """
                UPDATE Product
                SET StockQuantity = StockQuantity - %s
                WHERE ProductID = %s
                  AND StockQuantity >= %s
                """,
                (quantity, product_id, quantity)
            )

            if cursor.rowcount != 1:
                raise ValueError(
                    f"Stock changed while creating the order "
                    f"for product ID {product_id}. "
                    "Please try again."
                )

            total_amount += price * quantity

        cursor.execute(
            """
            UPDATE orders
            SET TotalAmount = %s
            WHERE OrderID = %s
            """,
            (total_amount, order_id)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    else:
        return order_id

    finally:
        if cursor:
            cursor.close()

        connection.close()


def get_all_orders():
    """Return all orders with customer information."""

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                o.OrderID,
                o.CustomerID,
                c.FirstName,
                c.LastName,
                o.OrderDate,
                o.OrderStatus,
                o.TotalAmount
            FROM orders o
            JOIN customer c ON o.CustomerID = c.CustomerID
            ORDER BY o.OrderID
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        connection.close()


def get_order_details(order_id):
    """Return the main details of one order."""

    if type(order_id) is not int or order_id <= 0:
        raise ValueError("Order ID must be a positive whole number.")

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                OrderID,
                CustomerID,
                OrderDate,
                OrderStatus,
                TotalAmount
            FROM orders
            WHERE OrderID = %s
            """,
            (order_id,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        connection.close()


def delete_order(order_id):
    """
    Delete an unpaid Pending or Processing order
    and restore its product stock in one transaction.
    """

    if type(order_id) is not int or order_id <= 0:
        raise ValueError("Order ID must be a positive whole number.")

    connection = get_connection()
    cursor = None

    try:
        connection.start_transaction()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT OrderStatus
            FROM orders
            WHERE OrderID = %s
            FOR UPDATE
            """,
            (order_id,)
        )

        order = cursor.fetchone()

        if order is None:
            raise ValueError("Order not found.")

        order_status = order[0]

        if order_status not in ("Pending", "Processing"):
            raise ValueError(
                "Only Pending or Processing orders can be deleted. "
                "Shipped and Delivered orders cannot be deleted."
            )

        cursor.execute(
            """
            SELECT PaymentID
            FROM payment
            WHERE OrderID = %s
            """,
            (order_id,)
        )

        if cursor.fetchone() is not None:
            raise ValueError(
                "This order has a recorded payment and cannot be deleted."
            )

        cursor.execute(
            """
            SELECT ProductID, Quantity
            FROM orderitem
            WHERE OrderID = %s
            FOR UPDATE
            """,
            (order_id,)
        )

        order_items = cursor.fetchall()

        if not order_items:
            raise ValueError(
                "This order has no products and cannot be deleted."
            )

        for product_id, quantity in order_items:

            cursor.execute(
                """
                UPDATE Product
                SET StockQuantity = StockQuantity + %s
                WHERE ProductID = %s
                """,
                (quantity, product_id)
            )

            if cursor.rowcount != 1:
                raise ValueError(
                    f"Could not restore stock for product ID {product_id}."
                )

        cursor.execute(
            """
            DELETE FROM orderitem
            WHERE OrderID = %s
            """,
            (order_id,)
        )

        cursor.execute(
            """
            DELETE FROM orders
            WHERE OrderID = %s
            """,
            (order_id,)
        )

        if cursor.rowcount != 1:
            raise ValueError("The order could not be deleted.")

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


def update_order_status(order_id, status):
    """Update an order only to its next permitted status."""

    if type(order_id) is not int or order_id <= 0:
        raise ValueError("Order ID must be a positive whole number.")

    status = validate_order_status(status)

    connection = get_connection()
    cursor = None

    try:
        connection.start_transaction()
        cursor = connection.cursor()

        # Lock the order while checking and changing its status.
        cursor.execute(
            """
            SELECT OrderStatus
            FROM orders
            WHERE OrderID = %s
            FOR UPDATE
            """,
            (order_id,)
        )

        order = cursor.fetchone()

        if order is None:
            raise ValueError("Order not found.")

        current_status = order[0]

        if current_status == status:
            raise ValueError(
                f"The order is already {current_status}."
            )

        allowed_next_status = ALLOWED_STATUS_TRANSITIONS.get(
            current_status
        )

        if status != allowed_next_status:

            if allowed_next_status is None:
                raise ValueError(
                    "A Delivered order cannot move to another status."
                )

            raise ValueError(
                f"Invalid status change. An order with status "
                f"{current_status} can only move to "
                f"{allowed_next_status}."
            )

        cursor.execute(
            """
            UPDATE orders
            SET OrderStatus = %s
            WHERE OrderID = %s
            """,
            (status, order_id)
        )

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


def record_payment(order_id, method):
    """Record one full payment and update Pending orders to Processing."""

    order_id, method = validate_payment(order_id, method)

    connection = get_connection()
    cursor = None

    try:
        connection.start_transaction()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT TotalAmount, OrderStatus
            FROM orders
            WHERE OrderID = %s
            FOR UPDATE
            """,
            (order_id,)
        )

        order = cursor.fetchone()

        if order is None:
            raise ValueError("Order not found.")

        amount = order[0]
        current_status = order[1]

        cursor.execute(
            """
            SELECT PaymentID
            FROM payment
            WHERE OrderID = %s
            """,
            (order_id,)
        )

        if cursor.fetchone():
            raise ValueError(
                "A payment has already been recorded for this order."
            )

        cursor.execute(
            """
            INSERT INTO payment
            (OrderID, Amount, Method, PaymentDate, PaymentStatus)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s)
            """,
            (order_id, amount, method, "Paid")
        )

        if current_status == "Pending":

            cursor.execute(
                """
                UPDATE orders
                SET OrderStatus = %s
                WHERE OrderID = %s
                """,
                ("Processing", order_id)
            )

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
