
from product_operations import (
    get_all_products,
    search_products,
    get_product_by_id,
    add_products,
    delete_product
)


def main():
    while True:
        print("\n===== Online Store Application =====")
        print("1. Display all products")
        print("2. Search products")
        print("3. Find product by ID")
        print("4. Add a new product")
        print("5. Delete a product")
        print("6. Exit")

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
            print("Thank you for using Online Store Application.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
