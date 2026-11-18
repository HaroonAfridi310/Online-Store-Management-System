# Online Store Management System

## 1. Project Overview

The Online Store Management System is a Python application developed to help store administrators manage products, stock, customers, orders, and payments.

The application uses Streamlit for its user interface and MySQL for database management.

## 2. Main Features

- **Product Management:** View, search, add, and delete products.
- **Stock Management:** Increase stock quantities for existing products.
- **Order Management:** Create orders, view order details, update order status, and delete eligible unpaid orders.
- **Payment Management:** Record payments and view payment details.
- **Data Validation:** Validate user input before processing operations.
- **Database Transactions:** Use commit and rollback to maintain database consistency.
- **Error Handling:** Handle database and application errors.

## 3. Technologies Used

- Python
- Streamlit
- MySQL
- MySQL Connector/Python
- Python-dotenv
- Pytest
- Git and GitHub

## 4. Project Structure

```text
python_mysql/
│
├── ApplicationScreenshots/
│
├── Database/
│   └── Ecommerce.sql
│
├── ProjectDocumentation/
│   ├── Daily Progress.md
│   ├── Project Plan.md
│   ├── Week 1 Detailed Progress Report.md
│   ├── Week 2 Detailed Progress Report.md
│   └── Week 3 Detailed Progress Report.md
│
├── Tests/
│   ├── test_order_operations.py
│   ├── test_product_operations.py
│   └── test_stock_operations.py
│
├── app.py
├── database.py
├── main.py
├── order_operations.py
├── product_operations.py
├── stock_operations.py
├── validation.py
├── requirements.txt
├── readme.md
└── .gitignore
```

## 5. Installation and Setup

### Requirements

- Python installed on your computer
- MySQL Server
- MySQL Workbench (recommended)

### Step 1: Download the project

Clone the repository or download the project files and open the project folder in VS Code.

### Step 2: Create a virtual environment

Open the terminal in the project folder and run:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate
```

### Step 3: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Set up the database

1. Open MySQL Workbench.
2. Open `Database/Ecommerce.sql`.
3. Execute the SQL script to create the database tables and sample data.

The database contains five main tables:

- **Customer:** Stores customer information.
- **Product:** Stores product details and stock quantities.
- **orders:** Stores customer orders and their status.
- **OrderItem:** Stores the products and quantities included in each order.
- **Payment:** Stores payment information.

### Step 5: Configure the database password

Create a `.env` file in the project root directory.

Add your MySQL password:

```env
MYSQL_PASSWORD=your_mysql_password
```

Replace `your_mysql_password` with your own MySQL password.

Keep `.env` private and do not upload it to GitHub.

## 6. Run the Application

With the virtual environment activated, run:

```powershell
python -m streamlit run app.py
```

Streamlit will open the application in your web browser.

## 7. Run Tests

To run the automated tests, execute:

```powershell
python -m pytest -v
```

### Test Results

The project currently has **28 passing tests** covering:

- Order operations
- Product operations
- Stock management
- Input validation
- Database error handling and rollback

Latest recorded test result: **28 passed**.

## 8. Project Documentation

Additional project documents are available in the `ProjectDocumentation` folder:

- Daily Progress
- Project Plan
- Week 1 Detailed Progress Report
- Week 2 Detailed Progress Report
- Week 3 Detailed Progress Report
- Week 4 Detailed Progress Report


Application screenshots are available in the `ApplicationScreenshots` folder.

## 9. Project Team

- Haroon Afridi
- Pradeep Sapkota
- Poshan Oli
- Lamyae Echaoui

