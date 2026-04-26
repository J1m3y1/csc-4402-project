import csv
import os
import numpy as np
import pandas as pd
import sqlite3

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BooksDatasetClean.csv')


def process_single_csv():
    try:
        with sqlite3.connect('my.db') as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row_num, row in enumerate(reader):
                    if row_num >= 500:
                        break

                    # --- Publisher ---
                    cursor.execute("insert or ignore into publishers (publisher_name, country) values (?, ?)", (row['Publisher'], 'Unknown'))
                    cursor.execute("select publisher_id from publishers where publisher_name = ?", (row['Publisher'],))
                    pub_id = cursor.fetchone()[0]

                    # --- Book ---
                    isbn = f"978-{abs(hash(row['Title'])) % 1000000000}"
                    stock = np.random.randint(1, 100)
                    price_raw = row['Price'].replace('$', '').strip()
                    price = float(price_raw) if price_raw else 0.0
                    month = row.get('Publish Date (Month)', '').strip()
                    year = row.get('Publish Date (Year)', '').strip()
                    publish_date = f"{month} {year}".strip() if month or year else None

                    cursor.execute("insert or ignore into books (isbn, title, price, publisher_id, stock_quantity, publish_date) values (?, ?, ?, ?, ?, ?)",
                                   (isbn, row['Title'], price, pub_id, stock, publish_date))
                    # Fetch by ISBN so duplicate inserts still return the correct book_id
                    cursor.execute("select book_id from books where isbn = ?", (isbn,))
                    book_id = cursor.fetchone()[0]

                    # --- Authors ---
                    raw = row['Authors'].strip()
                    if raw.startswith("By "):
                        raw = raw[3:]

                    for chunk in raw.split(" and "):
                        parts = chunk.strip().split(',', 1)  # maxsplit=1 keeps suffixes like "(COM)" intact
                        if len(parts) == 2:
                            last_name = parts[0].strip()
                            first_name = parts[1].strip()
                        elif len(parts) == 1 and parts[0]:
                            last_name = parts[0].strip()
                            first_name = ''
                        else:
                            continue

                        cursor.execute('insert or ignore into authors (first_name, last_name, country) values (?, ?, ?)',
                                       (first_name, last_name, 'Unknown'))
                        cursor.execute('select author_id from authors where first_name = ? and last_name = ?',
                                       (first_name, last_name))
                        result = cursor.fetchone()
                        if result:
                            cursor.execute('insert or ignore into book_authors (book_id, author_id, role) values (?, ?, ?)',
                                           (book_id, result[0], 'Author'))

                    # --- Categories ---
                    for category in row['Category'].split(','):
                        category = category.strip()
                        if not category:
                            continue
                        cursor.execute('insert or ignore into categories (category_name) values (?)', (category,))
                        cursor.execute('select category_id from categories where category_name = ?', (category,))
                        cat_id = cursor.fetchone()[0]
                        cursor.execute('insert or ignore into book_categories (book_id, category_id) values (?, ?)',
                                       (book_id, cat_id))

                conn.commit()
            print("Data inserted successfully.")
    except sqlite3.Error as e:
        print("Failed to insert data:", e)

process_single_csv()
