# Software Development – Week 1 Progress Report

**Group Members:**
1. Haroon Afridi
2. Pradeep Sapkota
3. Poshan Oli
4. Lamyae Echaoui

**Week:** Week 1  
**Topic:** Project Introduction, Requirements Analysis and Planning

---

## 1. Introduction

During Week 1, our group started planning the Online Store Management System project. The main purpose was to understand the project requirements, identify the main features, review the existing database and divide responsibilities among the four group members.

We discussed how the application would manage products, customers, orders and payments using Python, MySQL and Streamlit.

## 2. Project Overview

The Online Store Management System is a Python-based application designed to manage basic online store operations.

The system aims to provide the following features:

- Manage product information.
- Add, view, update and delete products.
- Search products by name or category.
- Manage customer information.
- Create and manage customer orders.
- Connect orders with products.
- Display order information and status.
- Store and manage information in a MySQL database.

## 3. Project Requirements

During the planning stage, we identified the following main requirements.

### Functional Requirements

1. Add new products to the database.
2. Display all available products.
3. Update existing product information.
4. Delete products from the database.
5. Search products by name or category.
6. Manage customer information.
7. Create new customer orders.
8. Connect orders with products using the OrderItem table.
9. Display order details and status.

### Non-Functional Requirements

- The application should be simple and user-friendly.
- Database operations should work correctly.
- The system should provide accurate information.
- The application should be organised and easy to maintain.
- The system should handle errors appropriately.

## 4. Database Review

Our group reviewed the existing MySQL database, `ecommerce_storedb`, which will be used for the project.

The database contains the following main tables:

| Table | Purpose |
|---|---|
| Customer | Stores customer information |
| Product | Stores product details, prices and stock quantities |
| Order | Stores customer order information |
| OrderItem | Connects orders with individual products |
| Payment | Stores payment information |

We also discussed the relationships between the tables and how they will support the main application features.

## 5. Technologies and Tools

The following technologies and tools were selected for the project:

| Technology / Tool | Purpose |
|---|---|
| Python | Backend programming |
| MySQL | Database management |
| Streamlit | User interface |
| mysql-connector-python | Connecting Python with MySQL |
| GitHub | Code sharing and version control |
| pytest | Automated testing |
| Visual Studio Code | Development environment |

## 6. Division of Team Responsibilities

The group divided the main project responsibilities among four members.

### Haroon Afridi – Database Management

- Maintain the existing MySQL database.
- Review database structure and relationships.
- Support database changes and integration.
- Help team members with SQL queries and database operations.

### Pradeep Sapkota – Product Module and Backend

- Develop Python database connection functions.
- Implement Product CRUD operations.
- Develop product management pages using Streamlit.
- Implement product listing and searching.

### Poshan Oli – Order Module

- Develop the Order section using Streamlit.
- Implement order creation and processing.
- Connect orders with products through OrderItem.
- Display order details and status.

### Lamyae Echaoui – Testing and Documentation

- Maintain the GitHub repository.
- Prepare and update project documentation.
- Develop automated tests using pytest.
- Coordinate team contributions and prepare the final presentation.

## 7. Project Planning and Milestones

The group discussed the main development stages and prepared an initial project timeline.

| Week | Planned Activities |
|---|---|
| Week 1 | Project introduction, requirements and planning |
| Week 2 | Python and MySQL database practice |
| Week 3 | Database integration |
| Week 4 | Product and Order module development |
| Week 5 | Feature completion and integration |
| Week 6 | Testing and error handling |
| Week 7 | Documentation and improvements |
| Week 8 | Final testing and presentation |

## 8. Problems and Challenges

During the planning stage, the main challenges were:

- Understanding the complete project requirements.
- Reviewing the existing database structure.
- Deciding how to divide responsibilities among group members.
- Planning how the different modules would work together.
- Organising the project files and GitHub repository.

These points were discussed during the initial planning process to prepare for the development stages.

## 9. Learning Outcomes

By the end of Week 1, our group:

- Understood the main purpose of the Online Store Management System.
- Identified the main functional and non-functional requirements.
- Reviewed the existing MySQL database and its tables.
- Selected the technologies required for development.
- Divided responsibilities among all four group members.
- Prepared an initial development plan and project timeline.
- Established a basic workflow for collaboration through GitHub.

## 10. Conclusion

Week 1 focused mainly on understanding, discussing and planning the Online Store Management System. The group identified the project requirements, reviewed the database, selected the development tools and divided responsibilities among the members.

This planning stage provided a foundation for the practical Python and MySQL exercises carried out in Week 2 and the upcoming application development work.
