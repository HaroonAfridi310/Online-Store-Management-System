# Software Development – Week 2 Progress Report

**Group Members:**
1. Haroon Afridi
2. Pradeep Sapkota
3. Poshan Oli
4. Lamyae Echaoui

**Week:** Week 2  
**Topic:** Python and MySQL Database Operations

---

## 1. Introduction

During Week 2, we practised connecting Python with a MySQL database and performing basic database operations using Python.

The main purpose of these exercises was to understand how a Python application can communicate with a database, retrieve information, insert new records and delete existing records.

We used our Online Store Management System database for the practical exercises.

## 2. Database Used

**Database name:** `ecommerce_storedb`

**Table used:** `Product`

We mainly used the Product table to practise database operations.

### Product Table Structure

| Column | Data Type | Description |
|---|---|---|
| ProductID | INT | Unique product ID and primary key |
| Name | VARCHAR(100) | Product name |
| Category | VARCHAR(50) | Product category |
| Price | DECIMAL(10,2) | Product price |
| StockQuantity | INT | Available stock quantity |

### Example Product Records

| ProductID | Name | Category | Price | StockQuantity |
|---|---|---|---:|---:|
| 1 | Wireless Mouse | Electronics | 25.99 | 50 |
| 2 | Mechanical Keyboard | Electronics | 79.99 | 30 |
| 3 | USB-C Hub | Electronics | 39.99 | 40 |
| 4 | Laptop Stand | Accessories | 29.99 | 25 |
| 5 | Noise Cancelling Headphones | Electronics | 89.99 | 20 |
| 6 | Webcam HD | Electronics | 49.99 | 35 |
| 7 | Desk Lamp LED | Accessories | 19.99 | 45 |
| 8 | Notebook Pack | Stationery | 9.99 | 100 |

*Note: The prices and quantities above illustrate the initial sample records used in our exercises.*

## 3. Tools and Technologies

- Python
- MySQL Database
- MySQL Connector for Python (`mysql-connector-python`)
- Visual Studio Code
- MySQL Workbench

## 4. Connecting Python to MySQL

First, we established a connection between Python and our MySQL database.

### Code

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="ecommerce_storedb"
)

print("Connected to MySQL successfully!")

cursor = connection.cursor()
```

### Steps followed

1. Imported the `mysql.connector` library.
2. Entered the MySQL host, username, password and database name.
3. Established the database connection.
4. Created a cursor to execute SQL queries.

**Result:** Python successfully connected to the MySQL database.

## 5. Retrieving All Products – SELECT and fetchall()

We retrieved all records from the Product table using the SELECT statement.

### Code

```python
cursor.execute("SELECT * FROM Product")

products = cursor.fetchall()

for product in products:
    print(product)
```

### Steps followed

1. Executed a SELECT query to retrieve all products.
2. Used `fetchall()` to collect all returned records.
3. Stored the records in the `products` variable.
4. Used a `for` loop to display each product.

**Result:** All product records were displayed in the Python terminal.

## 6. Displaying Individual Product Details

We also practised accessing individual values from the returned product records using tuple indexing.

### Code

```python
for product in products:
    print(
        f"ID: {product[0]} | "
        f"Name: {product[1]} | "
        f"Category: {product[2]} | "
        f"Price: {product[3]} | "
        f"Stock: {product[4]}"
    )
```

### Steps followed

1. Retrieved product records from MySQL.
2. Used a `for` loop to access each product.
3. Used tuple indexes to access individual columns.
4. Displayed the product information in a readable format.

**Result:** Product details were displayed with clear labels.

## 7. Retrieving a Single Product – fetchone()

We practised retrieving one product record using `fetchone()`.

### Code

```python
cursor = connection.cursor(buffered=True)

cursor.execute("SELECT * FROM Product")

product = cursor.fetchone()

if product:
    print("Product ID:", product[0])
    print("Product Name:", product[1])
    print("Category:", product[2])
    print("Price:", product[3])
    print("Stock:", product[4])
```

### Steps followed

1. Created a buffered cursor.
2. Executed the SELECT query.
3. Used `fetchone()` to retrieve one record.
4. Checked whether a record was returned.
5. Displayed its individual values.

**Result:** One product record was retrieved and displayed.

## 8. Inserting a New Product – INSERT

We inserted a new product into the Product table using Python.

### Code

```python
sql = """
INSERT INTO Product (Name, Category, Price, StockQuantity)
VALUES (%s, %s, %s, %s)
"""

values = ("Bluetooth Speaker", "Electronics", 59.99, 75)

cursor.execute(sql, values)

connection.commit()

print("New Product ID:", cursor.lastrowid)
```

### Steps followed

1. Prepared an INSERT SQL statement.
2. Used `%s` placeholders for the product values.
3. Stored the new product details in a tuple.
4. Executed the query using `cursor.execute()`.
5. Used `connection.commit()` to save the changes.
6. Displayed the newly generated product ID.

**Result:** A new product was inserted into the database.

## 9. Inserting Multiple Products – executemany()

We also practised inserting multiple product records in one operation using `executemany()`.

### Code

```python
sql = """
INSERT INTO Product (Name, Category, Price, StockQuantity)
VALUES (%s, %s, %s, %s)
"""

values = [
    ("Wireless Charger", "Electronics", 24.99, 100),
    ("Gaming Mouse Pad", "Accessories", 14.99, 150),
    ("Office Chair", "Furniture", 149.99, 30)
]

cursor.executemany(sql, values)

connection.commit()

print(cursor.rowcount, "products inserted successfully!")
```

### Steps followed

1. Prepared an INSERT statement.
2. Created a list containing multiple product records.
3. Used `executemany()` to insert all records.
4. Committed the database transaction.
5. Displayed the number of inserted records.

**Result:** Multiple products were inserted into the Product table.

## 10. Deleting a Product – DELETE

Finally, we practised deleting a product record using Python.

### Code

```python
sql = "DELETE FROM Product WHERE ProductID = %s"

values = (9,)

cursor.execute(sql, values)

connection.commit()

print(cursor.rowcount, "product(s) deleted successfully!")
```

### Steps followed

1. Prepared a DELETE SQL statement.
2. Used the ProductID to identify the product.
3. Passed the product ID as a parameter.
4. Executed the DELETE statement.
5. Committed the changes.
6. Checked the number of deleted records using `rowcount`.

**Important:** We used a newly inserted product ID that was not referenced by the OrderItem table. The ID must be checked in the database before running the DELETE query.

**Result:** The selected product record was deleted from the Product table.

## 11. Closing the Database Connection

After completing the database operations, we closed the cursor and database connection.

### Code

```python
cursor.close()
connection.close()

print("Database connection closed.")
```

### Steps followed

1. Closed the cursor.
2. Closed the database connection.
3. Confirmed that the connection was closed.

## 12. Key Concepts Learned

During these exercises, we learned:

- How to connect Python with MySQL.
- How to create and use a database cursor.
- How to retrieve records using `SELECT`.
- The difference between `fetchone()` and `fetchall()`.
- How to access database values using tuple indexing.
- How to insert one record using `INSERT`.
- How to insert multiple records using `executemany()`.
- How to delete records using `DELETE`.
- Why `connection.commit()` is required to save database changes.
- How to close database connections properly.

## 13. Conclusion

In Week 2, we successfully practised the basic interaction between Python and MySQL using our Online Store Management System database.

We used the Product table to perform SELECT, INSERT and DELETE operations. These exercises helped us understand how Python can manage database records and how these operations can be used in a real application.

The knowledge gained will support the further development of our Online Store Management System, especially when implementing product management and CRUD functionality.

## 14. Next Steps

In the next learning sessions, we plan to:

1. Learn how to organise Python code into modules.
2. Practise updating existing database records using UPDATE.
3. Learn Git and version control.
4. Apply the database operations to our Online Store Management System project.
5. Continue developing product CRUD functionality.
