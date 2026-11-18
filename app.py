
import logging

import mysql.connector
import streamlit as st

from database import get_connection

from product_operations import (
    get_all_products,
    search_products,
    get_product_by_id,
    add_products,
    delete_product
)

from stock_operations import increase_product_stock

from order_operations import (
    create_order,
    get_all_orders,
    get_order_details,
    update_order_status,
    record_payment,
    delete_order
)


# ==================================================
# LOGGING AND SESSION STATE
# ==================================================

logger = logging.getLogger(__name__)

DB_ERROR = object()

if "add_product_form_version" not in st.session_state:
    st.session_state.add_product_form_version = 0

if "product_added_flash" in st.session_state:
    st.success(st.session_state.product_added_flash)
    del st.session_state.product_added_flash

if "product_restocked_flash" in st.session_state:
    st.success(st.session_state.product_restocked_flash)
    del st.session_state.product_restocked_flash


def database_call(action, function, *args):
    """Run a database operation and handle database errors safely."""

    try:
        return function(*args)

    except mysql.connector.Error:
        logger.exception("Database error while trying to %s.", action)

        st.error(
            f"Could not {action}. Please try again later."
        )

        return DB_ERROR


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def get_customers():
    """Return all customers."""

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT CustomerID, FirstName, LastName
            FROM customer
            ORDER BY CustomerID
        """)

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        connection.close()


def get_product_categories():
    """Return all existing product categories."""

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT DISTINCT Category
            FROM Product
            WHERE Category IS NOT NULL
              AND TRIM(Category) <> ''
            ORDER BY Category
        """)

        return [
            row[0] for row in cursor.fetchall()
        ]

    finally:
        if cursor:
            cursor.close()

        connection.close()


def get_order_items(order_id):
    """Return all products belonging to an order."""

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                oi.ProductID,
                p.Name,
                oi.Quantity,
                oi.UnitPrice,
                oi.Quantity * oi.UnitPrice
            FROM orderitem oi
            JOIN Product p ON oi.ProductID = p.ProductID
            WHERE oi.OrderID = %s
        """, (order_id,))

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        connection.close()


def get_payment_details(order_id):
    """Return payment information for an order."""

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                PaymentID,
                Amount,
                Method,
                PaymentDate,
                PaymentStatus
            FROM payment
            WHERE OrderID = %s
        """, (order_id,))

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        connection.close()


# ==================================================
# APPLICATION SETTINGS
# ==================================================

st.set_page_config(
    page_title="Online Store Management",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Online Store Management System")
st.caption("Manage products, orders and payments.")

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Products",
        "Create Order",
        "Orders",
        "Payments"
    ]
)


# ==================================================
# 1. PRODUCT MANAGEMENT
# ==================================================

if page == "Products":

    st.header("Product Management")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "All Products",
        "Search Product",
        "Add Product",
        "Restock Existing Product",
        "Delete Product"
    ])

    with tab1:

        st.subheader("Available Products")

        if st.button("Refresh Products"):
            st.rerun()

        products = database_call(
            "load products",
            get_all_products
        )

        if products is DB_ERROR:
            pass

        elif products:

            st.dataframe(
                [
                    {
                        "Product ID": p[0],
                        "Name": p[1],
                        "Category": p[2],
                        "Price (€)": float(p[3]),
                        "Stock": p[4]
                    }
                    for p in products
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No products available.")

    with tab2:

        search_type = st.radio(
            "Search method",
            [
                "Search by name or category",
                "Find by Product ID"
            ]
        )

        if search_type == "Search by name or category":

            keyword = st.text_input(
                "Enter product name or category"
            )

            if st.button("Search"):

                try:

                    results = search_products(keyword)

                    if results:

                        st.dataframe(
                            [
                                {
                                    "Product ID": p[0],
                                    "Name": p[1],
                                    "Category": p[2],
                                    "Price (€)": float(p[3]),
                                    "Stock": p[4]
                                }
                                for p in results
                            ],
                            use_container_width=True,
                            hide_index=True
                        )

                    else:
                        st.warning("No matching products found.")

                except ValueError as error:
                    st.error(str(error))

                except mysql.connector.Error:

                    logger.exception(
                        "Database error while searching products."
                    )

                    st.error(
                        "Could not search products. Please try again later."
                    )

        else:

            product_id = st.number_input(
                "Enter Product ID",
                min_value=1,
                step=1
            )

            if st.button("Find Product"):

                product = database_call(
                    "find the product",
                    get_product_by_id,
                    int(product_id)
                )

                if product is DB_ERROR:
                    pass

                elif product:

                    st.write(f"**Name:** {product[1]}")
                    st.write(f"**Category:** {product[2]}")
                    st.write(f"**Price:** €{product[3]}")
                    st.write(f"**Stock:** {product[4]}")

                else:
                    st.warning("Product not found.")

    with tab3:

        st.subheader("Add New Product")

        categories = database_call(
            "load product categories",
            get_product_categories
        )

        if categories is DB_ERROR:
            categories = []

        st.caption(
            "Choose an existing category or enter a new one. "
            "Examples: Electronics, Accessories, Home, Stationery."
        )

        form_version = st.session_state.add_product_form_version

        category_options = [
            "Select an existing category"
        ] + categories

        with st.form(f"add_product_form_{form_version}"):

            name = st.text_input(
                "Product Name",
                key=f"product_name_{form_version}"
            )

            selected_category = st.selectbox(
                "Choose an existing category",
                category_options,
                key=f"product_category_{form_version}"
            )

            new_category = st.text_input(
                "Or enter a new category",
                key=f"new_product_category_{form_version}"
            )

            price = st.number_input(
                "Price (€)",
                min_value=0.01,
                value=10.00,
                step=0.50,
                key=f"product_price_{form_version}"
            )

            stock = st.number_input(
                "Stock Quantity",
                min_value=0,
                step=1,
                key=f"product_stock_{form_version}"
            )

            submitted = st.form_submit_button("Add Product")

            if submitted:

                if new_category.strip():
                    category = new_category.strip()

                elif selected_category != "Select an existing category":
                    category = selected_category

                else:
                    category = ""

                try:

                    result = add_products(
                        name,
                        category,
                        price,
                        int(stock)
                    )

                except ValueError as error:

                    st.error(str(error))

                except mysql.connector.Error:

                    logger.exception(
                        "Database error while adding product."
                    )

                    st.error(
                        "Could not add the product. "
                        "Please try again later."
                    )

                else:

                    if result:

                        st.session_state.product_added_flash = (
                            "Product added successfully!"
                        )

                        st.session_state.add_product_form_version += 1

                        st.rerun()

    with tab4:

        st.subheader("Restock Existing Product")

        st.caption(
            "Select a product already in the database and add units to its "
            "current stock. This updates the existing product; it does not "
            "create another product record."
        )

        products_for_restock = database_call(
            "load products for restocking",
            get_all_products
        )

        if products_for_restock is DB_ERROR:
            pass

        elif products_for_restock:

            restock_options = {
                (
                    f"{product[0]} - {product[1]} "
                    f"(Current stock: {product[4]})"
                ): product
                for product in products_for_restock
            }

            selected_restock_label = st.selectbox(
                "Select existing product",
                list(restock_options.keys()),
                key="restock_product_selection"
            )

            selected_restock_product = restock_options[
                selected_restock_label
            ]

            st.write(
                f"**Product:** {selected_restock_product[1]}"
            )
            st.write(
                f"**Current stock:** {selected_restock_product[4]} units"
            )

            restock_quantity = st.number_input(
                "Additional units to add",
                min_value=1,
                value=1,
                step=1,
                key="restock_quantity"
            )

            if st.button("Increase Stock", key="increase_product_stock"):

                try:

                    result = increase_product_stock(
                        int(selected_restock_product[0]),
                        int(restock_quantity)
                    )

                except ValueError as error:

                    st.error(str(error))

                except mysql.connector.Error:

                    logger.exception(
                        "Database error while increasing product stock."
                    )

                    st.error(
                        "Could not increase product stock. "
                        "Please try again later."
                    )

                else:

                    if result:

                        st.session_state.product_restocked_flash = (
                            f"Stock increased successfully for "
                            f"{selected_restock_product[1]}."
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "Stock was not updated. Please check the product."
                        )

        else:

            st.info("No products are available to restock.")

    with tab5:

        st.subheader("Delete Product")

        products = database_call(
            "load products",
            get_all_products
        )

        if products is DB_ERROR:
            pass

        elif products:

            product_options = {
                f"{p[0]} - {p[1]}": p[0]
                for p in products
            }

            selected_product = st.selectbox(
                "Select product",
                list(product_options.keys())
            )

            confirm_delete = st.checkbox(
                "I confirm that I want to delete this product."
            )

            if st.button("Delete Selected Product"):

                if not confirm_delete:

                    st.warning(
                        "Please confirm before deleting."
                    )

                else:

                    try:

                        result = delete_product(
                            int(product_options[selected_product])
                        )

                    except ValueError as error:

                        st.error(str(error))

                    except mysql.connector.Error:

                        logger.exception(
                            "Database error while deleting product."
                        )

                        st.error(
                            "Could not delete the product. "
                            "It may be linked to an existing order."
                        )

                    else:

                        if result:

                            st.success("Product deleted successfully!")
                            st.rerun()

                        else:

                            st.warning(
                                "Product was not found or was not deleted."
                            )

        else:
            st.info("No products available.")


# ==================================================
# 2. CREATE ORDER
# ==================================================

elif page == "Create Order":

    st.header("Create New Order")

    customers = database_call(
        "load customers",
        get_customers
    )

    products = database_call(
        "load products",
        get_all_products
    )

    if customers is DB_ERROR or products is DB_ERROR:
        pass

    elif not customers:

        st.warning("No customers found in the database.")

    elif not products:

        st.warning("No products available.")

    else:

        customer_options = {
            f"{c[0]} - {c[1]} {c[2]}": c[0]
            for c in customers
        }

        selected_customer = st.selectbox(
            "Select Customer",
            list(customer_options.keys())
        )

        available_products = [
            p for p in products if p[4] > 0
        ]

        if not available_products:

            st.warning("There are no products currently in stock.")

        else:

            product_options = {
                f"{p[0]} - {p[1]} (€{p[3]}) - Stock: {p[4]}": p
                for p in available_products
            }

            selected_products = st.multiselect(
                "Select Products",
                list(product_options.keys())
            )

            items = []
            invalid_quantity = False

            for selected in selected_products:

                product = product_options[selected]
                available_stock = int(product[4])

                quantity = st.number_input(
                    f"Quantity for {product[1]}",
                    min_value=1,
                    value=1,
                    step=1,
                    key=f"quantity_{product[0]}"
                )

                quantity = int(quantity)

                if quantity > available_stock:

                    st.warning(
                        f"Low stock: only {available_stock} units of "
                        f"{product[1]} are available. "
                        f"You entered {quantity}."
                    )

                    invalid_quantity = True

                items.append(
                    (int(product[0]), quantity)
                )

            if items:

                total = sum(
                    product_options[selected][3] * quantity
                    for selected, (_, quantity) in zip(
                        selected_products,
                        items
                    )
                )

                st.write(f"**Order Total: €{total:.2f}**")

            if st.button(
                "Create Order",
                disabled=not items or invalid_quantity
            ):

                customer_id = int(
                    customer_options[selected_customer]
                )

                try:

                    order_id = create_order(
                        customer_id,
                        items
                    )

                except ValueError as error:

                    st.error(str(error))

                except mysql.connector.Error:

                    logger.exception(
                        "Database error while creating order."
                    )

                    st.error(
                        "Could not create the order. "
                        "Please try again later."
                    )

                else:

                    st.success(
                        f"Order created successfully! Order ID: {order_id}"
                    )

                    st.balloons()


# ==================================================
# 3. ORDER MANAGEMENT
# ==================================================

elif page == "Orders":

    st.header("Order Management")

    orders = database_call(
        "load orders",
        get_all_orders
    )

    if orders is DB_ERROR:
        pass

    elif orders:

        st.subheader("All Orders")

        st.dataframe(
            [
                {
                    "Order ID": o[0],
                    "Customer ID": o[1],
                    "Customer": f"{o[2]} {o[3]}",
                    "Order Date": str(o[4]),
                    "Status": o[5],
                    "Total (€)": float(o[6])
                }
                for o in orders
            ],
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        tab1, tab2, tab3 = st.tabs([
            "Order Details",
            "Update Order Status",
            "Delete Order"
        ])

        # --------------------------------------------------
        # ORDER DETAILS
        # --------------------------------------------------

        with tab1:

            order_ids = [
                o[0] for o in orders
            ]

            selected_order = st.selectbox(
                "Select Order ID",
                order_ids,
                key="details_order"
            )

            if st.button("View Order Details"):

                order = database_call(
                    "load order details",
                    get_order_details,
                    int(selected_order)
                )

                if order is DB_ERROR:
                    pass

                elif order:

                    st.subheader(f"Order #{order[0]}")

                    col1, col2 = st.columns(2)

                    col1.write(f"**Customer ID:** {order[1]}")
                    col1.write(f"**Order Date:** {order[2]}")

                    col2.write(f"**Status:** {order[3]}")
                    col2.write(f"**Total:** €{order[4]}")

                    order_items = database_call(
                        "load order products",
                        get_order_items,
                        int(selected_order)
                    )

                    if order_items is not DB_ERROR:

                        st.subheader("Products in this order")

                        if order_items:

                            st.dataframe(
                                [
                                    {
                                        "Product ID": i[0],
                                        "Product": i[1],
                                        "Quantity": i[2],
                                        "Unit Price (€)": float(i[3]),
                                        "Subtotal (€)": float(i[4])
                                    }
                                    for i in order_items
                                ],
                                use_container_width=True,
                                hide_index=True
                            )

                        else:
                            st.info("No products found for this order.")

                    st.divider()
                    st.subheader("Payment Information")

                    payment = database_call(
                        "load payment information",
                        get_payment_details,
                        int(selected_order)
                    )

                    if payment is DB_ERROR:
                        pass

                    elif payment:

                        st.success(
                            f"Payment recorded — {payment[4]}"
                        )

                        payment_col1, payment_col2 = st.columns(2)

                        payment_col1.metric(
                            "Payment Status",
                            payment[4]
                        )

                        payment_col2.metric(
                            "Payment Method",
                            payment[2]
                        )

                        payment_col3, payment_col4 = st.columns(2)

                        payment_col3.write(
                            f"**Payment ID:** {payment[0]}"
                        )

                        payment_col4.write(
                            f"**Amount Paid:** €{payment[1]}"
                        )

                        st.write(
                            f"**Payment Date:** {payment[3]}"
                        )

                    else:

                        st.info(
                            "Payment has not yet been recorded for this order."
                        )

                else:
                    st.error("Order not found.")

        # --------------------------------------------------
        # UPDATE ORDER STATUS
        # --------------------------------------------------

        with tab2:

            selected_status_order = st.selectbox(
                "Select Order",
                [o[0] for o in orders],
                key="status_order"
            )

            new_status = st.selectbox(
                "New Order Status",
                [
                    "Pending",
                    "Processing",
                    "Shipped",
                    "Delivered"
                ]
            )

            if st.button("Update Status"):

                try:

                    result = update_order_status(
                        int(selected_status_order),
                        new_status
                    )

                except ValueError as error:

                    st.error(str(error))

                except mysql.connector.Error:

                    logger.exception(
                        "Database error while updating order status."
                    )

                    st.error(
                        "Could not update the order status. "
                        "Please try again later."
                    )

                else:

                    if result:

                        st.success(
                            "Order status updated successfully!"
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "Order not found or status was unchanged."
                        )

        # --------------------------------------------------
        # DELETE ORDER
        # --------------------------------------------------

        with tab3:

            st.subheader("Delete an Unpaid Order")

            st.warning(
                "Deleting an order restores its product quantities "
                "to stock. This action cannot be undone."
            )

            delete_order_options = {
                (
                    f"Order {o[0]} - {o[2]} {o[3]} "
                    f"- {o[5]} - €{o[6]}"
                ): o[0]
                for o in orders
            }

            selected_delete_order = st.selectbox(
                "Select an order to delete",
                list(delete_order_options.keys()),
                key="delete_order_selection"
            )

            selected_delete_order_id = int(
                delete_order_options[selected_delete_order]
            )

            delete_order_info = database_call(
                "check selected order",
                get_order_details,
                selected_delete_order_id
            )

            delete_payment_info = database_call(
                "check order payment",
                get_payment_details,
                selected_delete_order_id
            )

            if (
                delete_order_info is not DB_ERROR
                and delete_payment_info is not DB_ERROR
            ):

                current_status = delete_order_info[3]

                if delete_payment_info:

                    st.error(
                        "This order has a recorded payment. "
                        "It cannot be deleted."
                    )

                elif current_status in ("Shipped", "Delivered"):

                    st.error(
                        f"This order is {current_status}. "
                        "Shipped and Delivered orders cannot be deleted."
                    )

                elif current_status not in ("Pending", "Processing"):

                    st.error(
                        "This order cannot be deleted because its status "
                        "does not allow deletion."
                    )

                else:

                    st.info(
                        f"Order status: {current_status}. "
                        "No payment has been recorded. "
                        "This order can be deleted."
                    )

                    confirm_delete_order = st.checkbox(
                        "I understand that this will delete the order "
                        "and restore its products to stock.",
                        key="confirm_delete_order"
                    )

                    if st.button(
                        "Delete Selected Order",
                        disabled=not confirm_delete_order
                    ):

                        try:

                            result = delete_order(
                                selected_delete_order_id
                            )

                        except ValueError as error:

                            st.error(str(error))

                        except mysql.connector.Error:

                            logger.exception(
                                "Database error while deleting order."
                            )

                            st.error(
                                "Could not delete the order. "
                                "No changes have been saved."
                            )

                        else:

                            if result:

                                st.success(
                                    f"Order {selected_delete_order_id} "
                                    "was deleted and its stock was restored."
                                )

                                st.rerun()

                            else:

                                st.error("The order could not be deleted.")

    else:
        st.info("No orders found.")


# ==================================================
# 4. PAYMENT MANAGEMENT
# ==================================================

elif page == "Payments":

    st.header("Payment Management")

    orders = database_call(
        "load orders",
        get_all_orders
    )

    if orders is DB_ERROR:
        pass

    elif orders:

        order_options = {
            f"Order {o[0]} - {o[2]} {o[3]} - €{o[6]}": o
            for o in orders
        }

        selected_payment_order = st.selectbox(
            "Select Order",
            list(order_options.keys())
        )

        order = order_options[selected_payment_order]
        order_id = int(order[0])

        st.subheader("Order Information")

        col1, col2 = st.columns(2)

        col1.write(f"**Order ID:** {order_id}")
        col1.write(f"**Customer:** {order[2]} {order[3]}")

        col2.write(f"**Order Total:** €{order[6]}")
        col2.write(f"**Order Status:** {order[5]}")

        st.divider()

        payment = database_call(
            "load payment information",
            get_payment_details,
            order_id
        )

        if payment is DB_ERROR:
            pass

        elif payment:

            st.subheader("Payment Information")

            col1, col2 = st.columns(2)

            col1.metric(
                "Payment Status",
                payment[4]
            )

            col2.metric(
                "Payment Method",
                payment[2]
            )

            col3, col4 = st.columns(2)

            col3.write(f"**Payment ID:** {payment[0]}")
            col4.write(f"**Amount Paid:** €{payment[1]}")

            st.write(f"**Payment Date:** {payment[3]}")

            st.success(
                "Payment has already been recorded successfully."
            )

        else:

            st.subheader("Record New Payment")

            method = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "Card",
                    "Bank Transfer",
                    "Online"
                ]
            )

            if st.button("Record Payment"):

                try:

                    result = record_payment(
                        order_id,
                        method
                    )

                except ValueError as error:

                    st.error(str(error))

                except mysql.connector.Error:

                    logger.exception(
                        "Database error while recording payment."
                    )

                    st.error(
                        "Could not record the payment. "
                        "Please try again later."
                    )

                else:

                    if result:

                        st.success(
                            "Payment recorded successfully!"
                        )

                        st.rerun()

    else:

        st.info("No orders available for payment.")

