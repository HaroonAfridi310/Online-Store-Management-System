
from unittest.mock import MagicMock, patch

import product_operations


def make_database():
    connection = MagicMock()
    cursor = MagicMock()
    connection.cursor.return_value = cursor
    return connection, cursor


@patch("product_operations.get_connection")
def test_get_all_products(mock_get_connection):
    connection, cursor = make_database()
    expected_products = [
        (1, "Mouse", "Accessories", 15.00, 10),
        (2, "Keyboard", "Accessories", 25.00, 5),
    ]
    cursor.fetchall.return_value = expected_products
    mock_get_connection.return_value = connection

    result = product_operations.get_all_products()

    assert result == expected_products
    cursor.execute.assert_called_once_with("SELECT * FROM Product")
    connection.close.assert_called_once()


@patch("product_operations.get_connection")
def test_search_products(mock_get_connection):
    connection, cursor = make_database()
    expected_products = [(1, "Wireless Mouse", "Accessories", 15.00, 10)]
    cursor.fetchall.return_value = expected_products
    mock_get_connection.return_value = connection

    result = product_operations.search_products("Mouse")

    assert result == expected_products
    cursor.execute.assert_called_once()
    assert cursor.execute.call_args.args[1] == ("%Mouse%", "%Mouse%")
    connection.close.assert_called_once()


@patch("product_operations.get_connection")
def test_get_product_by_id(mock_get_connection):
    connection, cursor = make_database()
    expected_product = (1, "Mouse", "Accessories", 15.00, 10)
    cursor.fetchone.return_value = expected_product
    mock_get_connection.return_value = connection

    result = product_operations.get_product_by_id(1)

    assert result == expected_product
    cursor.execute.assert_called_once_with(
        "SELECT * FROM Product WHERE ProductID = %s",
        (1,)
    )
    connection.close.assert_called_once()


@patch("product_operations.get_connection")
def test_add_products(mock_get_connection):
    connection, cursor = make_database()
    mock_get_connection.return_value = connection

    result = product_operations.add_products(
        "Mouse",
        "Accessories",
        15.00,
        10
    )

    assert result is True
    cursor.execute.assert_called_once()
    assert cursor.execute.call_args.args[1] == (
        "Mouse",
        "Accessories",
        15.00,
        10
    )
    connection.commit.assert_called_once()
    connection.close.assert_called_once()


@patch("product_operations.get_connection")
def test_delete_product_success(mock_get_connection):
    connection, cursor = make_database()
    cursor.rowcount = 1
    mock_get_connection.return_value = connection

    result = product_operations.delete_product(1)

    assert result is True
    cursor.execute.assert_called_once_with(
        "DELETE FROM Product WHERE ProductID = %s",
        (1,)
    )
    connection.commit.assert_called_once()
    connection.close.assert_called_once()


@patch("product_operations.get_connection")
def test_delete_product_not_found(mock_get_connection):
    connection, cursor = make_database()
    cursor.rowcount = 0
    mock_get_connection.return_value = connection

    result = product_operations.delete_product(999)

    assert result is False
    connection.commit.assert_called_once()
    connection.close.assert_called_once()


@patch("product_operations.get_connection")
def test_product_function_when_database_connection_fails(mock_get_connection):
    mock_get_connection.return_value = None

    assert product_operations.get_all_products() is None
    assert product_operations.search_products("Mouse") is None
    assert product_operations.get_product_by_id(1) is None
    assert product_operations.add_products(
        "Mouse", "Accessories", 15.00, 10
    ) is False
    assert product_operations.delete_product(1) is False
