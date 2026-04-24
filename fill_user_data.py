import numpy as np
import pandas as pd
import sqlite3

first_name = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]
last_name = ["Smith", "Doe", "Johnson", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson"]
city_state = ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ", "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA"]

def fill_user_data():
    try:
        with sqlite3.connect('my.db') as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            for i in range(1, 26):
                first = np.random.choice(first_name)
                last = np.random.choice(last_name)
                email = f"{first.lower()}.{last.lower()}@gmail.com"
                reg_date = pd.Timestamp.now() - pd.to_timedelta(np.random.randint(0, 365), unit='d')
                city, state = np.random.choice(city_state).split(', ')
                cursor.execute("insert or ignore into customers (first_name, last_name, email, registration_date, city, state) values (?, ?, ?, ?, ?, ?)", 
                               (first, last, email, reg_date.strftime('%Y-%m-%d'), city, state))
            conn.commit()
            print("User data inserted successfully.")
    except sqlite3.Error as e:
        print("Failed to insert user data:", e)
fill_user_data()