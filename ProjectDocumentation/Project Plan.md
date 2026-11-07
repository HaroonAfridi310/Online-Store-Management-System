# Project Plan – Online Store Management System

## 1. Project Overview

The aim of this project is to develop a Python-based Online Store Management System that allows store administrators to manage products and customer orders through a graphical user interface.

The application will use Streamlit for the user interface and MySQL for storing and managing data.

## 2. Project Purpose

The purpose is to create a simple system that makes it easier to manage product information, stock quantities and customer orders.

## 3. Intended Users

- Online store administrators.
- Staff responsible for product and order management.

## 4. Functional Requirements

- FR1: Add new products.
- FR2: View all products.
- FR3: Update existing product details.
- FR4: Delete products.
- FR5: Search products by name or category.
- FR6: Display product details, including price and stock quantity.
- FR7: Create and manage customer orders.
- FR8: Connect orders with products using the OrderItem table.
- FR9: Display order information and status.

## 5. Non-Functional Requirements

- Validate user input and display understandable error messages.
- Store database changes reliably.
- Provide a simple and user-friendly interface.
- Organise Python code into reusable functions and modules.
- Test important application functions.

## 6. Database

**Database:** `ecommerce_storedb`

**Main tables:**
- Customer
- Product
- Order
- OrderItem
- Payment

The Product table stores product information, including ProductID, Name, Category, Price and StockQuantity.

The Order and OrderItem tables are used to manage customer orders and their related products.

## 7. Technologies

- Python – application logic and backend.
- Streamlit – graphical user interface.
- MySQL – database management.
- mysql-connector-python – Python and MySQL connection.
- GitHub – source code management and collaboration.
- pytest – automated testing.

## 8. Project Milestones

| Week | Main activities |
|---|---|
| Weeks 1–2 | Project planning, requirements and initial database preparation |
| Week 3 | Python–MySQL connection and database integration |
| Weeks 4–5 | Product and Order CRUD operations and Streamlit interface |
| Week 6 | Testing, validation and error handling |
| Week 7 | Documentation and final improvements |
| Week 8 | Final testing, demonstration and submission |

## 9. Team Organisation

The project is divided among four members:

- Haroon Afridi – Database Management
- Pradeep Sapkota – Product Module and Backend
- Poshan Oli – Order Module
- Lamyae Echaoui – Testing, Documentation and Collaboration

Detailed responsibilities and weekly assignments are maintained in `team-workflow.md`.

## 10. Expected Outcome

The final result will be a working Online Store Management System with product management, product searching, order processing, MySQL database integration and a Streamlit interface. The application will be tested and documented before submission.
