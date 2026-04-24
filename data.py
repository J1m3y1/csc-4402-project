import sqlite3

sql_statements = [ 
    """CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY, 
            first_name text NOT NULL, 
            last_name text NOT NULL,
            email text NOT NULL UNIQUE,
            registration_date text NOT NULL,
            city text NOT NULL,
            state text NOT NULL
        );""",

    """CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY, 
            publisher_name text NOT NULL,
            country text NOT NULL
        );""",
    """CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL, 
            order_date text NOT NULL,
            order_status text NOT NULL,
            total_amount real NOT NULL,
            foreign key (customer_id) references customers (customer_id)
            );""",
    """create table if not exists books (
            book_id integer primary key,
            publisher_id integer not null,
            isbn text not null unique,
            title text not null,
            price real not null,
            stock_quantity integer not null,
            foreign key (publisher_id) references publishers (publisher_id)
        );""",
    """create table if not exists authors (
            author_id integer primary key,
            first_name text not null,
            last_name text not null,
            country text not null
        );""",
    """create table if not exists categories (
            category_id integer primary key,
            category_name text not null unique
        );""",
    """create table if not exists payments (
            payment_id integer primary key,
            order_id integer not null unique,
            payment_method text not null,
            payment_status text not null,
            amount_paid real not null,
            foreign key (order_id) references orders (order_id)
        );""",
    """create table if not exists order_items (
            order_id INTEGER,
            book_id INTEGER,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            Primary key (order_id, book_id),
            foreign key (order_id) references orders (order_id),
            foreign key (book_id) references books (book_id)
        );""",
    """create table if not exists reviews (
            review_id integer primary key,
            customer_id integer not null,
            book_id integer not null,
            rating integer not null,
            review_date text not null,
            foreign key (customer_id) references customers (customer_id),
            foreign key (book_id) references books (book_id)
        );""",
    """create table if not exists book_authors (
            book_id integer,
            author_id integer,
            role text not null,
            primary key (book_id, author_id),
            foreign key (book_id) references books (book_id),
            foreign key (author_id) references authors (author_id)
        );""",
    """create table if not exists book_categories (
            book_id integer,
            category_id integer,
            primary key (book_id, category_id),
            foreign key (book_id) references books (book_id),
            foreign key (category_id) references categories (category_id)
        );""",
]

# create a database connection
try:
    with sqlite3.connect('my.db') as conn:
        # create a cursor
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")
        # execute statements
        for statement in sql_statements:
            cursor.execute(statement)

        # commit the changes
        conn.commit()

        print("Tables created successfully.")
except sqlite3.Error as e:
    print("Failed to create tables:", e)
