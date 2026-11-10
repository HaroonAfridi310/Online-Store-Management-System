
from decimal import Decimal
from unittest.mock import MagicMock, patch

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
        (1,),                    # Customer exists
        (Decimal("10.00"), 5),   # Product price and stock
    ]
    cursor.lastrowid = 99
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

    result = order_operations.create_order(999, [(2, 1)])

    assert result is None
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_create_order_insufficient_stock(mock_get_connection):
    connection, cursor = make_database()

    cursor.fetchone.side_effect = [
        (1,),                    # Customer exists
        (Decimal("10.00"), 1),   # Only one item in stock
    ]
    cursor.lastrowid = 99
    mock_get_connection.return_value = connection

    result = order_operations.create_order(1, [(2, 3)])

    assert result is None
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_create_order_empty_items(mock_get_connection):
    connection, cursor = make_database()
    cursor.fetchone.return_value = (1,)
    mock_get_connection.return_value = connection

    result = order_operations.create_order(1, [])

    assert result is None
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_update_order_status_success(mock_get_connection):
    connection, cursor = make_database()
    cursor.rowcount = 1
    mock_get_connection.return_value = connection

    result = order_operations.update_order_status(5, "Shipped")

    assert result is True
    cursor.execute.assert_called_once()
    assert cursor.execute.call_args.args[1] == ("Shipped", 5)
    connection.commit.assert_called_once()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_update_order_status_invalid_value(mock_get_connection):
    result = order_operations.update_order_status(5, "Cancelled")

    assert result is False
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

    # Check that the order status was changed to Processing.
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
        (10,),  # An existing payment was found
    ]
    mock_get_connection.return_value = connection

    result = order_operations.record_payment(5, "Card")

    assert result is False
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_record_payment_order_not_found(mock_get_connection):
    connection, cursor = make_database()
    cursor.fetchone.return_value = None
    mock_get_connection.return_value = connection

    result = order_operations.record_payment(999, "Card")

    assert result is False
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


@patch("order_operations.get_connection")
def test_order_function_when_database_connection_fails(
    mock_get_connection
):
    mock_get_connection.return_value = None

    assert order_operations.create_order(1, [(2, 1)]) is None
    assert order_operations.get_all_orders() is None
    assert order_operations.get_order_details(1) is None
    assert order_operations.update_order_status(1, "Shipped") is False
    assert order_operations.record_payment(1, "Card") is False
