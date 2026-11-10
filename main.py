
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


def main():
    while True:
        print("\n===== Online Store Application =====")

        print("\n--- Product Management ---")
        print("1. Display all products")
        print("2. Search products")
        print("3. Find product by ID")
        print("4. Add a new product")
        print("5. Delete a product")

        print("\n--- Order Management ---")
        print("6. Create a new order")
        print("7. Display all orders")
        print("8. View order details")
        print("9. Update order status")
        print("10. Record payment")

        print("\n11. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            get_all_products()

        elif choice == "2":
            keyword = input("Enter product name or category: ")
            search_products(keyword)

        elif choice == "3":
            product_id = input("Enter product ID: ")

            if product_id.isdigit():
                get_product_by_id(int(product_id))
            else:
                print("Please enter a valid product ID.")

        elif choice == "4":
            name = input("Enter product name: ")
            category = input("Enter product category: ")

            try:
                price = float(input("Enter product price: "))
                stock = int(input("Enter stock quantity: "))

                if price < 0 or stock < 0:
                    print("Price and stock cannot be negative.")
                else:
                    add_products(name, category, price, stock)

            except ValueError:
                print("Please enter a valid price and stock quantity.")

        elif choice == "5":
            product_id = input("Enter product ID to delete: ")

            if product_id.isdigit():
                delete_product(int(product_id))
            else:
                print("Please enter a valid product ID.")

        elif choice == "6":
            customer_id = input("Enter customer ID: ")

            if not customer_id.isdigit():
                print("Please enter a valid customer ID.")
                continue

            items = []

            while True:
                product_id = input("Enter product ID: ")
                quantity = input("Enter quantity: ")

                if not product_id.isdigit() or not quantity.isdigit():
                    print("Please enter valid numbers.")
                    continue

                if int(quantity) <= 0:
                    print("Quantity must be greater than zero.")
                    continue

                items.append((int(product_id), int(quantity)))

                more = input("Add another product? (y/n): ").lower()

                if more != "y":
                    break

            if items:
                create_order(int(customer_id), items)

        elif choice == "7":
            get_all_orders()

        elif choice == "8":
            order_id = input("Enter order ID: ")

            if order_id.isdigit():
                get_order_details(int(order_id))
            else:
                print("Please enter a valid order ID.")

        elif choice == "9":
            order_id = input("Enter order ID: ")

            if not order_id.isdigit():
                print("Please enter a valid order ID.")
                continue

            print("Available statuses:")
            print("1. Pending")
            print("2. Processing")
            print("3. Shipped")
            print("4. Delivered")

            status_choice = input("Choose status: ")

            statuses = {
                "1": "Pending",
                "2": "Processing",
                "3": "Shipped",
                "4": "Delivered"
            }

            if status_choice in statuses:
                update_order_status(
                    int(order_id),
                    statuses[status_choice]
                )
            else:
                print("Invalid status choice.")

        elif choice == "10":
            order_id = input("Enter order ID: ")

            if not order_id.isdigit():
                print("Please enter a valid order ID.")
                continue

            method = input("Enter payment method: ")

            if method.strip():
                record_payment(int(order_id), method)
            else:
                print("Payment method cannot be empty.")

        elif choice == "11":
            print("Thank you for using Online Store Application.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
