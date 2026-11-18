
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
import order_operations


def make_database():
    connection = MagicMock()
    cursor = MagicMock()
    connection.cursor.return_value = cursor
    return connection, cursor


@patch("order_operations.get_connection")
def test_create_order_success(mock_get_connection):
    connection, cursor = make_database()

    cursor.fetchone.side_effect = [
        (1,),                   # Customer exists
        (Decimal("10.00"), 5),  # Product price and stock
    ]
    cursor.lastrowid = 99
    cursor.rowcount = 1
    mock_get_connection.return_value = connection

    result = order_operations.create_order(1, [(2, 2)])

    assert result == 99
    connection.start_transaction.assert_called_once()
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_create_order_customer_not_found(mock_get_connection):
    connection, cursor = make_database()
    cursor.fetchone.return_value = None
    mock_get_connection.return_value = connection

    with pytest.raises(ValueError, match="Customer not found"):
        order_operations.create_order(999, [(2, 1)])

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_create_order_insufficient_stock(mock_get_connection):
    connection, cursor = make_database()

    cursor.fetchone.side_effect = [
        (1,),                   # Customer exists
        (Decimal("10.00"), 1),  # Only one item in stock
    ]
    mock_get_connection.return_value = connection

    with pytest.raises(ValueError, match="Insufficient stock"):
        order_operations.create_order(1, [(2, 3)])

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_create_order_empty_items(mock_get_connection):
    with pytest.raises(ValueError, match="at least one product"):
        order_operations.create_order(1, [])

    # Validation happens before opening a database connection.
    mock_get_connection.assert_not_called()


@patch("order_operations.get_connection")
def test_update_order_status_success(mock_get_connection):
    connection, cursor = make_database()

    # An order must be Processing before it can become Shipped.
    cursor.fetchone.return_value = ("Processing",)
    mock_get_connection.return_value = connection

    result = order_operations.update_order_status(5, "Shipped")

    assert result is True
    assert cursor.execute.call_count == 2
    assert cursor.execute.call_args.args[1] == ("Shipped", 5)
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_update_order_status_invalid_value(mock_get_connection):
    with pytest.raises(ValueError, match="valid order status"):
        order_operations.update_order_status(5, "Cancelled")

    mock_get_connection.assert_not_called()


@patch("order_operations.get_connection")
def test_record_payment_success_changes_pending_to_processing(
    mock_get_connection
):
    connection, cursor = make_database()

    cursor.fetchone.side_effect = [
        (Decimal("25.00"), "Pending"),  # Order amount and status
        None,                           # No existing payment
    ]
    mock_get_connection.return_value = connection

    result = order_operations.record_payment(5, "Card")

    assert result is True
    connection.start_transaction.assert_called_once()
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()

    update_calls = [
        call for call in cursor.execute.call_args_list
        if "UPDATE orders" in call.args[0]
    ]

    assert len(update_calls) == 1
    assert update_calls[0].args[1] == ("Processing", 5)

    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_record_payment_rejects_duplicate_payment(mock_get_connection):
    connection, cursor = make_database()

    cursor.fetchone.side_effect = [
        (Decimal("25.00"), "Pending"),
        (10,),  # Existing payment
    ]
    mock_get_connection.return_value = connection

    with pytest.raises(ValueError, match="already been recorded"):
        order_operations.record_payment(5, "Card")

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_record_payment_order_not_found(mock_get_connection):
    connection, cursor = make_database()
    cursor.fetchone.return_value = None
    mock_get_connection.return_value = connection

    with pytest.raises(ValueError, match="Order not found"):
        order_operations.record_payment(999, "Card")

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()
