import csv
import os
from datetime import datetime

# ===== PRODUCT MANAGER =====
# This tool helps you manage your e-commerce products
# You can add products, view them, and get basic stats


class ProductManager:
    """
    A simple tool to manage your product listings.
    Stores products in a CSV file (like Excel).
    """

    def __init__(self, filename="products.csv"):
        """
        Initialize the product manager with a filename.
        If the file doesn't exist, it will create one.
        """
        self.filename = filename
        self.products = []
        self.load_products()

    def load_products(self):
        """
        Load products from the CSV file into memory.
        If file doesn't exist, create an empty one.
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.products = list(reader)
                print(f"✓ Loaded {len(self.products)} products from {self.filename}")
            except Exception as e:
                print(f"Error loading products: {e}")
                self.products = []
        else:
            print(f"No {self.filename} found. Creating new one...")
            self.create_file()

    def create_file(self):
        """Create a new CSV file with headers."""
        headers = ['product_id', 'name', 'price', 'quantity', 'description', 'date_added']
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
        print(f"✓ Created {self.filename}")

    def add_product(self, name, price, quantity, description=""):
        """
        Add a new product to your inventory.

        Parameters:
        - name: Product name (e.g., "Horse Saddle")
        - price: Price in pounds (e.g., 150.00)
        - quantity: How many in stock (e.g., 5)
        - description: Optional details about the product
        """
        product_id = len(self.products) + 1
        new_product = {
            'product_id': product_id,
            'name': name,
            'price': price,
            'quantity': quantity,
            'description': description,
            'date_added': datetime.now().strftime('%Y-%m-%d')
        }
        self.products.append(new_product)
        self.save_products()
        print(f"✓ Added: {name} (ID: {product_id})")

    def save_products(self):
        """Save all products to the CSV file."""
        headers = ['product_id', 'name', 'price', 'quantity', 'description', 'date_added']
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(self.products)
            print(f"✓ Saved {len(self.products)} products to {self.filename}")
        except Exception as e:
            print(f"Error saving products: {e}")

    def view_all_products(self):
        """Display all products in a nice format."""
        if not self.products:
            print("No products yet!")
            return

        print("\n" + "="*80)
        print("YOUR PRODUCTS")
        print("="*80)
        for product in self.products:
            print(f"\nID: {product['product_id']}")
            print(f"Name: {product['name']}")
            print(f"Price: £{product['price']}")
            print(f"Quantity: {product['quantity']}")
            if product['description']:
                print(f"Description: {product['description']}")
            print(f"Added: {product['date_added']}")
            print("-" * 80)

    def get_stats(self):
        """Show basic statistics about your inventory."""
        if not self.products:
            print("No products to analyze yet!")
            return

        total_products = len(self.products)
        total_value = sum(float(p['price']) * int(p['quantity']) for p in self.products)
        total_quantity = sum(int(p['quantity']) for p in self.products)
        avg_price = sum(float(p['price']) for p in self.products) / total_products

        print("\n" + "="*80)
        print("INVENTORY STATISTICS")
        print("="*80)
        print(f"Total different products: {total_products}")
        print(f"Total items in stock: {total_quantity}")
        print(f"Average product price: £{avg_price:.2f}")
        print(f"Total inventory value: £{total_value:.2f}")
        print("="*80 + "\n")

    def find_product(self, name):
        """Search for a product by name."""
        results = [p for p in self.products if name.lower() in p['name'].lower()]
        if results:
            print(f"\nFound {len(results)} product(s):")
            for p in results:
                print(f"  - {p['name']} (£{p['price']}, Stock: {p['quantity']})")
        else:
            print(f"No products found matching '{name}'")

    def update_product(self, product_id, name=None, price=None, quantity=None, description=None):
        """
        Update an existing product's details.

        Parameters:
        - product_id: The ID of the product to update
        - name: New product name (optional)
        - price: New price (optional)
        - quantity: New quantity (optional)
        - description: New description (optional)
        """
        for product in self.products:
            if int(product['product_id']) == product_id:
                if name:
                    product['name'] = name
                if price:
                    product['price'] = price
                if quantity is not None:
                    product['quantity'] = quantity
                if description is not None:
                    product['description'] = description
                self.save_products()
                print(f"✓ Updated product ID {product_id}")
                return
        print(f"No product found with ID {product_id}")

    def delete_product(self, product_id):
        """
        Remove a product from inventory.

        Parameters:
        - product_id: The ID of the product to delete
        """
        for i, product in enumerate(self.products):
            if int(product['product_id']) == product_id:
                removed_name = product['name']
                self.products.pop(i)
                self.save_products()
                print(f"✓ Deleted: {removed_name} (ID: {product_id})")
                return
        print(f"No product found with ID {product_id}")


# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    # Create a product manager
    manager = ProductManager()

    # Add Jock & Co products
    print("\n--- Adding Jock & Co products ---")
    manager.add_product("Jodhpurs", 54.99, 12, "Classic riding pants")
    manager.add_product("Waterproof Jacket", 89.99, 8, "Weather-resistant riding jacket")
    manager.add_product("Riding Goggles", 19.99, 20, "Protective riding goggles")
    manager.add_product("Thick Riding Socks", 9.99, 35, "Durable equestrian socks")

    # View all products
    manager.view_all_products()

    # Show statistics
    manager.get_stats()

    # Search for a product
    manager.find_product("jacket")

    # Update a product (e.g., raise price of Jodhpurs to £59.99)
    print("\n--- Updating Jodhpurs price ---")
    manager.update_product(1, price=59.99)

    # Show products after update
    manager.view_all_products()

    # Delete a product (e.g., remove Riding Goggles)
    print("\n--- Deleting Riding Goggles ---")
    manager.delete_product(3)

    # Final stats
    manager.get_stats()
