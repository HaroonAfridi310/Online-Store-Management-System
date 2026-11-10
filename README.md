# Online Store Management System

## 1. Project Overview

The Online Store Management System is a Python application developed to manage the main operations of an online store. It uses MySQL to store information and Streamlit to provide a simple graphical user interface.

The application allows store administrators to manage products, create customer orders, update order statuses and record payments.

## 2. Project Objectives

- Develop a working Python application.
- Connect Python with a MySQL database.
- Implement database operations using Python.
- Provide a user-friendly interface using Streamlit.
- Manage products, orders and payments.
- Validate user input and handle errors.
- Test the application and document the development process.

## 3. Intended Users

Store administrators and employees responsible for managing products, customer orders and payments.

## 4. Main Features

### Product Management
- View all available products.
- Search products by name or category.
- Find a product using its ID.
- Add new products.
- Delete products.

### Order Management
- Create orders for existing customers.
- Select multiple products for an order.
- Set product quantities.
- Calculate the total order amount.
- View all orders and order details.
- Update order statuses.

### Payment Management
- Record payments for orders.
- Select a payment method.
- Display payment information.
- View payment status, method, amount and date.
- Automatically change an order status from Pending to Processing after successful payment.

## 5. Database

The application uses MySQL.

**Database name:** `ecommerce_storedb`

The main database tables are:

| Table | Purpose |
|---|---|
| Customer | Stores customer information. |
| Product | Stores product names, categories, prices and stock quantities. |
| orders | Stores customer order information and status. |
| OrderItem | Connects orders with products and stores quantities and unit prices. |
| Payment | Stores payment information related to orders. |

The tables are connected through primary keys and foreign keys to maintain relationships between customers, products, orders and payments.

## 6. Technologies Used

- Python
- MySQL
- MySQL Connector
- Streamlit
- python-dotenv
- Git and GitHub
- pytest (for automated testing)

## 7. Project Structure

```text
python_mysql/
│
├── Database/
│   └── Ecomerce.sql
│
├── ProjectDocumentation/
│   ├── Daily Progress.md
│   ├── Project Plan.md
│   ├── Team WOrkflow.md
│   ├── Week 1 Detailed Progress Report.md
│   └── Week 2 Detailed Progress Report.md
│
├── database.py
├── product_operations.py
├── order_operations.py
├── main.py
├── app.py
├── requirements.txt
├── readme.md
└── .gitignore
```

The `.env` file contains the local database password and should not be uploaded to GitHub.

## 8. Installation and Setup

### Requirements

- Python installed on the computer.
- MySQL Server.
- Visual Studio Code.
- Git.

### Step 1: Clone the repository

```bash
git clone https://github.com/HaroonAfridi310/Online-Store-Management-System.git
```

Open the project folder in Visual Studio Code.

### Step 2: Create and activate a virtual environment

```bash
python -m venv .venv
```

In PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install the required packages

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure the database

Create the MySQL database and import the SQL file located in the `Database` folder.

Create a `.env` file in the main project folder and add:

```text
MYSQL_PASSWORD=your_actual_mysql_password
```

Replace the example value with your local MySQL password.

Do not upload the `.env` file to GitHub.

### Step 5: Run the application

```bash
python -m streamlit run app.py
```

Streamlit will open the application in your web browser.

## 9. Team Contributions

| Team Member | Responsibility |
|---|---|
| Haroon Afridi | Database management and integration |
| Pradeep Sapkota | Product module and backend development |
| Poshan Oli | Order management module |
| Lamyae Echaoui | Testing, documentation and collaboration |

Team members collaborate on integration, testing and project improvements.

## 10. Development Plan

1. Finalize project requirements and structure.
2. Connect Python to the MySQL database.
3. Implement product operations.
4. Develop order management.
5. Implement payment management.
6. Build the Streamlit interface.
7. Perform application testing and debugging.
8. Complete documentation and prepare the final demonstration.

## 11. Testing

The application will be tested to check:

- Database connectivity.
- Product operations.
- Order creation and calculations.
- Stock quantity updates.
- Order status changes.
- Payment recording.
- Input validation and error handling.

Automated tests will be developed using pytest.

## 12. Future Improvements

- Add product update functionality.
- Add customer management operations.
- Improve input validation.
- Expand automated test coverage.
- Improve the user interface.
