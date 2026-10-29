use ecommerce_storeDB;

-- 1. Customer
CREATE TABLE Customer (
    CustomerID      INT PRIMARY KEY AUTO_INCREMENT,
    FirstName       VARCHAR(50) NOT NULL,
    MiddleName      VARCHAR(50),                 -- Optional
    LastName        VARCHAR(50) NOT NULL,
    Email           VARCHAR(100) NOT NULL UNIQUE,
    Phone           VARCHAR(20),
    Address         VARCHAR(200)
);

-- 2. Product
CREATE TABLE Product (
    ProductID       INT PRIMARY KEY AUTO_INCREMENT,
    Name            VARCHAR(100) NOT NULL,
    Category        VARCHAR(50),
    Price           DECIMAL(10,2) NOT NULL CHECK (Price > 0),
    StockQuantity   INT NOT NULL DEFAULT 0 CHECK (StockQuantity >= 0)
);

-- 3. Order
CREATE TABLE `Order` (
    OrderID         INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID      INT NOT NULL,
    OrderDate       DATETIME DEFAULT CURRENT_TIMESTAMP,
    OrderStatus     VARCHAR(20),
    TotalAmount     DECIMAL(12,2) DEFAULT 0.00,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- 4. Order Item (Weak Entity)
CREATE TABLE OrderItem (
    OrderItem_ID    INT PRIMARY KEY AUTO_INCREMENT,
    OrderID         INT NOT NULL,
    ProductID       INT NOT NULL,
    Quantity        INT NOT NULL CHECK (Quantity > 0),
    UnitPrice       DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    UNIQUE (OrderID, ProductID)                       -- Prevent same product twice in one order
);

-- 5. Payment
CREATE TABLE Payment (
    PaymentID       INT PRIMARY KEY AUTO_INCREMENT,
    OrderID         INT NOT NULL UNIQUE,          -- 1:1 relationship
    Amount          DECIMAL(12,2) NOT NULL,
    Method          VARCHAR(50),
    PaymentDate     DATETIME,
    PaymentStatus   VARCHAR(20),
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID)
);

-- Customers
INSERT INTO Customer (FirstName, MiddleName, LastName, Email, Phone, Address) VALUES
('John', NULL, 'Smith', 'john.smith@email.com', '555-0101', '123 Main St, New York'),
('Emily', 'A', 'Johnson', 'emily.j@email.com', '555-0102', '456 Oak Ave, Los Angeles'),
('Michael', NULL, 'Brown', 'michael.b@email.com', '555-0103', '789 Pine Rd, Chicago'),
('Sarah', NULL, 'Davis', 'sarah.d@email.com', '555-0104', '321 Elm St, Houston'),
('David', 'R', 'Wilson', 'david.w@email.com', '555-0105', '654 Maple Dr, Phoenix');

-- Products
INSERT INTO Product (Name, Category, Price, StockQuantity) VALUES
('Wireless Mouse', 'Electronics', 29.99, 150),
('Mechanical Keyboard', 'Electronics', 89.99, 80),
('USB-C Hub', 'Electronics', 49.99, 120),
('Laptop Stand', 'Accessories', 39.99, 200),
('Noise Cancelling Headphones', 'Electronics', 199.99, 60),
('Webcam HD', 'Electronics', 69.99, 90),
('Desk Lamp LED', 'Home', 34.99, 110),
('Notebook Pack', 'Stationery', 19.99, 300);

-- Orders
INSERT INTO `Order` (CustomerID, OrderDate, OrderStatus, TotalAmount) VALUES
(1, '2025-01-15 10:30:00', 'Delivered', 119.97),
(2, '2025-01-16 14:20:00', 'Shipped', 289.97),
(1, '2025-01-20 09:15:00', 'Processing', 69.98),
(3, '2025-02-01 16:45:00', 'Delivered', 199.99),
(4, '2025-02-05 11:00:00', 'Pending', 139.97),
(5, '2025-02-10 13:30:00', 'Cancelled', 49.99),
(2, '2025-02-12 08:50:00', 'Delivered', 89.99);

-- Order Items
INSERT INTO OrderItem (OrderID, ProductID, Quantity, UnitPrice) VALUES
(1, 1, 2, 29.99),
(1, 3, 1, 49.99),
(2, 5, 1, 199.99),
(2, 2, 1, 89.99),
(3, 4, 1, 39.99),
(3, 1, 1, 29.99),
(4, 5, 1, 199.99),
(5, 2, 1, 89.99),
(5, 7, 1, 34.99),
(5, 8, 1, 19.99),
(6, 3, 1, 49.99),
(7, 2, 1, 89.99);

-- Payments
INSERT INTO Payment (OrderID, Amount, Method, PaymentDate, PaymentStatus) VALUES
(1, 119.97, 'Credit Card', '2025-01-15 10:35:00', 'Completed'),
(2, 289.97, 'PayPal', '2025-01-16 14:25:00', 'Completed'),
(3, 69.98, 'Debit Card', '2025-01-20 09:20:00', 'Completed'),
(4, 199.99, 'Credit Card', '2025-02-01 16:50:00', 'Completed'),
(5, 139.97, 'Bank Transfer', '2025-02-05 11:05:00', 'Pending'),
(6, 49.99, 'Credit Card', '2025-02-10 13:35:00', 'Refunded'),
(7, 89.99, 'PayPal', '2025-02-12 08:55:00', 'Completed');

SELECT * FROM ecommerce_storedb.customer;
SELECT * FROM ecommerce_storedb.order;
SELECT * FROM ecommerce_storedb.orderitem;
SELECT * FROM ecommerce_storedb.payment;
SELECT * FROM ecommerce_storedb.product;