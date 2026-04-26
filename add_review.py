import numpy as np
import pandas as pd
import sqlite3

def add_review():
    try: 
        with sqlite3.connect('my.db') as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            customers = cursor.execute("SELECT customer_id FROM customers").fetchall()
            books = cursor.execute("SELECT book_id FROM books").fetchall()

            if not customers or not books:
                print("Error: Customers or Books table is empty.")
                return
            
            book_ids = [b[0] for b in books]
            customer_ids = [c[0] for c in customers]

            for i in range(250):
                customer = int(np.random.choice(customer_ids))
                book = int(np.random.choice(book_ids))
                rating = round(np.random.uniform(0, 10), 1)
                review_date = (pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(1, 365))).isoformat()

                cursor.execute("""
                    INSERT INTO reviews (customer_id, book_id, rating, review_date) 
                    VALUES (?, ?, ?, ?)""", 
                    (customer, book, rating, review_date))

            conn.commit()
            print("Reviews added successfully.")
    except sqlite3.Error as e:
        print("Failed to add reviews:", e)
add_review()