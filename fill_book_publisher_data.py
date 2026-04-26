import csv
import numpy as np
import pandas as pd
import sqlite3

file_path = ("C:\\Users\\homec\\csc-4402-project\\BooksDatasetClean.csv")


def process_single_csv():
    try:
        with sqlite3.connect('my.db') as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for i, row in enumerate(reader):
                    if i >= 500: 
                        break
                    cursor.execute("insert or ignore into publishers (publisher_name, country) values (?, ?)", (row['Publisher'], 'USA'))  # Assuming publisher name is in the third column
                    cursor.execute("select publisher_id from publishers where publisher_name = ?", (row['Publisher'],))
                    pub_id = cursor.fetchone()[0]

                    isbn = f"978-{abs(hash(row['Title'])) % 1000000000}"  
                    stock = np.random.randint(1, 100)  
                    price_raw = row['Price'].replace('$', '').strip()
                    price = float(price_raw) if price_raw else 0.0
                    cursor.execute("insert or ignore into books (isbn, title, price, publisher_id, stock_quantity) values (?, ?, ?, ?, ?)", (isbn, row['Title'], price, pub_id, stock))
                    book_id = cursor.lastrowid
                    
                    clean_string = row['Authors'].replace("By ", "").replace(" and ", "")
                    bits = [b.strip() for b in clean_string.split(',')]
                    authors = []
                    for i in range(0, len(bits), 2):
                        if i + 1 < len(bits):
                            last_name = bits[i]
                            first_name = bits[i + 1]
                            cursor.execute('insert or ignore into authors (first_name, last_name, country) values (?, ?, ?)', (first_name, last_name, 'USA'))
                            cursor.execute('select author_id from authors where first_name = ? and last_name = ?', (first_name, last_name))
                            auth_id = cursor.fetchone()[0]                            
                            cursor.execute('insert or ignore into book_authors (book_id, author_id, role) values (?, ?, ?)', (book_id, auth_id, 'Author'))
                    
                    categories = row['Category'].split(',')
                    for category in categories:
                        cursor.execute('insert or ignore into categories (category_name) values (?)', (category.strip(),))
                        cursor.execute('select category_id from categories where category_name = ?', (category.strip(),))
                        cat_id = cursor.fetchone()[0]
                        cursor.execute('insert or ignore into book_categories (book_id, category_id) values (?, ?)', (book_id, cat_id))

                conn.commit()
            print("Data inserted successfully.")
    except sqlite3.Error as e:
        print("Failed to insert data:", e)
process_single_csv()