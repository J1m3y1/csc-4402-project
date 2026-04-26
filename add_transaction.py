import numpy as np
import pandas as pd
import sqlite3

def add_transaction():
    try:
        with sqlite3.connect('my.db') as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            customers = cursor.execute("SELECT customer_id FROM customers").fetchall()
            books = cursor.execute("SELECT book_id, price FROM books").fetchall()

            if not customers or not books:
                print("Error: Customers or Books table is empty.")
                return
            
            book_prices = {b[0]: b[1] for b in books}
            book_ids = list(book_prices.keys())
            customer_ids = [c[0] for c in customers]

            for i in range(500):
                # Step 1: Prepare data (No manual order_id here)
                customer = int(np.random.choice(customer_ids))
                book = int(np.random.choice(book_ids))
                quantity = int(np.random.randint(1, 5))
                order_date = (pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(1, 365))).isoformat()
                order_status = np.random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'])
                unit_price = book_prices[book]
                total_price = round(quantity * unit_price, 2)

                # Step 2: Insert into parent table (orders)
                # We omit order_id so SQLite auto-generates it
                cursor.execute("""
                    INSERT INTO orders (customer_id, order_date, order_status, total_amount) 
                    VALUES (?, ?, ?, ?)""", 
                    (customer, order_date, order_status, total_price))

                # Step 3: Capture the generated ID
                new_order_id = cursor.lastrowid

                # Step 4: Use new_order_id for child tables
                cursor.execute("""
                    INSERT INTO order_items (order_id, book_id, quantity, unit_price) 
                    VALUES (?, ?, ?, ?)""", 
                    (new_order_id, book, quantity, unit_price))

                payment_method = np.random.choice(['Credit Card', 'PayPal', 'Bank Transfer'])
                payment_status = np.random.choice(['Completed', 'Pending'])
                
                cursor.execute("""
                    INSERT INTO payments (order_id, payment_method, payment_status, amount_paid) 
                    VALUES (?, ?, ?, ?)""", 
                    (new_order_id, payment_method, payment_status, total_price))

            conn.commit()
            print("Transactions added successfully.")
    except sqlite3.Error as e:
        print("Failed to add transactions:", e) 

add_transaction()