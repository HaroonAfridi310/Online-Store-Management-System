from unittest.mock import MagicMock, patch

import pytest

import stock_operations


def make_database():
    connection = MagicMock()
    cursor = MagicMock()
    connection.cursor.return_value = cursor
    cursor.rowcount = 1
    return connection, cursor


@patch("stock_operations.get_connection")
def test_increase_product_stock_updates_existing_product(mock_get_connection):
    connection, cursor = make_database()
    mock_get_connection.return_value = connection

    result = stock_operations.increase_product_stock(12, 5)

    assert result is True
    cursor.execute.assert_called_once()
    sql, values = cursor.execute.call_args.args
    assert "UPDATE Product" in sql
    assert "StockQuantity = StockQuantity + %s" in sql
    assert values == (5, 12)
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True, "3"])
def test_increase_product_stock_rejects_invalid_quantity(quantity):
    with patch("stock_operations.get_connection") as mock_get_connection:
        with pytest.raises(ValueError):
            stock_operations.increase_product_stock(12, quantity)

    mock_get_connection.assert_not_called()


@pytest.mark.parametrize("product_id", [0, -1, 1.5, True, "12"])
def test_increase_product_stock_rejects_invalid_product_id(product_id):
    with patch("stock_operations.get_connection") as mock_get_connection:
        with pytest.raises(ValueError):
            stock_operations.increase_product_stock(product_id, 3)

    mock_get_connection.assert_not_called()


@patch("stock_operations.get_connection")
def test_increase_product_stock_when_product_does_not_exist(mock_get_connection):
    connection, cursor = make_database()
    cursor.rowcount = 0
    mock_get_connection.return_value = connection

    with pytest.raises(ValueError, match="Product not found"):
        stock_operations.increase_product_stock(999, 3)

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


@patch("stock_operations.get_connection")
def test_increase_product_stock_rolls_back_database_failure(mock_get_connection):
    connection, cursor = make_database()
    cursor.execute.side_effect = RuntimeError("simulated failure")
    mock_get_connection.return_value = connection

    with pytest.raises(RuntimeError, match="simulated failure"):
        stock_operations.increase_product_stock(12, 3)

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()

