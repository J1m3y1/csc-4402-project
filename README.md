# Online Bookstore Database System

A relational database project for CSC 4402 modeling an online bookstore. The database stores and manages information about books, authors, publishers, categories, customers, orders, payments, and reviews.

## Database Schema

| Table | Description |
|---|---|
| `books` | Book catalog with title, price, stock, and publish date |
| `authors` | Author records linked to books via `book_authors` |
| `publishers` | Publisher records linked to books |
| `categories` | Genre categories linked to books via `book_categories` |
| `customers` | Registered customer accounts |
| `orders` | Customer orders with status and total amount |
| `order_items` | Individual books within each order |
| `payments` | Payment record for each order |
| `reviews` | Customer ratings (0–10) for books |
| `book_authors` | Many-to-many: books ↔ authors |
| `book_categories` | Many-to-many: books ↔ categories |

## Setup

### Requirements

- Python 3
- pandas
- numpy

Install dependencies:
```bash
pip3 install pandas numpy
```

### Build the Database

Run the following scripts in order. Each one depends on the previous.

```bash
python3 data.py                   # Creates all tables
python3 fill_book_publisher_data.py  # Loads 500 books from CSV with authors, publishers, categories
python3 fill_user_data.py         # Generates fake customer accounts
python3 add_transaction.py        # Creates random orders and payments
python3 add_review.py             # Adds random book reviews
```

This produces `my.db`, a SQLite database file ready to query.

To rebuild from scratch (resets all data):
```bash
rm my.db
python3 data.py
python3 fill_book_publisher_data.py
python3 fill_user_data.py
python3 add_transaction.py
python3 add_review.py
```

## Testing

Run the test suite to verify the database was built correctly:

```bash
python3 test_db.py
```

This runs 16 checks across three categories:

- **Table population** — confirms every table has data
- **Relationship integrity** — confirms no broken foreign keys
- **Data quality** — confirms no empty categories, invalid prices, out-of-range ratings, etc.

All 16 tests should pass on a clean build.

## Querying the Database

Open an interactive SQLite shell:

```bash
sqlite3 my.db
```

### Example Queries

**Find all books by a specific author:**
```sql
SELECT b.title, b.price
FROM books b
JOIN book_authors ba ON b.book_id = ba.book_id
JOIN authors a ON ba.author_id = a.author_id
WHERE a.last_name = 'Colton';
```

**List all books in a category:**
```sql
SELECT b.title
FROM books b
JOIN book_categories bc ON b.book_id = bc.book_id
JOIN categories c ON bc.category_id = c.category_id
WHERE c.category_name = 'Fiction';
```

**Show a customer's order history:**
```sql
SELECT o.order_id, o.order_date, o.order_status, o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.first_name = 'John' AND c.last_name = 'Smith';
```

**Find books low in stock:**
```sql
SELECT title, stock_quantity
FROM books
WHERE stock_quantity < 10
ORDER BY stock_quantity ASC;
```

**Get average rating per book:**
```sql
SELECT b.title, ROUND(AVG(r.rating), 2) AS avg_rating, COUNT(*) AS num_reviews
FROM books b
JOIN reviews r ON b.book_id = r.book_id
GROUP BY b.book_id
ORDER BY avg_rating DESC
LIMIT 10;
```

Type `.quit` to exit the SQLite shell.

## Data Source

Book data is loaded from `BooksDatasetClean.csv` (500 of ~271,000 rows), which contains real book titles, authors, publishers, categories, and prices.
