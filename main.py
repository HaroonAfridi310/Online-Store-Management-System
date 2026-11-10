
from product_operations import get_all_products, search_products

def main():
    print("Welcome to Online Store Application")

    print("\n1. Display all products")
    print("2. Search products")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        products = get_all_products()

    elif choice == "2":
        keyword = input("Enter product name or category: ")
        products = search_products(keyword)

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
