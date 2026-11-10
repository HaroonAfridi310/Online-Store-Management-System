
from database import get_connection
from mysql.connector import Error
from decimal import Decimal


def create_order(customer_id, items):
    """Create an order containing one or more products."""
    connection = get_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor()
        connection.start_transaction()

        # Check whether the customer exists.
        cursor.execute(
            "SELECT CustomerID FROM customer WHERE CustomerID = %s",
            (customer_id,)
        )

        if cursor.fetchone() is None:
            print("Customer not found.")
            connection.rollback()
            return None

        # Combine repeated product IDs.
        combined_items = {}

        for product_id, quantity in items:
            combined_items[product_id] = (
                combined_items.get(product_id, 0) + quantity
            )

        # Create the order.
        cursor.execute(
            """
            INSERT INTO orders (CustomerID, OrderStatus, TotalAmount)
            VALUES (%s, %s, %s)
            """,
            (customer_id, "Pending", Decimal("0.00"))
        )

        order_id = cursor.lastrowid
        total_amount = Decimal("0.00")

        # Add products to the order.
        for product_id, quantity in combined_items.items():

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
            stock = product[1]

            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")

            if stock < quantity:
                raise ValueError(
                    f"Not enough stock for product ID {product_id}. "
                    f"Available stock: {stock}"
                )

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
                """,
                (quantity, product_id)
            )

            total_amount += price * quantity

        # Update the total order amount.
        cursor.execute(
            """
            UPDATE orders
            SET TotalAmount = %s
            WHERE OrderID = %s
            """,
            (total_amount, order_id)
        )

        connection.commit()

        print(f"Order created successfully. Order ID: {order_id}")
        print(f"Total amount: €{total_amount:.2f}")

        return order_id

    except (Error, ValueError) as e:
        connection.rollback()
        print(f"Could not create order: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()


def get_all_orders():
    connection = get_connection()

    if connection is None:
        return None

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

        orders = cursor.fetchall()

        if not orders:
            print("No orders found.")
            return []

        for order in orders:
            print(
                f"Order ID: {order[0]} | "
                f"Customer ID: {order[1]} | "
                f"Customer: {order[2]} {order[3]} | "
                f"Date: {order[4]} | "
                f"Status: {order[5]} | "
                f"Total: €{order[6]}"
            )
            print()

        return orders

    except Error as e:
        print(f"Error displaying orders: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()


def get_order_details(order_id):
    connection = get_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT OrderID, CustomerID, OrderDate, OrderStatus, TotalAmount
            FROM orders
            WHERE OrderID = %s
            """,
            (order_id,)
        )

        order = cursor.fetchone()

        if order is None:
            print("Order not found.")
            return None

        print("\n===== Order Details =====")
        print(f"Order ID: {order[0]}")
        print(f"Customer ID: {order[1]}")
        print(f"Order Date: {order[2]}")
        print(f"Status: {order[3]}")
        print(f"Total Amount: €{order[4]}")

        cursor.execute(
            """
            SELECT
                oi.ProductID,
                p.Name,
                oi.Quantity,
                oi.UnitPrice,
                (oi.Quantity * oi.UnitPrice) AS Subtotal
            FROM orderitem oi
            JOIN Product p ON oi.ProductID = p.ProductID
            WHERE oi.OrderID = %s
            """,
            (order_id,)
        )

        items = cursor.fetchall()

        print("\nProducts:")

        for item in items:
            print(
                f"Product ID: {item[0]} | "
                f"Name: {item[1]} | "
                f"Quantity: {item[2]} | "
                f"Unit Price: €{item[3]} | "
                f"Subtotal: €{item[4]}"
            )

        return order

    except Error as e:
        print(f"Error displaying order details: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()


def update_order_status(order_id, status):
    allowed_statuses = [
        "Pending",
        "Processing",
        "Shipped",
        "Delivered"
    ]

    if status not in allowed_statuses:
        print("Invalid order status.")
        return False

    connection = get_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE orders
            SET OrderStatus = %s
            WHERE OrderID = %s
            """,
            (status, order_id)
        )

        connection.commit()

        if cursor.rowcount > 0:
            print("Order status updated successfully.")
            return True

        print("Order not found or status unchanged.")
        return False

    except Error as e:
        connection.rollback()
        print(f"Error updating order status: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()


def record_payment(order_id, method):
    """Record one full payment for an order."""
    connection = get_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT TotalAmount
            FROM orders
            WHERE OrderID = %s
            """,
            (order_id,)
        )

        order = cursor.fetchone()

        if order is None:
            print("Order not found.")
            return False

        # Check whether this order already has a payment.
        cursor.execute(
            "SELECT PaymentID FROM payment WHERE OrderID = %s",
            (order_id,)
        )

        if cursor.fetchone():
            print("A payment has already been recorded for this order.")
            return False

        cursor.execute(
            """
            INSERT INTO payment
            (OrderID, Amount, Method, PaymentDate, PaymentStatus)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s)
            """,
            (order_id, order[0], method, "Paid")
        )

        connection.commit()

        print("Payment recorded successfully.")
        print(f"Payment amount: €{order[0]}")

        return True

    except Error as e:
        connection.rollback()
        print(f"Error recording payment: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()
