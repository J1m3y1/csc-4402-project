import sqlite3

def run_tests():
    with sqlite3.connect('my.db') as conn:
        cursor = conn.cursor()
        passed = 0
        failed = 0

        def check(label, query, condition):
            nonlocal passed, failed
            cursor.execute(query)
            result = cursor.fetchone()
            value = result[0] if result else None
            ok = condition(value)
            status = "PASS" if ok else "FAIL"
            if ok:
                passed += 1
            else:
                failed += 1
            print(f"[{status}] {label} (got: {value})")

        # --- Table population ---
        check("Books table has 500 rows",      "SELECT count(*) FROM books",      lambda n: n == 500)
        check("Authors table is not empty",    "SELECT count(*) FROM authors",    lambda n: n > 0)
        check("Customers table is not empty",  "SELECT count(*) FROM customers",  lambda n: n > 0)
        check("Orders table is not empty",     "SELECT count(*) FROM orders",     lambda n: n > 0)
        check("Reviews table is not empty",    "SELECT count(*) FROM reviews",    lambda n: n > 0)
        check("Publishers table is not empty", "SELECT count(*) FROM publishers", lambda n: n > 0)

        # --- Relationship integrity ---
        check("Every book_author links to a real book",
              "SELECT count(*) FROM book_authors ba LEFT JOIN books b ON ba.book_id = b.book_id WHERE b.book_id IS NULL",
              lambda n: n == 0)

        check("Every order_item links to a real order",
              "SELECT count(*) FROM order_items oi LEFT JOIN orders o ON oi.order_id = o.order_id WHERE o.order_id IS NULL",
              lambda n: n == 0)

        check("Every payment links to a real order",
              "SELECT count(*) FROM payments p LEFT JOIN orders o ON p.order_id = o.order_id WHERE o.order_id IS NULL",
              lambda n: n == 0)

        check("Every review links to a real customer",
              "SELECT count(*) FROM reviews r LEFT JOIN customers c ON r.customer_id = c.customer_id WHERE c.customer_id IS NULL",
              lambda n: n == 0)

        # --- Data quality ---
        check("No empty category names",
              "SELECT count(*) FROM categories WHERE category_name = '' OR category_name IS NULL",
              lambda n: n == 0)

        check("No books with zero or negative price",
              "SELECT count(*) FROM books WHERE price <= 0",
              lambda n: n == 0)

        check("All orders have a matching payment",
              "SELECT count(*) FROM orders o LEFT JOIN payments p ON o.order_id = p.order_id WHERE p.payment_id IS NULL",
              lambda n: n == 0)

        check("Ratings are within valid range (0-10)",
              "SELECT count(*) FROM reviews WHERE rating < 0 OR rating > 10",
              lambda n: n == 0)

        check("No books missing a publish date",
              "SELECT count(*) FROM books WHERE publish_date IS NULL OR publish_date = ''",
              lambda n: n == 0)

        check("No publisher country set to USA (should be Unknown)",
              "SELECT count(*) FROM publishers WHERE country = 'USA'",
              lambda n: n == 0)

        print(f"\nResults: {passed} passed, {failed} failed")

run_tests()
