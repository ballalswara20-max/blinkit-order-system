import json
import random
from datetime import datetime

PRODUCTS = {
    1: {"name": "Amul Milk (500 ml)", "price": 33},
    2: {"name": "Bread (400 g)", "price": 45},
    3: {"name": "Eggs (6 pcs)", "price": 60},
    4: {"name": "Banana (1 dozen)", "price": 55},
    5: {"name": "Maggi Noodles (4 pack)", "price": 56},
    6: {"name": "Lays Chips", "price": 20},
    7: {"name": "Coca-Cola (750 ml)", "price": 40},
    8: {"name": "Tata Salt (1 kg)", "price": 28},
}

COUPONS = {"BLINK10": 10, "FIRST50": 50}
FREE_DELIVERY_ABOVE = 199
DELIVERY_FEE = 25
ORDERS_FILE = "orders.json"


def show_menu():
    print("\n===== BLINKIT: DELIVERED IN 10 MINUTES =====")
    for pid, item in PRODUCTS.items():
        print(f"{pid}. {item['name']:<26} Rs {item['price']}")
    print("0. Checkout")


def add_to_cart(cart):
    while True:
        show_menu()
        try:
            choice = int(input("\nEnter product number (0 to checkout): "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 0:
            return
        if choice not in PRODUCTS:
            print("Product not found.")
            continue

        try:
            qty = int(input(f"Quantity of {PRODUCTS[choice]['name']}: "))
        except ValueError:
            print("Quantity must be a number.")
            continue
        if qty <= 0:
            print("Quantity must be at least 1.")
            continue

        cart[choice] = cart.get(choice, 0) + qty
        print(f"Added {qty} x {PRODUCTS[choice]['name']}")


def calculate_bill(cart, coupon=None):
    subtotal = sum(PRODUCTS[pid]["price"] * qty for pid, qty in cart.items())

    discount = 0
    if coupon in COUPONS:
        value = COUPONS[coupon]
        discount = subtotal * value / 100 if coupon == "BLINK10" else value
        discount = min(discount, subtotal)

    delivery = 0 if subtotal >= FREE_DELIVERY_ABOVE else DELIVERY_FEE
    total = subtotal - discount + delivery
    return subtotal, discount, delivery, total


def print_bill(cart, subtotal, discount, delivery, total):
    print("\n---------- YOUR BILL ----------")
    for pid, qty in cart.items():
        item = PRODUCTS[pid]
        print(f"{item['name']:<26} {qty} x {item['price']} = Rs {qty * item['price']}")
    print("-------------------------------")
    print(f"Subtotal:  Rs {subtotal:.2f}")
    print(f"Discount: -Rs {discount:.2f}")
    print(f"Delivery:  Rs {delivery}")
    print(f"TOTAL:     Rs {total:.2f}")


def save_order(cart, total, address):
    order = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "address": address,
        "items": {PRODUCTS[pid]["name"]: qty for pid, qty in cart.items()},
        "total": round(total, 2),
    }
    try:
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = []

    orders.append(order)
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)


def view_past_orders():
    try:
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No past orders yet.")
        return
    for i, o in enumerate(orders, 1):
        print(f"{i}. {o['time']} | Rs {o['total']} | {o['address']}")


def place_order():
    cart = {}
    add_to_cart(cart)

    if not cart:
        print("Your cart is empty.")
        return

    coupon = input("Have a coupon? (BLINK10 / FIRST50, or press Enter to skip): ").strip().upper()
    if coupon and coupon not in COUPONS:
        print("Invalid coupon, continuing without it.")
        coupon = None

    subtotal, discount, delivery, total = calculate_bill(cart, coupon)
    print_bill(cart, subtotal, discount, delivery, total)

    address = input("\nEnter delivery address: ").strip()
    if not address:
        print("Address is required. Order cancelled.")
        return

    save_order(cart, total, address)
    eta = random.randint(8, 15)
    print(f"\nOrder placed! Arriving at {address} in about {eta} minutes.")


def main():
    while True:
        print("\n1. Place new order")
        print("2. View past orders")
        print("3. Exit")
        option = input("Choose an option: ").strip()

        if option == "1":
            place_order()
        elif option == "2":
            view_past_orders()
        elif option == "3":
            print("Thanks for using Blinkit. Bye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()