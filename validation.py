from decimal import Decimal, InvalidOperation

MAX_PRODUCT_NAME_LENGTH = 100
MAX_CATEGORY_LENGTH = 50


def validate_product(name, category, price, stock):
    """Validate product information before saving it."""

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Product name cannot be empty.")

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Product category cannot be empty.")

    name = name.strip()
    category = category.strip()

    if len(name) > MAX_PRODUCT_NAME_LENGTH:
        raise ValueError("Product name cannot exceed 100 characters.")

    if len(category) > MAX_CATEGORY_LENGTH:
        raise ValueError("Category cannot exceed 50 characters.")

    try:
        price = Decimal(str(price))
    except (InvalidOperation, ValueError):
        raise ValueError("Price must be a valid number.")

    if not price.is_finite() or price <= 0:
        raise ValueError("Price must be greater than zero.")

    if price > Decimal("99999999.99"):
        raise ValueError("Price is too large.")

    if price != price.quantize(Decimal("0.01")):
        raise ValueError("Price cannot have more than two decimal places.")

    if type(stock) is not int or stock < 0:
        raise ValueError("Stock quantity must be a whole number, 0 or more.")

    return name, category, price, stock


def validate_product_id(product_id):
    """Validate a product ID."""

    if type(product_id) is not int or product_id <= 0:
        raise ValueError("Product ID must be a positive whole number.")

    return product_id


def validate_restock_quantity(quantity):
    """Validate the number of units being added to existing stock."""

    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Restock quantity must be a positive whole number.")

    return quantity


def validate_order(customer_id, items):
    """Validate customer ID and order items."""

    if type(customer_id) is not int or customer_id <= 0:
        raise ValueError("Please select a valid customer.")

    if not isinstance(items, (list, tuple)) or not items:
        raise ValueError("An order must contain at least one product.")

    for item in items:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise ValueError("Invalid order item.")

        product_id, quantity = item

        if type(product_id) is not int or product_id <= 0:
            raise ValueError("Invalid product ID.")

        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Product quantity must be greater than zero.")

    return customer_id, items


def validate_order_status(status):
    """Validate order status."""

    allowed_statuses = [
        "Pending",
        "Processing",
        "Shipped",
        "Delivered"
    ]

    if status not in allowed_statuses:
        raise ValueError("Please select a valid order status.")

    return status


def validate_payment(order_id, method):
    """Validate payment information."""

    allowed_methods = [
        "Cash",
        "Card",
        "Bank Transfer",
        "Online"
    ]

    if type(order_id) is not int or order_id <= 0:
        raise ValueError("Invalid order ID.")

    if method not in allowed_methods:
        raise ValueError("Please select a valid payment method.")

    return order_id, method


def validate_search_keyword(keyword):
    """Check that a product search keyword is not empty."""

    if not isinstance(keyword, str) or not keyword.strip():
        raise ValueError(
            "Please enter a product name or category to search."
        )

    return keyword.strip()

