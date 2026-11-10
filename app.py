
import streamlit as st

from database import get_connection

from product_operations import (
    get_all_products,
    search_products,
    get_product_by_id,
    add_products,
    delete_product
)

from order_operations import (
    create_order,
    get_all_orders,
    get_order_details,
    update_order_status,
    record_payment
)


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def get_customers():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT CustomerID, FirstName, LastName
            FROM customer
            ORDER BY CustomerID
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_order_items(order_id):

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor()

    try:
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
        cursor.close()
        connection.close()


def get_payment_details(order_id):

    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor()

    try:
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

    tab1, tab2, tab3, tab4 = st.tabs([
        "All Products",
        "Search Product",
        "Add Product",
        "Delete Product"
    ])

    # ALL PRODUCTS

    with tab1:

        st.subheader("Available Products")

        if st.button("Refresh Products"):
            st.rerun()

        products = get_all_products()

        if products:

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

        elif products == []:
            st.info("No products available.")

        else:
            st.error("Could not load products.")

    # SEARCH PRODUCTS

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

                if keyword.strip():

                    results = search_products(keyword.strip())

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

                else:
                    st.warning("Please enter a search keyword.")

        else:

            product_id = st.number_input(
                "Enter Product ID",
                min_value=1,
                step=1
            )

            if st.button("Find Product"):

                product = get_product_by_id(product_id)

                if product:

                    st.write(f"**Name:** {product[1]}")
                    st.write(f"**Category:** {product[2]}")
                    st.write(f"**Price:** €{product[3]}")
                    st.write(f"**Stock:** {product[4]}")

                else:
                    st.warning("Product not found.")

    # ADD PRODUCT

    with tab3:

        st.subheader("Add New Product")

        with st.form("add_product_form"):

            name = st.text_input("Product Name")

            category = st.text_input("Category")

            price = st.number_input(
                "Price (€)",
                min_value=0.01,
                value=10.00,
                step=0.50
            )

            stock = st.number_input(
                "Stock Quantity",
                min_value=0,
                step=1
            )

            submitted = st.form_submit_button("Add Product")

            if submitted:

                if not name.strip() or not category.strip():

                    st.error(
                        "Please enter the product name and category."
                    )

                else:

                    try:

                        result = add_products(
                            name.strip(),
                            category.strip(),
                            price,
                            stock
                        )

                        if result:

                            st.success("Product added successfully!")
                            st.rerun()

                        else:
                            st.error("Could not add product.")

                    except Exception as e:
                        st.error(f"Error adding product: {e}")

    # DELETE PRODUCT

    with tab4:

        st.subheader("Delete Product")

        products = get_all_products()

        if products:

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
                            product_options[selected_product]
                        )

                        if result:

                            st.success("Product deleted successfully!")
                            st.rerun()

                        else:

                            st.error(
                                "Product was not deleted. "
                                "It may not exist or may be linked to an order."
                            )

                    except Exception as e:

                        st.error(
                            "Could not delete product. "
                            "It may be linked to an existing order. "
                            f"Details: {e}"
                        )

        else:
            st.info("No products available.")


# ==================================================
# 2. CREATE ORDER
# ==================================================

elif page == "Create Order":

    st.header("Create New Order")

    customers = get_customers()
    products = get_all_products()

    if not customers:

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

        product_options = {
            f"{p[0]} - {p[1]} (€{p[3]}) - Stock: {p[4]}": p
            for p in available_products
        }

        selected_products = st.multiselect(
            "Select Products",
            list(product_options.keys())
        )

        items = []

        for selected in selected_products:

            product = product_options[selected]

            quantity = st.number_input(
                f"Quantity for {product[1]}",
                min_value=1,
                max_value=product[4],
                value=1,
                step=1,
                key=f"quantity_{product[0]}"
            )

            items.append(
                (product[0], quantity)
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

        if st.button("Create Order", disabled=not items):

            customer_id = customer_options[selected_customer]

            try:

                order_id = create_order(
                    customer_id,
                    items
                )

                if order_id:

                    st.success(
                        f"Order created successfully! Order ID: {order_id}"
                    )

                    st.balloons()

                else:

                    st.error(
                        "Order creation failed. Check the customer, "
                        "product stock and terminal messages."
                    )

            except Exception as e:

                st.error(f"Error creating order: {e}")


# ==================================================
# 3. ORDER MANAGEMENT
# ==================================================

elif page == "Orders":

    st.header("Order Management")

    orders = get_all_orders()

    if orders:

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

        tab1, tab2 = st.tabs([
            "Order Details",
            "Update Order Status"
        ])

        # ORDER DETAILS

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

                order = get_order_details(selected_order)

                if order:

                    st.subheader(f"Order #{order[0]}")

                    col1, col2 = st.columns(2)

                    col1.write(f"**Customer ID:** {order[1]}")
                    col1.write(f"**Order Date:** {order[2]}")

                    col2.write(f"**Status:** {order[3]}")
                    col2.write(f"**Total:** €{order[4]}")

                    order_items = get_order_items(selected_order)

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

                else:
                    st.error("Order not found.")

        # UPDATE ORDER STATUS

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
                        selected_status_order,
                        new_status
                    )

                    if result:

                        st.success(
                            "Order status updated successfully!"
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "Order not found or status was unchanged."
                        )

                except Exception as e:

                    st.error(f"Error updating order: {e}")

    else:
        st.info("No orders found.")


# ==================================================
# 4. PAYMENT MANAGEMENT
# ==================================================

elif page == "Payments":

    st.header("Payment Management")

    orders = get_all_orders()

    if orders:

        order_options = {
            f"Order {o[0]} - {o[2]} {o[3]} - €{o[6]}": o
            for o in orders
        }

        selected_payment_order = st.selectbox(
            "Select Order",
            list(order_options.keys())
        )

        order = order_options[selected_payment_order]
        order_id = order[0]

        st.subheader("Order Information")

        col1, col2 = st.columns(2)

        col1.write(f"**Order ID:** {order_id}")
        col1.write(f"**Customer:** {order[2]} {order[3]}")
        col2.write(f"**Order Total:** €{order[6]}")
        col2.write(f"**Order Status:** {order[5]}")

        st.divider()

        # CHECK EXISTING PAYMENT

        payment = get_payment_details(order_id)

        if payment:

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

        # RECORD NEW PAYMENT

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

                    if result:

                        st.success(
                            "Payment recorded successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Payment was not recorded. "
                            "Please check the terminal for details."
                        )

                except Exception as e:

                    st.error(
                        f"Error recording payment: {e}"
                    )

    else:

        st.info("No orders available for payment.")
